import { useParams } from 'react-router-dom';

export function useEnvParam(): string {
  const { env } = useParams<{ env: string }>();
  return env!;
}
