import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("working_on pin", () => {
  test("F shortcut toggles working_on on the selected item and pins it", async ({ page }) => {
    await seedItemInNext({ title: "Older" });
    await seedItemInNext({ title: "Newer" });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Older" })).toBeVisible();

    // j selects the first card (newest-first → "Newer").
    await page.keyboard.press("j");
    const cards = page.locator(".item");
    await expect(cards.nth(0)).toHaveClass(/(^| )selected( |$)/);

    // Move to "Older" with j; press F to pin it as working_on.
    await page.keyboard.press("j");
    const olderCard = page.locator(".item", { hasText: "Older" });
    await expect(olderCard).toHaveClass(/(^| )selected( |$)/);

    const patchResp = page.waitForResponse(
      (r) => /\/items\/[^/]+\/$/.test(r.url()) && r.request().method() === "PATCH" && r.ok(),
    );
    await page.keyboard.press("f");
    await patchResp;

    // Pin class lands on the card and the item floats to the top.
    await expect(olderCard).toHaveClass(/(^| )working-on( |$)/);
    await expect(cards.nth(0)).toHaveText(/Older/);
  });

  test("clicking the pin button toggles working_on and persists across reload", async ({
    page,
  }) => {
    await seedItemInNext({ title: "Pinnable" });

    await page.goto(`/${ENV}/next`);
    const card = page.locator(".item", { hasText: "Pinnable" });
    await expect(card).toBeVisible();

    const patchResp = page.waitForResponse(
      (r) => /\/items\/[^/]+\/$/.test(r.url()) && r.request().method() === "PATCH" && r.ok(),
    );
    await card.locator(".working-on-toggle").click();
    await patchResp;

    await expect(card).toHaveClass(/(^| )working-on( |$)/);

    await page.reload();
    await expect(page.locator(".item", { hasText: "Pinnable" })).toHaveClass(
      /(^| )working-on( |$)/,
    );
  });
});
