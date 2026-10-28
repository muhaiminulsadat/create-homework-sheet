"""Shared design tokens, fonts and drawing helpers for the homework-sheet skill.

Everything visual (palette, fonts, arrows, labels, small decorative symbols) lives here so
the icon library and the page engine stay in sync. Do not change values casually: they
define the look every sheet shares.
"""
import math, os, re
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------------ palette
NAVY = HexColor("#142D4E")      # headings, primary text
TEAL = HexColor("#168D94")      # formula panel, vector fills
ORANGE = HexColor("#F3A34B")    # small highlights, force arrows
PALE = HexColor("#F3F6FA")      # card background
GREY = HexColor("#8A94A3")      # secondary text
LINE = HexColor("#D5DBE4")      # thin borders
TEAL_L = HexColor("#D6EEF0")
ORANGE_L = HexColor("#FCE7C8")
GREEN = HexColor("#2E9E5B")     # EASY
RED = HexColor("#C0504D")       # HARD (muted)
GRASS = HexColor("#4FAE72")
SOFT = HexColor("#D6E0EE")      # light text on navy
HILITE = HexColor("#8FD0D4")    # light teal line-art on navy

# ------------------------------------------------------------------ fonts
_FONT_CANDIDATES = {
    # role: [ (regular_path_candidates...) ]
    "Body":  ["segoeui.ttf", "SegoeUI.ttf", "arial.ttf", "Arial.ttf", "DejaVuSans.ttf"],
    "BodyB": ["segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"],
    "BodyI": ["segoeuii.ttf", "ariali.ttf", "Arial Italic.ttf", "DejaVuSans-Oblique.ttf"],
    "Head":  ["seguibl.ttf", "segoeuib.ttf", "arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"],
}
_FONT_DIRS = [
    "C:/Windows/Fonts", os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts"),
    "/Library/Fonts", "/System/Library/Fonts/Supplemental", os.path.expanduser("~/Library/Fonts"),
    "/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/truetype/msttcorefonts",
]
FONT_USED = {}

def register_fonts():
    if FONT_USED:
        return
    for role, names in _FONT_CANDIDATES.items():
        for d in _FONT_DIRS:
            hit = next((os.path.join(d, n) for n in names if os.path.exists(os.path.join(d, n))), None)
            if hit:
                pdfmetrics.registerFont(TTFont(role, hit)); FONT_USED[role] = hit; break
        else:
            raise SystemExit(f"No usable font found for {role}. Install Segoe UI (Windows) or DejaVu Sans.")

def font_has(char, role="Body"):
    try:
        return ord(char) in pdfmetrics.getFont(role).face.charToGlyph
    except Exception:
        return True

# ------------------------------------------------------------------ small helpers
def stroke_style(c, lw=1.2):
    c.setStrokeColor(NAVY); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)

def arrow(c, x1, y1, x2, y2, col, lw=1.6, head=4.5):
    c.saveState(); c.setStrokeColor(col); c.setFillColor(col); c.setLineWidth(lw); c.setLineCap(1)
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * 0.8 * math.cos(ang), y2 - head * 0.8 * math.sin(ang)
    c.line(x1, y1, bx, by)
    p = c.beginPath(); p.moveTo(x2, y2)
    p.lineTo(x2 - head * math.cos(ang) + head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) - head * 0.55 * math.cos(ang))
    p.lineTo(x2 - head * math.cos(ang) - head * 0.55 * math.sin(ang), y2 - head * math.sin(ang) + head * 0.55 * math.cos(ang))
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

