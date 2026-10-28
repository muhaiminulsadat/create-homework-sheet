"""HSC Chemistry 2nd Paper - Organic Chemistry: one icon per written question (100 x 64 box, y up).
No answers shown: only apparatus, reagents named in the question and neutral model atoms."""
import math
from drawkit import *

def _tube_path(c, cx, yt, yb, w):
    p = c.beginPath(); p.moveTo(cx - w / 2, yt); p.lineTo(cx - w / 2, yb + w / 2)
    p.arcTo(cx - w / 2, yb, cx + w / 2, yb + w, 180, 180); p.lineTo(cx + w / 2, yt); return p

def _tube(c, cx, yt, yb, w, liquid=None, level=None, lw=1.3):
    if liquid is not None:
        c.saveState(); c.clipPath(_tube_path(c, cx, yt, yb, w), stroke=0, fill=0)
        c.setFillColor(liquid); c.rect(cx - w, yb - 1, 2 * w, level - yb + 1, fill=1, stroke=0); c.restoreState()
    stroke_style(c, lw); c.drawPath(_tube_path(c, cx, yt, yb, w), fill=0, stroke=1)
    c.line(cx - w / 2 - 1.5, yt, cx + w / 2 + 1.5, yt)

def _flame(c, x, y, s=1.0):
    c.setFillColor(ORANGE); c.setStrokeColor(NAVY); c.setLineWidth(0.9)
    p = c.beginPath(); p.moveTo(x, y); p.curveTo(x - 5 * s, y + 4 * s, x - 3 * s, y + 9 * s, x, y + 13 * s)
    p.curveTo(x + 3 * s, y + 9 * s, x + 5 * s, y + 4 * s, x, y); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(ORANGE_L); c.circle(x, y + 3.5 * s, 1.8 * s, fill=1, stroke=0)

def _flask(c, cx, yb, r, neck_w, neck_top, liquid=None, level=None):
    """Round-bottom flask: sphere centre (cx, yb+r) and a neck up to neck_top."""
    cy = yb + r; a = math.asin(neck_w / 2 / r); ang = math.degrees(a)
    p = c.beginPath(); p.moveTo(cx - neck_w / 2, neck_top); p.lineTo(cx - neck_w / 2, cy + r * math.cos(a))
    p.arcTo(cx - r, cy - r, cx + r, cy + r, 90 + ang, 360 - 2 * ang)
    p.lineTo(cx + neck_w / 2, neck_top)
    if liquid is not None:
        c.saveState(); c.clipPath(p, stroke=0, fill=0); c.setFillColor(liquid)
        c.rect(cx - r, yb - 1, 2 * r, level - yb + 1, fill=1, stroke=0); c.restoreState()
    stroke_style(c, 1.3); c.drawPath(p, fill=0, stroke=1)

def _bubbles(c, pts, r=1.5):
    stroke_style(c, 0.8); c.setFillColor(white)
    for x, y in pts: c.circle(x, y, r, fill=1, stroke=1)

def _atom(c, x, y, r, fill, s=""):
    ball(c, x, y, r, fill, shine=False, lw=1.1)
    if s: txt(c, x, y - 2.2, s, 6.2, white if fill in (TEAL, NAVY) else NAVY)

@icon("organic-q1")
def q1(c):
    pts = [(16, 22), (34, 38), (52, 22), (70, 38)]
    stroke_style(c, 2.0)
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]): c.line(x1, y1, x2, y2)
    for x, y in pts[:3]: _atom(c, x, y, 6.5, TEAL, "C")
    _atom(c, 70, 38, 7, ORANGE, "OH")
    txt(c, 84, 22, "?", 15, ORANGE)
    lab(c, 50, 6, "chain of 3 C", GREY, 6.5)

@icon("organic-q2")
def q2(c):
    stroke_style(c, 1.4)
    c.setFillColor(TEAL_L); c.rect(28, 8, 40, 26, fill=1, stroke=0)
    p = c.beginPath(); p.moveTo(25, 56); p.lineTo(28, 56); p.lineTo(28, 8); p.lineTo(68, 8); p.lineTo(68, 56); p.lineTo(71, 56)
    c.drawPath(p, fill=0, stroke=1)
    c.setFillColor(HexColor("#C9D0DA")); stroke_style(c, 1.1); c.roundRect(42, 24, 12, 8, 1.5, fill=1, stroke=1)
    txt(c, 48, 26.5, "Na", 6, NAVY)
    _bubbles(c, [(36, 18), (40, 40), (55, 40), (60, 22), (50, 47), (46, 14), (62, 33)], 1.5)
    txt(c, 48, 0, "ethanol", 6.5, GREY, "c", False)
    

@icon("organic-q3")
def q3(c):
    _flask(c, 28, 8, 13, 7, 52, TEAL_L, 18)
    stroke_style(c, 1.3)
    p = c.beginPath(); p.moveTo(28, 52); p.lineTo(28, 58); p.lineTo(60, 58); p.lineTo(60, 35); c.drawPath(p, fill=0, stroke=1)
    _tube(c, 72, 56, 6, 22, TEAL_L, 30)
    stroke_style(c, 1.3); c.line(60, 35, 60, 22)
    c.setFillColor(white); c.rect(56, 13, 8, 3, fill=0, stroke=0)
    _bubbles(c, [(66, 20), (72, 26)], 1.6)
    _flame(c, 28, -8, 0.6)
    txt(c, 28, 0, "ethanol", 6, GREY, "c", False)

