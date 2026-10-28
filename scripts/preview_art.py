"""python preview_art.py <art-name> <out.png> [scale]  -> draws one registered icon/diagram large on a pale card
so you can inspect it before using it in a sheet. Also: preview_art.py --all <out.png> for a gallery."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reportlab.pdfgen import canvas
from drawkit import *
register_fonts()
import icons

def card(c, name, x, y, w, h, scale):
    bw, bh = icons.box_of(name)
    c.setFillColor(PALE); c.setStrokeColor(LINE); c.roundRect(x, y, w, h, 8, fill=1, stroke=1)
    s = min((w - 16) / bw, (h - 26) / bh) * 1.0
    c.saveState(); c.translate(x + (w - bw * s) / 2, y + 8); c.scale(s, s); icons.get(name)(c); c.restoreState()
    c.setFillColor(GREY); c.setFont("Body", 7); c.drawString(x + 6, y + h - 12, f"{name}  ({bw}x{bh})")

def main():
    a = sys.argv[1:]
    if not a: raise SystemExit(__doc__)
    names = sorted(set(icons.REGISTRY)) if a[0] == "--all" else [a[0]]
    out = a[1]
    pdf = out.rsplit(".", 1)[0] + ".pdf"
    if a[0] == "--all":
        seen, uniq = set(), []
        for n in names:
            f = icons.REGISTRY[n]
            if f not in seen: seen.add(f); uniq.append(n)
        cols = 4; cw_, ch_ = 190, 130; rows = (len(uniq) + cols - 1) // cols
        c = canvas.Canvas(pdf, pagesize=(cols * (cw_ + 10) + 10, rows * (ch_ + 10) + 10))
        for k, n in enumerate(uniq):
            card(c, n, 10 + (k % cols) * (cw_ + 10), c._pagesize[1] - 10 - ch_ - (k // cols) * (ch_ + 10), cw_, ch_, 1)
    else:
        scale = float(a[2]) if len(a) > 2 else 4.0
        bw, bh = icons.box_of(a[0])
        c = canvas.Canvas(pdf, pagesize=(bw * scale * 0.6 + 40, bh * scale * 0.6 + 50))
        card(c, a[0], 10, 10, c._pagesize[0] - 20, c._pagesize[1] - 20, scale)
    c.save()
    try:
        import fitz
        fitz.open(pdf)[0].get_pixmap(dpi=150).save(out); os.remove(pdf); print("wrote", out)
    except ImportError:
        print("wrote", pdf, "(install PyMuPDF to get a PNG)")
main()
