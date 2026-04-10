import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  MutationCache,
  QueryCache,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query';
import App from './App';
import { Toaster, toasts } from './toast';
import './styles.css';

function describe(error: unknown): string {
  if (error instanceof Error) return error.message;
  if (typeof error === 'string') return error;
  return 'Request failed';
}

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => toasts.show('error', `Load failed: ${describe(error)}`),
  }),
  mutationCache: new MutationCache({
    onError: (error) => toasts.show('error', `Action failed: ${describe(error)}`),
  }),
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 5_000,
      retry: 1,
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      <Toaster />
    </QueryClientProvider>
  </React.StrictMode>
);
