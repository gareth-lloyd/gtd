import { useEffect, useState } from 'react';

export type ToastType = 'error' | 'success' | 'info';

export interface Toast {
  id: number;
  type: ToastType;
  message: string;
}

type Listener = (toasts: Toast[]) => void;

const DURATIONS: Record<ToastType, number> = {
  error: 8000,
  success: 3000,
  info: 4000,
};

class ToastStore {
  private toasts: Toast[] = [];
  private listeners = new Set<Listener>();
  private counter = 0;

  show(type: ToastType, message: string): number {
    const id = ++this.counter;
    this.toasts = [...this.toasts, { id, type, message }];
    this.emit();
    setTimeout(() => this.dismiss(id), DURATIONS[type]);
    return id;
  }

  dismiss(id: number) {
    const before = this.toasts.length;
    this.toasts = this.toasts.filter((t) => t.id !== id);
    if (this.toasts.length !== before) this.emit();
  }

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    listener(this.toasts);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private emit() {
    for (const l of this.listeners) l(this.toasts);
  }
}

export const toasts = new ToastStore();

export function Toaster() {
  const [list, setList] = useState<Toast[]>([]);
  useEffect(() => toasts.subscribe(setList), []);

  if (list.length === 0) return null;

  return (
    <div className="toast-container" role="status" aria-live="polite">
      {list.map((t) => (
        <div key={t.id} className={`toast toast-${t.type}`}>
          <span className="toast-message">{t.message}</span>
          <button
            type="button"
            className="toast-close"
            onClick={() => toasts.dismiss(t.id)}
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
