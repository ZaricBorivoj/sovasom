import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';

async function signIn(page: Page) {
  await page.goto('/');
  await page.getByLabel('Email', { exact: true }).fill('colleague@example.com');
  await page
    .getByLabel('Password', { exact: true })
    .fill('synthetic password only');
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  await expect(
    page.getByRole('heading', { name: 'Office runs', exact: true }),
  ).toBeVisible();
}

test('a colleague can sign in, reload and sign out', async ({
  page,
  context,
}) => {
  await signIn(page);
  await expect(
    page.getByRole('heading', { name: 'No runs yet.' }),
  ).toBeVisible();
  await expect(page.getByRole('button', { name: /announce/i })).toHaveCount(0);
  const cookies = await context.cookies();
  const session = cookies.find(
    (cookie) => cookie.name === '__Host-office_session',
  );
  expect(session).toMatchObject({
    secure: true,
    httpOnly: true,
    sameSite: 'Strict',
  });
  await page.reload();
  await expect(
    page.getByRole('heading', { name: 'Office runs', exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  expect(await page.evaluate(() => document.cookie)).not.toContain(
    'office_session',
  );
  await page.getByRole('button', { name: 'Sign out', exact: true }).click();
  await expect(
    page.getByRole('button', { name: 'Sign in', exact: true }),
  ).toBeVisible();
  await page.reload();
  await expect(
    page.getByRole('button', { name: 'Sign in', exact: true }),
  ).toBeVisible();
});

test('private data and sign-in reject unauthorized requests', async ({
  page,
}) => {
  await page.goto('/');
  const response = await page.request.get('/api/office/home');
  expect(response.status()).toBe(401);
  await page.getByLabel('Email', { exact: true }).fill('colleague@example.com');
  await page.getByLabel('Password', { exact: true }).fill('wrong password');
  await page.getByRole('button', { name: 'Sign in', exact: true }).click();
  await expect(page.getByRole('alert')).toHaveText(
    'Email or password is incorrect.',
  );
});

test('CSRF denial leaves the colleague signed in', async ({ page }) => {
  await signIn(page);
  expect(
    await page.evaluate(
      async () => (await fetch('/api/auth/logout', { method: 'POST' })).status,
    ),
  ).toBe(403);
  await page.reload();
  await expect(
    page.getByRole('heading', { name: 'Office runs', exact: true }),
  ).toBeVisible();
});

for (const state of ['expired', 'revoked']) {
  test(`${state} sessions lose access on reload`, async ({ page }) => {
    test.skip(
      process.env.OFFICE_TEST_STACK !== '1',
      'Session mutations require the isolated synthetic Compose harness.',
    );
    await signIn(page);
    const assignment =
      state === 'expired'
        ? "expires_at = now() - interval '1 second'"
        : 'revoked_at = now()';
    execFileSync(
      'docker',
      [
        'compose',
        'exec',
        '-T',
        'db',
        'psql',
        '-U',
        'office',
        '-d',
        'office',
        '-v',
        'ON_ERROR_STOP=1',
        '-c',
        `UPDATE login_sessions SET ${assignment} WHERE account_id IN (SELECT id FROM accounts WHERE email = 'colleague@example.com')`,
      ],
      { cwd: '..', stdio: 'pipe' },
    );
    await page.reload();
    await expect(
      page.getByRole('button', { name: 'Sign in', exact: true }),
    ).toBeVisible();
  });
}

test('a session persists across service restart', async ({
  page,
  context,
}, info) => {
  const phase = process.env.PERSISTENCE_PHASE;
  const file = `${process.env.PERSISTED_SESSION_FILE}-${info.project.name}.json`;
  test.skip(
    !phase || !process.env.PERSISTED_SESSION_FILE,
    'Run by the isolated restart harness.',
  );
  if (phase === 'save') {
    await signIn(page);
    await context.storageState({ path: file });
  } else {
    await context.addCookies(JSON.parse(readFileSync(file, 'utf8')).cookies);
    await page.goto('/');
    await expect(
      page.getByRole('heading', { name: 'Office runs', exact: true }),
    ).toBeVisible();
  }
});
