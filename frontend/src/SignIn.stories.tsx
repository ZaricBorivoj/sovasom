import type { Meta, StoryObj } from '@storybook/react-vite';
import { SignIn } from './SignIn';

export default {
  title: 'Office/SignIn',
  component: SignIn,
  args: { onSubmit: async () => {} },
} satisfies Meta<typeof SignIn>;
type Story = StoryObj<typeof SignIn>;
export const Default: Story = {};
export const SessionEnded: Story = {
  args: { notice: 'Your session ended. Please sign in again.' },
};
export const Rejected: Story = {
  args: {
    onSubmit: async () => {
      throw new Error('Email or password is incorrect.');
    },
  },
};
export const Pending: Story = {
  args: { onSubmit: () => new Promise(() => {}) },
};
