import { test, expect, ENV, seedItemInNext } from './fixtures';

test.describe('inline editing', () => {
  test('title edit autosaves and persists across reload', async ({ page }) => {
    await seedItemInNext({ title: 'Original title', energy: 'medium' });

    await page.goto(`/${ENV}/next`);
    const card = page.locator('.item-title', { hasText: 'Original title' });
    await expect(card).toBeVisible();
    await card.click();

    const titleEditor = page.locator('input[value="Original title"]').first();
    await expect(titleEditor).toBeVisible();

    const patchLanded = page.waitForResponse(
      (r) => /\/api\/envs\/[^/]+\/items\/[^/]+\/$/.test(r.url())
        && r.request().method() === 'PATCH'
        && r.ok(),
    );
    await titleEditor.fill('Edited title');
    await patchLanded;

    await page.reload();
    await expect(
      page.locator('.item-title', { hasText: 'Edited title' }),
    ).toBeVisible();
    await expect(
      page.locator('.item-title', { hasText: 'Original title' }),
    ).toHaveCount(0);
  });
});
