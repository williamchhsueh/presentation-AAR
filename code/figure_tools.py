"""
figure_tools.py — PNG inspection & transform toolkit

Usage:
  python figure_tools.py inspect <file> [file ...]
  python figure_tools.py invert-bg <file> --out <out>
  python figure_tools.py set-bg <file> --color R,G,B [--threshold N] --out <out>
  python figure_tools.py make-transparent <file> [--bg R,G,B] [--tolerance N] --out <out>
  python figure_tools.py resize <file> [--width W] [--height H] [--scale S] --out <out>
  python figure_tools.py change-ratio <file> --ratio W:H [--mode crop|pad] [--pad-color R,G,B] --out <out>
  python figure_tools.py to-svg <file> [--method embed|vtracer|potrace] --out <out>
  python figure_tools.py batch "<glob>" <command> [options] [--out-suffix SUFFIX]
"""

from __future__ import annotations

import argparse
import base64
import glob
import io
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops


# ---------------------------------------------------------------------------
# Inspect
# ---------------------------------------------------------------------------

def inspect(path: str | Path) -> None:
    path = Path(path)
    img = Image.open(path)
    print(f"\n{'='*60}")
    print(f"File   : {path}")
    print(f"Format : {img.format}")
    print(f"Size   : {img.size[0]} × {img.size[1]} px")
    print(f"Mode   : {img.mode}")
    dpi = img.info.get("dpi")
    print(f"DPI    : {dpi if dpi else 'not set'}")
    icc = img.info.get("icc_profile")
    print(f"ICC    : {'present (' + str(len(icc)) + ' bytes)' if icc else 'none'}")
    other = {k: v for k, v in img.info.items() if k not in ("dpi", "icc_profile")}
    if other:
        print(f"Info   : {other}")
    print(f"File sz: {path.stat().st_size / 1024:.1f} KB")


# ---------------------------------------------------------------------------
# Background helpers
# ---------------------------------------------------------------------------

def _to_rgba(img: Image.Image) -> Image.Image:
    return img.convert("RGBA") if img.mode != "RGBA" else img


def invert_bg(src: str | Path, out: str | Path) -> None:
    """Invert all RGB channels; preserve alpha if present."""
    img = Image.open(src).convert("RGBA")
    r, g, b, a = img.split()
    rgb = Image.merge("RGB", (r, g, b))
    rgb_inv = ImageChops.invert(rgb)
    r2, g2, b2 = rgb_inv.split()
    result = Image.merge("RGBA", (r2, g2, b2, a))
    result.save(out)
    print(f"Saved inverted → {out}")


