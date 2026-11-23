import { useState } from 'react';
import type { Account } from './api';
import { Brand } from './Brand';
import { Button } from './design-system/Button';
import { Postcard } from './design-system/Postcard';

export function OfficeHome({
  account,
  onSignOut,
  notice,
}: {
  account: Account;
  onSignOut: () => Promise<void>;
  notice?: string;
}) {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  async function signOut() {
    setPending(true);
    try {
      await onSignOut();
    } catch {
      setError('Could not sign out. Check your connection and try again.');
    } finally {
      setPending(false);
    }
  }
  return (
    <>
      <header className="site-header">
        <Brand />
        <div className="account">
          <div className="account-details">
            <strong>{account.display_name}</strong>
            <span>{account.email}</span>
          </div>
          <Button variant="secondary" onClick={signOut} disabled={pending}>
            {pending ? 'Signing out…' : 'Sign out'}
          </Button>
        </div>
      </header>
      <main className="page">
        <div className="intro">
          <p className="eyebrow">A little office happiness</p>
          <h1>Office runs</h1>
          <p className="muted">Two stops. One office. Excellent taste.</p>
        </div>
        <div className="stack">
          {notice && (
            <p role="status" className="alert">
              {notice}
            </p>
          )}
          {error && (
            <p role="alert" className="alert">
              {error}
            </p>
          )}
          <Postcard className="empty-state" aria-labelledby="empty-title">
            <div className="copy stack">
              <p className="eyebrow">Room for something good</p>
              <h2 id="empty-title">No runs yet.</h2>
              <p>
                When a colleague announces a coffee and bakery run, it will
                appear here. A little something to look forward to.
              </p>
            </div>
            <div className="postmark" aria-hidden="true">
              OFFICE POST<span>✳</span>GOOD COMPANY
            </div>
          </Postcard>
        </div>
        <p className="office-note muted">
          Your private office corner for coffee and bakery trips.
        </p>
      </main>
    </>
  );
}
