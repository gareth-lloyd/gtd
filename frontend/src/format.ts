import type { Project } from "./api";

export function generateProjectId(title: string): string {
  return `${new Date().toISOString().slice(0, 10)}-${slugify(title)}`;
}

export function slugify(text: string): string {
  return (
    text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "")
      .slice(0, 50) || "untitled"
  );
}

export function fmtDate(iso: string): string {
  if (!iso) return "";
  return iso.slice(0, 10);
}

export function fmtDateTime(iso: string): string {
  if (!iso) return "";
  const date = iso.slice(0, 10);
  const time = iso.slice(11, 16);
  return time ? `${date} ${time}` : date;
}

/** Coarse elapsed time since `iso`: "just now", "15m", "3h", "2d", "2w". */
export function fmtAge(iso: string, now: Date = new Date()): string {
  const mins = Math.floor((now.getTime() - new Date(iso).getTime()) / 60_000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  const days = Math.floor(hours / 24);
  if (days < 14) return `${days}d`;
  return `${Math.floor(days / 7)}w`;
}

export function fmtMinutes(m: number): string {
  if (m === 0) return "0m";
  const h = Math.floor(m / 60);
  const mm = m % 60;
  if (h === 0) return `${mm}m`;
  if (mm === 0) return `${h}h`;
  return `${h}h ${mm}m`;
}

export function sortProjects(projects: Project[]): Project[] {
  return [...projects].sort((a, b) => {
    const pa = a.priority ?? 99;
    const pb = b.priority ?? 99;
    if (pa !== pb) return pa - pb;
    if (a.due && b.due) return a.due.localeCompare(b.due);
    if (a.due) return -1;
    if (b.due) return 1;
    return a.title.localeCompare(b.title);
  });
}
