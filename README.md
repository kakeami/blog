# Kakeami's Blog

A data science blog built with [Quarto](https://quarto.org/) and deployed on GitHub Pages.

Topics: data visualization, pop culture × statistics, and lessons from side projects.

**Live site**: [kakeami.github.io/blog](https://kakeami.github.io/blog)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Development

### Local preview

```bash
source .venv/bin/activate
quarto preview
```

### Build

```bash
source .venv/bin/activate
quarto render
```

The `pre-render` hook automatically runs `scripts/generate_og.py`, which generates OG images for each post and injects `image: og-image.png` into the front matter.

### New post

1. Create `posts/YYYY-MM-topic/index.qmd`
2. Run `quarto render` or `quarto preview`

#### OG image options

**Option A: Use a chart as the OG image**

1. Add `og-source: chart` to the front matter
2. In a hidden cell, call `fig.write_image("og-image.png", width=1200, height=630)`
3. Run `quarto render`

**Option B: Default (cat icon + pastel background)**

1. Write the post
2. Run `quarto render` — the OG image is generated automatically

### Deploy

Push to `main`. GitHub Actions builds and deploys to GitHub Pages.

## Tech stack

- **Quarto** v1.8.27+
- **Python** 3.12
- **Plotly** 5.24.1 (v6 is incompatible with Quarto)
- **GitHub Pages** via GitHub Actions
