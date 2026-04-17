import type { Project } from './api';

export function generateProjectId(title: string): string {
  return `${new Date().toISOString().slice(0, 10)}-${slugify(title)}`;
}

export function slugify(text: string): string {
  return (
    text
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .slice(0, 50) || 'untitled'
  );
}

export function fmtDate(iso: string): string {
  if (!iso) return '';
  return iso.slice(0, 10);
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
