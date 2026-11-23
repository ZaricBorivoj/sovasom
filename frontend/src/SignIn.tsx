import { useState, type FormEvent } from 'react';
import { Brand } from './Brand';
import { Button } from './design-system/Button';
import { Postcard } from './design-system/Postcard';
import { TextField } from './design-system/TextField';

export function SignIn({
  onSubmit,
  notice,
}: {
  onSubmit: (email: string, password: string) => Promise<void>;
  notice?: string;
}) {
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setPending(true);
    setError('');
    try {
      await onSubmit(String(form.get('email')), String(form.get('password')));
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Could not sign in. Try again.',
      );
    } finally {
      setPending(false);
    }
  }
  return (
    <>
      <header className="site-header">
        <Brand />
        <span className="private-label">Private office</span>
      </header>
      <main className="page">
        <div className="sign-in">
          <div className="intro">
            <p className="eyebrow">Coffee. Bakery. Good company.</p>
            <h1>A little office happiness.</h1>
            <p className="muted">
              Sign in to see what’s brewing at the office.
            </p>
          </div>
          <Postcard aria-labelledby="sign-in-title">
            <form onSubmit={submit} aria-busy={pending}>
              <h2 id="sign-in-title">Welcome back.</h2>
              {notice && <p role="status">{notice}</p>}
              {error && (
                <p role="alert" className="alert">
                  {error}
                </p>
              )}
              <TextField
                label="Email"
                name="email"
                type="email"
                autoComplete="username"
                required
                maxLength={320}
                disabled={pending}
              />
              <TextField
                label="Password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                maxLength={1024}
                disabled={pending}
              />
              <Button type="submit" disabled={pending}>
                {pending ? 'Signing in…' : 'Sign in'}
              </Button>
              <p className="muted">
                Need access or a new password? Ask an office administrator.
              </p>
            </form>
          </Postcard>
        </div>
      </main>
    </>
  );
}
