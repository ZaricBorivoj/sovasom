import { useEffect, useState } from 'react';
import { api, ApiError, type Identity } from './api';
import { OfficeHome } from './OfficeHome';
import { ScreenMessage } from './ScreenMessage';
import { SignIn } from './SignIn';

type State = {
  page: 'loading' | 'signin' | 'home' | 'denied' | 'error';
  identity?: Identity;
  notice?: string;
};

export function App() {
  const [state, setState] = useState<State>({ page: 'loading' });
  useEffect(() => {
    if (state.page !== 'loading' && state.page !== 'home') return;
    let live = true;
    let pending = false;
    async function refresh() {
      if (pending) return;
      pending = true;
      try {
        const identity = await api.session();
        await api.home();
        if (live) setState({ page: 'home', identity });
      } catch (error) {
        if (!live) return;
        if (error instanceof ApiError && error.status === 401) {
          setState((previous) => ({
            page: 'signin',
            notice:
              previous.page === 'home'
                ? 'Your session ended. Please sign in again.'
                : previous.notice,
          }));
        } else if (error instanceof ApiError && error.status === 403) {
          setState((previous) => ({ ...previous, page: 'denied' }));
        } else {
          setState((previous) =>
            previous.page === 'home'
              ? { ...previous, notice: 'Connection lost. Reconnecting…' }
              : { page: 'error' },
          );
        }
      } finally {
        pending = false;
      }
    }
    void refresh();
    const timer = window.setInterval(() => {
      if (document.visibilityState === 'visible') void refresh();
    }, 5000);
    window.addEventListener('focus', refresh);
    window.addEventListener('online', refresh);
    return () => {
      live = false;
      clearInterval(timer);
      window.removeEventListener('focus', refresh);
      window.removeEventListener('online', refresh);
    };
  }, [state.page]);

  async function signOut() {
    try {
      const identity = state.identity || (await api.session());
      await api.logout(identity.csrf_token);
    } catch (error) {
      if (!(error instanceof ApiError && error.status === 401)) throw error;
    }
    setState({ page: 'signin' });
  }

  if (state.page === 'signin')
    return (
      <SignIn
        notice={state.notice}
        onSubmit={async (email, password) => {
          const identity = await api.login(email, password);
          await api.home();
          setState({ page: 'home', identity });
        }}
      />
    );
  if (state.page === 'home' && state.identity)
    return (
      <OfficeHome
        account={state.identity.account}
        onSignOut={signOut}
        notice={state.notice}
      />
    );
  if (state.page === 'denied')
    return (
      <ScreenMessage
        title="Office access unavailable"
        onRetry={() => window.location.reload()}
      >
        Ask an office administrator about your membership.
      </ScreenMessage>
    );
  if (state.page === 'error')
    return (
      <ScreenMessage
        title="Couldn’t reach the office"
        onRetry={() => window.location.reload()}
      >
        Check your connection, then try again.
      </ScreenMessage>
    );
  return (
    <ScreenMessage title="Opening the office…">Just a moment.</ScreenMessage>
  );
}
