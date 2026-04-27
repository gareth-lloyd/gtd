import { useNextFilters } from './filters';
import { contextHue } from './context-colors';
import type { Energy, EnvConfig } from './api';

const ENERGY_CHOICES: (Energy | '')[] = ['', 'low', 'medium', 'high'];

const TIME_CHOICES: { label: string; value: string }[] = [
  { label: 'any', value: '' },
  { label: '5m', value: '5' },
  { label: '15m', value: '15' },
  { label: '30m', value: '30' },
  { label: '60m', value: '60' },
  { label: '2h+', value: '240' },
];

export function FilterPanel({ config }: { config: EnvConfig | undefined }) {
  const {
    contexts,
    energy,
    maxMinutes,
    noProject,
    setContexts,
    setEnergy,
    setMaxMinutes,
    setNoProject,
  } = useNextFilters();
  return (
    <div className="filter-panel">
      <div className="filter-section">
        <h3>Contexts</h3>
        {config?.contexts.map((c) => (
          <label
            key={c}
            className="check-row"
            style={{ borderLeft: `3px solid hsl(${contextHue(c)}, 38%, 72%)` }}
          >
            <input
              type="checkbox"
              checked={contexts.includes(c)}
              onChange={(e) =>
                setContexts((prev) =>
                  e.target.checked ? [...prev, c] : prev.filter((x) => x !== c)
                )
              }
            />
            <span>@{c}</span>
          </label>
        ))}
        {contexts.length > 0 && (
          <button
            type="button"
            className="clear-link"
            onClick={() => setContexts(() => [])}
          >
            clear
          </button>
        )}
      </div>

      <div className="filter-section">
        <h3>Energy</h3>
        <div className="btn-group">
          {ENERGY_CHOICES.map((e) => (
            <button
              type="button"
              key={e || 'any'}
              className={energy === e ? 'active' : ''}
              onClick={() => setEnergy(e)}
            >
              {e || 'any'}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3>Max time</h3>
        <div className="btn-group">
          {TIME_CHOICES.map((t) => (
            <button
              type="button"
              key={t.label}
              className={maxMinutes === t.value ? 'active' : ''}
              onClick={() => setMaxMinutes(t.value)}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      <div className="filter-section">
        <h3>Project</h3>
        <label className="check-row">
          <input
            type="checkbox"
            checked={noProject}
            onChange={(e) => setNoProject(e.target.checked)}
          />
          <span>No project</span>
        </label>
      </div>
    </div>
  );
}
