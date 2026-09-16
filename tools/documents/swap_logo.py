#!/usr/bin/env python3
"""Replace a logo embedded in a Word document, keeping the layout intact.

The addendum carried the old Protego logo as word/media/image1.png. A docx
sizes a picture by the drawing extent recorded in document.xml, not by the
file's pixel size, so dropping in an image of a different shape stretches it
into the old box. The replacement is therefore drawn onto a canvas of exactly
the original's pixel dimensions, scaled to fit and centred, which leaves both
the aspect ratio and the page layout alone.

    python3 tools/documents/swap_logo.py --logo tools/slides/media/image3.png \
        --member word/media/image1.png documents/tpp/addendum-*.docx
"""
import argparse, io, shutil, zipfile
from PIL import Image


def fit(logo_path, size, pad=0.04, bg=(255, 255, 255)):
    """The logo scaled to fit `size`, centred, on a background of `bg`."""
    w, h = size
    logo = Image.open(logo_path).convert("RGBA")
    inner = (int(w * (1 - 2 * pad)), int(h * (1 - 2 * pad)))
    scale = min(inner[0] / logo.width, inner[1] / logo.height)
    logo = logo.resize((max(1, int(logo.width * scale)), max(1, int(logo.height * scale))),
                       Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (w, h), bg)
    canvas.paste(logo, ((w - logo.width) // 2, (h - logo.height) // 2), logo)
    return canvas


def swap(doc, member, logo_path, dry_run=False):
    zin = zipfile.ZipFile(doc)
    if member not in zin.namelist():
        zin.close()
        return None
    original = Image.open(io.BytesIO(zin.read(member)))
    replacement = fit(logo_path, original.size)
    buf = io.BytesIO()
    replacement.save(buf, format="PNG", optimize=True)
    parts = {n: (buf.getvalue() if n == member else zin.read(n)) for n in zin.namelist()}
    zin.close()
    if not dry_run:
        shutil.copy2(doc, doc + ".bak")
        with zipfile.ZipFile(doc, "w", zipfile.ZIP_DEFLATED) as zout:
            for n, data in parts.items():
                zout.writestr(n, data)
    return original.size


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--logo", required=True)
    ap.add_argument("--member", default="word/media/image1.png")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    for f in a.files:
        size = swap(f, a.member, a.logo, a.dry_run)
        print(f"  {'would swap' if a.dry_run else 'swapped':>11}  {f}  ({a.member} @ {size[0]}x{size[1]})"
              if size else f"  {'no ' + a.member:>11}  {f}")
