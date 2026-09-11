import { test, expect } from '@playwright/test';

test.describe("SauceDemo Login", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('https://www.saucedemo.com');
  });

  test('FT-001 – Valid Login', async ({ page }) => {
    await page.locator('[data-test="username"]').fill('standard_user');
    await page.locator('[data-test="password"]').fill('secret_sauce');
    await page.locator('[data-test="login-button"]').click();
    await expect(page.locator('[data-test="title"]')).toHaveText("Products");
  });

  test('UX-001 – Swag Labs Heading', async ({ page }) => {
    const logo = page.locator('.login_logo');
    await expect(logo).toBeVisible();
    await expect(logo).toHaveText("Swag Labs");
    await expect(logo).toHaveCSS("font-family", "\"DM Mono\", \"sans-serif\"");
    await expect(logo).toHaveCSS("font-size", "28px");
    await expect(logo).toHaveCSS("font-weight", "400");
  });
});