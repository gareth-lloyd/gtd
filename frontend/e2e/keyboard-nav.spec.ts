import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("keyboard nav", () => {
  test("j/k navigate selection without entering edit mode; Enter opens editor; Escape ladder", async ({
    page,
  }) => {
    await seedItemInNext({ title: "Alpha" });
    await seedItemInNext({ title: "Bravo" });
    await seedItemInNext({ title: "Charlie" });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Alpha" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Bravo" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Charlie" })).toBeVisible();

    // Items render newest-first, so the first card is "Charlie".
    const cards = page.locator(".item");
    await expect(cards).toHaveCount(3);

    // From idle, j picks the first card; no editor visible.
    await page.keyboard.press("j");
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);
    await expect(cards.nth(0)).not.toHaveClass(/(^| )editing( |$)/);
    await expect(page.getByPlaceholder(/Notes/i)).toHaveCount(0);

    // j moves to the second card.
    await page.keyboard.press("j");
    await expect(cards.nth(0)).not.toHaveClass(/(^| )selected( |$)/);
    await expect(cards.nth(1)).toHaveClass(/(^| )selected( |$)/);

    // k moves back.
    await page.keyboard.press("k");
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);

    // Enter opens the editor on the selected card.
    await page.keyboard.press("Enter");
    await expect(cards.nth(0)).toHaveClass(/(^| )editing( |$)/);
    await expect(page.getByPlaceholder(/Notes/i)).toBeVisible();

    // Single Escape from inside the editor: stop editing, stay selected.
    await page.keyboard.press("Escape");
    await expect(cards.nth(0)).not.toHaveClass(/(^| )editing( |$)/);
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);

    // Second Escape: deselect.
    await page.keyboard.press("Escape");
    await expect(cards.nth(0)).not.toHaveClass(/(^| )selected( |$)/);
  });

  test("first click selects (collapsed); second click opens the editor", async ({ page }) => {
    await seedItemInNext({ title: "Alpha" });
    await page.goto(`/${ENV}/next`);

    const card = page.locator(".item").first();
    await expect(card).toBeVisible();

    await card.click();
    await expect(card).toHaveClass(/(^| )selected( |$)/);
    await expect(card).not.toHaveClass(/(^| )editing( |$)/);
    await expect(page.getByPlaceholder(/Notes/i)).toHaveCount(0);

    await card.click();
    await expect(card).toHaveClass(/(^| )editing( |$)/);
    await expect(page.getByPlaceholder(/Notes/i)).toBeVisible();
  });

  test("Escape inside the capture bar blurs the input but preserves item selection", async ({
    page,
  }) => {
    await seedItemInNext({ title: "Alpha" });
    await page.goto(`/${ENV}/next`);

    // Wait for items to render before keyboard nav — navigableIds is wired
    // up only after the first ItemList render.
    await expect(page.locator(".item-title", { hasText: "Alpha" })).toBeVisible();

    await page.keyboard.press("j");
    const cards = page.locator(".item");
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);

    // Open capture and type something.
    await page.keyboard.press("c");
    const capture = page.getByPlaceholder("Capture to inbox…");
    await expect(capture).toBeFocused();
    await capture.fill("draft thought");

    // Escape blurs the capture input — the underlying selection should remain.
    await page.keyboard.press("Escape");
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);
  });
});
