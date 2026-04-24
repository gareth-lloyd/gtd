import { test, expect, ENV } from './fixtures';
import { STUB_AI_RESPONSE } from './global-setup';

test.describe('capture', () => {
  test('regular capture via C shortcut lands item in inbox', async ({ page }) => {
    await page.goto(`/${ENV}/inbox`);
    await expect(page.getByRole('heading', { name: 'gtd' })).toBeVisible();

    await page.keyboard.press('c');
    const titleInput = page.getByPlaceholder('Capture to inbox…');
    await expect(titleInput).toBeFocused();
    await titleInput.fill('Buy milk');
    await page.getByRole('button', { name: 'Capture', exact: true }).click();

    await expect(page.locator('.item-title', { hasText: 'Buy milk' })).toBeVisible();
  });

  test('AI capture via A shortcut uses stub response and creates item', async ({ page }) => {
    await page.goto(`/${ENV}/inbox`);

    await page.keyboard.press('a');
    const aiInput = page.getByPlaceholder(/Describe the action/);
    await expect(aiInput).toBeFocused();
    await aiInput.fill('email jane re Q2 roadmap');
    await page.getByRole('button', { name: /Capture with AI/ }).click();

    await expect(
      page.locator('.item-title', { hasText: STUB_AI_RESPONSE.title }),
    ).toBeVisible();
    await expect(
      page.locator('.context-chip', { hasText: `@${STUB_AI_RESPONSE.contexts[0]}` }),
    ).toBeVisible();
  });
});
