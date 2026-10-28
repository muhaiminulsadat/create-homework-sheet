"""Work, Energy and Power: one icon per MCQ (100 x 64 box, y up)."""
import math
from drawkit import *

def _cart(c, x, y, w=24, h=16, fill=TEAL):
    """Block on two wheels, bottom-left at (x, y+3.5)."""
    for wx in (x + 5, x + w - 5):
        stroke_style(c, 1.1); c.setFillColor(NAVY); c.circle(wx, y + 2.6, 2.6, fill=1, stroke=1)
    block(c, x, y + 4, w, h, fill, 2)


@icon("wep-q1")
def q1(c):
    floor(c, 4, 96, 12)
    _cart(c, 30, 12, 26, 18)
    lab(c, 43, 20, "2 kg", white, 7.5)
    arrow(c, 60, 24, 92, 24, ORANGE, 2.2, 5.5); lab(c, 76, 30, "5 m/s", ORANGE, 7.5)


@icon("wep-q2")
def q2(c):
    floor(c, 4, 96, 14)
    block(c, 6, 14, 24, 14, TEAL, 2)
    ox, oy = 30, 28
    th = math.radians(60)
    arrow(c, ox, oy, ox + 28 * math.cos(th), oy + 28 * math.sin(th), ORANGE, 2.2, 5.5)
    lab(c, ox + 30 * math.cos(th) + 3, oy + 28 * math.sin(th) - 6, "10 N", ORANGE, 7.5, "l")
    dashed(c, ox, oy, ox + 44, oy, GREY, 1, 2.5, 2.5)
    angle_arc(c, ox, oy, 12, 0, 60, "60°", ORANGE, 1.3, 6.8)
    dim_arrow(c, 8, 5, 52, 5, TEAL, 1.2, 3.4); lab(c, 74, 3, "s = 4 m", TEAL, 7)


@icon("wep-q3")
def q3(c):
    floor(c, 4, 96, 10)
    c.saveState(); c.translate(18, 10); car2(c, 0.8); c.restoreState()
    arrow(c, 32, 26, 48, 26, ORANGE, 2, 5); lab(c, 40, 32, "v", ORANGE, 8)
    c.saveState(); c.translate(62, 10); car2(c, 0.8, NAVY); c.restoreState()
    arrow(c, 70, 26, 96, 26, ORANGE, 2.4, 5.5); lab(c, 83, 32, "2v", ORANGE, 8)


@icon("wep-q4")
def q4(c):
    # gear (machine)
    gx, gy = 28, 32
    stroke_style(c, 1.3); c.setFillColor(TEAL)
    for i in range(8):
        a = math.radians(i * 45)
        c.saveState(); c.translate(gx + 17 * math.cos(a), gy + 17 * math.sin(a)); c.rotate(i * 45)
        c.roundRect(-4, -3.5, 8, 7, 1.2, fill=1, stroke=1); c.restoreState()
    c.circle(gx, gy, 16, fill=1, stroke=1)
    c.setFillColor(white); c.circle(gx, gy, 6, fill=1, stroke=1)
    lab(c, gx, 4, "1200 J", NAVY, 7.5)
    # stopwatch
    sx, sy = 74, 30
    stroke_style(c, 1.3); c.setFillColor(ORANGE_L); c.circle(sx, sy, 16, fill=1, stroke=1)
    c.setFillColor(NAVY); c.rect(sx - 3, sy + 16, 6, 4, fill=1, stroke=0)
    c.setLineWidth(1.5); c.line(sx, sy, sx + 8, sy + 8)
    c.setLineWidth(1.5); c.line(sx, sy, sx, sy + 11)
    dot(c, sx, sy, 1.8)
    lab(c, sx, 4, "20 s", NAVY, 7.5)


@icon("wep-q5")
def q5(c):
    hatch(c, 8, 8, 60, 8, 6, 4, -1)
    stroke_style(c, 1.4); c.line(8, 8, 60, 8)
    dim_arrow(c, 14, 10, 14, 54, ORANGE, 1.3, 3.8); lab(c, 18, 30, "h", ORANGE, 9, "l")
    dashed(c, 14, 56, 40, 56, GREY, 0.9, 2.5, 2.5)
    ball(c, 40, 52, 6, TEAL)
    arrow(c, 40, 43, 40, 18, NAVY, 1.8, 5)
    lab(c, 46, 28, "free fall", NAVY, 6.8, "l")
    ball(c, 40, 14, 5, TEAL_L)
    lab(c, 76, 52, "KE = ?", ORANGE, 8)


