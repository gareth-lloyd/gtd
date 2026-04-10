import type { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  busy?: boolean;
}

export function Button({
  busy = false,
  disabled,
  className = '',
  children,
  ...rest
}: ButtonProps) {
  const cls = busy ? `${className} busy`.trim() : className;
  return (
    <button
      {...rest}
      disabled={busy || disabled}
      className={cls}
      aria-busy={busy || undefined}
    >
      <span className="btn-label" style={busy ? { visibility: 'hidden' } : undefined}>
        {children}
      </span>
      {busy && <span className="spinner" aria-hidden="true" />}
    </button>
  );
}
