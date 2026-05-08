import { useMemo } from "react";

const URL_RE = /https?:\/\/[^\s)<>]+/g;

function extractUrls(text: string): string[] {
  const matches = text.match(URL_RE);
  if (!matches) return [];
  return [...new Set(matches)];
}

function formatUrl(url: string): string {
  try {
    const u = new URL(url);
    const path = u.pathname.replace(/\/$/, "");
    if (!path || path === "/") return u.hostname;
    const segments = path.split("/").filter(Boolean);
    const short =
      segments.length <= 2
        ? segments.join("/")
        : `${segments[0]}/…/${segments[segments.length - 1]}`;
    return `${u.hostname}/${short}`;
  } catch {
    return url.length > 40 ? url.slice(0, 37) + "…" : url;
  }
}

export function ItemLinks({ body }: { body: string }) {
  const urls = useMemo(() => (body ? extractUrls(body) : []), [body]);
  if (urls.length === 0) return null;
  return (
    <div className="item-links">
      {urls.map((url) => (
        <a
          key={url}
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="link-chip"
          title={url}
        >
          {formatUrl(url)}
        </a>
      ))}
    </div>
  );
}
