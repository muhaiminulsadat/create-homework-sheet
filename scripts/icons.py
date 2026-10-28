"""Illustration library. Every icon is draw(c) in a local 100 x 64 box (y up), flat vector line art:
navy outlines, teal fills, orange accents. Keep to that style when adding icons.

Register with @icon("name", "alias1", ...). Custom icons live in icons_custom.py (auto-loaded).
"""
import math
from reportlab.lib.colors import HexColor, white
from drawkit import *

REGISTRY = {}
BOXES = {}          # name -> (width, height) of the drawing's local box
ICON_BOX = (100, 64)     # small symbolic illustration (default)
DIAGRAM_BOX = (150, 100) # full diagram: renders larger, in a wider right-hand column

def icon(*names, box=ICON_BOX):
    """Register art under one or more names. box=DIAGRAM_BOX for a full diagram."""
    def deco(fn):
        for n in names:
            REGISTRY[n.lower()] = fn; BOXES[n.lower()] = box
        return fn
    return deco

# ============================================================ Friction / dynamics set (the original 10)
@icon("plane", "airplane", "air-friction")
def i_plane(c):
    stroke_style(c, 1.2)
    p = c.beginPath(); p.moveTo(18, 37); p.lineTo(10, 54); p.lineTo(22, 54); p.lineTo(34, 40); p.close()
    c.setFillColor(TEAL); c.drawPath(p, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(44, 34); p.lineTo(38, 22); p.lineTo(50, 22); p.lineTo(62, 34); p.close()
    c.setFillColor(NAVY); c.drawPath(p, fill=1, stroke=1)
    p = c.beginPath(); p.moveTo(44, 40); p.lineTo(38, 58); p.lineTo(52, 58); p.lineTo(64, 40); p.close()
    c.setFillColor(ORANGE); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(TEAL); c.ellipse(8, 30, 92, 46, fill=1, stroke=1)
    c.setFillColor(white)
    for wx in (62, 69, 76, 83): c.ellipse(wx - 2.2, 36, wx + 2.2, 41, fill=1, stroke=0)
    arrow(c, 80, 17, 24, 17, ORANGE, 1.8); lab(c, 52, 7, "air friction", ORANGE)

@icon("box", "push", "box-push")
def i_box(c):
    floor(c, 4, 96, 16)
    stroke_style(c, 1.2); c.setFillColor(TEAL); c.rect(52, 16, 32, 28, fill=1, stroke=1)
    c.setStrokeColor(white); c.setLineWidth(0.8); c.line(55, 20, 81, 20); c.line(55, 40, 81, 40)
    arrow(c, 8, 30, 48, 30, ORANGE, 2.2, 5.5); lab(c, 8, 36, "push", ORANGE, 7, "l")

@icon("fall", "falling", "air-resistance")
def i_fall(c):
    stroke_style(c, 1.2); c.setFillColor(TEAL); c.circle(40, 20, 12, fill=1, stroke=1)
    c.setFillColor(white); c.circle(36, 24, 2.6, fill=1, stroke=0)
    stroke_style(c, 1); c.setStrokeColor(TEAL); c.setDash(2, 2); c.line(22, 38, 22, 54); c.line(30, 38, 30, 54); c.setDash()
    arrow(c, 40, 36, 40, 60, ORANGE, 2, 5)
    lab(c, 50, 44, "air", ORANGE, 6.8, "l"); lab(c, 50, 36, "resistance", ORANGE, 6.8, "l")

@icon("jackfruit", "hanging", "fruit")
def i_jack(c):
    stroke_style(c, 2); c.setStrokeColor(HexColor("#8A5A2B")); c.line(6, 58, 94, 58)
    stroke_style(c, 1); c.setFillColor(TEAL)
    for (lx, ly, r) in [(18, 60, -20), (30, 55, 15), (72, 61, 20), (84, 56, -10)]:
        c.saveState(); c.translate(lx, ly); c.rotate(r); c.ellipse(-7, -3, 7, 3, fill=1, stroke=1); c.restoreState()
    stroke_style(c, 1.4); c.line(48, 58, 48, 49)
    c.setFillColor(ORANGE); c.ellipse(33, 6, 63, 49, fill=1, stroke=1)
    c.setFillColor(HexColor("#C77A1E"))
    for (dx, dy) in [(41, 40), (50, 41), (40, 31), (48, 32), (56, 30), (43, 22), (52, 21), (47, 13)]:
        c.circle(dx, dy, 1.4, fill=1, stroke=0)
    arrow(c, 80, 54, 80, 8, TEAL, 2.2, 5.5)

@icon("incline", "slope", "car-incline")
def i_incline(c):
    ang = math.atan2(38, 84)
    stroke_style(c, 1.3); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(4, 8); p.lineTo(96, 8); p.lineTo(96, 8 + 92 * math.tan(ang)); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.saveState(); x = 56; y = 8 + (x - 4) * math.tan(ang)
    c.translate(x, y); c.rotate(math.degrees(ang)); car2(c, 1.0); c.restoreState()
    c.setStrokeColor(ORANGE); c.setLineWidth(1.5); c.arc(-10, -10, 26, 26, 0, math.degrees(ang))
    lab(c, 29, 12, "θ", ORANGE, 9)

@icon("slide", "block-friction", "sliding-block")
def i_slide(c):
    floor(c, 4, 96, 18)
    stroke_style(c, 1.2); c.setFillColor(TEAL); c.rect(38, 18, 30, 24, fill=1, stroke=1)
    arrow(c, 38, 22, 6, 22, ORANGE, 2.2, 5.5); lab(c, 5, 27, "friction", ORANGE, 7, "l")
    arrow(c, 44, 52, 82, 52, NAVY, 1.4, 4.5); lab(c, 46, 57, "motion", NAVY, 6.4, "l")

@icon("football", "ball", "rolling-ball")
def i_ball(c):
    c.setFillColor(GRASS); c.setStrokeColor(NAVY); c.setLineWidth(1); c.rect(4, 8, 92, 8, fill=1, stroke=1)
    c.setStrokeColor(GRASS); c.setLineWidth(1)
    for gx in range(8, 94, 4): c.line(gx, 16, gx + 1, 19.5)
    bx, by, r = 66, 29, 13
    c.setStrokeColor(HexColor("#7BC2C6")); c.setLineWidth(1.4)
    for (yy, x1) in [(36, 20), (29, 12), (22, 22)]: c.line(x1, yy, x1 + 28, yy)
    stroke_style(c, 1.3); c.setFillColor(white); c.circle(bx, by, r, fill=1, stroke=1)
    c.setFillColor(NAVY); pent(c, bx, by, 4.8)
    for k in range(5):
        a = math.radians(90 + 72 * k + 36); pent(c, bx + 11 * math.cos(a), by + 11 * math.sin(a), 3.2, math.degrees(a) + 180)

@icon("roadcar", "car-forces", "car")
def i_roadcar(c):
    floor(c, 4, 96, 14, False)
    c.setStrokeColor(NAVY); c.setLineWidth(2.2); c.line(4, 12, 96, 12)
    c.saveState(); c.translate(50, 12); c.scale(1.35, 1.35); car2(c, 1.0); c.restoreState()
    arrow(c, 74, 32, 98, 32, ORANGE, 2); lab(c, 80, 39, "driving force", ORANGE, 5.8)
    arrow(c, 26, 32, 2, 32, ORANGE, 2); lab(c, 14, 39, "friction", ORANGE, 5.8)
    arrow(c, 50, 42, 50, 60, NAVY, 1.6, 4.5); lab(c, 56, 55, "N", NAVY, 7, "l")
    arrow(c, 50, 11, 50, 1, NAVY, 1.4, 3.5); lab(c, 56, 1.5, "mg", NAVY, 6.4, "l")

@icon("brake", "skid", "braking-car")
def i_brake(c):
    floor(c, 4, 96, 15, False)
    c.setStrokeColor(NAVY); c.setLineWidth(2.2); c.line(4, 13, 96, 13)
    c.setLineWidth(2.4); c.setLineCap(0)
    c.line(6, 9, 44, 9); c.line(6, 4, 44, 4)
    c.saveState(); c.translate(68, 13); c.scale(1.3, 1.3); car2(c, 1.0); c.restoreState()
    arrow(c, 94, 46, 56, 46, ORANGE, 2); lab(c, 75, 52, "friction", ORANGE, 6.8)

@icon("sand", "impact", "falling-into-sand")
def i_sand(c):
    stroke_style(c, 1.3); c.setFillColor(ORANGE_L)
    p = c.beginPath(); p.moveTo(4, 4); p.lineTo(96, 4); p.lineTo(96, 24); p.curveTo(70, 30, 30, 30, 4, 24); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setFillColor(ORANGE)
    for (dx, dy) in [(12, 12), (24, 20), (36, 9), (62, 21), (74, 10), (86, 17), (48, 7), (20, 8)]:
        c.circle(dx, dy, 1, fill=1, stroke=0)
    c.setFillColor(white); stroke_style(c, 1.1); c.setDash(2, 2); c.circle(50, 17, 8, fill=1, stroke=1); c.setDash()
    stroke_style(c, 1.3); c.setFillColor(TEAL); c.circle(50, 46, 9, fill=1, stroke=1)
    arrow(c, 50, 63, 50, 56, NAVY, 1.5, 4)
    c.setStrokeColor(ORANGE); c.setLineWidth(1.4); c.setDash(1, 2); c.line(50, 36, 50, 26); c.setDash()

# ============================================================ Extra mechanics
@icon("projectile", "trajectory", "parabola")
def i_projectile(c):
    floor(c, 4, 96, 12, False)
    c.setStrokeColor(NAVY); c.setLineWidth(1.6); c.line(4, 12, 96, 12)
    stroke_style(c, 1.3); c.setStrokeColor(TEAL); c.setDash(2.5, 2.5)
    p = c.beginPath(); p.moveTo(10, 12)
    for i in range(1, 41):
        x = 10 + 80 * i / 40; t = (x - 50) / 40.0
        p.lineTo(x, 12 + 40 * (1 - t * t))
    c.drawPath(p, fill=0, stroke=1); c.setDash()
    arrow(c, 10, 12, 26, 29, NAVY, 1.6, 4.5); lab(c, 30, 24, "v", NAVY, 7.5, "l")
    c.setStrokeColor(ORANGE); c.setLineWidth(1.4); c.arc(-4, -2, 24, 26, 0, 46); lab(c, 28, 15, "θ", ORANGE, 8, "l")
    t = (70 - 50) / 40.0; stroke_style(c, 1.2); c.setFillColor(TEAL); c.circle(70, 12 + 40 * (1 - t * t), 5.5, fill=1, stroke=1)
    arrow(c, 70, 12 + 40 * (1 - t * t) - 6, 70, 18, ORANGE, 1.6, 4)

@icon("pulley", "atwood")
def i_pulley(c):
    stroke_style(c, 1.6); c.line(36, 62, 64, 62); c.setLineWidth(0.7); c.setStrokeColor(HexColor("#7B8AA0"))
    for hx in range(38, 64, 6): c.line(hx, 62, hx + 3, 65.5)
    stroke_style(c, 1.5); c.line(50, 62, 50, 54)
    c.setFillColor(white); c.circle(50, 46, 11, fill=1, stroke=1); c.setFillColor(NAVY); c.circle(50, 46, 2, fill=1, stroke=0)
    stroke_style(c, 1.2); c.line(39, 46, 39, 30); c.line(61, 46, 61, 40)
    c.setFillColor(TEAL); c.rect(28, 14, 22, 16, fill=1, stroke=1)
    c.setFillColor(ORANGE); c.rect(54, 28, 14, 12, fill=1, stroke=1)
    lab(c, 39, 19.5, "M", white, 8); lab(c, 61, 31, "m", NAVY, 7)

@icon("spring", "spring-mass", "shm")
def i_spring(c):
    stroke_style(c, 2); c.line(8, 10, 8, 50); c.setLineWidth(0.7); c.setStrokeColor(HexColor("#7B8AA0"))
    for hy in range(14, 50, 6): c.line(8, hy, 4, hy - 3)
    floor(c, 8, 96, 14, False); c.setStrokeColor(NAVY); c.setLineWidth(1.5); c.line(8, 14, 96, 14)
    stroke_style(c, 1.4); c.setStrokeColor(TEAL)
    p = c.beginPath(); p.moveTo(8, 28); p.lineTo(14, 28)
    for i in range(7): p.lineTo(18 + i * 5, 28 + (7 if i % 2 == 0 else -7))
    p.lineTo(52, 28); c.drawPath(p, fill=0, stroke=1)
    stroke_style(c, 1.2); c.setFillColor(TEAL); c.rect(52, 14, 26, 28, fill=1, stroke=1)
    arrow(c, 82, 46, 94, 46, ORANGE, 1.8, 4.5); arrow(c, 82, 46, 70, 46, ORANGE, 1.8, 4.5)

@icon("pendulum", "swing")
def i_pendulum(c):
    stroke_style(c, 2); c.line(34, 60, 66, 60); c.setLineWidth(0.7); c.setStrokeColor(HexColor("#7B8AA0"))
    for hx in range(36, 66, 6): c.line(hx, 60, hx + 3, 63.5)
    c.setStrokeColor(GREY); c.setLineWidth(0.9); c.setDash(2, 2); c.line(50, 60, 50, 6); c.setDash()
    stroke_style(c, 1.3); c.line(50, 60, 72, 22)
    c.setFillColor(TEAL); c.circle(72, 22, 8, fill=1, stroke=1)
    c.setStrokeColor(ORANGE); c.setLineWidth(1.5); c.arc(36, 46, 64, 74, 270, 30); lab(c, 53, 40, "θ", ORANGE, 8, "l")

@icon("lever", "balance", "moments")
def i_lever(c):
    stroke_style(c, 1.3); c.setFillColor(NAVY)
    p = c.beginPath(); p.moveTo(50, 22); p.lineTo(42, 6); p.lineTo(58, 6); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.saveState(); c.translate(50, 24); c.rotate(-6); c.setFillColor(TEAL_L); c.rect(-42, -2.5, 84, 5, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(-38, 2.5, 18, 14, fill=1, stroke=1); c.setFillColor(ORANGE); c.rect(26, 2.5, 10, 8, fill=1, stroke=1); c.restoreState()
    arrow(c, 18, 56, 18, 42, NAVY, 1.4, 4); arrow(c, 82, 52, 82, 40, NAVY, 1.4, 4)

# ============================================================ Electricity & magnetism
@icon("circuit", "current", "resistor")
def i_circuit(c):
    stroke_style(c, 1.4)
    p = c.beginPath(); p.moveTo(14, 28); p.lineTo(14, 10); p.lineTo(86, 10); p.lineTo(86, 25); c.drawPath(p, fill=0, stroke=1)
    p = c.beginPath(); p.moveTo(14, 36); p.lineTo(14, 54); p.lineTo(34, 54); c.drawPath(p, fill=0, stroke=1)
    p = c.beginPath(); p.moveTo(34, 54)
    for i, dy in enumerate([6, -6, 6, -6, 6, -6]): p.lineTo(38 + i * 4.5, 54 + dy)
    p.lineTo(66, 54); p.lineTo(86, 54); p.lineTo(86, 39); c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(2.2); c.line(7, 36, 21, 36); c.setLineWidth(2.2); c.line(10, 28, 18, 28)
    lab(c, 22, 38, "+", ORANGE, 8, "l")
    c.setLineWidth(1.4); c.setFillColor(ORANGE_L); c.circle(86, 32, 7, fill=1, stroke=1)
    c.line(81, 27, 91, 37); c.line(81, 37, 91, 27)
    arrow(c, 52, 61, 68, 61, ORANGE, 1.4, 4)

@icon("charges", "coulomb", "electrostatics")
def i_charges(c):
    stroke_style(c, 1.3); c.setFillColor(ORANGE); c.circle(22, 32, 11, fill=1, stroke=1)
    c.setFillColor(TEAL); c.circle(78, 32, 11, fill=1, stroke=1)
    lab(c, 22, 28.2, "+", white, 13); lab(c, 78, 28.2, "−", white, 13)
    arrow(c, 36, 32, 46, 32, NAVY, 1.6, 4.5); arrow(c, 64, 32, 54, 32, NAVY, 1.6, 4.5)
    lab(c, 41, 38, "F", NAVY, 7); lab(c, 59, 38, "F", NAVY, 7)
    c.setStrokeColor(GREY); c.setLineWidth(0.9); c.setDash(2, 2); c.line(22, 12, 78, 12); c.setDash(); lab(c, 50, 4, "r", NAVY, 7)

@icon("magnet", "magnetic", "field")
def i_magnet(c):
    c.setStrokeColor(HILITE); c.setLineWidth(1.1); c.setDash(2.5, 2.5)
    c.ellipse(16, 6, 84, 58, fill=0, stroke=1); c.ellipse(26, 14, 74, 50, fill=0, stroke=1); c.setDash()
    stroke_style(c, 1.3); c.setFillColor(ORANGE); c.rect(28, 26, 22, 13, fill=1, stroke=1)
    c.setFillColor(TEAL); c.rect(50, 26, 22, 13, fill=1, stroke=1)
    lab(c, 39, 29.6, "N", white, 9); lab(c, 61, 29.6, "S", white, 9)

# ============================================================ Waves, optics, heat, gases, space
@icon("wave", "waves", "sound")
def i_wave(c):
    c.setStrokeColor(GREY); c.setLineWidth(0.9); c.setDash(2, 2); c.line(4, 32, 96, 32); c.setDash()
    stroke_style(c, 2); c.setStrokeColor(TEAL)
    p = c.beginPath(); p.moveTo(6, 32)
    for i in range(1, 89): x = 6 + i; p.lineTo(x, 32 + 17 * math.sin(i / 88.0 * 4 * math.pi))
    c.drawPath(p, fill=0, stroke=1)
    stroke_style(c, 1.2); c.setStrokeColor(ORANGE); c.setFillColor(ORANGE)
    arrow(c, 17, 56, 61, 56, ORANGE, 1.3, 4); arrow(c, 61, 56, 17, 56, ORANGE, 1.3, 4); lab(c, 39, 59, "λ", ORANGE, 8)

@icon("lens", "optics", "ray")
def i_lens(c):
    c.setStrokeColor(GREY); c.setLineWidth(0.9); c.line(4, 32, 96, 32)
    stroke_style(c, 1.4); c.setFillColor(TEAL_L)
    p = c.beginPath(); p.moveTo(50, 9); p.curveTo(62, 22, 62, 42, 50, 55); p.curveTo(38, 42, 38, 22, 50, 9); p.close(); c.drawPath(p, fill=1, stroke=1)
    c.setStrokeColor(ORANGE); c.setLineWidth(1.6)
    for y0 in (46, 18):
        c.line(6, y0, 50, y0); c.line(50, y0, 80, 32); c.line(80, 32, 96, 32 - (y0 - 32) * 0.53)
    c.setFillColor(NAVY); c.circle(80, 32, 2.2, fill=1, stroke=0); lab(c, 80, 24, "F", NAVY, 7)
    arrow(c, 16, 32, 16, 42, NAVY, 1.5, 4)

@icon("flask", "chemistry", "heat")
def i_flask(c):
    stroke_style(c, 1.4)
    c.setFillColor(TEAL_L)
    p = c.beginPath(); p.moveTo(34.3, 28); p.lineTo(65.7, 28); p.lineTo(76, 12); p.lineTo(24, 12); p.close(); c.drawPath(p, fill=1, stroke=0)
    stroke_style(c, 1.4)
    p = c.beginPath(); p.moveTo(42, 58); p.lineTo(42, 40); p.lineTo(24, 12); p.lineTo(76, 12); p.lineTo(58, 40); p.lineTo(58, 58); c.drawPath(p, fill=0, stroke=1)
    c.line(39, 58, 61, 58); c.setStrokeColor(TEAL); c.line(34.3, 28, 65.7, 28)
    c.setFillColor(white); c.setStrokeColor(TEAL); c.setLineWidth(1)
    for (bx, by, r) in [(45, 18, 2.4), (54, 22, 1.8), (50, 15, 1.4)]: c.circle(bx, by, r, fill=1, stroke=1)
    c.setFillColor(ORANGE); stroke_style(c, 1)
    p = c.beginPath(); p.moveTo(50, 8); p.curveTo(44, 4, 46, 1, 50, 0); p.curveTo(54, 1, 56, 4, 50, 8); p.close(); c.drawPath(p, fill=1, stroke=0)

@icon("piston", "gas", "ideal-gas")
def i_piston(c):
    stroke_style(c, 1.5); c.setFillColor(PALE); c.rect(12, 10, 52, 40, fill=1, stroke=1)
    c.setFillColor(NAVY); c.rect(60, 12, 5, 36, fill=1, stroke=1); c.line(65, 30, 90, 30); c.line(90, 22, 90, 38)
    c.setFillColor(TEAL); c.setLineWidth(0.9)
    for (x, y, r) in [(22, 20, 2.6), (34, 38, 2.6), (44, 22, 2.6), (30, 28, 2.6), (52, 40, 2.6), (50, 30, 2.6), (20, 40, 2.6)]:
        c.circle(x, y, r, fill=1, stroke=1)
    arrow(c, 52, 56, 38, 56, ORANGE, 1.5, 4)

@icon("orbit", "satellite", "gravitation")
def i_orbit(c):
    c.setStrokeColor(NAVY); c.setLineWidth(1.2); c.setDash(2.5, 2.5); c.ellipse(14, 14, 86, 50, fill=0, stroke=1); c.setDash()
    stroke_style(c, 1.3); c.setFillColor(TEAL); c.circle(50, 32, 11, fill=1, stroke=1)
    c.setFillColor(white); c.circle(46, 36, 2.6, fill=1, stroke=0)
    c.saveState(); c.translate(81, 41); c.rotate(-24); c.setFillColor(ORANGE); c.rect(-4, -3, 8, 6, fill=1, stroke=1)
    c.setFillColor(TEAL_L); c.rect(-11, -1.5, 6, 3, fill=1, stroke=1); c.rect(5, -1.5, 6, 3, fill=1, stroke=1); c.restoreState()
    arrow(c, 76, 40, 64, 36, ORANGE, 1.5, 4)

@icon("graph", "plot", "axes")
def i_graph(c):
    stroke_style(c, 1.4); c.line(14, 8, 14, 58); c.line(14, 8, 92, 8)
    arrow(c, 14, 54, 14, 60, NAVY, 1.4, 4); arrow(c, 88, 8, 94, 8, NAVY, 1.4, 4)
    c.setStrokeColor(TEAL); c.setLineWidth(2)
    p = c.beginPath(); p.moveTo(14, 12); p.curveTo(40, 12, 54, 30, 88, 52); c.drawPath(p, fill=0, stroke=1)
    c.setStrokeColor(ORANGE); c.setLineWidth(1.1); c.setDash(2, 2); c.line(54, 8, 54, 30); c.line(14, 30, 54, 30); c.setDash()
    c.setFillColor(ORANGE); c.circle(54, 30, 2.4, fill=1, stroke=0)

@icon("atom", "modern-physics", "nuclear", "generic")
def i_atom(c):
    c.saveState(); c.translate(50, 32)
    stroke_style(c, 1.4); c.setStrokeColor(TEAL)
    for a in (0, 60, 120):
        c.saveState(); c.rotate(a); c.ellipse(-34, -12, 34, 12, fill=0, stroke=1)
        c.setFillColor(ORANGE); c.setStrokeColor(NAVY); c.setLineWidth(1); c.circle(34, 0, 3, fill=1, stroke=1); c.setStrokeColor(TEAL); c.setLineWidth(1.4); c.restoreState()
    c.setFillColor(ORANGE); c.setStrokeColor(NAVY); c.setLineWidth(1.2); c.circle(0, 0, 5.5, fill=1, stroke=1); c.restoreState()

# Per-question art from earlier sheets: every .py in ../art is imported
import os, sys, importlib.util
_ART = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art")
def load_art_dir(path=_ART):
    if not os.path.isdir(path): return
    if path not in sys.path: sys.path.insert(0, path)
    for fn in sorted(os.listdir(path)):
        if fn.endswith(".py") and not fn.startswith("_"):
            spec = importlib.util.spec_from_file_location("art_" + fn[:-3], os.path.join(path, fn))
            mod = importlib.util.module_from_spec(spec)
            mod.__dict__.update({"icon": icon, "ICON_BOX": ICON_BOX, "DIAGRAM_BOX": DIAGRAM_BOX})
            spec.loader.exec_module(mod)
load_art_dir()

def get(name):
    return REGISTRY.get((name or "").lower().strip())

def box_of(name):
    return BOXES.get((name or "").lower().strip(), ICON_BOX)

def is_diagram(name):
    return box_of(name)[0] > ICON_BOX[0]

def draw_icon(c, name, x, y, w, h):
    fn = get(name) or REGISTRY["generic"]
    bw, bh = box_of(name) if get(name) else ICON_BOX
    s = min(w / float(bw), h / float(bh))
    c.saveState(); c.translate(x + (w - bw * s) / 2, y + (h - bh * s) / 2); c.scale(s, s)
    fn(c); c.restoreState()
