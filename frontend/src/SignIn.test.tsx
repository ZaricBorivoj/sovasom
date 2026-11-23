import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { expect, test, vi } from 'vitest';
import { SignIn } from './SignIn';

test('a colleague can submit credentials and sees a pending state', async () => {
  const submit = vi.fn(() => new Promise<void>(() => {}));
  render(<SignIn onSubmit={submit} />);
  const user = userEvent.setup();
  await user.type(screen.getByLabelText('Email'), 'colleague@example.com');
  await user.type(screen.getByLabelText('Password'), 'synthetic password');
  await user.click(screen.getByRole('button', { name: 'Sign in' }));
  expect(submit).toHaveBeenCalledWith(
    'colleague@example.com',
    'synthetic password',
  );
  expect(screen.getByRole('button', { name: 'Signing in…' })).toBeDisabled();
});

test('rejected sign-in presents a readable error and allows retry', async () => {
  render(
    <SignIn
      onSubmit={async () => {
        throw new Error('Email or password is incorrect.');
      }}
    />,
  );
  const user = userEvent.setup();
  await user.type(screen.getByLabelText('Email'), 'colleague@example.com');
  await user.type(screen.getByLabelText('Password'), 'wrong password');
  await user.click(screen.getByRole('button', { name: 'Sign in' }));
  expect(screen.getByRole('alert')).toHaveTextContent(
    'Email or password is incorrect.',
  );
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled();
});
