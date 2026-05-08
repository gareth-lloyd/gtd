import { test, expect, ENV, seedItemInNext } from "./fixtures";

test.describe("detail panel", () => {
  test("selecting a card renders the detail panel with project/contexts/energy/actions", async ({
    page,
  }) => {
    await seedItemInNext({ title: "Inspect me", contexts: ["calls"], energy: "low" });

    await page.goto(`/${ENV}/next`);
    await expect(page.locator(".item-title", { hasText: "Inspect me" })).toBeVisible();

    // Click selects (without entering edit mode); detail panel should populate.
    await page.locator(".item", { hasText: "Inspect me" }).click();

    const detail = page.locator(".detail-panel");
    await expect(detail).toBeVisible();
    await expect(detail.getByText("Project", { exact: true })).toBeVisible();
    await expect(detail.getByText("Contexts", { exact: true })).toBeVisible();
    await expect(detail.getByText("Energy", { exact: true })).toBeVisible();
    await expect(detail.getByText("Actions", { exact: true })).toBeVisible();

    // The seeded contexts/energy are already toggled on in the panel.
    await expect(
      detail.locator('.chip-toggle[aria-pressed="true"]', { hasText: "@calls" }),
    ).toBeVisible();
    await expect(
      detail.locator('.chip-toggle[aria-pressed="true"]', { hasText: /low/ }),
    ).toBeVisible();
  });

  test("toggling a context chip in the detail panel patches the item", async ({ page }) => {
    await seedItemInNext({ title: "Context-less" });

    await page.goto(`/${ENV}/next`);
    await page.locator(".item", { hasText: "Context-less" }).click();

    const detail = page.locator(".detail-panel");
    await expect(detail).toBeVisible();

    const patchResp = page.waitForResponse(
      (r) => /\/items\/[^/]+\/$/.test(r.url()) && r.request().method() === "PATCH" && r.ok(),
    );
    await detail
      .locator(".detail-section", { hasText: "Contexts" })
      .getByRole("button", { name: "@computer" })
      .click();
    await patchResp;

    // The collapsed card sports the new chip.
    await expect(
      page.locator(".item", { hasText: "Context-less" }).locator(".context-chip", {
        hasText: "@computer",
      }),
    ).toBeVisible();
  });
});
