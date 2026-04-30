import { useSearchParams } from 'react-router-dom';
import type { Energy } from './api';

export interface NextFilters {
  contexts: string[];
  energy: Energy | '';
  maxMinutes: string;
  minMinutes: string;
  noProject: boolean;
  setContexts: (updater: (prev: string[]) => string[]) => void;
  setEnergy: (e: Energy | '') => void;
  setMaxMinutes: (s: string) => void;
  setMinMinutes: (s: string) => void;
  setNoProject: (v: boolean) => void;
}

export function useNextFilters(): NextFilters {
  const [params, setParams] = useSearchParams();

  const contexts = params.get('contexts')?.split(',').filter(Boolean) ?? [];
  const energy = (params.get('energy') ?? '') as Energy | '';
  const maxMinutes = params.get('max_minutes') ?? '';
  const minMinutes = params.get('min_minutes') ?? '';
  const noProject = params.get('no_project') === 'true';

  const patch = (entries: Record<string, string>) => {
    setParams(
      (prev) => {
        const next = new URLSearchParams(prev);
        for (const [key, value] of Object.entries(entries)) {
          if (value) next.set(key, value);
          else next.delete(key);
        }
        return next;
      },
      { replace: true },
    );
  };

  return {
    contexts,
    energy,
    maxMinutes,
    minMinutes,
    noProject,
    setContexts: (updater) => patch({ contexts: updater(contexts).join(',') }),
    setEnergy: (e) => patch({ energy: e }),
    setMaxMinutes: (s) => patch({ max_minutes: s, min_minutes: '' }),
    setMinMinutes: (s) => patch({ min_minutes: s, max_minutes: '' }),
    setNoProject: (v) => patch({ no_project: v ? 'true' : '' }),
  };
}
