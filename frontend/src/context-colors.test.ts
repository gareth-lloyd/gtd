import { describe, it, expect } from 'vitest';
import { contextHue, contextChipStyle, contextTintStyle } from './context-colors';

describe('contextHue', () => {
  it('returns a number between 0 and 359', () => {
    const names = ['calls', 'computer', 'errands', 'meetings', 'office',
                   'anywhere', 'garden', 'home', 'kitchen'];
    for (const name of names) {
      const hue = contextHue(name);
      expect(hue).toBeGreaterThanOrEqual(0);
      expect(hue).toBeLessThan(360);
    }
  });

  it('is deterministic', () => {
    expect(contextHue('calls')).toBe(contextHue('calls'));
    expect(contextHue('computer')).toBe(contextHue('computer'));
  });

  it('produces distinct hues for common GTD contexts', () => {
    const names = ['calls', 'computer', 'errands', 'meetings', 'office', 'anywhere'];
    const hues = names.map(contextHue);
    // No two hues should be within 15° of each other
    for (let i = 0; i < hues.length; i++) {
      for (let j = i + 1; j < hues.length; j++) {
        const diff = Math.abs(hues[i] - hues[j]);
        const circularDiff = Math.min(diff, 360 - diff);
        expect(circularDiff, `${names[i]}(${hues[i]}) vs ${names[j]}(${hues[j]})`)
          .toBeGreaterThanOrEqual(15);
      }
    }
  });

  it('distributes across the full hue range (not all clustered)', () => {
    const names = ['calls', 'computer', 'errands', 'meetings', 'office',
                   'anywhere', 'garden', 'home', 'kitchen'];
    const hues = names.map(contextHue);
    const min = Math.min(...hues);
    const max = Math.max(...hues);
    // Spread should cover at least 180° of the wheel
    expect(max - min).toBeGreaterThanOrEqual(180);
  });
});

describe('contextChipStyle', () => {
  it('returns backgroundColor and color properties', () => {
    const style = contextChipStyle('calls');
    expect(style).toHaveProperty('backgroundColor');
    expect(style).toHaveProperty('color');
  });

  it('background is a light pastel (90% lightness)', () => {
    const style = contextChipStyle('calls');
    expect(style.backgroundColor).toMatch(/^hsl\(\d+, 60%, 90%\)$/);
  });

  it('text is dark (30% lightness)', () => {
    const style = contextChipStyle('calls');
    expect(style.color).toMatch(/^hsl\(\d+, 50%, 30%\)$/);
  });

  it('different contexts produce different colors', () => {
    const a = contextChipStyle('calls');
    const b = contextChipStyle('computer');
    expect(a.backgroundColor).not.toBe(b.backgroundColor);
  });
});

describe('contextTintStyle', () => {
  it('returns undefined when no contexts selected', () => {
    expect(contextTintStyle([])).toBeUndefined();
  });

  it('returns a background-color for single context', () => {
    const style = contextTintStyle(['calls']);
    expect(style).toBeDefined();
    expect(style!.backgroundColor).toMatch(/^hsl\(\d+, 25%, 97%\)$/);
  });

  it('tint hue matches the context hue for single selection', () => {
    const hue = contextHue('calls');
    const style = contextTintStyle(['calls']);
    expect(style!.backgroundColor).toBe(`hsl(${hue}, 25%, 97%)`);
  });

  it('averages hues for multiple selections', () => {
    const hueA = contextHue('calls');
    const hueB = contextHue('computer');
    const avg = Math.round((hueA + hueB) / 2);
    const style = contextTintStyle(['calls', 'computer']);
    expect(style!.backgroundColor).toBe(`hsl(${avg}, 25%, 97%)`);
  });

  it('tint is very subtle (97% lightness, 25% saturation)', () => {
    const style = contextTintStyle(['errands']);
    // The lightness and saturation should be low enough to not
    // overpower the UI
    expect(style!.backgroundColor).toContain('25%, 97%');
  });
});
