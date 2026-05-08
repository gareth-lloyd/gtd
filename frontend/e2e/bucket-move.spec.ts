import { test, expect, ENV, seedItemInNext } from "./fixtures";

async function clickAndAwait(page: import("@playwright/test").Page, name: string) {
  const moveResp = page.waitForResponse(
    (r) => /\/items\/[^/]+\/move\//.test(r.url()) && r.request().method() === "POST" && r.ok(),
  );
  await page.getByRole("button", { name }).first().click();
  await moveResp;
}

test.describe("bucket transitions", () => {
  test("→ waiting moves item from next to waiting", async ({ page }) => {
    await seedItemInNext({ title: "Awaiting reply" });

    await page.goto(`/${ENV}/next`);
    const card = page.locator(".item", { hasText: "Awaiting reply" });
    await expect(card).toBeVisible();
    await card.hover();
    await clickAndAwait(page, "→ waiting");

    await expect(page.locator(".item-title", { hasText: "Awaiting reply" })).toHaveCount(0);

    await page.locator(".side-nav").getByRole("link", { name: "waiting" }).click();
    await expect(page.locator(".item-title", { hasText: "Awaiting reply" })).toBeVisible();
  });

  test("→ someday moves item from next to someday and back", async ({ page }) => {
    await seedItemInNext({ title: "Maybe later" });

    await page.goto(`/${ENV}/next`);
    const card = page.locator(".item", { hasText: "Maybe later" });
    await expect(card).toBeVisible();
    await card.hover();
    await clickAndAwait(page, "→ someday");

    await page.locator(".side-nav").getByRole("link", { name: "someday" }).click();
    const someday = page.locator(".item", { hasText: "Maybe later" });
    await expect(someday).toBeVisible();
    await someday.hover();
    await clickAndAwait(page, "→ next");

    await page.locator(".side-nav").getByRole("link", { name: "next" }).click();
    await expect(page.locator(".item-title", { hasText: "Maybe later" })).toBeVisible();
  });
});
