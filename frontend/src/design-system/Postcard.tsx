import type { HTMLAttributes } from 'react';

export function Postcard({
  tone = 'peach',
  className = '',
  ...props
}: HTMLAttributes<HTMLElement> & { tone?: 'peach' | 'lavender' | 'green' }) {
  return (
    <section className={`postcard postcard--${tone} ${className}`} {...props} />
  );
}
