"""
gen_fig06_dark.py — Dark-background variants of paper_fig06 animated GIF.

Three variants (pass A, B, C, or nothing to run all):
  python gen_fig06_dark.py          # all three
  python gen_fig06_dark.py A        # only variant A
  python gen_fig06_dark.py B C      # variants B and C

Variant A — Palette remap  (zero re-quantization, cleanest edges)
  Remap only the 256-color palette table; pixel indices stay untouched.
  Background (pure white) → BG_DARK. Achromatic grays → L-inversion so
  dark axes/text become light and near-white anti-alias becomes near-dark.
  Chromatic halos (pastel, L≥0.80) → same hue+sat, L drastically reduced.
  Chromatic core (swarm dots) → L clamped to [0.40, 0.85] for visibility.

Variant B — Adaptive threshold + morphological composite
  Per frame: compute near-white mask → morphological erosion (removes thin
  anti-alias rims) → Gaussian blur (smooth edges) → composite fg over BG_DARK
  → re-quantize to P mode (256 colours, FASTOCTREE).

Variant C — Chrominance-split composite
  Per frame: classify pixels by HLS saturation.
  Achromatic (S < 0.08): remap gray value through dark-bg L-inversion curve.
  Chromatic (S ≥ 0.08): blend toward BG_DARK via min-channel coverage, then
  boost any very-dark chromatic pixels for visibility.
  Blend region smoothed over S ∈ [0.04, 0.12] to avoid hard edge.
"""
from __future__ import annotations

import colorsys
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

BASE = Path(__file__).parent.parent / "figure"
SRC  = BASE / "paper_fig06_swarm_orbit_animation.gif"
BG_DARK = (8, 16, 16)

try:
    _QUANTIZE_METHOD = Image.Quantize.FASTOCTREE
except AttributeError:
    _QUANTIZE_METHOD = 2  # Pillow < 9.1 fallback


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _iter_frames(gif: Image.Image):
    """Yield (composed_frame_copy, duration_ms) for every frame."""
    try:
        while True:
            yield gif.copy(), gif.info.get("duration", 80)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass


def _save_gif(frames: list[Image.Image], durations: list[int],
              out: Path, loop: int) -> None:
    frames[0].save(
        out, save_all=True, append_images=frames[1:],
        loop=loop, duration=durations, optimize=False,
    )


# ---------------------------------------------------------------------------
# Variant A — Palette remap
# ---------------------------------------------------------------------------

def _remap_palette_entry(r: int, g: int, b: int, bg_dark: tuple) -> tuple:
    """Classify one palette entry and return its dark-bg replacement."""
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

    # 1) Pure background: near-white, achromatic
    if l >= 0.95 and s < 0.08:
        return bg_dark

    # 2) Achromatic gray (axes, grid, text, near-bg anti-alias)
    if s < 0.08:
        # Gamma-curved L inversion mapped to dark-bg brightness range:
        #   white (l=1) → 0.05  (nearly bg-dark)
        #   mid-gray (l=0.7) → 0.39  (visible grid on dark)
        #   black (l=0) → 0.90  (near-white text on dark)
        new_l = (1.0 - l) ** 0.70 * 0.85 + 0.05
        gray = max(0, min(255, round(new_l * 255)))
        return (gray, gray, gray)

    # 3) Light chromatic: near-white territory (L ≥ 0.80) — two sub-cases
    if l >= 0.80:
        if s < 0.25:
            # Low-saturation near-bg tint (anti-alias ring around text/axes)
            # → aggressively darken so it reads as near-invisible on dark bg
            new_l = max(0.10, l - 0.82)
        else:
            # High-saturation light fill (actual bubble fill, coloured dot interior)
            # → reduce L to ~50% so it reads as a clearly visible saturated colour
            new_l = max(0.50, l - 0.35)
        rn, gn, bn = colorsys.hls_to_rgb(h, new_l, s)
        return (round(rn * 255), round(gn * 255), round(bn * 255))

    # 4) Chromatic foreground: swarm dot core colors
    # Boost very dark dots for visibility; cap brightness so colors stay rich
    new_l = max(0.40, min(0.85, l))
    rn, gn, bn = colorsys.hls_to_rgb(h, new_l, s)
    return (round(rn * 255), round(gn * 255), round(bn * 255))


def _build_remapped_palette(raw: list[int], bg_dark: tuple) -> list[int]:
    new_palette = list(raw)
    for i in range(256):
        r, g, b = raw[i * 3], raw[i * 3 + 1], raw[i * 3 + 2]
        nr, ng, nb = _remap_palette_entry(r, g, b, bg_dark)
        new_palette[i * 3 : i * 3 + 3] = [nr, ng, nb]
    return new_palette


