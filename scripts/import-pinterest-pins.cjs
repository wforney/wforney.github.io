#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const { chromium } = require("@playwright/test");

const ROOT = process.cwd();
const DEFAULT_OUTPUT = path.join(ROOT, "_data", "pins.json");

function parseArgs(argv) {
  const args = {
    username: "wforney",
    max: 200,
    scrolls: 24,
    apply: false,
    output: DEFAULT_OUTPUT,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--apply") {
      args.apply = true;
    } else if (arg.startsWith("--username=")) {
      args.username = arg.split("=", 2)[1];
    } else if (arg === "--username") {
      args.username = argv[i + 1];
      i += 1;
    } else if (arg.startsWith("--max=")) {
      args.max = Number(arg.split("=", 2)[1]);
    } else if (arg === "--max") {
      args.max = Number(argv[i + 1]);
      i += 1;
    } else if (arg.startsWith("--scrolls=")) {
      args.scrolls = Number(arg.split("=", 2)[1]);
    } else if (arg === "--scrolls") {
      args.scrolls = Number(argv[i + 1]);
      i += 1;
    } else if (arg.startsWith("--output=")) {
      args.output = path.resolve(arg.split("=", 2)[1]);
    } else if (arg === "--output") {
      args.output = path.resolve(argv[i + 1]);
      i += 1;
    }
  }

  if (!args.username) {
    throw new Error("username is required");
  }
  if (!Number.isFinite(args.max) || args.max <= 0) {
    throw new Error("max must be a positive number");
  }
  if (!Number.isFinite(args.scrolls) || args.scrolls <= 0) {
    throw new Error("scrolls must be a positive number");
  }

  return args;
}

function loadPins(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`pins file not found: ${filePath}`);
  }
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function normalizeUrl(value) {
  if (!value) return "";
  try {
    const u = new URL(value);
    u.hash = "";
    u.search = "";
    return u.toString().replace(/\/+$/, "");
  } catch {
    return String(value).trim().replace(/\/+$/, "");
  }
}

function extractPinId(value) {
  if (!value) return "";
  const m = String(value).match(/\/pin\/(\d+)/i);
  return m ? m[1] : "";
}

function buildExistingKeys(pins) {
  const pinIds = new Set();
  const sourceUrls = new Set();
  const urls = new Set();
  for (const pin of pins) {
    const nSource = normalizeUrl(pin.source_url);
    const nUrl = normalizeUrl(pin.url);
    if (nSource) sourceUrls.add(nSource);
    if (nUrl) urls.add(nUrl);

    const idA = extractPinId(pin.source_url);
    const idB = extractPinId(pin.url);
    if (idA) pinIds.add(idA);
    if (idB) pinIds.add(idB);
  }
  return { pinIds, sourceUrls, urls };
}

function parseSrcset(srcset) {
  if (!srcset) return "";
  const first = srcset.split(",")[0]?.trim() ?? "";
  return first.split(/\s+/)[0] ?? "";
}

async function scrapePinterestPins({ username, max, scrolls }) {
  const url = `https://www.pinterest.com/${encodeURIComponent(username)}/`;
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(2000);

    for (let i = 0; i < scrolls; i += 1) {
      await page.mouse.wheel(0, 6000);
      await page.waitForTimeout(900);
      const count = await page.evaluate(() =>
        document.querySelectorAll("a[href*='/pin/']").length
      );
      if (count >= max) break;
    }

    const pins = await page.evaluate((cap) => {
      const seen = new Set();
      const results = [];
      const nodes = Array.from(document.querySelectorAll("a[href*='/pin/']"));

      for (const a of nodes) {
        if (results.length >= cap) break;
        let href = "";
        try {
          href = new URL(a.getAttribute("href"), window.location.origin).toString();
        } catch {
          continue;
        }

        if (!/\/pin\/\d+\/?$/i.test(href)) continue;

        const normalized = href.replace(/[?#].*$/, "").replace(/\/+$/, "");
        if (seen.has(normalized)) continue;
        seen.add(normalized);

        const img =
          a.querySelector("img") ||
          a.closest('[data-test-id="pinWrapper"]')?.querySelector("img") ||
          a.parentElement?.querySelector("img");

        const title = (img?.getAttribute("alt") || "").trim();
        const image =
          img?.getAttribute("src") ||
          img?.getAttribute("data-src") ||
          parseSrcset(img?.getAttribute("srcset")) ||
          "";

        if (!image) continue;

        results.push({ pinUrl: normalized, title, image });
      }

      function parseSrcset(srcset) {
        if (!srcset) return "";
        const first = srcset.split(",")[0]?.trim() ?? "";
        return first.split(/\s+/)[0] ?? "";
      }

      return results;
    }, max);

    return pins;
  } finally {
    await context.close();
    await browser.close();
  }
}

function toPinRecord(item) {
  const pinId = extractPinId(item.pinUrl);
  const title = item.title || `Pinterest Pin ${pinId}`;
  const now = new Date().toISOString();
  return {
    title,
    url: item.pinUrl,
    image: item.image,
    excerpt: title,
    categories: ["Pinterest"],
    source_url: item.pinUrl,
    source_text: "Source: pinterest.com",
    date: now,
  };
}

function mergePins(existing, imported) {
  const keys = buildExistingKeys(existing);
  const merged = [...existing];
  const added = [];
  const skipped = [];

  for (const item of imported) {
    const normalized = normalizeUrl(item.pinUrl);
    const pinId = extractPinId(item.pinUrl);
    const isDup =
      (pinId && keys.pinIds.has(pinId)) ||
      keys.urls.has(normalized) ||
      keys.sourceUrls.has(normalized);

    if (isDup) {
      skipped.push(item.pinUrl);
      continue;
    }

    const record = toPinRecord(item);
    merged.push(record);
    added.push(record);

    keys.urls.add(normalizeUrl(record.url));
    keys.sourceUrls.add(normalizeUrl(record.source_url));
    if (pinId) keys.pinIds.add(pinId);
  }

  return { merged, added, skipped };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const existing = loadPins(args.output);
  const scraped = await scrapePinterestPins(args);
  const { merged, added, skipped } = mergePins(existing, scraped);

  console.log(`Pinterest profile: ${args.username}`);
  console.log(`Scraped candidates: ${scraped.length}`);
  console.log(`Added: ${added.length}`);
  console.log(`Skipped as duplicates: ${skipped.length}`);

  if (!args.apply) {
    console.log("\nDry run complete. Re-run with --apply to write changes.");
    return;
  }

  fs.writeFileSync(args.output, `${JSON.stringify(merged, null, 2)}\n`, "utf8");
  console.log(`\nUpdated ${args.output}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
