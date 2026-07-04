const { test, expect } = require("@playwright/test");

test("opens the pin detail card", async ({ page }) => {
  await page.goto("/pins/");

  const firstPin = page.locator(".pin-card-trigger").first();
  await expect(firstPin).toBeVisible();

  await firstPin.click();

  await expect(page.locator("#pin-modal")).toBeVisible();
  await expect(page.locator("#pin-modal-title")).not.toHaveText("");
});
