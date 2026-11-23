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

function stubFetch(handler: typeof fetch) {
  const original = globalThis.fetch;
  globalThis.fetch = handler;
  return () => {
    globalThis.fetch = original;
  };
}

export const Loading: StoryObj<typeof App> = {
  beforeEach: () => stubFetch(() => new Promise(() => {})),
};
export const Home: StoryObj<typeof App> = {
  beforeEach: () =>
    stubFetch(async (input) =>
      Response.json(
        String(input).endsWith('/home')
          ? {
              active_run: null,
              history: [],
            }
          : {
              account: {
                id: 'synthetic-app',
                email: 'colleague@example.com',
                display_name: 'Test colleague',
                is_administrator: true,
                is_menu_maintainer: true,
              },
              csrf_token: 'synthetic-csrf',
            },
      ),
    ),
};
export const AccessLost: StoryObj<typeof App> = {
  beforeEach: () =>
    stubFetch(async () =>
      Response.json({ detail: 'Office access unavailable' }, { status: 403 }),
    ),
};
export const ConnectionError: StoryObj<typeof App> = {
  beforeEach: () =>
    stubFetch(async () => {
      throw new TypeError('Network unavailable');
    }),
};
