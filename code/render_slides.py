"""Convert PPTX to per-slide PNG via LibreOffice + pdf2image."""

import subprocess
import sys
import tempfile
from pathlib import Path

from pdf2image import convert_from_path


def pptx_to_pngs(pptx_path: Path, out_dir: Path, dpi: int = 150) -> list[Path]:
    pptx_path = Path(pptx_path).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        result = subprocess.run(
            [
                "soffice",
                "--headless",
                "--convert-to", "pdf",
                "--outdir", str(tmp_path),
                str(pptx_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            raise RuntimeError("LibreOffice conversion failed")

        pdf_path = tmp_path / (pptx_path.stem + ".pdf")
        if not pdf_path.exists():
            raise FileNotFoundError(f"Expected PDF not found: {pdf_path}")

        images = convert_from_path(pdf_path, dpi=dpi)

    out_paths = []
    for i, img in enumerate(images, start=1):
        out_path = out_dir / f"slide_{i:02d}.png"
        img.save(out_path, "PNG")
        out_paths.append(out_path)
        print(f"  saved {out_path.name}")

    return out_paths


if __name__ == "__main__":
    repo = Path(__file__).parent.parent
    pptx = repo / "ppt" / "AAR_Paper_Sharing.pptx"
    out = repo / "ppt" / "slides_png"

    print(f"Converting: {pptx.name}")
    slides = pptx_to_pngs(pptx, out)
    print(f"\nDone — {len(slides)} slides → {out}")
