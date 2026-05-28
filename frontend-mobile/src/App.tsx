import { useCallback, useEffect, useState } from "react";
import {
  capture,
  clearToken,
  errorMessage,
  getToken,
  listEnvs,
  listInbox,
  listNext,
  setToken,
  UnauthorizedError,
  type EnvName,
  type Item,
} from "./api";

const ENV_KEY = "gtd:env";
type Tab = "capture" | "inbox" | "next";

export default function App() {
  const [token, setTokenState] = useState<string | null>(getToken());
  const [authError, setAuthError] = useState<string | null>(null);

  const handleUnauthorized = useCallback(() => {
    clearToken();
    setTokenState(null);
    setAuthError("Incorrect passphrase or session expired. Please re-enter.");
  }, []);

  if (!token) {
    return (
      <PassphraseGate
        error={authError}
        onSubmit={(value) => {
          setToken(value);
          setTokenState(value);
          setAuthError(null);
        }}
      />
    );
  }
  return <Main onUnauthorized={handleUnauthorized} />;
}

function PassphraseGate({
  error,
  onSubmit,
}: {
  error: string | null;
  onSubmit: (value: string) => void;
}) {
  const [value, setValue] = useState("");
  return (
    <div className="gate">
      <h1>gtd</h1>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (value.trim()) onSubmit(value.trim());
        }}
      >
        <input
          type="password"
          autoFocus
          placeholder="Passphrase"
          aria-label="Passphrase"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <button type="submit">Unlock</button>
      </form>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

function Main({ onUnauthorized }: { onUnauthorized: () => void }) {
  const [envs, setEnvs] = useState<EnvName[]>([]);
  const [env, setEnv] = useState<string>(() => localStorage.getItem(ENV_KEY) ?? "home");
  const [tab, setTab] = useState<Tab>("capture");

  const selectEnv = useCallback((next: string) => {
    setEnv(next);
    localStorage.setItem(ENV_KEY, next);
  }, []);

  useEffect(() => {
    listEnvs()
      .then((list) => {
        setEnvs(list);
        // If the persisted env no longer exists on the server, fall back to a
        // real one so reads/captures don't keep hitting a non-existent env.
        if (list.length > 0 && !list.some((e) => e.name === env)) {
          selectEnv(list.some((e) => e.name === "home") ? "home" : list[0].name);
        }
      })
      .catch((err) => {
        if (err instanceof UnauthorizedError) onUnauthorized();
        // A failed env list isn't fatal: the switcher just shows the current
        // env until the next load. Per-tab errors are surfaced below.
      });
  }, [env, selectEnv, onUnauthorized]);

  return (
    <div className="app">
      <header>
        <select aria-label="Environment" value={env} onChange={(e) => selectEnv(e.target.value)}>
          {!envs.some((e) => e.name === env) && <option value={env}>{env}</option>}
          {envs.map((e) => (
            <option key={e.name} value={e.name}>
              {e.name}
            </option>
          ))}
        </select>
        <nav>
          {(["capture", "inbox", "next"] as Tab[]).map((t) => (
            <button
              key={t}
              className={tab === t ? "active" : ""}
              onClick={() => setTab(t)}
              aria-current={tab === t ? "page" : undefined}
            >
              {t}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {tab === "capture" && <CaptureTab env={env} onUnauthorized={onUnauthorized} />}
        {tab === "inbox" && (
          <ListTab key={`inbox-${env}`} env={env} kind="inbox" onUnauthorized={onUnauthorized} />
        )}
        {tab === "next" && (
          <ListTab key={`next-${env}`} env={env} kind="next" onUnauthorized={onUnauthorized} />
        )}
      </main>
    </div>
  );
}

function CaptureTab({ env, onUnauthorized }: { env: string; onUnauthorized: () => void }) {
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<{ kind: "ok" | "pending" | "error"; text: string } | null>(
    null,
  );

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || busy) return;
    const [title, ...rest] = trimmed.split("\n");
    setBusy(true);
    setNotice(null);
    try {
      const result = await capture(env, title, rest.join("\n").trim());
      setText("");
      setNotice(
        result.synced === false
          ? { kind: "pending", text: `Captured to ${env} — sync pending (not yet saved remotely)` }
          : { kind: "ok", text: `Captured to ${env} inbox` },
      );
    } catch (err) {
      if (err instanceof UnauthorizedError) onUnauthorized();
      else setNotice({ kind: "error", text: errorMessage(err) });
    } finally {
      setBusy(false);
    }
  };

  return (
    <form className="capture" onSubmit={submit}>
      <textarea
        autoFocus
        placeholder="Capture to inbox…"
        aria-label="Capture"
        value={text}
        onChange={(e) => {
          setText(e.target.value);
          setNotice(null);
        }}
      />
      <button type="submit" disabled={busy || !text.trim()}>
        {busy ? "Saving…" : "Capture"}
      </button>
      {notice && (
        <p
          className={
            notice.kind === "error" ? "error" : notice.kind === "pending" ? "pending" : "ok"
          }
          role={notice.kind === "error" ? "alert" : "status"}
        >
          {notice.text}
        </p>
      )}
    </form>
  );
}

function ListTab({
  env,
  kind,
  onUnauthorized,
}: {
  env: string;
  kind: "inbox" | "next";
  onUnauthorized: () => void;
}) {
  const [items, setItems] = useState<Item[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setItems(null);
    setError(null);
    const load = kind === "inbox" ? listInbox : listNext;
    load(env)
      .then(setItems)
      .catch((err) => {
        if (err instanceof UnauthorizedError) onUnauthorized();
        else setError(errorMessage(err));
      });
  }, [env, kind, onUnauthorized]);

  if (error)
    return (
      <p className="error" role="alert">
        {error}
      </p>
    );
  if (items === null) return <p className="muted">Loading…</p>;
  if (items.length === 0) return <p className="muted">Nothing here.</p>;
  return (
    <ul className="items">
      {items.map((item) => (
        <li key={item.id}>
          <span className="title">{item.title}</span>
          <span className="chips">
            {item.project && <span className="chip project">{item.project}</span>}
            {item.contexts.map((c) => (
              <span key={c} className="chip">
                {c}
              </span>
            ))}
            {item.overdue && <span className="chip overdue">overdue</span>}
          </span>
        </li>
      ))}
    </ul>
  );
}