def lab(c, x, y, s, col=NAVY, size=6.6, al="c"):
    """Small bold caption inside an icon (al = c|l|r)."""
    c.setFillColor(col); c.setFont("BodyB", size)
    {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[al](x, y, s)

def floor(c, x1=4, x2=96, y=12, hatch=True):
    stroke_style(c, 1.3); c.line(x1, y, x2, y)
    if hatch:
        c.setLineWidth(0.7); c.setStrokeColor(HexColor("#7B8AA0"))
        for hx in range(int(x1) + 4, int(x2) - 2, 6): c.line(hx, y, hx - 3, y - 4)

def car2(c, scale=1.0, body=TEAL):
    """Side-view car, origin at bottom centre of the wheels' contact line."""
    c.saveState(); c.scale(scale, scale)
    stroke_style(c, 1.1)
    c.setFillColor(body); c.roundRect(-16, 3.5, 32, 8.5, 3, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(-9, 12); p.lineTo(-5.5, 18); p.lineTo(7, 18); p.lineTo(11, 12); p.close()
    c.setFillColor(body); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(white); c.setLineWidth(0.7)
    p = c.beginPath(); p.moveTo(-7, 12.4); p.lineTo(-4.6, 16.8); p.lineTo(-0.5, 16.8); p.lineTo(-0.5, 12.4); p.close(); c.drawPath(p, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(1, 12.4); p.lineTo(1, 16.8); p.lineTo(6.4, 16.8); p.lineTo(9, 12.4); p.close(); c.drawPath(p, fill=1, stroke=0)
    stroke_style(c, 1.1)
    for wx in (-9, 9):
        c.setFillColor(NAVY); c.circle(wx, 3.5, 3.4, fill=1, stroke=1); c.setFillColor(white); c.circle(wx, 3.5, 1.1, fill=1, stroke=0)
    c.setFillColor(ORANGE); c.circle(14.2, 8.5, 1.3, fill=1, stroke=0)
    c.restoreState()

def pent(c, cx, cy, rr, rot=90):
    p = c.beginPath()
    for i in range(5):
        a = math.radians(rot + 72 * i); px, py = cx + rr * math.cos(a), cy + rr * math.sin(a)
        (p.moveTo if i == 0 else p.lineTo)(px, py)
    p.close(); c.drawPath(p, fill=1, stroke=0)

# ------------------------------------------------------------------ decorative symbols (headers/footers)
def atom_symbol(c, x, y, s=1.0, col=white, lw=1.0):
    c.saveState(); c.translate(x, y); c.scale(s, s); c.setStrokeColor(col); c.setLineWidth(lw)
    for a in (0, 60, 120):
        c.saveState(); c.rotate(a); c.ellipse(-8, -3.2, 8, 3.2, fill=0, stroke=1); c.restoreState()
    c.setFillColor(col); c.circle(0, 0, 1.6, fill=1, stroke=0); c.restoreState()

def gear_symbol(c, x, y, s=1.0, col=white):
    c.saveState(); c.translate(x, y); c.scale(s, s); c.setStrokeColor(col); c.setLineWidth(1.6); c.setLineCap(0)
    for i in range(8):
        a = math.radians(i * 45); c.line(5.2 * math.cos(a), 5.2 * math.sin(a), 7.4 * math.cos(a), 7.4 * math.sin(a))
    c.setLineWidth(1); c.circle(0, 0, 5.2, fill=0, stroke=1); c.circle(0, 0, 2, fill=0, stroke=1); c.restoreState()

def incline_symbol(c, x, y, s=1.0, col=white):
    """Triangle glyph centred near (x, y)."""
    c.saveState(); c.translate(x, y); c.scale(s, s); c.setStrokeColor(col); c.setLineWidth(1.1)
    p = c.beginPath(); p.moveTo(-11, -7.5); p.lineTo(11, -7.5); p.lineTo(11, 7.5); p.close(); c.drawPath(p, fill=0, stroke=1)
    c.restoreState()

SYMBOLS = {"atom": atom_symbol, "gear": gear_symbol, "incline": incline_symbol}

# ------------------------------------------------------------------ rich text: _{sub}, ^{sup}
_TOK = re.compile(r"_\{([^}]*)\}|\^\{([^}]*)\}")

def parse_rich(text, base="n"):
    """'f_{s,max} = μ_{s} × R' -> [('f','n'),('s,max','sub'),(' = μ','n'),('s','sub'),(' × R','n')]"""
    out, pos = [], 0
    for m in _TOK.finditer(text):
        if m.start() > pos: out.append((text[pos:m.start()], base))
        out.append((m.group(1), "sub") if m.group(1) is not None else (m.group(2), "sup"))
        pos = m.end()
    if pos < len(text): out.append((text[pos:], base))
    return out

def rich(c, x, y, segs, size=9.8, col=white):
    c.setFillColor(col)
    for text, mode in segs:
        if mode in ("sub", "sup"):
            fs = size * 0.7; dy = -2.2 if mode == "sub" else size * 0.38
            c.setFont("Body", fs); c.drawString(x, y + dy, text); x += pdfmetrics.stringWidth(text, "Body", fs)
        else:
            fn = "BodyB" if mode == "b" else "Body"
            c.setFont(fn, size); c.drawString(x, y, text); x += pdfmetrics.stringWidth(text, fn, size)
    return x

# ------------------------------------------------------------------ authoring helpers for new art
# Use these when drawing a fresh illustration/diagram so every figure shares one visual language.
HATCH = HexColor("#7B8AA0")

def hatch(c, x1, y1, x2, y2, step=6, length=4, side=-1):
    """Ground/wall hatching along the line (x1,y1)-(x2,y2); side=-1 hatches below/left, +1 above/right."""
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    nx, ny = -uy * side, ux * side
    c.saveState(); c.setStrokeColor(HATCH); c.setLineWidth(0.7); c.setLineCap(1)
    t = step / 2.0
    while t < L:
        px, py = x1 + ux * t, y1 + uy * t
        c.line(px, py, px - ux * length * 0.7 + nx * length, py - uy * length * 0.7 + ny * length); t += step
    c.restoreState()

def dim_arrow(c, x1, y1, x2, y2, col=ORANGE, lw=1.2, head=3.6):
    """Double-headed dimension arrow."""
    arrow(c, (x1 + x2) / 2, (y1 + y2) / 2, x1, y1, col, lw, head); arrow(c, (x1 + x2) / 2, (y1 + y2) / 2, x2, y2, col, lw, head)

def angle_arc(c, cx, cy, r, a0, a1, text=None, col=ORANGE, lw=1.4, size=8):
    """Arc from a0 to a1 degrees about (cx,cy) with an optional centred label just outside it."""
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw); c.setLineCap(1)
    c.arc(cx - r, cy - r, cx + r, cy + r, a0, a1 - a0); c.restoreState()
    if text:
        m = math.radians((a0 + a1) / 2); lab(c, cx + (r + 5.5) * math.cos(m), cy + (r + 5.5) * math.sin(m) - size * 0.35, text, col, size)

def zigzag(c, x1, y1, x2, y2, n=6, amp=5, lead=0.15, col=NAVY, lw=1.4):
    """Spring/resistor zig-zag with straight leads; n teeth."""
    dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy, ux
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath(); p.moveTo(x1, y1); a = L * lead; b = L * (1 - lead)
    p.lineTo(x1 + ux * a, y1 + uy * a)
    for i in range(n):
        t = a + (b - a) * (i + 0.5) / n; s = amp if i % 2 == 0 else -amp
        p.lineTo(x1 + ux * t + nx * s, y1 + uy * t + ny * s)
    p.lineTo(x1 + ux * b, y1 + uy * b); p.lineTo(x2, y2); c.drawPath(p, fill=0, stroke=1); c.restoreState()

def block(c, x, y, w, h, fill=TEAL, r=1.5, lw=1.2):
    stroke_style(c, lw); c.setFillColor(fill); c.roundRect(x, y, w, h, r, fill=1, stroke=1)

def ball(c, x, y, r, fill=TEAL, shine=True, lw=1.2):
    stroke_style(c, lw); c.setFillColor(fill); c.circle(x, y, r, fill=1, stroke=1)
    if shine: c.setFillColor(white); c.circle(x - r * 0.33, y + r * 0.33, r * 0.2, fill=1, stroke=0)

def dot(c, x, y, r=1.8, col=NAVY):
    c.saveState(); c.setFillColor(col); c.circle(x, y, r, fill=1, stroke=0); c.restoreState()

def dashed(c, x1, y1, x2, y2, col=GREY, lw=0.9, on=2.5, off=2.5):
    c.saveState(); c.setStrokeColor(col); c.setLineWidth(lw); c.setDash(on, off); c.line(x1, y1, x2, y2); c.restoreState()

def txt(c, x, y, s, size=7, col=NAVY, al="c", bold=True):
    """Free caption/variable name in a figure (use sparingly; <= 3 words)."""
    c.setFillColor(col); c.setFont("BodyB" if bold else "Body", size)
    {"c": c.drawCentredString, "l": c.drawString, "r": c.drawRightString}[al](x, y, s)

from mathtex import mlab, draw_math, math_width, math_obj, MATH_RE   # LaTeX-style maths (see mathtex.py)
