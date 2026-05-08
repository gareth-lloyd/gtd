import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("search", () => {
  test("/ focuses the search bar and Enter on a hit navigates to the item", async ({ page }) => {
    await seedItemInNext({ title: "Searchable widget" });
    await seedItemInNext({ title: "Other unrelated" });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Searchable widget" })).toBeVisible();

    // / focuses the bar.
    await page.keyboard.press("/");
    const bar = page.getByPlaceholder(/Search…/);
    await expect(bar).toBeFocused();

    await bar.fill("widget");
    const dropdown = page.locator(".search-dropdown");
    await expect(dropdown).toBeVisible();
    await expect(dropdown.locator(".search-hit", { hasText: "Searchable widget" })).toBeVisible();

    await bar.press("Enter");
    await expect(page).toHaveURL(/\/items\//);
    await expect(page.locator(".item-title", { hasText: "Searchable widget" })).toBeVisible();
  });

  test("Escape inside the search bar clears the query without navigating", async ({ page }) => {
    await seedItemInNext({ title: "Stay put" });

    await page.goto(`/${ENV}/next`);
    await page.keyboard.press("/");
    const bar = page.getByPlaceholder(/Search…/);
    await bar.fill("stay");
    await expect(page.locator(".search-dropdown")).toBeVisible();

    await bar.press("Escape");
    await expect(bar).toHaveValue("");
    await expect(page).toHaveURL(/\/next/);
  });
});
