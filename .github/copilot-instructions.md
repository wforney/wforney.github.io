# Copilot Instructions

## Overview

This is a Jekyll static site for William Forney's personal blog, hosted on GitHub Pages at [wforney.github.io](https://wforney.github.io). The site uses the [Chirpy theme](https://github.com/cotes2333/jekyll-theme-chirpy) v7.2 and is migrated from a WordPress blog.

## Build & Local Development

```bash
# Install dependencies
bundle install

# Serve locally with live reload
bundle exec jekyll serve

# Production build (matches CI)
bundle exec jekyll build
```

Ruby 3.3 is required (matches CI). Deployment happens automatically via GitHub Actions on push to `main`.

## Architecture

- `_posts/` — blog posts as Markdown, named `YYYY-MM-DD-slug.md`
- `_tabs/` — nav tabs collection (about, archives, categories, tags, writings); each file controls a top-level nav item
- `writings/` — creative writing pieces (separate from blog posts)
- `assets/img/posts/` — post images
- `_includes/` — custom theme overrides (footer, sidebar-bottom)
- `_config.yml` — all site configuration including permalink structure

Permalinks are set to `/:year/:month/:day/:title/` to match the original WordPress URL structure.

## Post Front Matter

Every post must include this front matter shape:

```yaml
---
title: "Post Title Here"
date: YYYY-MM-DD
categories: ["Primary Category", "Secondary Category"]
tags: ["tag1", "tag2"]
---
```

- `categories` and `tags` use **inline YAML list syntax** with double-quoted strings: `["foo", "bar"]`
- `original_url` is optional — include it when a post was migrated from WordPress
- Comments are disabled globally; do not add `comments: true` to individual posts
- `toc: true` is the default; add `toc: false` only to short posts where a TOC would be unhelpful

## Tab Pages (`_tabs/`)

Tab pages use a minimal front matter with `icon` (Font Awesome class) and `order`:

```yaml
---
icon: fas fa-some-icon
order: N
---
```

## Python Utility Scripts

These scripts are used for blog migration/maintenance and are excluded from the Jekyll build:

- `scrape_blog.py` — scrapes WordPress site via sitemap and converts posts to Jekyll Markdown
- `cleanup_posts.py` — deduplicates categories/tags, converts indented code blocks to fenced blocks
- `download_images.py` / `recover_images.py` — fetch post images into `assets/img/posts/`

Run `python cleanup_posts.py` after scraping or manually editing posts in bulk to normalize formatting.
