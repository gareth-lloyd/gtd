import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import MiniSearch from 'minisearch';
import { api, type Item, type Project } from './api';

export type SearchHit =
  | { kind: 'item'; id: string; item: Item }
  | { kind: 'project'; id: string; project: Project };

interface SearchDoc {
  id: string;
  kind: 'item' | 'project';
  title: string;
  body: string;
  outcome: string;
  contexts: string;
  tags: string;
  area: string;
  projectTitle: string;
}

const SEARCH_FIELDS = [
  'title',
  'body',
  'outcome',
  'contexts',
  'tags',
  'area',
  'projectTitle',
];

const FIELD_BOOSTS = {
  title: 3,
  outcome: 2,
  body: 1,
  contexts: 1.5,
  tags: 1.5,
  projectTitle: 1.2,
  area: 1,
};

function itemDoc(item: Item, projectTitle: string): SearchDoc {
  return {
    id: `item:${item.id}`,
    kind: 'item',
    title: item.title,
    body: item.body,
    outcome: '',
    contexts: item.contexts.join(' '),
    tags: item.tags.join(' '),
    area: item.area ?? '',
    projectTitle,
  };
}

function projectDoc(project: Project): SearchDoc {
  return {
    id: `project:${project.id}`,
    kind: 'project',
    title: project.title,
    body: project.body,
    outcome: project.outcome ?? '',
    contexts: '',
    tags: project.tags.join(' '),
    area: project.area ?? '',
    projectTitle: '',
  };
}

export interface SearchIndex {
  search: (query: string, limit?: number) => SearchHit[];
  size: number;
}

function buildIndex(items: Item[], projects: Project[]): SearchIndex {
  const projectTitleById = new Map(projects.map((p) => [p.id, p.title]));
  const itemsById = new Map(items.map((i) => [i.id, i]));
  const projectsById = new Map(projects.map((p) => [p.id, p]));

  const mini = new MiniSearch<SearchDoc>({
    fields: SEARCH_FIELDS,
    searchOptions: {
      prefix: true,
      fuzzy: 0.15,
      combineWith: 'AND',
      boost: FIELD_BOOSTS,
    },
  });

  for (const item of items) {
    const pTitle = (item.project && projectTitleById.get(item.project)) || '';
    mini.add(itemDoc(item, pTitle));
  }
  for (const project of projects) {
    mini.add(projectDoc(project));
  }

  return {
    size: items.length + projects.length,
    search: (query, limit = 200) => {
      const trimmed = query.trim();
      if (!trimmed) return [];
      const raw = mini.search(trimmed);
      const hits: SearchHit[] = [];
      for (const r of raw) {
        if (hits.length >= limit) break;
        const docId = String(r.id);
        const [kind, id] = docId.split(':', 2) as ['item' | 'project', string];
        if (kind === 'item') {
          const item = itemsById.get(id);
          if (item) hits.push({ kind: 'item', id, item });
        } else {
          const project = projectsById.get(id);
          if (project) hits.push({ kind: 'project', id, project });
        }
      }
      return hits;
    },
  };
}

const indexCache = new WeakMap<object, SearchIndex>();

function getOrBuildIndex(data: { items: Item[]; projects: Project[] }): SearchIndex {
  const cached = indexCache.get(data);
  if (cached) return cached;
  const built = buildIndex(data.items, data.projects);
  indexCache.set(data, built);
  return built;
}

export function useSearchIndex(
  env: string | undefined,
  { enabled = true }: { enabled?: boolean } = {},
): {
  index: SearchIndex | null;
  isLoading: boolean;
} {
  const { data, isLoading } = useQuery({
    queryKey: ['search-corpus', env],
    queryFn: () => api.listSearchCorpus(env!),
    enabled: !!env && enabled,
    staleTime: 60_000,
  });

  const index = useMemo(() => (data ? getOrBuildIndex(data) : null), [data]);

  return { index, isLoading };
}
