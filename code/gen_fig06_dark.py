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


def _read_all_frame_palettes(src: Path) -> list[list[int]]:
    """Parse the GIF binary and return each frame's effective 768-int palette.

    259/260 frames have per-frame local color tables (LCTs). Pillow's getpalette()
    returns None for RGBA-composited frames, so we read LCTs directly from the file.
    Frames without an LCT fall back to the global color table.
    """
    with open(src, "rb") as f:
        data = f.read()

    # Logical Screen Descriptor (bytes 6–12)
    packed    = data[10]
    has_gct   = (packed >> 7) & 1
    gct_bits  = packed & 0x7
    gct_len   = 3 * (2 ** (gct_bits + 1)) if has_gct else 0

    global_pal = [0] * 768
    if has_gct:
        raw = list(data[13 : 13 + gct_len])
        global_pal[: len(raw)] = raw

    palettes: list[list[int]] = []
    pos = 13 + gct_len

    while pos < len(data) - 1:
        b = data[pos]
        if b == 0x3B:  # GIF Trailer
            break
        elif b == 0x21:  # Extension block
            pos += 2  # introducer + label
            while True:
                sub_len = data[pos]; pos += 1 + sub_len
                if sub_len == 0:
                    break
        elif b == 0x2C:  # Image Descriptor
            packed_img = data[pos + 9]
            has_lct    = (packed_img >> 7) & 1
            lct_bits   = packed_img & 0x7
            pos += 10  # Image Descriptor is 10 bytes (including the 0x2C)
            if has_lct:
                lct_len = 3 * (2 ** (lct_bits + 1))
                raw = list(data[pos : pos + lct_len])
                frame_pal = [0] * 768
                frame_pal[: len(raw)] = raw
                pos += lct_len
            else:
                frame_pal = list(global_pal)
            palettes.append(frame_pal)
            # Skip compressed pixel data (LZW min-code-size byte + sub-blocks)
            pos += 1
            while True:
                sub_len = data[pos]; pos += 1 + sub_len
                if sub_len == 0:
                    break
        else:
            pos += 1

    return palettes


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


def _process_frame_A_pixel(arr: np.ndarray, bg_dark: tuple) -> np.ndarray:
    """Apply vA classification pixel-by-pixel using vectorized HLS.

    This avoids the palette-mismatch artifact (white pixels near text) that occurs
    when using a single palette template for all 260 frames, each of which has its
    own local color table.  Logic mirrors _remap_palette_entry exactly.
    """
    arr_f = arr.astype(np.float32) / 255.0
    r_n = arr_f[:, :, 0]; g_n = arr_f[:, :, 1]; b_n = arr_f[:, :, 2]

    # --- RGB → HLS ---
    mx = np.maximum(np.maximum(r_n, g_n), b_n)
    mn = np.minimum(np.minimum(r_n, g_n), b_n)
    l_ = (mx + mn) / 2.0
    chroma = mx - mn
    has_c  = chroma > 1e-6

    # Saturation
    denom = np.where(l_ < 0.5, mx + mn, 2.0 - mx - mn)
    s_ = np.where(has_c, chroma / np.clip(denom, 1e-6, 2.0), 0.0)

    # Hue  (0..1)
    safe_c = np.where(has_c, chroma, 1.0)
    r_is_max = has_c & (mx == r_n)
    g_is_max = has_c & (mx == g_n) & ~r_is_max
    b_is_max = has_c & ~r_is_max & ~g_is_max
    h_r = ((g_n - b_n) / safe_c) % 6.0 / 6.0
    h_g = ((b_n - r_n) / safe_c + 2.0) / 6.0
    h_b = ((r_n - g_n) / safe_c + 4.0) / 6.0
    h_  = np.where(r_is_max, h_r, np.where(g_is_max, h_g, np.where(b_is_max, h_b, 0.0)))

    # --- Compute new L per vA rules ---
    is_ach = s_ < 0.08
    is_bg  = (l_ >= 0.95) & is_ach

    new_l = np.copy(l_)

    # Achromatic (non-bg): gamma-curved L-inversion
    ach_mask = is_ach & ~is_bg
    new_l = np.where(ach_mask, np.clip((1.0 - l_) ** 0.70 * 0.85 + 0.05, 0.0, 1.0), new_l)

    # Light chromatic, low-S (anti-alias tints): crush toward zero
    lc_ls = (~is_ach) & (l_ >= 0.80) & (s_ < 0.25)
    new_l = np.where(lc_ls, np.maximum(0.10, l_ - 0.82), new_l)

    # Light chromatic, high-S (bubble fills): moderate reduction
    lc_hs = (~is_ach) & (l_ >= 0.80) & (s_ >= 0.25)
    new_l = np.where(lc_hs, np.maximum(0.50, l_ - 0.35), new_l)

    # Foreground chromatic: clamp L
    fg_c = (~is_ach) & (l_ < 0.80)
    new_l = np.where(fg_c, np.clip(l_, 0.40, 0.85), new_l)

    # --- HLS → RGB (vectorized standard formula) ---
    m2 = np.where(new_l <= 0.5, new_l * (1.0 + s_), new_l + s_ - new_l * s_)
    m1 = 2.0 * new_l - m2

    def _hue_interp(m1: np.ndarray, m2: np.ndarray, hue: np.ndarray) -> np.ndarray:
        hue = hue % 1.0
        return np.where(hue < 1/6, m1 + (m2 - m1) * hue * 6.0,
               np.where(hue < 0.5, m2,
               np.where(hue < 2/3, m1 + (m2 - m1) * (2/3 - hue) * 6.0,
                        m1)))

    out_r = _hue_interp(m1, m2, h_ + 1/3)
    out_g = _hue_interp(m1, m2, h_)
    out_b = _hue_interp(m1, m2, h_ - 1/3)
    out = np.stack([out_r, out_g, out_b], axis=2)

    # Override background pixels with exact BG_DARK
    D = np.array(bg_dark, dtype=np.float32) / 255.0
    out[is_bg] = D

    return np.clip(out * 255, 0, 255).astype(np.uint8)


def remap_palette_gif(src: Path, out: Path, bg_dark: tuple = BG_DARK) -> None:
    """Pixel-level vA classification → quantize to remapped frame-0 palette.

    Root cause of white-pixel artifacts in the original palette-remap approach:
    259/260 frames have per-frame local color tables (LCTs). Composited RGBA frames
    include colors from multiple LCTs. Quantizing all frames against frame 0's LCT
    caused anti-alias colors unique to other frames to snap to wrong entries, which
    the remap then made near-white.

    Fix: apply vA's HLS classification pixel-by-pixel (vectorized), then quantize
    to a single remapped palette derived from frame 0's LCT. No per-frame palette
    dependency → no mismatch artifacts. File size stays close to original vA.
    """
    print(f"[A] pixel-level vA → {out.name}")
    gif = Image.open(src)
    loop = gif.info.get("loop", 0)

    # Build fixed output palette from frame 0's LCT (remapped to dark-bg colors)
    orig_pal_flat = gif.getpalette()
    new_pal_flat  = _build_remapped_palette(orig_pal_flat, bg_dark)
    new_p_template = Image.new("P", (1, 1))
    new_p_template.putpalette(new_pal_flat)

    frames: list[Image.Image] = []
    durations: list[int] = []
    for i, (frame, dur) in enumerate(_iter_frames(gif)):
        arr      = np.array(frame.convert("RGB"))
        processed = _process_frame_A_pixel(arr, bg_dark)
        p_out = Image.fromarray(processed).quantize(
            palette=new_p_template, dither=Image.Dither.NONE
        )
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