@icon("organic-q4")
def q4(c):
    _tube(c, 40, 56, 6, 20, HexColor("#F5B461"), 40)
    arrow(c, 76, 36, 52, 24, ORANGE, 1.5, 4.5)
    _bubbles(c, [(36, 14), (42, 22), (38, 30)], 1.5)
    txt(c, 90, 44, "C₂H₄", 8, TEAL, "r")
    txt(c, 40, 0, "bromine water", 6.2, GREY, "c", False)

@icon("organic-q5")
def q5(c):
    _tube(c, 26, 54, 8, 16, TEAL_L, 30)
    _tube(c, 74, 54, 8, 16, ORANGE_L, 30)
    txt(c, 26, 58, "CH₃CHO", 7, TEAL)
    txt(c, 74, 58, "CH₃COCH₃", 7, NAVY)
    txt(c, 50, 24, "?", 18, ORANGE)
    dim_arrow(c, 40, 34, 60, 34, ORANGE, 1.1, 3.4)

@icon("organic-q6")
def q6(c):
    for row, n in enumerate((2, 3, 4)):
        y = 48 - row * 18; x0 = 14
        stroke_style(c, 1.8)
        for i in range(n - 1): c.line(x0 + i * 15, y + (i % 2) * 5, x0 + (i + 1) * 15, y + ((i + 1) % 2) * 5)
        for i in range(n): _atom(c, x0 + i * 15, y + (i % 2) * 5, 5, TEAL)
    arrow(c, 86, 50, 86, 10, ORANGE, 1.4, 4.5)

@icon("organic-q7")
def q7(c):
    _flask(c, 32, 4, 15, 8, 46, TEAL_L, 16)
    c.setFillColor(HexColor("#B7BFCB")); stroke_style(c, 1.0)
    for x, y in ((26, 11), (33, 9), (38, 13)): c.roundRect(x - 3, y - 2, 7, 5, 1, fill=1, stroke=1)
    txt(c, 32, 22, "CaC₂", 6.4, NAVY)
    # dropping funnel
    stroke_style(c, 1.3); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(26, 62); p.lineTo(38, 62); p.lineTo(34, 50); p.lineTo(30, 50); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.line(32, 50, 32, 40); c.line(28, 46, 36, 46)
    p = c.beginPath(); p.moveTo(40, 40); p.lineTo(52, 40); p.lineTo(52, 8); c.drawPath(p, fill=0, stroke=1)
    _tube(c, 74, 56, 4, 20, TEAL_L, 24)
    stroke_style(c, 1.3); c.line(52, 8, 64, 8); c.line(64, 8, 72, 20)
    _bubbles(c, [(70, 14), (76, 18)], 1.5)

@icon("organic-q8")
def q8(c):
    for x, order in ((26, (TEAL, TEAL, ORANGE)), (74, (TEAL, ORANGE, TEAL))):
        c.setFillColor(PALE); c.setStrokeColor(LINE); c.setLineWidth(1); c.roundRect(x - 21, 14, 42, 38, 4, fill=1, stroke=1)
        stroke_style(c, 1.8)
        pts = [(x - 13, 28), (x, 40), (x + 13, 28)]
        c.line(*pts[0], *pts[1]); c.line(*pts[1], *pts[2])
        for (px, py), col in zip(pts, order): _atom(c, px, py, 5.6, col)
    txt(c, 50, 30, "=", 12, ORANGE)
    lab(c, 50, 4, "same molecular formula", GREY, 6.2)

@icon("organic-q9")
def q9(c):
    _flask(c, 36, 4, 14, 7, 30, HexColor("#F5B461"), 17)
    stroke_style(c, 1.3); c.setFillColor(white)
    c.roundRect(32, 26, 8, 34, 2, fill=1, stroke=1)
    c.setFillColor(TEAL_L); c.roundRect(29, 32, 14, 22, 2, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(29.5, 34, 13, 3, fill=1, stroke=0)
    arrow(c, 50, 36, 50, 54, TEAL, 1.2, 3.6)
    arrow(c, 80, 56, 80, 38, TEAL, 1.2, 3.6)
    txt(c, 90, 44, "", 6)
    _flame(c, 36, -9, 0.6)
    lab(c, 76, 28, "heat", ORANGE, 7.5)
    lab(c, 78, 62 - 4, "oxidant", GREY, 6.2)

@icon("organic-q10")
def q10(c):
    _tube(c, 40, 52, 6, 18, ORANGE_L, 34)
    c.setFillColor(HexColor("#F3A34B")); c.saveState(); c.clipPath(_tube_path(c, 40, 52, 6, 18), stroke=0, fill=0)
    c.rect(30, 4, 20, 8, fill=1, stroke=0); c.restoreState()
    stroke_style(c, 1.3); c.drawPath(_tube_path(c, 40, 52, 6, 18), fill=0, stroke=1)
    # dropper
    stroke_style(c, 1.2); c.setFillColor(TEAL); c.roundRect(68, 52, 10, 8, 3, fill=1, stroke=1)
    c.setFillColor(white); c.rect(71, 38, 4, 14, fill=1, stroke=1)
    c.setFillColor(ORANGE); c.circle(73, 34, 1.6, fill=1, stroke=0); c.circle(73, 28, 1.6, fill=1, stroke=0)
    txt(c, 90, 20, "2,4-DNPH", 6.2, NAVY, "r")
    txt(c, 40, 56, "CH₃CHO", 6.4, TEAL)