def remap_palette_gif(src: Path, out: Path, bg_dark: tuple = BG_DARK) -> None:
    """Palette remap via: RGB → quantize-to-original-palette → swap to remapped palette.

    Frames 1+ come out of Pillow as RGBA (disposal compositing), so we can't
    call putpalette() directly. Instead we round-trip: convert each composed
    frame to RGB, quantize it to the ORIGINAL palette (pixel → nearest original
    index, exact match since every RGBA pixel came from that palette), then
    swap in the new palette table without touching index data.
    """
    print(f"[A] palette-remap → {out.name}")
    gif = Image.open(src)
    loop = gif.info.get("loop", 0)

    # Build original palette (for re-quantizing back to original indices)
    orig_palette_flat = gif.getpalette()
    new_palette_flat  = _build_remapped_palette(orig_palette_flat, bg_dark)

    # Template P-mode image used as quantization target (original palette)
    orig_p_template = Image.new("P", (1, 1))
    orig_p_template.putpalette(orig_palette_flat)

    frames: list[Image.Image] = []
    durations: list[int] = []
    for i, (frame, dur) in enumerate(_iter_frames(gif)):
        # Quantize composed RGB frame back to the original palette indices
        rgb   = frame.convert("RGB")
        p_out = rgb.quantize(palette=orig_p_template, dither=Image.Dither.NONE)
        # Swap in the remapped palette (indices unchanged)
        p_out.putpalette(new_palette_flat)
        # Clear any stale transparency metadata that confuses the GIF saver
        p_out.info.pop("transparency", None)
        frames.append(p_out)
        durations.append(dur)
        if i % 50 == 0:
            print(f"  frame {i}")

    _save_gif(frames, durations, out, loop)
    print(f"[A] done  {len(frames)} frames  {out.stat().st_size/1e6:.1f} MB")


# ---------------------------------------------------------------------------
# Variant B — Adaptive threshold + morphological erosion composite
# ---------------------------------------------------------------------------

def _process_frame_B(arr: np.ndarray, bg_dark: tuple) -> np.ndarray:
    """arr: uint8 H×W×3 RGB → uint8 H×W×3 dark-bg composited.

    Two-step approach: apply the same chrominance-split as variant C to get
    correct colours for fg elements (especially achromatic axes/text via
    L-inversion), then override confirmed background pixels with exact BG_DARK
    using a morphological erosion mask.  Result: C's colour accuracy + hard
    clean edges where the bg is unambiguous.
    """
    # Step 1: chrominance-split (identical to variant C)
    base = _process_frame_C(arr, bg_dark).astype(np.float32)

    # Step 2: binary bg mask via near-white threshold + MinFilter erosion
    near_white = np.all(arr >= 218, axis=2).astype(np.uint8) * 255
    eroded     = Image.fromarray(near_white, "L").filter(ImageFilter.MinFilter(3))
    bg_mask    = (np.array(eroded) > 128)[:, :, None]          # H×W×1 bool

    D      = np.array(bg_dark, dtype=np.float32)
    result = np.where(bg_mask, D[None, None, :], base)
    return result.clip(0, 255).astype(np.uint8)


def floodfill_gif(src: Path, out: Path, bg_dark: tuple = BG_DARK) -> None:
    """Variant B: chrominance-split + morphological binary bg override.
    Quantized to the palette-remap colour set for minimal file size."""
    print(f"[B] chroma-split + morph-override → {out.name}")
    gif  = Image.open(src)
    loop = gif.info.get("loop", 0)

    orig_palette_flat = gif.getpalette()
    new_palette_flat  = _build_remapped_palette(orig_palette_flat, bg_dark)
    new_p_template    = Image.new("P", (1, 1))
    new_p_template.putpalette(new_palette_flat)

    frames: list[Image.Image] = []
    durations: list[int] = []
    for i, (frame, dur) in enumerate(_iter_frames(gif)):
        arr       = np.array(frame.convert("RGB"))
        processed = _process_frame_B(arr, bg_dark)
        p_out = Image.fromarray(processed).quantize(
            palette=new_p_template, dither=Image.Dither.NONE
        )
        p_out.info.pop("transparency", None)
        frames.append(p_out)
        durations.append(dur)
        if i % 50 == 0:
            print(f"  frame {i}")

    _save_gif(frames, durations, out, loop)
    print(f"[B] done  {len(frames)} frames  {out.stat().st_size/1e6:.1f} MB")


# ---------------------------------------------------------------------------
# Variant C — Chrominance-split composite
# ---------------------------------------------------------------------------

