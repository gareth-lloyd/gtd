import type React from 'react';

/**
 * Deterministic hue from a context name. Uses djb2 hash for good
 * distribution across the full 0-360° range.
 */
export function contextHue(name: string): number {
  let hash = 5381;
  for (let i = 0; i < name.length; i++) {
    hash = ((hash << 5) + hash + name.charCodeAt(i)) >>> 0;
  }
  return hash % 360;
}

/**
 * Inline style for a context chip: pastel background + darker text,
 * both derived from the context's hue.
 */
export function contextChipStyle(name: string): React.CSSProperties {
  const h = contextHue(name);
  return {
    backgroundColor: `hsl(${h}, 60%, 90%)`,
    color: `hsl(${h}, 50%, 30%)`,
  };
}

/**
 * Subtle background tint for the whole page when context filters are active.
 * Returns undefined when no contexts are selected (revert to default bg).
 * When multiple contexts selected, averages their hues.
 */
export function contextTintStyle(
  selected: string[]
): React.CSSProperties | undefined {
  if (selected.length === 0) return undefined;
  const avg =
    selected.reduce((sum, c) => sum + contextHue(c), 0) / selected.length;
  return { backgroundColor: `hsl(${Math.round(avg)}, 25%, 97%)` };
}
