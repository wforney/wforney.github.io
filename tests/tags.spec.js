const { test, expect } = require("@playwright/test");

test("every tag links to an archive containing its posts", async ({ page, request }) => {
  await page.goto("/tags/");

  const tags = await page.locator("#tags a.tag").evaluateAll((links) =>
    links.map((link) => ({
      href: link.getAttribute("href"),
      count: Number(link.querySelector("span").textContent),
    }))
  );
  expect(tags.length).toBeGreaterThan(0);
  expect(new Set(tags.map((tag) => tag.href)).size).toBe(tags.length);

  for (const tag of tags) {
    const response = await request.get(tag.href);
    expect(response.status(), tag.href).toBe(200);
    const html = await response.text();
    const postCount = await page.evaluate((html) => {
      const doc = new DOMParser().parseFromString(html, "text/html");
      return doc.querySelectorAll("#page-tag ul.content > li").length;
    }, html);
    expect(postCount, tag.href).toBe(tag.count);
  }
});

test("post and trending tag links open tag archives", async ({ page }) => {
  await page.goto("/tags/asp-net-core/");
  await page.locator("#page-tag ul.content a").first().click();

  const links = page.locator('a.post-tag[href^="/tags/"]');
  const destinations = [...new Set(await links.evaluateAll((elements) =>
    elements.map((element) => element.getAttribute("href"))
  ))];
  expect(destinations).toContain("/tags/asp-net-core/");
  expect(destinations).toContain("/tags/c/");
  expect(destinations).toContain("/tags/net/");

  for (const href of destinations) {
    const response = await page.goto(href);
    expect(response.status(), href).toBe(200);
    await expect(page.locator("#page-tag ul.content > li").first()).toBeVisible();
  }
});
