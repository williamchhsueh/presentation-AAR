# Image Format Reference

Technical notes on raster vs vector formats as used in `figure_tools.py`.

---

## First Principles

### Raster (PNG)

A 2D grid of pixels. Each pixel stores color values (R, G, B, A). The image is defined at a fixed resolution.

- **Pros**: Exact pixel-level control; lossless; supports alpha channel (RGBA); universally compatible; zero approximation
- **Cons**: Fixed resolution — zooming past 100% reveals the pixel grid; file size grows with dimensions squared; no semantic structure

**Project note**: All 10 source figures are RGBA PNGs at 1999 px wide, no embedded DPI metadata.

---

### SVG — embed method (`--method embed`)

The PNG bytes are base64-encoded and placed inside a single `<image>` tag in an SVG wrapper:

```xml
<svg width="1999" height="825">
  <image href="data:image/png;base64,iVBOR..."/>
</svg>
```

The SVG container is resolution-independent, but the *content* (`<image>`) is still a bitmap. Zooming past 100% pixelates exactly like a PNG.

- **Pros**: Lossless, zero approximation, always works, trivial to generate
- **Cons**: Not actually vector; file is ~33% larger than source PNG (base64 overhead); "SVG" in name only

---

### SVG — vtracer method (`--method vtracer`)

The raster bitmap is algorithmically traced into `<path>` bezier curves organized in color layers. Output is pure mathematical path data — no pixel grid:

```xml
<svg>
  <path d="M 42 17 C 43 18 44 19 ..."/>
  <path d="M 120 55 L 200 55 ..."/>
  ...
</svg>
```

Bezier curves are parametric equations evaluated at render time, so there is no native pixel size — 400% zoom is as sharp as 100%.

- **Pros**: Resolution-independent at any zoom; semantically structured; scales perfectly for print
- **Cons**: Auto-tracing is *approximation* — text becomes traced outlines (not selectable), fine gradients get segmented into many small path fills, dense scatter plots may look painted-over; file can be larger than source PNG for high-complexity figures (e.g., fig01: 772 KB SVG vs 378 KB PNG)

---

### SVG — potrace method (`--method potrace`)

Converts the image to grayscale, then traces black/white boundaries into bezier paths via the `potrace` CLI.

- **Pros**: Very clean output for pure line art; minimal file size
- **Cons**: Loses all color; output is monochrome — not suitable for scientific figures with colored data

---

## Decision Matrix

| Format | Resolution-independent | Lossless | Preserves color | Complexity |
|---|---|---|---|---|
| PNG | No | Yes | Yes (exact) | Simple |
| SVG embed | No (raster inside) | Yes | Yes (exact) | Simple |
| SVG vtracer | **Yes** | No (approximated) | Yes (approximate) | Medium |
| SVG potrace | **Yes** | No | No (B&W only) | Low |

**Rule of thumb**: Use `vtracer` when zoom/print fidelity matters. Fall back to `embed` (or high-res PNG) when tracing artifacts are unacceptable — dense scatter plots, heatmaps, smooth gradients.

---

## Verification: confirming true vector output

```bash
# vtracer SVG: expect many <path> elements, zero <image> tags
grep -c '<path' figure/paper_fig02_PGR_schematic.svg   # e.g., 569
grep -c '<image' figure/paper_fig02_PGR_schematic.svg  # should be 0

# embed SVG: expect 0 paths, 1 image tag
grep -c '<path' figure/paper_fig02_PGR_schematic.svg   # 0
grep -c '<image' figure/paper_fig02_PGR_schematic.svg  # 1
```
