import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test } from 'vitest';
import { OfficeHome } from './OfficeHome';

const account = {
  id: 'synthetic',
  display_name: 'Test colleague',
  email: 'colleague@example.com',
  is_administrator: false,
  is_menu_maintainer: false,
};

test('the empty office has no nonworking run action', () => {
  render(<OfficeHome account={account} onSignOut={async () => {}} />);
  expect(screen.getByRole('heading', { name: 'Office runs' })).toBeVisible();
  expect(screen.getByRole('heading', { name: 'No runs yet.' })).toBeVisible();
  expect(
    screen.queryByRole('button', { name: /announce/i }),
  ).not.toBeInTheDocument();
});

test('sign-out failure leaves a useful retry action', async () => {
  render(
    <OfficeHome
      account={account}
      onSignOut={async () => {
        throw new Error('offline');
      }}
    />,
  );
  await userEvent.click(screen.getByRole('button', { name: 'Sign out' }));
  expect(screen.getByRole('alert')).toHaveTextContent('Could not sign out');
  expect(screen.getByRole('button', { name: 'Sign out' })).toBeEnabled();
});