def set_bg(
    src: str | Path,
    out: str | Path,
    color: tuple[int, int, int] = (0, 0, 0),
    threshold: int = 30,
    target_bg: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """Replace pixels near `target_bg` with `color`."""
    img = _to_rgba(Image.open(src))
    data = img.load()
    width, height = img.size
    tr, tg, tb = target_bg
    nr, ng, nb = color
    for y in range(height):
        for x in range(width):
            r, g, b, a = data[x, y]
            if abs(r - tr) <= threshold and abs(g - tg) <= threshold and abs(b - tb) <= threshold:
                data[x, y] = (nr, ng, nb, a)
    img.save(out)
    print(f"Saved with replaced bg → {out}")


def make_transparent(
    src: str | Path,
    out: str | Path,
    bg_color: tuple[int, int, int] = (255, 255, 255),
    tolerance: int = 30,
) -> None:
    """Make pixels near `bg_color` fully transparent."""
    img = _to_rgba(Image.open(src))
    data = img.load()
    width, height = img.size
    tr, tg, tb = bg_color
    for y in range(height):
        for x in range(width):
            r, g, b, a = data[x, y]
            if abs(r - tr) <= tolerance and abs(g - tg) <= tolerance and abs(b - tb) <= tolerance:
                data[x, y] = (r, g, b, 0)
    if not str(out).lower().endswith(".png"):
        out = str(out) + ".png"
    img.save(out)
    print(f"Saved with transparent bg → {out}")


# ---------------------------------------------------------------------------
# Animated GIF dark background
# ---------------------------------------------------------------------------

def darken_gif(
    src: str | Path,
    out: str | Path,
    bg_color: tuple[int, int, int] = (8, 16, 16),
    min_fg_brightness: int = 50,
    target_bg: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """Convert animated GIF to dark-background version with smooth alpha matting.

    Uses per-pixel coverage estimation (soft matte) to smoothly recomposite
    foreground over the new dark background, fixing anti-aliasing halos.
    Near-black foreground pixels are boosted to remain visible against dark bg.
    """
    gif = Image.open(src)
    loop = gif.info.get("loop", 0)
    frames: list[Image.Image] = []
    durations: list[int] = []

    D = np.array(bg_color, dtype=np.float32)
    W = np.array(target_bg, dtype=np.float32)
    diff = D - W  # channel-wise shift when coverage=1

    try:
        while True:
            frame_rgba = gif.convert("RGBA")
            data = np.array(frame_rgba, dtype=np.float32)  # H×W×4

            P = data[:, :, :3]

            # coverage ∈ [0,1]: fraction of white background in each pixel
            # min(R/W_r, G/W_g, B/W_b) → 1 for pure white, 0 for fully dark foreground
            coverage = np.clip(np.min(P / np.maximum(W, 1.0), axis=2), 0.0, 1.0)

            # Recomposite: P_new = P + (D - W) * coverage
            new_rgb = np.clip(P + coverage[:, :, np.newaxis] * diff, 0.0, 255.0)

            # Boost near-black foreground pixels so they stay visible on the dark bg
            if min_fg_brightness > 0:
                max_ch = np.max(new_rgb, axis=2)
                fg_mask = (coverage < 0.95) & (max_ch < min_fg_brightness)
                safe_max = np.where(max_ch > 0, max_ch, 1.0)
                boost = np.where(fg_mask, min_fg_brightness / safe_max, 1.0)
                new_rgb = np.clip(new_rgb * boost[:, :, np.newaxis], 0.0, 255.0)

            result = np.concatenate([new_rgb, data[:, :, 3:4]], axis=2).astype(np.uint8)
            frame_out = Image.fromarray(result, "RGBA").quantize(colors=256)
            frames.append(frame_out)
            durations.append(gif.info.get("duration", 50))

            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        loop=loop,
        duration=durations,
        optimize=False,
    )
    print(f"Saved dark GIF ({len(frames)} frames) → {out}")


def darken_gif_v2(
    src: str | Path,
    out: str | Path,
    bg_color: tuple[int, int, int] = (8, 16, 16),
    bg_threshold: int = 200,
    min_fg_brightness: int = 80,
    target_bg: tuple[int, int, int] = (255, 255, 255),
) -> None:
    """Convert animated GIF to dark background, preserving light-colored foreground.

    Fixes the issue where light-colored text/labels become nearly invisible:
    Only pixels with min_channel >= bg_threshold are treated as (partial) background.
    Pixels below that threshold are pure foreground and keep their original color.

    Args:
        bg_threshold: minimum channel value to start treating pixel as background.
                      Pixels with min_channel < bg_threshold → coverage=0 (pure fg).
                      Default 200 preserves light-colored text (e.g. salmon, light gray).
        min_fg_brightness: floor brightness for foreground pixels on the dark bg.
    """
    gif = Image.open(src)
    loop = gif.info.get("loop", 0)
    frames: list[Image.Image] = []
    durations: list[int] = []

    D = np.array(bg_color, dtype=np.float32)
    W = np.array(target_bg, dtype=np.float32)
    diff = D - W

    bg_range = 255.0 - bg_threshold  # denominator for coverage formula

    try:
        while True:
            frame_rgba = gif.convert("RGBA")
            data = np.array(frame_rgba, dtype=np.float32)

            P = data[:, :, :3]

            # Only pixels with min_channel >= bg_threshold get darkened.
            # coverage = (min_channel - bg_threshold) / (255 - bg_threshold), clipped [0, 1].
            # Pixels with min_channel < bg_threshold → coverage=0 → unchanged.
            min_ch = np.min(P, axis=2)
            coverage = np.clip((min_ch - bg_threshold) / bg_range, 0.0, 1.0)

            new_rgb = np.clip(P + coverage[:, :, np.newaxis] * diff, 0.0, 255.0)

            # Boost near-black foreground pixels so they stay visible
            if min_fg_brightness > 0:
                max_ch = np.max(new_rgb, axis=2)
                fg_mask = (coverage < 0.95) & (max_ch < min_fg_brightness)
                safe_max = np.where(max_ch > 0, max_ch, 1.0)
                boost = np.where(fg_mask, min_fg_brightness / safe_max, 1.0)
                new_rgb = np.clip(new_rgb * boost[:, :, np.newaxis], 0.0, 255.0)

            result = np.concatenate([new_rgb, data[:, :, 3:4]], axis=2).astype(np.uint8)
            frame_out = Image.fromarray(result, "RGBA").quantize(colors=256)
            frames.append(frame_out)
            durations.append(gif.info.get("duration", 50))

            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        loop=loop,
        duration=durations,
        optimize=False,
    )
    print(f"Saved dark GIF v2 ({len(frames)} frames) → {out}")


