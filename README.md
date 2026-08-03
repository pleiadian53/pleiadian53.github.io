# pleiadian53.github.io

Personal site for **Po-Hsiang (Barnett) Chiu** — served at <https://pleiadian53.github.io/>.

Hand-written HTML and CSS. No build step, no framework, no JavaScript.

```
index.html          the whole page (content + inline SVG schematic + JSON-LD)
styles.css          palette tokens, light/dark, responsive
assets/og-image.png 1200x630 social card
llms.txt            plain-text summary for LLM crawlers
sitemap.xml         one URL
robots.txt          allow all
```

## Preview locally

```bash
python3 -m http.server 8080
open http://localhost:8080/
```

Check both colour schemes — macOS System Settings → Appearance, or DevTools →
Rendering → *Emulate prefers-color-scheme*.

## Publishing

This repository is named after the account, so GitHub Pages serves it at the account root.
In **Settings → Pages**, set the source to *Deploy from a branch* → `main` / `/ (root)`.

It does **not** affect the project sites already published from other repositories
(`/agentic-spliceai/`, `/ssl-lab/`, `/GRL/`, `/genai-lab/`, `/ehr-sequencing/`, `/cf-ensemble/`) —
those are separate repositories on separate paths.

## Editing

- **Palette** — every colour is a custom property at the top of `styles.css`, defined three times:
  `:root`, `@media (prefers-color-scheme: dark)`, and the two `:root[data-theme=…]` blocks.
  Change a value in all the places it appears; never style a component inside the media query.
- **Adding a project** — copy an `<article class="proj">` block. Private, unlinked projects use
  `class="proj is-private"` with a `<span class="tag">private</span>` and no `<a>` on the heading.
- **The schematic** — plain SVG in `index.html`, laid out on a 940×344 grid. Nodes are
  `<rect>` + `<text>` pairs; `.hot` outlines a focus project in the accent blue, `.priv` marks a
  private one in dashed copper. Keep the `<desc>` in sync — it is what screen readers and
  crawlers read.
- **`llms.txt`** — mirrors the page in prose. Update it whenever a project is added or its
  description changes materially, otherwise the two drift.

## Custom domain, if ever

Add a `CNAME` file containing the bare domain, point a `CNAME`/`ALIAS` record at
`pleiadian53.github.io`, and enable *Enforce HTTPS*. Nothing else changes.

Renaming the GitHub account is **not** the way to get a name into the URL: GitHub does not
redirect Pages URLs on rename, and `https://pleiadian53.github.io/agentic-spliceai/` is baked into
that project's `CITATION.cff` and its Zenodo record.
