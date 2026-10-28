"""Bangla support for the sheet generator (does not touch the fixed design files).
Bengali runs are shaped with HarfBuzz (uharfbuzz) and drawn as vector outlines from Nirmala UI;
Latin runs / formulas keep the normal Segoe UI path. Import this BEFORE building: `import bn_patch`.
Also maps the sheet's few fixed English labels (Name, Class, Date, Score, Page n of N) to Bangla."""
import re
import uharfbuzz as hb
from fontTools.ttLib import TTCollection
from fontTools.pens.basePen import BasePen
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas as _cv

_TTC = "C:/Windows/Fonts/Nirmala.ttc"
_BN = r"[\u0964\u0965\u0980-\u09FF\u200c\u200d]"
_BN_RE = re.compile(r"(" + _BN + r"+(?:[ ]+" + _BN + r"+)*)")
_DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
_MAP = {"Name": "নাম", "Class": "শ্রেণি", "Date": "তারিখ", "Score": "প্রাপ্ত নম্বর", "/10": "/১০", "continued": "চলমান",
        "chain of 3 C": "৩ কার্বনের শিকল", "ethanol": "ইথানল", "bromine water": "ব্রোমিন পানি",
        "same molecular formula": "একই আণবিক সংকেত", "oxidant": "জারক", "heat": "তাপ"}

_fonts = {}
def _font(bold):
    if bold not in _fonts:
        col = TTCollection(_TTC); tt = col.fonts[1 if bold else 0]
        blob = hb.Blob.from_file_path(_TTC); face = hb.Face(blob, 1 if bold else 0)
        _fonts[bold] = (tt, hb.Font(face), tt["head"].unitsPerEm, tt.getGlyphOrder(), tt.getGlyphSet())
    return _fonts[bold]

_cache = {}
def _shape(s, bold):
    k = (s, bold)
    if k not in _cache:
        tt, hf, upem, order, gs = _font(bold)
        buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties(); hb.shape(hf, buf, {})
        _cache[k] = [(i.codepoint, p.x_advance, p.x_offset, p.y_offset) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]
    return _cache[k]

def _tr(s):
    if s in _MAP: return _MAP[s]
    m = re.fullmatch(r"Page (\d+) of (\d+)", s)
    if m: return f"পৃষ্ঠা {m.group(1).translate(_DIG)} / {m.group(2).translate(_DIG)}"
    return s

def _bold(fn): return fn in ("BodyB", "Head")

_orig_sw = pdfmetrics.stringWidth
def _sw(text, fontName, fontSize, *a, **k):
    text = _tr(text)
    if not _BN_RE.search(text): return _orig_sw(text, fontName, fontSize, *a, **k)
    w = 0.0
    for part in _BN_RE.split(text):
        if not part: continue
        if _BN_RE.fullmatch(part):
            upem = _font(_bold(fontName))[2]
            w += sum(g[1] for g in _shape(part, _bold(fontName))) * fontSize / upem
        else: w += _orig_sw(part, fontName, fontSize, *a, **k)
    return w
pdfmetrics.stringWidth = _sw

class _Pen(BasePen):
    def __init__(self, gs, path, sc, ox, oy):
        super().__init__(gs); self.p, self.sc, self.ox, self.oy = path, sc, ox, oy
    def _t(self, pt): return (self.ox + pt[0] * self.sc, self.oy + pt[1] * self.sc)
    def _moveTo(self, pt): self.p.moveTo(*self._t(pt))
    def _lineTo(self, pt): self.p.lineTo(*self._t(pt))
    def _curveToOne(self, a, b, c): self.p.curveTo(*self._t(a), *self._t(b), *self._t(c))
    def _closePath(self): self.p.close()

def _draw_bn(c, x, y, s, bold, size):
    tt, hf, upem, order, gs = _font(bold); sc = size / upem
    path = c.beginPath(); pen_x = 0.0
    for gid, adv, xo, yo in _shape(s, bold):
        gs[order[gid]].draw(_Pen(gs, path, sc, x + (pen_x + xo) * sc, y + yo * sc)); pen_x += adv
    c.drawPath(path, stroke=0, fill=1, fillMode=1)
    return pen_x * sc

def _draw(self, x, y, text, align):
    text = _tr(str(text)); fn, fs = self._fontname, self._fontsize
    if align == "l" and not _BN_RE.search(text): return _orig[align](self, x, y, text)
    if align == "c" and re.fullmatch(r"\d+", text) and fn == "Head" and False: pass
    w = _sw(text, fn, fs)
    if align == "c": x -= w / 2
    elif align == "r": x -= w
    if not _BN_RE.search(text):
        return _orig["l"](self, x, y, text)
    for part in _BN_RE.split(text):
        if not part: continue
        if _BN_RE.fullmatch(part): x += _draw_bn(self, x, y, part, _bold(fn), fs)
        else: _orig["l"](self, x, y, part); x += _orig_sw(part, fn, fs)

_orig = {"l": _cv.Canvas.drawString, "c": _cv.Canvas.drawCentredString, "r": _cv.Canvas.drawRightString}
_cv.Canvas.drawString = lambda self, x, y, t, *a, **k: _draw(self, x, y, t, "l")
_cv.Canvas.drawCentredString = lambda self, x, y, t, *a, **k: (
    _draw(self, x, y, t.translate(_DIG) if (isinstance(t, str) and t.isdigit() and self._fontname == "Head") else t, "c"))
_cv.Canvas.drawRightString = lambda self, x, y, t, *a, **k: _draw(self, x, y, t, "r")
