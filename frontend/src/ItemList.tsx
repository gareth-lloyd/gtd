import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { api, type Bucket, type Item } from './api';
import { useNextFilters } from './filters';
import { ItemCard } from './ItemCard';
import { useEnvParam } from './useEnvParam';

export function NextActionsView() {
  const env = useEnvParam();
  const { contexts, energy, maxMinutes, minMinutes, noProject } = useNextFilters();
  const params: Record<string, string> = { status: 'next' };
  if (contexts.length) params.contexts = contexts.join(',');
  if (energy) params.energy = energy;
  if (maxMinutes) params.max_minutes = maxMinutes;
  if (minMinutes) params.min_minutes = minMinutes;
  if (noProject) params.no_project = 'true';

  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, 'next', contexts, energy, maxMinutes, minMinutes, noProject],
    queryFn: () => api.listItems(env, params),
  });

  if (isLoading) return <div className="empty">Loading…</div>;
  return <ItemList env={env} items={items ?? []} />;
}

export function BucketView({ env, bucket }: { env: string; bucket: Bucket }) {
  const [params, setParams] = useSearchParams();
  const includeDeferred =
    bucket === 'inbox' && params.get('include_deferred') === 'true';

  const listParams: Record<string, string> = { status: bucket };
  if (includeDeferred) listParams.include_deferred = 'true';

  const { data: items, isLoading } = useQuery({
    queryKey: ['items', env, bucket, includeDeferred],
    queryFn: () => api.listItems(env, listParams),
  });

  return (
    <>
      {bucket === 'inbox' && (
        <div className="bucket-toolbar">
          <label className="toggle">
            <input
              type="checkbox"
              checked={includeDeferred}
              onChange={(e) => {
                const next = new URLSearchParams(params);
                if (e.target.checked) next.set('include_deferred', 'true');
                else next.delete('include_deferred');
                setParams(next, { replace: true });
              }}
            />
            Show deferred
          </label>
        </div>
      )}
      {isLoading ? (
        <div className="empty">Loading…</div>
      ) : (
        <ItemList env={env} items={items ?? []} />
      )}
    </>
  );
}

export function BucketRoute({ bucket }: { bucket: Bucket }) {
  const env = useEnvParam();
  return <BucketView env={env} bucket={bucket} />;
}

export function ItemList({ env, items }: { env: string; items: Item[] }) {
  const { data: projects } = useQuery({
    queryKey: ['projects', env, false],
    queryFn: () => api.listProjects(env, false),
  });
  if (items.length === 0) return <div className="empty">Nothing here.</div>;
  return (
    <ul className="item-list">
      {items.map((item) => (
        <li key={item.id}>
          <ItemCard
            env={env}
            item={item}
            projects={projects}
          />
        </li>
      ))}
    </ul>
  );
}
