"""HSC Higher Mathematics - Integration: one graph icon per MCQ (100 x 64 box, y up)."""
import math
from drawkit import *


def _axes(c, ox=14, oy=12, xr=88, yt=58, xl=None, yb=None):
    stroke_style(c, 1.0)
    c.setStrokeColor(GREY)
    c.line(xl if xl is not None else 6, oy, xr, oy)
    c.line(ox, yb if yb is not None else 4, ox, yt)
    arrow(c, xr - 3, oy, xr, oy, GREY, 1.0, 3.2)
    arrow(c, ox, yt - 3, ox, yt, GREY, 1.0, 3.2)


def _curve(c, f, x0, x1, tx, ty, n=60, col=NAVY, lw=1.6, ymin=0, ymax=64):
    """Plot f over [x0, x1] mapped through tx, ty (clipped to the box)."""
    stroke_style(c, lw); c.setStrokeColor(col)
    p = c.beginPath(); started = False
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        y = ty(f(x))
        if y > ymax or y < ymin:
            continue
        if not started:
            p.moveTo(tx(x), y); started = True
        else:
            p.lineTo(tx(x), y)
    c.drawPath(p, fill=0, stroke=1)


def _area(c, f, a, b, tx, ty, base, fill=TEAL_L, n=40):
    c.setFillColor(fill); c.setStrokeColor(fill); c.setLineWidth(0.1)
    p = c.beginPath(); p.moveTo(tx(a), base)
    for i in range(n + 1):
        x = a + (b - a) * i / n
        p.lineTo(tx(x), ty(f(x)))
    p.lineTo(tx(b), base); p.close(); c.drawPath(p, fill=1, stroke=0)


def _plot(c, f, x0, x1, sx, sy, ox=14, oy=12, shade=None, **kw):
    tx = lambda x: ox + sx * x
    ty = lambda y: oy + sy * y
    if shade:
        _area(c, f, shade[0], shade[1], tx, ty, oy)
    _axes(c, ox, oy)
    _curve(c, f, x0, x1, tx, ty, **kw)
    return tx, ty


@icon("hmi-q1")
def q1(c):
    # y = x^3
    tx, ty = _plot(c, lambda x: x ** 3, 0, 2.0, 30, 6.2, shade=(0, 1.6))
    _curve(c, lambda x: x ** 3, 0, 2.0, tx, ty, col=NAVY, lw=1.8)
    mlab(c, 22, 52, r"$y=x^3$", TEAL, 8, "l")
    dashed(c, tx(1.6), 12, tx(1.6), ty(1.6 ** 3), GREY, 0.9, 2, 2)


@icon("hmi-q2")
def q2(c):
    # y = 1/x
    tx, ty = _plot(c, lambda x: 1 / x, 0.28, 2.8, 28, 10, shade=(1, 2.4))
    _curve(c, lambda x: 1 / x, 0.22, 2.8, tx, ty, col=NAVY, lw=1.8, ymax=58)
    mlab(c, 56, 42, r"$y=\dfrac{1}{x}$", TEAL, 8, "l")


@icon("hmi-q3")
def q3(c):
    # y = e^{2x}
    tx, ty = _plot(c, lambda x: math.exp(2 * x), 0, 1.5, 38, 2.0, shade=(0, 1.2))
    _curve(c, lambda x: math.exp(2 * x), -0.3, 1.5, tx, ty, col=NAVY, lw=1.8, ymax=58)
    mlab(c, 20, 52, r"$y=e^{2x}$", TEAL, 8, "l")


@icon("hmi-q4")
def q4(c):
    # y = sin 3x
    ox, oy = 8, 34
    stroke_style(c, 1.0); c.setStrokeColor(GREY)
    c.line(ox, oy, 92, oy); c.line(ox, 6, ox, 60)
    arrow(c, 89, oy, 92, oy, GREY, 1.0, 3.2); arrow(c, ox, 57, ox, 60, GREY, 1.0, 3.2)
    f = lambda x: 20 * math.sin(3 * x)
    tx = lambda x: ox + 26 * x
    stroke_style(c, 1.8); c.setStrokeColor(NAVY)
    p = c.beginPath(); p.moveTo(tx(0), oy)
    for i in range(1, 81):
        x = 3.1 * i / 80
        p.lineTo(tx(x), oy + f(x))
    c.drawPath(p, fill=0, stroke=1)
    # shaded first lobe
    c.setFillColor(TEAL_L)
    q = c.beginPath(); q.moveTo(tx(0), oy)
    for i in range(0, 41):
        x = (math.pi / 3) * i / 40
        q.lineTo(tx(x), oy + f(x))
    q.close(); c.drawPath(q, fill=1, stroke=0)
    stroke_style(c, 1.8); c.setStrokeColor(NAVY)
    p = c.beginPath(); p.moveTo(tx(0), oy)
    for i in range(1, 81):
        x = 3.1 * i / 80
        p.lineTo(tx(x), oy + f(x))
    c.drawPath(p, fill=0, stroke=1)
    mlab(c, 48, 56, r"$y=\sin 3x$", TEAL, 7.5, "c")