@icon("wep-q6")
def q6(c):
    ox, oy = 14, 10
    stroke_style(c, 1.3)
    arrow(c, ox, oy, 94, oy, NAVY, 1.4, 4); arrow(c, ox, oy, ox, 60, NAVY, 1.4, 4)
    lab(c, 94, oy - 8, "x", NAVY, 8, "r"); lab(c, ox - 3, 56, "F", NAVY, 8, "r")
    ex, ey = 74, 54
    p = c.beginPath(); p.moveTo(ox, oy); p.lineTo(ex, oy); p.lineTo(ex, ey); p.close()
    c.setFillColor(TEAL_L); c.setStrokeColor(TEAL); c.setLineWidth(0.8); c.drawPath(p, fill=1, stroke=0)
    c.setStrokeColor(ORANGE); c.setLineWidth(2); c.setLineCap(1); c.line(ox, oy, ex, ey)
    dashed(c, ex, oy, ex, ey, GREY, 0.9)
    lab(c, ex, oy - 8, "3 m", NAVY, 7.2)
    lab(c, 22, 52, "F = 2x", ORANGE, 8, "l")


@icon("wep-q7")
def q7(c):
    cx, cy, r = 38, 32, 21
    stroke_style(c, 1.2); c.setStrokeColor(GREY); c.setDash(3, 2.5); c.circle(cx, cy, r, fill=0, stroke=1); c.setDash()
    dot(c, cx, cy, 2.2)
    bx, by = cx + r, cy
    arrow(c, bx, by, bx, by + 22, TEAL, 2, 5); lab(c, bx + 4, by + 16, "v", TEAL, 8.5, "l")
    arrow(c, bx, by, bx - 17, by, ORANGE, 2, 5)
    lab(c, bx + 5, by - 12, "centripetal", ORANGE, 6.3, "l")
    lab(c, bx + 5, by - 19, "force", ORANGE, 6.3, "l")
    ball(c, bx, by, 5, TEAL)


@icon("wep-q8")
def q8(c):
    # ground, low tank, pump, pipe up to high tank
    hatch(c, 4, 6, 96, 6, 6, 4, -1); stroke_style(c, 1.3); c.line(4, 6, 96, 6)
    stroke_style(c, 1.2); c.setFillColor(TEAL_L); c.rect(6, 6, 24, 12, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(6, 6, 24, 7, fill=1, stroke=0); c.rect(6, 6, 24, 12, fill=0, stroke=1)
    lab(c, 18, 21, "100 kg", NAVY, 6.8)
    block(c, 36, 6, 14, 11, ORANGE, 2); lab(c, 43, 9.5, "P", NAVY, 7.5)
    stroke_style(c, 2.4); c.setStrokeColor(NAVY)
    p = c.beginPath(); p.moveTo(30, 11); p.lineTo(36, 11); c.drawPath(p, fill=0, stroke=1)
    p = c.beginPath(); p.moveTo(50, 11); p.lineTo(62, 11); p.lineTo(62, 46); c.drawPath(p, fill=0, stroke=1)
    stroke_style(c, 1.2); c.setFillColor(TEAL_L); c.rect(54, 46, 36, 14, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(54, 46, 36, 6, fill=1, stroke=0); c.rect(54, 46, 36, 14, fill=0, stroke=1)
    dim_arrow(c, 93, 8, 93, 46, ORANGE, 1.2, 3.4)
    lab(c, 90, 26, "10 m", ORANGE, 7.2, "r")


@icon("wep-q9")
def q9(c):
    hatch(c, 8, 8, 8, 56, 6, 4, 1)
    stroke_style(c, 2); c.line(8, 8, 8, 56)
    floor(c, 8, 96, 8, hatch=True)
    zigzag(c, 8, 22, 62, 22, 8, 5, 0.12, NAVY, 1.5)
    block(c, 62, 8, 20, 28, TEAL, 2)
    dashed(c, 44, 8, 44, 44, GREY, 0.9)
    dim_arrow(c, 44, 46, 62, 46, ORANGE, 1.3, 3.4)
    lab(c, 53, 51, "x", ORANGE, 8.5)
    lab(c, 72, 18, "U", white, 9)


@icon("wep-q10")
def q10(c):
    floor(c, 4, 96, 12)
    _cart(c, 12, 12, 26, 18)
    lab(c, 25, 20, "2 kg", white, 7.5)
    arrow(c, 42, 24, 92, 24, ORANGE, 2.4, 5.5)
    lab(c, 67, 38, "p = 12", ORANGE, 7.5)
    lab(c, 67, 30, "kg·m/s", ORANGE, 7.5)
