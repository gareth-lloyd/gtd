import { useNextFilters } from './filters';
import { contextHue } from './context-colors';
import type { Energy, EnvConfig } from './api';

const ENERGY_CHOICES: (Energy | '')[] = ['', 'low', 'medium', 'high'];

// ">2h" needs a different shape than the rest: it filters for items longer
// than the budget, not items that fit within it.
type TimeChoice =
  | { label: string; kind: 'none' }
  | { label: string; kind: 'max'; value: string }
  | { label: string; kind: 'min'; value: string };

const TIME_CHOICES: TimeChoice[] = [
  { label: 'any', kind: 'none' },
  { label: '5m', kind: 'max', value: '5' },
  { label: '15m', kind: 'max', value: '15' },
  { label: '30m', kind: 'max', value: '30' },
  { label: '60m', kind: 'max', value: '60' },
  { label: '2h', kind: 'max', value: '120' },
  { label: '>2h', kind: 'min', value: '120' },
];

export function FilterPanel({ config }: { config: EnvConfig | undefined }) {
  const {
    contexts,
    energy,
    maxMinutes,
    minMinutes,
    noProject,
    setContexts,
    setEnergy,
    setMaxMinutes,
    setMinMinutes,
    setNoProject,
  } = useNextFilters();

  const isTimeActive = (t: TimeChoice) => {
    if (t.kind === 'none') return !maxMinutes && !minMinutes;
    if (t.kind === 'max') return maxMinutes === t.value;
    return minMinutes === t.value;
  };

  const selectTime = (t: TimeChoice) => {
    if (t.kind === 'none') setMaxMinutes('');
    else if (t.kind === 'max') setMaxMinutes(t.value);
    else setMinMinutes(t.value);
  };
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
        <div className="btn-group btn-group-vertical">
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
        <div className="btn-group btn-group-vertical">
          {TIME_CHOICES.map((t) => (
            <button
              type="button"
              key={t.label}
              className={isTimeActive(t) ? 'active' : ''}
              onClick={() => selectTime(t)}
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
