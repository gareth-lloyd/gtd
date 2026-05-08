import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("delete + restore", () => {
  test("Delete moves item to trash; restore brings it back to inbox", async ({ page }) => {
    await seedItemInNext({ title: "Throwaway" });

    await page.goto(`/${ENV}/next`);
    const card = page.locator(".item", { hasText: "Throwaway" });
    await expect(card).toBeVisible();
    await card.hover();

    const deleteResp = page.waitForResponse(
      (r) => /\/items\/[^/]+\/$/.test(r.url()) && r.request().method() === "DELETE" && r.ok(),
    );
    await page.getByRole("button", { name: "Delete" }).first().click();
    await deleteResp;

    await expect(page.locator(".item-title", { hasText: "Throwaway" })).toHaveCount(0);

    await page.locator(".side-nav").getByRole("link", { name: "trash" }).click();
    const trashed = page.locator(".item", { hasText: "Throwaway" });
    await expect(trashed).toBeVisible();
    await trashed.hover();

    const restoreResp = page.waitForResponse(
      (r) => /\/items\/[^/]+\/move\//.test(r.url()) && r.request().method() === "POST" && r.ok(),
    );
    await page
      .getByRole("button", { name: /↺ restore/ })
      .first()
      .click();
    await restoreResp;

    await page.locator(".side-nav").getByRole("link", { name: "inbox" }).click();
    await expect(page.locator(".item-title", { hasText: "Throwaway" })).toBeVisible();
  });
});
