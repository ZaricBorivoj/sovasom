import type { Meta, StoryObj } from '@storybook/react-vite';
import { TextField } from './TextField';

export default {
  title: 'Postcard Club/TextField',
  component: TextField,
  args: { label: 'Email', type: 'email', autoComplete: 'username' },
} satisfies Meta<typeof TextField>;
type Story = StoryObj<typeof TextField>;
export const Empty: Story = {};
export const Filled: Story = {
  args: { defaultValue: 'colleague@example.com' },
};
export const Invalid: Story = {
  args: { defaultValue: 'invalid', error: 'Enter an email address.' },
};
export const Disabled: Story = { args: { disabled: true } };
export const Password: Story = {
  args: {
    label: 'Password',
    type: 'password',
    autoComplete: 'current-password',
  },
};
