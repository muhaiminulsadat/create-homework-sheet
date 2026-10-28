"""LaTeX-style maths for the homework sheet (vector, Computer Modern look).

Write maths between dollar signs in any question or option, e.g.
    "Evaluate $\\int_0^1 3x^2\\,dx$"   "$\\dfrac{x^4}{4}+C$"   "$\\tan^{-1}\\frac{x}{2}$"
Rendered with matplotlib's mathtext (no TeX install needed) and drawn as filled vector paths,
so it stays sharp at any print size. In art, use mlab(c, x, y, r"$y=x^3$", col, size, al).
"""
import re
from functools import lru_cache
import matplotlib
matplotlib.rcParams["mathtext.fontset"] = "cm"
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path

_FP = FontProperties(family="serif")
MATH_RE = re.compile(r"(\$[^$]+\$)")

@lru_cache(maxsize=None)
def math_obj(latex, size):
    """-> (path, x0, width, ascent, descent) for a $...$ string at the given pt size."""
    tp = TextPath((0, 0), latex, size=size, prop=_FP)
    e = tp.get_extents()
    return tp, e.x0, e.x1 - e.x0, max(e.y1, 0), max(-e.y0, 0)

def math_width(latex, size):
    return math_obj(latex, size)[2]

def draw_math(c, x, y, latex, size, col, al="l"):
    """Draw maths with its baseline at y; x is the left edge (al=l), centre (c) or right edge (r)."""
    tp, x0, w, asc, desc = math_obj(latex, size)
    left = x - (w / 2 if al == "c" else w if al == "r" else 0)
    p = c.beginPath(); cur = (0, 0)
    for verts, code in tp.iter_segments(curves=True, simplify=False):
        pts = [(left + vx - x0, y + vy) for vx, vy in zip(verts[0::2], verts[1::2])]
        if code == Path.MOVETO:
            p.moveTo(*pts[0]); cur = pts[0]
        elif code == Path.LINETO:
            p.lineTo(*pts[0]); cur = pts[0]
        elif code == Path.CURVE3:      # quadratic -> cubic
            (qx, qy), (ex, ey) = pts[0], pts[1]
            p.curveTo(cur[0] + 2 / 3 * (qx - cur[0]), cur[1] + 2 / 3 * (qy - cur[1]),
                      ex + 2 / 3 * (qx - ex), ey + 2 / 3 * (qy - ey), ex, ey); cur = (ex, ey)
        elif code == Path.CURVE4:
            p.curveTo(*pts[0], *pts[1], *pts[2]); cur = pts[2]
        elif code == Path.CLOSEPOLY:
            p.close()
    c.saveState(); c.setFillColor(col); c.drawPath(p, fill=1, stroke=0); c.restoreState()

def mlab(c, x, y, latex, col=None, size=7.5, al="c"):
    """Maths caption inside an icon/diagram (same call shape as lab)."""
    from drawkit import NAVY
    draw_math(c, x, y, latex, size, col or NAVY, al)
