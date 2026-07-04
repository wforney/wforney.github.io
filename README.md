# wforney.github.io

William Forney's personal blog, built with [Jekyll](https://jekyllrb.com/) and the [Chirpy theme](https://github.com/cotes2333/jekyll-theme-chirpy) and hosted on GitHub Pages.

## Overview

- **Site type:** static blog and writing archive
- **Hosting:** GitHub Pages
- **Deployment:** GitHub Actions on pushes to `main`
- **Runtime:** Ruby 3.3

## Local development

```bash
bundle install
bundle exec jekyll serve
```

The site will be available locally at the URL printed by Jekyll, usually `http://127.0.0.1:4000`.

## Production build

```bash
bundle exec jekyll build
```

This matches the GitHub Pages build used in CI. The deploy workflow passes the GitHub Pages base path automatically.

## Browser tests

```bash
npm install
npm run test:playwright
```

The Playwright test suite spins up a local Jekyll server and exercises the Pins overlay.

## Repository structure

- `_posts/` - blog posts in `YYYY-MM-DD-slug.md` format
- `_tabs/` - top-level navigation pages
- `writings/` - creative writing pieces
- `assets/` - site images and CSS
- `_includes/` - theme overrides
- `_layouts/` - custom page layouts
- `_data/` - shared data files such as authors
- `.github/workflows/` - build and deploy automation

## Content conventions

- Posts use front matter with `title`, `date`, `categories`, and `tags`
- Categories and tags use inline YAML list syntax
- Comments are disabled globally
- Permalinks follow the original WordPress-style URL structure

## Deployment

Pushes to `main` trigger `.github/workflows/deploy.yml`, which:

1. Checks out the repository
2. Installs Ruby dependencies
3. Builds the site with Jekyll
4. Publishes the artifact to GitHub Pages
