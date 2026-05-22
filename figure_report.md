# Figure Report

Generated with `code/figure_tools.py inspect` on 2026-05-22.

## Attributes Summary

| # | Filename | Width × Height (px) | Mode | DPI | File Size |
|---|---|---|---|---|---|
| fig01 | paper_fig01_PGR_vs_hillclimbing_hours.png | 1999 × 825 | RGBA | — | 377.6 KB |
| fig02 | paper_fig02_PGR_schematic.png | 1999 × 647 | RGBA | — | 105.6 KB |
| fig03 | paper_fig03_human_baselines.png | 1999 × 860 | RGBA | — | 141.8 KB |
| fig04 | paper_fig04_AAR_setup_overview.png | 1999 × 1764 | RGBA | — | 385.7 KB |
| fig05 | paper_fig05_PGR_seeded_directions.png | 1999 × 825 | RGBA | — | 214.4 KB |
| fig06 | paper_fig06_swarm_orbit_animation.gif | 2175 × 1080 | P (palette) | — | 6910.2 KB |
| fig07 | paper_fig07_category_entropy.png | 1999 × 825 | RGBA | — | 210.5 KB |
| fig08 | paper_fig08_code_complexity.png | 1999 × 1495 | RGBA | — | 383.9 KB |
| fig09 | paper_fig09_AAR_ideas_transfer.png | 1999 × 1020 | RGBA | — | 103.3 KB |
| fig10 | paper_fig10_scaffolding_schematic.png | 1999 × 1118 | RGBA | — | 271.9 KB |

### Key observations
- All 9 PNGs share the same width (1999 px) — consistent export from the paper source
- All PNGs are **RGBA** mode — they carry an alpha channel (white background is not truly transparent yet)
- No DPI metadata is embedded in any file — assume 72 ppi (screen resolution)
- **fig06** is an **animated GIF**: 260 frames, palette mode, slightly different canvas size (2175 × 1080). It is excluded from PNG/SVG batch operations below.
- ICC color profile: none in all files

---

## Derived Assets

### Black-background PNGs (`*_dark.png`)

Created with `set-bg --color 0,0,0 --threshold 30`: replaces near-white pixels (±30 tolerance)
with black while preserving all other figure colors (chart lines, labels, data points).

| Filename | Source | Method |
|---|---|---|
| paper_fig01_PGR_vs_hillclimbing_hours_dark.png | fig01 | `invert-bg` (full channel inversion) |
| paper_fig02_PGR_schematic_dark.png | fig02 | `invert-bg` (full channel inversion) |
| paper_fig03_human_baselines_dark.png | fig03 | `set-bg --color 0,0,0` |
| paper_fig04_AAR_setup_overview_dark.png | fig04 | `set-bg --color 0,0,0` |
| paper_fig05_PGR_seeded_directions_dark.png | fig05 | `set-bg --color 0,0,0` |
| paper_fig07_category_entropy_dark.png | fig07 | `set-bg --color 0,0,0` |
| paper_fig08_code_complexity_dark.png | fig08 | `set-bg --color 0,0,0` |
| paper_fig09_AAR_ideas_transfer_dark.png | fig09 | `set-bg --color 0,0,0` |
| paper_fig10_scaffolding_schematic_dark.png | fig10 | `set-bg --color 0,0,0` |

> fig01 and fig02 `_dark` files were created in a previous session via `invert-bg` (inverts all RGB channels).
> figs 03–10 use `set-bg` which only replaces near-white background, preserving original colors.
> For consistency, consider regenerating fig01/02 with `set-bg --color 0,0,0`.

### SVG files (`*.svg`)

Created with `to-svg --method embed`: lossless PNG-in-SVG wrapper using base64 encoding.
These are vector containers — infinitely scalable — but raster content inside.

| Filename | Source |
|---|---|
| paper_fig01_PGR_vs_hillclimbing_hours.svg | fig01 |
| paper_fig02_PGR_schematic.svg | fig02 |
| paper_fig03_human_baselines.svg | fig03 |
| paper_fig04_AAR_setup_overview.svg | fig04 |
| paper_fig05_PGR_seeded_directions.svg | fig05 |
| paper_fig07_category_entropy.svg | fig07 |
| paper_fig08_code_complexity.svg | fig08 |
| paper_fig09_AAR_ideas_transfer.svg | fig09 |
| paper_fig10_scaffolding_schematic.svg | fig10 |

fig06 GIF is excluded (animated GIF → SVG conversion not supported by the embed method).
