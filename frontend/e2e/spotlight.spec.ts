import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("spotlight mode", () => {
  test("clicking spotlight hides other items, persists in URL, and updates document.title", async ({
    page,
  }) => {
    await seedItemInNext({ title: "Spotlight target" });
    await seedItemInNext({ title: "Background noise" });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Spotlight target" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Background noise" })).toBeVisible();

    const targetCard = page.locator(".item", { hasText: "Spotlight target" });
    await targetCard.locator(".spotlight-toggle").click();

    await expect(page).toHaveURL(/spotlight=/);
    await expect(page.locator(".item-list.spotlight-mode")).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Background noise" })).toHaveCount(0);
    await expect(page).toHaveTitle(/Spotlight target/);
  });

  test("escape exits spotlight and restores the full list", async ({ page }) => {
    await seedItemInNext({ title: "Focus me" });
    await seedItemInNext({ title: "Other thing" });

    await page.goto(`/${ENV}/next`);
    await page.locator(".item", { hasText: "Focus me" }).locator(".spotlight-toggle").click();
    await expect(page).toHaveURL(/spotlight=/);

    // First Escape deselects the auto-selected card (SelectionContext).
    await page.locator("body").press("Escape");
    // Second Escape exits spotlight.
    await page.locator("body").press("Escape");

    await expect(page).not.toHaveURL(/spotlight=/);
    await expect(page.locator(".item-title", { hasText: "Other thing" })).toBeVisible();
  });

  test("spotlight state restores from a direct URL load", async ({ page }) => {
    const { id } = await seedItemInNext({ title: "Deep link target" });
    await seedItemInNext({ title: "Should be hidden" });

    await page.goto(`/${ENV}/next?spotlight=${id}`);

    await expect(page.locator(".item-list.spotlight-mode")).toBeVisible();
    // Spotlit item is auto-selected; only its title shows.
    await expect(page.locator(".item.selected", { hasText: "Deep link target" })).toBeVisible();
    await expect(page.locator(".item-title", { hasText: "Should be hidden" })).toHaveCount(0);
  });

  test("navigating to a different bucket exits spotlight implicitly", async ({ page }) => {
    await seedItemInNext({ title: "Tracked focus" });

    await page.goto(`/${ENV}/next`);
    await page.locator(".item", { hasText: "Tracked focus" }).locator(".spotlight-toggle").click();
    await expect(page).toHaveURL(/spotlight=/);

    await page.locator(".side-nav").getByRole("link", { name: "inbox" }).click();
    await expect(page).not.toHaveURL(/spotlight=/);
  });
});
