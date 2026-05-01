import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("workflow", () => {
  test("complete action moves item out of next", async ({ page }) => {
    await seedItemInNext({ title: "Finish report" });

    await page.goto(`/${ENV}/next`);
    const card = page.locator(".item-title", { hasText: "Finish report" });
    await expect(card).toBeVisible();

    // Hover to reveal workflow actions, then click "✓ done".
    await card.hover();
    await page
      .getByRole("button", { name: /✓\s*done/ })
      .first()
      .click();

    await expect(page.locator(".item-title", { hasText: "Finish report" })).toHaveCount(0);
  });

  test("context filter narrows the next list", async ({ page }) => {
    await seedItemInNext({ title: "Call Alice", contexts: ["calls"] });
    await seedItemInNext({ title: "Draft wiki", contexts: ["computer"] });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Call Alice" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Draft wiki" })).toBeVisible();

    // Toggle the @calls checkbox in the filter aside.
    await page
      .locator(".filter-section", { hasText: "Contexts" })
      .getByRole("checkbox", { name: "@calls" })
      .check();

    await expect(page).toHaveURL(/contexts=calls/);
    await expect(page.locator(".item-title", { hasText: "Call Alice" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Draft wiki" })).toHaveCount(0);
  });
});
