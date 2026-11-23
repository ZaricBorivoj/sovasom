import type { Meta, StoryObj } from '@storybook/react-vite';
import { Brand } from './Brand';

export default { title: 'Office/Brand', component: Brand } satisfies Meta<
  typeof Brand
>;
export const Default: StoryObj<typeof Brand> = {};
