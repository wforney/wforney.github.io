const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  use: {
    baseURL: "http://127.0.0.1:4000",
    trace: "on-first-retry",
  },
  webServer: {
    command: "bundle exec jekyll serve --host 127.0.0.1 --port 4000 --no-watch",
    url: "http://127.0.0.1:4000",
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
