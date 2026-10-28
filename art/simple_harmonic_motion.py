"""Purpose-drawn illustrations for the SHM homework sheet (100 x 64 units)."""
import math
from drawkit import *


def _axis(c, x0=10, y0=30, x1=92):
    arrow(c, x0, y0, x1, y0, NAVY, 1.2, 3.5)
    dot(c, (x0 + x1) / 2, y0, 1.5)


def _pendulum(c, px, py, length, degrees, fill=TEAL):
    a = math.radians(degrees)
    bx, by = px + length * math.sin(a), py - length * math.cos(a)
    stroke_style(c, 1.3); c.line(px, py, bx, by)
    dot(c, px, py, 2)
    ball(c, bx, by, 6, fill)
    return bx, by


@icon("shm-q1")
def q1(c):
    arrow(c, 10, 31, 94, 31, NAVY, 1.2, 3)
    arrow(c, 12, 8, 12, 57, NAVY, 1.2, 3)
    p = c.beginPath()
    for i in range(81):
        x = 14 + i * 0.95
        y = 31 + 19 * math.cos(i * 2 * math.pi / 55)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    c.setStrokeColor(TEAL); c.setLineWidth(2); c.drawPath(p, stroke=1)
    mlab(c, 7, 54, r"$x$", NAVY, 8)
    mlab(c, 91, 23, r"$t$", NAVY, 8)
    mlab(c, 26, 53, r"$A$", ORANGE, 8)


@icon("shm-q2")
def q2(c):
    hatch(c, 7, 10, 7, 56, 6, 4, 1)
    stroke_style(c, 1.5); c.line(7, 10, 7, 56)
    floor(c, 8, 96, 13, False)
    zigzag(c, 8, 28, 59, 28, 8, 5, 0.12, NAVY, 1.5)
    block(c, 59, 14, 26, 28, TEAL, 2)
    mlab(c, 72, 25, r"$m$", white, 9)
    mlab(c, 34, 43, r"$k$", NAVY, 8)
    dashed(c, 49, 16, 49, 48, GREY)
    dim_arrow(c, 49, 51, 59, 51, ORANGE, 1.0, 2.5)
    mlab(c, 56, 56, r"$5\ \mathrm{cm}$", ORANGE, 6.5)


@icon("shm-q3")
def q3(c):
    hatch(c, 25, 59, 75, 59, 6, 3, 1)
    stroke_style(c, 1.5); c.line(25, 59, 75, 59)
    dashed(c, 50, 57, 50, 10, GREY)
    _pendulum(c, 50, 57, 42, 20)
    angle_arc(c, 50, 57, 13, 250, 270, None)
    mlab(c, 69, 34, r"$L$", ORANGE, 8)
    mlab(c, 21, 10, r"$g$", NAVY, 8)


@icon("shm-q4")
def q4(c):
    _axis(c, 8, 26, 94)
    for x in (16, 50, 67, 84):
        c.setStrokeColor(GREY); c.setLineWidth(1); c.line(x, 22, x, 30)
    ball(c, 50, 26, 5, TEAL)
    arrow(c, 58, 43, 77, 43, ORANGE, 1.8, 4)
    mlab(c, 50, 8, r"$0$", NAVY, 8)
    mlab(c, 67, 8, r"$A/2$", ORANGE, 8)
    mlab(c, 84, 8, r"$A$", NAVY, 8)


@icon("shm-q5")
def q5(c):
    _axis(c, 8, 26, 94)
    for x in (16, 50, 70, 84):
        c.setStrokeColor(GREY); c.setLineWidth(1); c.line(x, 22, x, 30)
    ball(c, 70, 26, 6, TEAL)
    arrow(c, 70, 44, 84, 44, ORANGE, 1.8, 4)
    mlab(c, 78, 50, r"$v$", ORANGE, 8)
    mlab(c, 50, 8, r"$0$", NAVY, 8)
    mlab(c, 70, 8, r"$x$", NAVY, 8)
    mlab(c, 85, 8, r"$A$", NAVY, 8)


@icon("shm-q6")
def q6(c):
    arrow(c, 8, 31, 94, 31, NAVY, 1.2, 3)
    arrow(c, 50, 6, 50, 58, NAVY, 1.2, 3)
    c.setStrokeColor(TEAL); c.setLineWidth(2); c.line(17, 53, 83, 10)
    dot(c, 50, 31, 2, ORANGE)
    mlab(c, 92, 22, r"$x$", NAVY, 8)
    mlab(c, 40, 54, r"$a$", NAVY, 8)


@icon("shm-q7")
def q7(c):
    hatch(c, 7, 9, 7, 55, 6, 4, 1)
    stroke_style(c, 1.5); c.line(7, 9, 7, 55)
    floor(c, 8, 96, 13, False)
    zigzag(c, 8, 29, 59, 29, 8, 5, 0.12, NAVY, 1.5)
    block(c, 59, 15, 25, 28, TEAL, 2)
    mlab(c, 71, 26, r"$m$", white, 9)
    mlab(c, 35, 45, r"$k$", NAVY, 8)
    dashed(c, 48, 12, 48, 51, GREY)
    dim_arrow(c, 48, 52, 59, 52, ORANGE, 1.2, 3)
    mlab(c, 54, 56, r"$A$", ORANGE, 7.5)


@icon("shm-q8")
def q8(c):
    for px, color in ((26, TEAL), (74, ORANGE)):
        stroke_style(c, 1.2); c.line(px - 15, 58, px + 15, 58)
        hatch(c, px - 15, 58, px + 15, 58, 6, 3, 1)
        _pendulum(c, px, 56, 33, 18, color)
    mlab(c, 25, 8, r"$g_E$", TEAL, 8)
    mlab(c, 74, 8, r"$g_M$", ORANGE, 8)


@icon("shm-q9")
def q9(c):
    hatch(c, 6, 7, 6, 57, 6, 4, 1)
    stroke_style(c, 1.5); c.line(6, 7, 6, 57)
    floor(c, 7, 96, 9, False)
    zigzag(c, 9, 23, 62, 23, 6, 3.8, 0.1, NAVY, 1.2)
    zigzag(c, 9, 40, 62, 40, 6, 3.8, 0.1, NAVY, 1.2)
    block(c, 62, 12, 25, 39, TEAL, 2)
    mlab(c, 74, 28, r"$m$", white, 9)
    mlab(c, 35, 51, r"$k$", ORANGE, 8)
    mlab(c, 35, 11, r"$k$", ORANGE, 8)


@icon("shm-q10")
def q10(c):
    for px, deg, color in ((28, 5, TEAL), (72, 10, ORANGE)):
        stroke_style(c, 1.2); c.line(px - 15, 59, px + 15, 59)
        hatch(c, px - 15, 59, px + 15, 59, 6, 3, 1)
        dashed(c, px, 57, px, 13, GREY)
        _pendulum(c, px, 57, 38, deg, color)
    mlab(c, 18, 7, r"$5^\circ$", TEAL, 8)
    mlab(c, 88, 7, r"$10^\circ$", ORANGE, 8)
