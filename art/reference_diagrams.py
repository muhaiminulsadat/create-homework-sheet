"""Reference FULL DIAGRAMS (150 x 100 box). They show the quality bar and the helper vocabulary for
diagram-type questions: force diagram on a slope, circuit diagram, ray diagram. Imitate, don't reuse blindly.
Variable names only (mg, N, f, R, V ...) -- never numbers or answers."""
import math
from drawkit import *

@icon("ref-incline-fbd", box=DIAGRAM_BOX)
def d_incline_fbd(c):
    th = math.radians(26)
    hatch(c, 8, 12, 142, 12, 7, 4.5, -1)
    stroke_style(c, 1.5); c.setFillColor(white)
    p = c.beginPath(); p.moveTo(10, 12); p.lineTo(140, 12); p.lineTo(140, 12 + 130 * math.tan(th)); p.close(); c.drawPath(p, fill=1, stroke=1)
    x0 = 78; y0 = 12 + (x0 - 10) * math.tan(th)
    c.saveState(); c.translate(x0, y0); c.rotate(26); block(c, -15, 0, 30, 19, TEAL, 2.5); c.restoreState()
    cx, cy = x0 - 9.5 * math.sin(th), y0 + 9.5 * math.cos(th)
    dot(c, cx, cy, 2, white)
    arrow(c, cx, cy, cx, cy - 30, NAVY, 1.8, 5.5); txt(c, cx + 4, cy - 31, "mg", 8.5, NAVY, "l")
    arrow(c, cx, cy, cx - 30 * math.sin(th), cy + 30 * math.cos(th), TEAL, 1.8, 5.5); txt(c, cx - 33 * math.sin(th) - 8, cy + 31 * math.cos(th), "N", 8.5, TEAL, "r")
    arrow(c, cx, cy, cx + 28 * math.cos(th), cy + 28 * math.sin(th), ORANGE, 1.8, 5.5); txt(c, cx + 30 * math.cos(th) + 2, cy + 28 * math.sin(th) + 2, "f", 8.5, ORANGE, "l")
    angle_arc(c, 10, 12, 24, 0, 26, "θ", ORANGE, 1.5, 9)

@icon("ref-circuit", box=DIAGRAM_BOX)
def d_circuit(c):
    stroke_style(c, 1.6)
    p = c.beginPath(); p.moveTo(24, 44); p.lineTo(24, 14); p.lineTo(126, 14); p.lineTo(126, 41); c.drawPath(p, fill=0, stroke=1)
    p = c.beginPath(); p.moveTo(24, 56); p.lineTo(24, 86); p.lineTo(52, 86); c.drawPath(p, fill=0, stroke=1)
    zigzag(c, 52, 86, 98, 86, 6, 6.5, 0.1, NAVY, 1.6)
    p = c.beginPath(); p.moveTo(98, 86); p.lineTo(126, 86); p.lineTo(126, 59); c.drawPath(p, fill=0, stroke=1)
    c.setLineWidth(2.6); c.line(15, 56, 33, 56); c.setLineWidth(2.6); c.line(19, 44, 29, 44)
    txt(c, 40, 59, "+", 9, ORANGE, "l"); txt(c, 40, 41, "−", 9, TEAL, "l"); txt(c, 12, 49, "V", 9, NAVY, "r")
    stroke_style(c, 1.6); c.setFillColor(white); c.circle(126, 50, 9, fill=1, stroke=1); txt(c, 126, 47, "A", 9, NAVY)
    txt(c, 75, 96, "R", 9, NAVY)
    arrow(c, 48, 6, 96, 6, ORANGE, 1.3, 4.2); txt(c, 72, 17, "I", 8.5, ORANGE)

@icon("ref-lens-rays", box=DIAGRAM_BOX)
def d_lens_rays(c):
    ay, lx = 50, 75
    dashed(c, 6, ay, 144, ay, GREY, 1, 3, 2.5)
    stroke_style(c, 1.6); c.setFillColor(TEAL_L)
    p = c.beginPath(); p.moveTo(lx, 14); p.curveTo(lx + 11, 32, lx + 11, 68, lx, 86); p.curveTo(lx - 11, 68, lx - 11, 32, lx, 14); p.close(); c.drawPath(p, fill=1, stroke=1)
    ox, tipy = 18, 66
    c.setStrokeColor(ORANGE); c.setLineWidth(1.5)
    c.line(ox, tipy, lx, tipy); c.line(lx, tipy, 123, 36.6)          # parallel ray then through F'
    c.line(ox, tipy, 123, 36.6)                                       # ray through the optical centre
    arrow(c, ox, ay, ox, tipy, NAVY, 2, 5.5); txt(c, ox - 4, tipy - 2, "O", 8.5, NAVY, "r")
    arrow(c, 123, ay, 123, 36.6, TEAL, 2, 5.5); txt(c, 127, 38, "I", 8.5, TEAL, "l")
    for fx, nm in ((49, "F"), (101, "F′")):
        dot(c, fx, ay, 2.2, NAVY); txt(c, fx, ay - 11, nm, 8, NAVY)
