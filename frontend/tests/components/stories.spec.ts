import { expect, test } from '@playwright/test';

test('every component story renders without a runtime failure', async ({
  page,
  request,
}) => {
  const response = await request.get('/index.json');
  const index: { entries: Record<string, { type: string; id: string }> } =
    await response.json();
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));
  for (const entry of Object.values(index.entries).filter(
    (entry) => entry.type === 'story',
  )) {
    await page.goto(`/iframe.html?id=${entry.id}&viewMode=story`);
    await expect(page.locator('#storybook-root')).not.toBeEmpty();
    await expect(page.locator('.sb-errordisplay')).toBeHidden();
  }
  expect(errors).toEqual([]);
});

test('sign-in stories show rejection and pending feedback', async ({
  page,
}) => {
  for (const state of ['rejected', 'pending']) {
    await page.goto(`/iframe.html?id=office-signin--${state}&viewMode=story`);
    await page
      .getByLabel('Email', { exact: true })
      .fill('colleague@example.com');
    await page
      .getByLabel('Password', { exact: true })
      .fill('synthetic password');
    await page.getByRole('button', { name: 'Sign in', exact: true }).click();
    if (state === 'rejected')
      await expect(page.getByRole('alert')).toHaveText(
        'Email or password is incorrect.',
      );
    else
      await expect(
        page.getByRole('button', { name: 'Signing in…' }),
      ).toBeDisabled();
  }
});

test('sign-out stories show pending and error feedback', async ({ page }) => {
  for (const state of ['sign-out-pending', 'sign-out-error']) {
    await page.goto(`/iframe.html?id=office-home--${state}&viewMode=story`);
    await page.getByRole('button', { name: 'Sign out', exact: true }).click();
    if (state === 'sign-out-error')
      await expect(page.getByRole('alert')).toContainText('Could not sign out');
    else
      await expect(
        page.getByRole('button', { name: 'Signing out…' }),
      ).toBeDisabled();
  }
});

test('the app renders its authentication, access and connection states', async ({
  page,
}) => {
  for (const [story, heading] of [
    ['signed-out', 'A little office happiness.'],
    ['loading', 'Opening the office…'],
    ['home', 'Office runs'],
    ['access-lost', 'Office access unavailable'],
    ['connection-error', 'Couldn’t reach the office'],
  ]) {
    await page.goto(`/iframe.html?id=office-app--${story}&viewMode=story`);
    await expect(
      page.getByRole('heading', { name: heading, exact: true }),
    ).toBeVisible();
  }
});

for (const story of [
  'office-signin--default',
  'office-home--empty',
  'office-home--long-identity',
  'office-screenmessage--access-lost',
]) {
  test(`@visual ${story}`, async ({ page }) => {
    await page.goto(`/iframe.html?id=${story}&viewMode=story`);
    await expect(page.locator('#storybook-root')).not.toBeEmpty();
    await page.evaluate(() => document.fonts.ready);
    await expect(page).toHaveScreenshot(`${story}.png`, {
      fullPage: true,
      animations: 'disabled',
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= window.innerWidth,
      ),
    ).toBe(true);
  });
}