def _process_frame_C(arr: np.ndarray, bg_dark: tuple) -> np.ndarray:
    """arr: uint8 H×W×3 RGB → uint8 H×W×3 dark-bg chrominance-split."""
    D     = np.array(bg_dark, dtype=np.float32)
    D_avg = float(np.mean(D))
    arr_f = arr.astype(np.float32)

    # --- Achromatic path: L-inversion curve (same formula as palette A) ---
    gray  = np.mean(arr_f, axis=2)           # H×W, 0..255
    l_frac = gray / 255.0                    # normalized [0,1]
    new_l  = (1.0 - l_frac) ** 0.70 * 0.85 + 0.05
    ach    = np.clip(new_l * 255, 0, 255)    # H×W
    ach_rgb = np.stack([ach, ach, ach], axis=2)   # H×W×3

    # --- Chromatic path: coverage blend + dark-dot boost ---
    min_ch   = np.min(arr_f, axis=2)
    coverage = np.clip((min_ch - 200.0) / 55.0, 0.0, 1.0)
    chroma   = np.clip(arr_f + coverage[:, :, None] * (D[None, None, :] - 255.0),
                       0.0, 255.0)
    # Boost very dark chromatic dots so they stay visible on dark bg
    max_ch    = np.max(chroma, axis=2)
    safe_max  = np.where(max_ch > 0, max_ch, 1.0)
    boost     = np.where(max_ch < 90, 90.0 / safe_max, 1.0)
    chroma    = np.clip(chroma * boost[:, :, None], 0.0, 255.0)

    # --- Per-pixel HLS saturation for blending weight ---
    r_n = arr_f[:, :, 0] / 255.0
    g_n = arr_f[:, :, 1] / 255.0
    b_n = arr_f[:, :, 2] / 255.0
    mx  = np.maximum(np.maximum(r_n, g_n), b_n)
    mn  = np.minimum(np.minimum(r_n, g_n), b_n)
    l_  = (mx + mn) / 2.0
    chroma_range = mx - mn
    s_  = np.where(
        mx == mn, 0.0,
        np.where(l_ < 0.5,
                 chroma_range / (mx + mn),
                 chroma_range / np.clip(2.0 - mx - mn, 1e-6, 2.0)),
    )

    # s < 0.04 → 100 % achromatic; s > 0.12 → 100 % chromatic; linear between
    s_weight = np.clip((s_ - 0.04) / 0.08, 0.0, 1.0)[:, :, None]
    result = (1.0 - s_weight) * ach_rgb + s_weight * chroma
    return result.clip(0, 255).astype(np.uint8)


def chroma_split_gif(src: Path, out: Path, bg_dark: tuple = BG_DARK) -> None:
    """Variant C: chrominance-split composite, quantized to the palette-remap
    colour set for consistent compression."""
    print(f"[C] chrominance-split → {out.name}")
    gif  = Image.open(src)
    loop = gif.info.get("loop", 0)

    orig_palette_flat = gif.getpalette()
    new_palette_flat  = _build_remapped_palette(orig_palette_flat, bg_dark)
    new_p_template    = Image.new("P", (1, 1))
    new_p_template.putpalette(new_palette_flat)

    frames: list[Image.Image] = []
    durations: list[int] = []
    for i, (frame, dur) in enumerate(_iter_frames(gif)):
        arr       = np.array(frame.convert("RGB"))
        processed = _process_frame_C(arr, bg_dark)
        p_out = Image.fromarray(processed).quantize(
            palette=new_p_template, dither=Image.Dither.NONE
        )
        p_out.info.pop("transparency", None)
        frames.append(p_out)
        durations.append(dur)
        if i % 50 == 0:
            print(f"  frame {i}")

    _save_gif(frames, durations, out, loop)
    print(f"[C] done  {len(frames)} frames  {out.stat().st_size/1e6:.1f} MB")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

VARIANTS = {
    "A": (BASE / "paper_fig06_swarm_orbit_animation_dark_vA.gif", remap_palette_gif),
    "B": (BASE / "paper_fig06_swarm_orbit_animation_dark_vB.gif", floodfill_gif),
    "C": (BASE / "paper_fig06_swarm_orbit_animation_dark_vC.gif", chroma_split_gif),
}

if __name__ == "__main__":
    run = [k.upper() for k in sys.argv[1:]] if sys.argv[1:] else list(VARIANTS)
    invalid = [k for k in run if k not in VARIANTS]
    if invalid:
        print(f"Unknown variants: {invalid}. Choose from A / B / C")
        sys.exit(1)

    for key in run:
        out_path, fn = VARIANTS[key]
        fn(SRC, out_path)

    print("\n--- summary ---")
    for key in run:
        out_path, _ = VARIANTS[key]
        if out_path.exists():
            print(f"  v{key}: {out_path.name}  {out_path.stat().st_size/1e6:.1f} MB")
