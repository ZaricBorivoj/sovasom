import { Button } from './design-system/Button';
import { Postcard } from './design-system/Postcard';

export function ScreenMessage({
  title,
  children,
  onRetry,
  action = 'Try again',
}: {
  title: string;
  children?: React.ReactNode;
  onRetry?: () => void;
  action?: string;
}) {
  return (
    <main className="screen-message">
      <Postcard tone="lavender" className="stack">
        <h1 style={{ fontSize: '2.5rem' }}>{title}</h1>
        <p role="status">{children}</p>
        {onRetry && <Button onClick={onRetry}>{action}</Button>}
      </Postcard>
    </main>
  );
}
