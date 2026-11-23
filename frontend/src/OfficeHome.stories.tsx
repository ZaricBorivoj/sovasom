import type { Meta, StoryObj } from '@storybook/react-vite';
import { OfficeHome } from './OfficeHome';

export default {
  title: 'Office/Home',
  component: OfficeHome,
  args: {
    account: {
      id: 'synthetic-story',
      display_name: 'Test colleague',
      email: 'colleague@example.com',
      is_administrator: true,
      is_menu_maintainer: true,
    },
    onSignOut: async () => {},
  },
} satisfies Meta<typeof OfficeHome>;
type Story = StoryObj<typeof OfficeHome>;
export const Empty: Story = {};
export const Reconnecting: Story = {
  args: { notice: 'Connection lost. Reconnecting…' },
};
export const LongIdentity: Story = {
  args: {
    account: {
      id: 'synthetic-long',
      display_name: 'A colleague with a longer display name',
      email: 'a.long.email.address.for.layout@example.com',
      is_administrator: false,
      is_menu_maintainer: false,
    },
  },
};
export const SignOutPending: Story = {
  args: { onSignOut: () => new Promise(() => {}) },
};
export const SignOutError: Story = {
  args: {
    onSignOut: async () => {
      throw new Error('Offline');
    },
  },
};
