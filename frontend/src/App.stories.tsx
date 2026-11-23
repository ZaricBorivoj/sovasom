import type { Meta, StoryObj } from '@storybook/react-vite';
import { App } from './App';

export default { title: 'Office/App', component: App } satisfies Meta<
  typeof App
>;
export const SignedOut: StoryObj<typeof App> = {
  beforeEach: () => {
    const original = globalThis.fetch;
    globalThis.fetch = async () =>
      Response.json({ detail: 'Please sign in again.' }, { status: 401 });
    return () => {
      globalThis.fetch = original;
    };
  },
};