@icon("hmi-q5")
def q5(c):
    # y = x sqrt(x^2+1)
    f = lambda x: x * math.sqrt(x * x + 1)
    tx, ty = _plot(c, f, 0, 2.0, 30, 5.4, shade=(0, 1.5))
    _curve(c, f, 0, 2.0, tx, ty, col=NAVY, lw=1.8, ymax=58)
    mlab(c, 22, 54, r"$y=x\sqrt{x^2+1}$", TEAL, 7.5, "l")


@icon("hmi-q6")
def q6(c):
    # y = 2x/(x^2+4)
    f = lambda x: 2 * x / (x * x + 4)
    tx, ty = _plot(c, f, 0, 4.2, 18, 36, shade=(0, 2.5))
    _curve(c, f, 0, 4.2, tx, ty, col=NAVY, lw=1.8)
    mlab(c, 40, 47, r"$y=\dfrac{2x}{x^2+4}$", TEAL, 7.5, "l")


@icon("hmi-q7")
def q7(c):
    # y = x e^x
    f = lambda x: x * math.exp(x)
    tx, ty = _plot(c, f, 0, 2.1, 30, 4.4, shade=(0, 1.5))
    _curve(c, f, 0, 2.1, tx, ty, col=NAVY, lw=1.8, ymax=58)
    mlab(c, 22, 54, r"$y=xe^{x}$", TEAL, 8, "l")


@icon("hmi-q8")
def q8(c):
    # y = 1/(1+x^2), bell curve about the y-axis
    ox, oy = 50, 10
    stroke_style(c, 1.0); c.setStrokeColor(GREY)
    c.line(6, oy, 94, oy); c.line(ox, 4, ox, 60)
    arrow(c, 91, oy, 94, oy, GREY, 1.0, 3.2); arrow(c, ox, 57, ox, 60, GREY, 1.0, 3.2)
    f = lambda x: 1 / (1 + x * x)
    tx = lambda x: ox + 22 * x
    ty = lambda y: oy + 40 * y
    c.setFillColor(TEAL_L)
    p = c.beginPath(); p.moveTo(tx(-1.5), oy)
    for i in range(61):
        x = -1.5 + 3 * i / 60
        p.lineTo(tx(x), ty(f(x)))
    p.lineTo(tx(1.5), oy); p.close(); c.drawPath(p, fill=1, stroke=0)
    stroke_style(c, 1.8); c.setStrokeColor(NAVY)
    p = c.beginPath(); p.moveTo(tx(-2.0), ty(f(-2.0)))
    for i in range(1, 81):
        x = -2.0 + 4 * i / 80
        p.lineTo(tx(x), ty(f(x)))
    c.drawPath(p, fill=0, stroke=1)
    mlab(c, 2, 49, r"$y=\dfrac{1}{1+x^2}$", TEAL, 7, "l")


@icon("hmi-q9")
def q9(c):
    # y = 3x^2 from 0 to 1 (shaded)
    f = lambda x: 3 * x * x
    tx, ty = _plot(c, f, 0, 1.25, 52, 13, shade=(0, 1.0))
    _curve(c, f, 0, 1.25, tx, ty, col=NAVY, lw=1.8, ymax=58)
    dashed(c, tx(1), 12, tx(1), ty(3), GREY, 0.9, 2, 2)
    mlab(c, tx(1), 4, r"$1$", NAVY, 7.5)
    mlab(c, tx(0) - 3, 4, r"$0$", NAVY, 7.5)
    mlab(c, 20, 52, r"$y=3x^2$", TEAL, 8, "l")


@icon("hmi-q10")
def q10(c):
    # y = 2x, triangle area from 0 to a
    tx, ty = _plot(c, lambda x: 2 * x, 0, 2.3, 28, 12, shade=(0, 1.8))
    _curve(c, lambda x: 2 * x, 0, 2.3, tx, ty, col=NAVY, lw=1.8, ymax=58)
    dashed(c, tx(1.8), 12, tx(1.8), ty(3.6), GREY, 0.9, 2, 2)
    mlab(c, tx(1.8), 4, r"$a$", ORANGE, 8)
    mlab(c, 20, 52, r"$y=2x$", TEAL, 8, "l")
    lab(c, tx(0.95), 20, "Area", NAVY, 6.8, "l")
