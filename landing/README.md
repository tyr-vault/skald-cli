# Skald — landing page

Static marketing site for the [Skald](../README.md) CLI — a local-first developer knowledge pipeline. Built with Vite, React, and TanStack Router; styled with Tailwind CSS v4.

## Local development

```bash
cd landing
npm install
npm run dev
```

Open the URL Vite prints (default `http://localhost:5173`). For the same asset paths as GitHub Pages:

```bash
VITE_BASE_PATH=/skald/ npm run dev
```

## Build

```bash
npm run build:pages
```

Produces `dist/` and copies `index.html` to `404.html` so client-side routes work on GitHub Pages.

Preview the production build:

```bash
VITE_BASE_PATH=/skald/ npm run preview
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `VITE_BASE_PATH` | Vite `base` and router basepath (default `/skald/`). In CI this is set to `/<repository-name>/`. |
| `VITE_TOOL_REPO_URL` | GitHub URL for the CLI repo (optional). |
| `VITE_TOOL_README_URL` | Full URL to the CLI README (optional). |

## Deploy to GitHub Pages

Live URL after first successful deploy (when the GitHub repo is named `skald`): https://rdvid.github.io/skald/

1. In GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Push to `master` (or run **Deploy GitHub Pages** from the Actions tab).

The workflow [`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml) builds from `landing/` with `VITE_BASE_PATH=/<repo>/`. Client routes work via `dist/404.html` plus `public/.nojekyll`.

## Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Dev server |
| `npm run build` | Production build to `dist/` |
| `npm run build:pages` | Build + SPA `404.html` for Pages |
| `npm run preview` | Serve `dist/` locally |
| `npm test` | Vitest routing smoke test |
