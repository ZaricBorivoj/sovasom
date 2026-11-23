import type { Meta, StoryObj } from '@storybook/react-vite';
import { ScreenMessage } from './ScreenMessage';

export default {
  title: 'Office/ScreenMessage',
  component: ScreenMessage,
} satisfies Meta<typeof ScreenMessage>;
type Story = StoryObj<typeof ScreenMessage>;
export const Loading: Story = {
  args: { title: 'Opening the office…', children: 'Just a moment.' },
};
export const AccessLost: Story = {
  args: {
    title: 'Office access unavailable',
    children: 'Ask an office administrator about your membership.',
    onRetry: () => {},
  },
};
export const ConnectionError: Story = {
  args: {
    title: 'Couldn’t reach the office',
    children: 'Check your connection, then try again.',
    onRetry: () => {},
  },
};
