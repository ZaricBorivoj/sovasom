import type { Meta, StoryObj } from '@storybook/react-vite';
import { Postcard } from './Postcard';

export default {
  title: 'Postcard Club/Postcard',
  component: Postcard,
  args: {
    children: (
      <>
        <h2>Good things come in runs.</h2>
        <p>Two stops. One office. Excellent taste.</p>
      </>
    ),
  },
} satisfies Meta<typeof Postcard>;
type Story = StoryObj<typeof Postcard>;
export const Peach: Story = {};
export const Lavender: Story = { args: { tone: 'lavender' } };
export const Green: Story = { args: { tone: 'green' } };
