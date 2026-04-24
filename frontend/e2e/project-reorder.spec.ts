import { test, expect, ENV, seedProject, seedItemInNext } from './fixtures';

test.describe('project reorder', () => {
  test('drag-reorder two actions persists on reload', async ({ page }) => {
    await seedProject({ id: 'launch-blog', title: 'Launch blog' });
    await seedItemInNext({ title: 'First action', project: 'launch-blog' });
    await seedItemInNext({ title: 'Second action', project: 'launch-blog' });

    await page.goto(`/${ENV}/projects/launch-blog`);
    const titles = page.locator('.item-with-handle .item-title');
    await expect(titles).toHaveCount(2);
    await expect(titles).toHaveText(['First action', 'Second action']);

    // @dnd-kit listens for pointer events (5px activation distance), so we
    // simulate manually rather than relying on Playwright's dragTo.
    const handles = page.getByRole('button', { name: 'Drag to reorder' });
    const src = await handles.nth(1).boundingBox();
    const dst = await handles.nth(0).boundingBox();
    if (!src || !dst) throw new Error('drag handles not visible');

    const srcX = src.x + src.width / 2;
    const srcY = src.y + src.height / 2;
    const dstX = dst.x + dst.width / 2;
    const dstY = dst.y + dst.height / 2;

    await page.mouse.move(srcX, srcY);
    await page.mouse.down();
    await page.mouse.move(srcX, srcY - 10, { steps: 5 });
    await page.mouse.move(dstX, dstY - 5, { steps: 10 });
    await page.mouse.up();

    // Optimistic update should flip the order immediately; wait for it.
    await expect(titles).toHaveText(['Second action', 'First action']);

    await page.reload();
    const titlesAfter = page.locator('.item-with-handle .item-title');
    await expect(titlesAfter).toHaveCount(2);
    await expect(titlesAfter).toHaveText(['Second action', 'First action']);
  });
});
