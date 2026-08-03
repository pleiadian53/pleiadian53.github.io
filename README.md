# pleiadian53.github.io

Personal site for **Barnett Chiu** — served at <https://pleiadian53.github.io/>.

The page presents the name he goes by. "Po-Hsiang Chiu" is the publishing name and is kept in
the meta description, the About note, and the JSON-LD `name` (mirroring the ORCID record, where
the credit-name is Po-Hsiang Chiu and Barnett Chiu is an other-name). Keep all three in place —
they are what tie searches for either name to the same person.

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
- **`assets/crop-*.svg`** — the crop circles in the background. See below.

## Crop circles

Five formations from the 2026 season, catalogued by [Temporary Temples][tt]:

| File | Formation | Reported | Catalogue description |
|---|---|---|---|
| `crop-cosmos.svg` | Zeals Knoll nr Mere, Wiltshire | 5 Jul 2026 | free standing bubbles in a flower-like design |
| `crop-helix.svg` | Zürcher Weinland, Switzerland | 23 Jun 2026 | double spiral design |
| `crop-13moons.svg` | Roundway (2), Wiltshire | 18 Jul 2026 | 13-point star & crescent moon |
| `crop-trine.svg` | Bishopstone, Wiltshire | 4 Jul 2026 | triangles and circles |
| `crop-cipher.svg` | Fox Hill, Wiltshire | 21 Jul 2026 | a long pictogram of circles, rings and keys |

Filenames follow how each formation is commonly *read* rather than its shape — bubbles at every
scale as nested worlds, a double spiral as a helix, thirteen points and a crescent as the year's
lunations, triangles in a round as a trine, a line of glyphs and keys as a cipher. Names only; no
claim is made about meaning.

The geometry is **original**, constructed from the catalogue's verbal description of each
formation. Nothing is traced from a photograph. Regenerate all five with `dev/mkfield.py`.

**Choosing a formation.** The [season list][tt] annotates commissioned formations explicitly —
Hackpen Hill (26 Jun, *man-made for TV*), Journet, France (28 Jun, *man-made for exhibition*).
None of the five above carries such an annotation. Keep to unflagged entries.

**How they are applied.** Each SVG is a CSS **mask**, so the figure takes its colour from
`--signal` and one file serves light and dark. A section opts in with `.field` plus a `.f-*`
modifier supplying the source, size and corner. `crop-cipher.svg` is laid along a line rather than
round, so it also sets `--f-ar` and runs as a wide strip.

Three multipliers govern how strongly a formation reads — the element's opacity (`--cc-op`,
`--cc-op-sm`), the radial fade composited into the mask, and the stroke/fill opacities inside the
SVG itself. They multiply, so a small change to one is easy to underestimate.

[tt]: https://temporarytemples.co.uk/project/crop-circles-2026-season-info

## Custom domain, if ever

Add a `CNAME` file containing the bare domain, point a `CNAME`/`ALIAS` record at
`pleiadian53.github.io`, and enable *Enforce HTTPS*. Nothing else changes.

Renaming the GitHub account is **not** the way to get a name into the URL: GitHub does not
redirect Pages URLs on rename, and `https://pleiadian53.github.io/agentic-spliceai/` is baked into
that project's `CITATION.cff` and its Zenodo record.
