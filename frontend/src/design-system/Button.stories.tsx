import type { Meta, StoryObj } from '@storybook/react-vite';
import { Button } from './Button';

export default {
  title: 'Postcard Club/Button',
  component: Button,
  args: { children: 'Sign in' },
} satisfies Meta<typeof Button>;
type Story = StoryObj<typeof Button>;
export const Primary: Story = {};
export const Secondary: Story = {
  args: { variant: 'secondary', children: 'Sign out' },
};
export const Pending: Story = {
  args: { disabled: true, children: 'Signing in…' },
};
