import { useSearchParams } from 'react-router-dom';
import type { Energy } from './api';

export interface NextFilters {
  contexts: string[];
  energy: Energy | '';
  maxMinutes: string;
  noProject: boolean;
  setContexts: (updater: (prev: string[]) => string[]) => void;
  setEnergy: (e: Energy | '') => void;
  setMaxMinutes: (s: string) => void;
  setNoProject: (v: boolean) => void;
}

export function useNextFilters(): NextFilters {
  const [params, setParams] = useSearchParams();

  const contexts = params.get('contexts')?.split(',').filter(Boolean) ?? [];
  const energy = (params.get('energy') ?? '') as Energy | '';
  const maxMinutes = params.get('max_minutes') ?? '';
  const noProject = params.get('no_project') === 'true';

  const patch = (key: string, value: string) => {
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        if (value) next.set(key, value);
        else next.delete(key);
        return next;
      },
      { replace: true },
    );
  };

  return {
    contexts,
    energy,
    maxMinutes,
    noProject,
    setContexts: (updater) => patch('contexts', updater(contexts).join(',')),
    setEnergy: (e) => patch('energy', e),
    setMaxMinutes: (s) => patch('max_minutes', s),
    setNoProject: (v) => patch('no_project', v ? 'true' : ''),
  };
}