# ---------------------------------------------------------------------------
# Resize / ratio
# ---------------------------------------------------------------------------

def resize(
    src: str | Path,
    out: str | Path,
    width: int | None = None,
    height: int | None = None,
    scale: float | None = None,
) -> None:
    img = Image.open(src)
    w0, h0 = img.size
    if scale is not None:
        new_w, new_h = int(w0 * scale), int(h0 * scale)
    elif width and height:
        new_w, new_h = width, height
    elif width:
        new_w = width
        new_h = int(h0 * width / w0)
    elif height:
        new_h = height
        new_w = int(w0 * height / h0)
    else:
        raise ValueError("Provide --width, --height, or --scale")
    result = img.resize((new_w, new_h), Image.LANCZOS)
    result.save(out)
    print(f"Saved resized ({w0}×{h0} → {new_w}×{new_h}) → {out}")


def change_ratio(
    src: str | Path,
    out: str | Path,
    ratio: float = 16 / 9,
    mode: str = "pad",
    pad_color: tuple[int, int, int] = (0, 0, 0),
) -> None:
    """Crop or pad image to target aspect ratio."""
    img = Image.open(src)
    w, h = img.size
    current_ratio = w / h

    if mode == "crop":
        if current_ratio > ratio:
            new_w = int(h * ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        img.save(out)
    else:  # pad
        if current_ratio > ratio:
            new_h = int(w / ratio)
            canvas = Image.new("RGB", (w, new_h), pad_color)
            canvas.paste(img, (0, (new_h - h) // 2))
        else:
            new_w = int(h * ratio)
            canvas = Image.new("RGB", (new_w, h), pad_color)
            canvas.paste(img, ((new_w - w) // 2, 0))
        canvas.save(out)
    print(f"Saved ratio-adjusted → {out}")


# ---------------------------------------------------------------------------
# SVG conversion
# ---------------------------------------------------------------------------

def to_svg_embed(src: str | Path, out: str | Path) -> None:
    """Wrap PNG as base64-embedded SVG. Lossless; always works."""
    src = Path(src)
    raw = src.read_bytes()
    b64 = base64.b64encode(raw).decode()
    img = Image.open(src)
    w, h = img.size
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f'  <image width="{w}" height="{h}" '
        f'href="data:image/png;base64,{b64}"/>\n'
        f'</svg>\n'
    )
    Path(out).write_text(svg)
    print(f"Saved SVG embed → {out}")


def to_svg_vtracer(src: str | Path, out: str | Path) -> None:
    """Auto-trace to SVG using vtracer (color-aware)."""
    try:
        import vtracer  # noqa: PLC0415
    except ImportError:
        sys.exit("vtracer not installed — run: poetry add vtracer")
    vtracer.convert_image_to_svg_py(
        str(src),
        str(out),
        colormode="color",
        hierarchical="stacked",
        mode="spline",
        filter_speckle=4,
        color_precision=6,
        layer_difference=16,
        corner_threshold=60,
        length_threshold=4.0,
        max_iterations=10,
        splice_threshold=45,
        path_precision=3,
    )
    print(f"Saved vtracer SVG → {out}")


def to_svg_potrace(src: str | Path, out: str | Path) -> None:
    """Auto-trace B&W bitmap to SVG via potrace CLI."""
    img = Image.open(src).convert("L")
    with tempfile.NamedTemporaryFile(suffix=".bmp", delete=False) as tmp:
        bmp_path = tmp.name
    img.save(bmp_path)
    result = subprocess.run(
        ["potrace", "--svg", bmp_path, "-o", str(out)],
        capture_output=True, text=True
    )
    Path(bmp_path).unlink(missing_ok=True)
    if result.returncode != 0:
        sys.exit(f"potrace failed: {result.stderr}")
    print(f"Saved potrace SVG → {out}")


def to_svg(src: str | Path, out: str | Path, method: str = "embed") -> None:
    if method == "embed":
        to_svg_embed(src, out)
    elif method == "vtracer":
        to_svg_vtracer(src, out)
    elif method == "potrace":
        to_svg_potrace(src, out)
    else:
        sys.exit(f"Unknown method: {method}. Choose embed | vtracer | potrace")


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------

def _derive_out(src: Path, suffix: str) -> Path:
    return src.with_stem(src.stem + suffix)


def batch(pattern: str, command: str, out_suffix: str = "_out", **kwargs) -> None:
    files = sorted(glob.glob(pattern))
    if not files:
        sys.exit(f"No files matched: {pattern}")
    for f in files:
        src = Path(f)
        out = _derive_out(src, out_suffix)
        kwargs["out"] = out
        dispatch(command, str(src), **kwargs)


# ---------------------------------------------------------------------------
# Dispatch + CLI
# ---------------------------------------------------------------------------

def dispatch(command: str, src: str, **kwargs) -> None:
    cmd = command.replace("-", "_")
    fn_map = {
        "invert_bg": invert_bg,
        "set_bg": set_bg,
        "make_transparent": make_transparent,
        "darken_gif": darken_gif,
        "darken_gif_v2": darken_gif_v2,
        "resize": resize,
        "change_ratio": change_ratio,
        "to_svg": to_svg,
    }
    fn = fn_map.get(cmd)
    if fn is None:
        sys.exit(f"Unknown command: {command}")
    # filter kwargs to only those the function accepts
    import inspect as _inspect  # noqa: PLC0415
    sig = _inspect.signature(fn)
    valid = {k: v for k, v in kwargs.items() if k in sig.parameters}
    fn(src, **valid)


def _parse_color(s: str) -> tuple[int, int, int]:
    parts = [int(x) for x in s.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("Color must be R,G,B (e.g. 0,0,0)")
    return tuple(parts)  # type: ignore[return-value]


def _parse_ratio(s: str) -> float:
    if ":" in s:
        w, h = s.split(":")
        return float(w) / float(h)
    return float(s)


def main() -> None:
    parser = argparse.ArgumentParser(description="PNG inspection & transform toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    # inspect
    p = sub.add_parser("inspect", help="Print PNG attributes")
    p.add_argument("files", nargs="+")

    # invert-bg
    p = sub.add_parser("invert-bg", help="Invert all RGB channels")
    p.add_argument("file")
    p.add_argument("--out", required=True)

    # set-bg
    p = sub.add_parser("set-bg", help="Replace near-white (or custom) bg with a color")
    p.add_argument("file")
    p.add_argument("--color", type=_parse_color, default=(0, 0, 0), metavar="R,G,B")
    p.add_argument("--target-bg", type=_parse_color, default=(255, 255, 255), metavar="R,G,B")
    p.add_argument("--threshold", type=int, default=30)
    p.add_argument("--out", required=True)

    # make-transparent
    p = sub.add_parser("make-transparent", help="Make background pixels transparent")
    p.add_argument("file")
    p.add_argument("--bg", type=_parse_color, default=(255, 255, 255), metavar="R,G,B")
    p.add_argument("--tolerance", type=int, default=30)
    p.add_argument("--out", required=True)

    # resize
    p = sub.add_parser("resize", help="Resize image")
    p.add_argument("file")
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--scale", type=float)
    p.add_argument("--out", required=True)

    # change-ratio
    p = sub.add_parser("change-ratio", help="Crop or pad to target aspect ratio")
    p.add_argument("file")
    p.add_argument("--ratio", type=_parse_ratio, default="16:9", metavar="W:H")
    p.add_argument("--mode", choices=["crop", "pad"], default="pad")
    p.add_argument("--pad-color", type=_parse_color, default=(0, 0, 0), metavar="R,G,B")
    p.add_argument("--out", required=True)

    # darken-gif
    p = sub.add_parser("darken-gif", help="Replace near-white bg with dark color in animated GIF")
    p.add_argument("file")
    p.add_argument("--bg", type=_parse_color, default=(8, 16, 16), metavar="R,G,B",
                   help="Dark background color (default: 8,16,16 = vis_style bg-base)")
    p.add_argument("--target-bg", type=_parse_color, default=(255, 255, 255), metavar="R,G,B")
    p.add_argument("--min-fg", type=int, default=50, dest="min_fg_brightness",
                   help="Minimum brightness for foreground pixels to ensure contrast (default: 50)")
    p.add_argument("--out", required=True)

    # darken-gif-v2
    p = sub.add_parser("darken-gif-v2",
                       help="Dark-bg GIF conversion that preserves light-colored foreground")
    p.add_argument("file")
    p.add_argument("--bg", type=_parse_color, default=(8, 16, 16), metavar="R,G,B")
    p.add_argument("--bg-threshold", type=int, default=200, dest="bg_threshold",
                   help="min_channel floor for background coverage (default: 200)")
    p.add_argument("--min-fg", type=int, default=80, dest="min_fg_brightness",
                   help="Minimum brightness for dark foreground pixels (default: 80)")
    p.add_argument("--out", required=True)

    # to-svg
    p = sub.add_parser("to-svg", help="Convert PNG to SVG")
    p.add_argument("file")
    p.add_argument("--method", choices=["embed", "vtracer", "potrace"], default="embed")
    p.add_argument("--out", required=True)

    # batch
    p = sub.add_parser("batch", help="Apply a command to many files")
    p.add_argument("pattern", help='Glob pattern, e.g. "figure/*.png"')
    p.add_argument("cmd", help="Command to run (e.g. invert-bg)")
    p.add_argument("--out-suffix", default="_out")
    p.add_argument("--color", type=_parse_color, metavar="R,G,B")
    p.add_argument("--threshold", type=int)
    p.add_argument("--method", choices=["embed", "vtracer", "potrace"])
    p.add_argument("--ratio", type=_parse_ratio, metavar="W:H")
    p.add_argument("--mode", choices=["crop", "pad"])
    p.add_argument("--pad-color", type=_parse_color, metavar="R,G,B")
    p.add_argument("--scale", type=float)

    args = parser.parse_args()

    if args.command == "inspect":
        for f in args.file if hasattr(args, "file") else args.files:
            inspect(f)
    elif args.command == "invert-bg":
        invert_bg(args.file, args.out)
    elif args.command == "set-bg":
        set_bg(args.file, args.out, color=args.color, threshold=args.threshold, target_bg=args.target_bg)
    elif args.command == "make-transparent":
        make_transparent(args.file, args.out, bg_color=args.bg, tolerance=args.tolerance)
    elif args.command == "darken-gif":
        darken_gif(args.file, args.out, bg_color=args.bg,
                   min_fg_brightness=args.min_fg_brightness, target_bg=args.target_bg)
    elif args.command == "darken-gif-v2":
        darken_gif_v2(args.file, args.out, bg_color=args.bg,
                      bg_threshold=args.bg_threshold,
                      min_fg_brightness=args.min_fg_brightness)
    elif args.command == "resize":
        resize(args.file, args.out, width=args.width, height=args.height, scale=args.scale)
    elif args.command == "change-ratio":
        change_ratio(args.file, args.out, ratio=args.ratio, mode=args.mode, pad_color=args.pad_color)
    elif args.command == "to-svg":
        to_svg(args.file, args.out, method=args.method)
    elif args.command == "batch":
        kw = {}
        for attr in ("color", "threshold", "method", "ratio", "mode", "pad_color", "scale"):
            v = getattr(args, attr, None)
            if v is not None:
                kw[attr] = v
        batch(args.pattern, args.cmd, out_suffix=args.out_suffix, **kw)


if __name__ == "__main__":
    # Special-case: `inspect` can take multiple positional args not caught above
    # Re-parse if needed
    if len(sys.argv) >= 2 and sys.argv[1] == "inspect":
        for f in sys.argv[2:]:
            inspect(f)
    else:
        main()
