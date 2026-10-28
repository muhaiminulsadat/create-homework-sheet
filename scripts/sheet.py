"""Page engine for the homework-sheet skill: turns a spec dict into a finished A4 PDF.

Spec (JSON) fields
  title            "Friction Homework Practice"
  subtitle         "HSC Physics 1st Paper | Newtonian Mechanics"
  copy_label       ""                           (footer label; empty = hidden, the default)
  footer_note      "Draw a free-body diagram first, then solve."
  banner_icon      block | atom | wave | flask   (right side of the page-1 banner)
  formula_title    "Quick Formula Box"
  formulas         [{"label": "Static friction", "expr": "f_{s,max} = μ_{s} × R"}, {"expr": "Use g = 9.8 m/s² where needed."}]
  questions        [{"text": "...", "tag": "BUET'11-12", "difficulty": "Easy|Medium|Hard|null", "icon": "plane"}]
"""
import math, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from drawkit import *
import icons

W, H = A4
MX = 34
CW = W - 2 * MX

DIFF = {"easy": (GREEN, white, "EASY"), "medium": (ORANGE, NAVY, "MEDIUM"), "hard": (RED, white, "HARD")}

# card typography / geometry (do not change: this is the approved design)
SZ, LD = 12, 16.5
ILLW = 138
TXW = CW - 46 - ILLW - 28
GAP = 12
CARD_CAP = 205
BADGE_H = 17 + 12          # badge row + spacing below
BOTTOM = 56                # lowest y a card may reach
PAGE1_CARDS, NEXT_CARDS = 8, 8      # space decides; compact cards, no working-space rows
SMALL_ICONS = ["atom", "incline", "gear"]   # continuation-header glyphs, cycled from page 2

# ------------------------------------------------------------------ text prep
_SUP = {"2": "²", "3": "³", "-1": "⁻¹"}

def clean_text(s, strip=True):
    """Light, safe normalisation of plain-text questions (never rewords); $maths$ is left untouched."""
    if "$" in s:
        return "".join(p if p.startswith("$") else clean_text(p, False) for p in MATH_RE.split(s.strip()))
    import re
    if strip: s = s.strip()
    for k, v in _SUP.items():
        rep = v if all(font_has(ch) for ch in v) else None
        if rep: s = re.sub(r"\^" + re.escape(k) + r"(?![0-9])", rep, s)
    s = re.sub(r"(?<=[A-Za-z])_([0-9])(?![0-9A-Za-z])", lambda m: chr(0x2080 + int(m.group(1))) if font_has(chr(0x2080 + int(m.group(1)))) else m.group(0), s)
    return s

DIAG_W = 218            # right-hand column width for a full diagram
DIAG_H = 143            # max drawn height of a diagram

def text_width(diagram):
    return CW - 46 - (DIAG_W if diagram else ILLW) - 28

TXT_ASC, TXT_DESC = 9.5, 3.0     # plain-text line extents at 12 pt

def seg_w(seg):
    return pdfmetrics.stringWidth(seg[1], "Body", SZ) if seg[0] == "t" else math_width(seg[1], SZ)

def rich_width(text):
    return sum(seg_w(sg) for sg in _segs(text))

def _segs(text):
    out = []
    for part in MATH_RE.split(text):
        if not part: continue
        out.append(("m", part) if part.startswith("$") else ("t", part))
    return out

def wrap_rich(text, width):
    """Greedy word wrap; $maths$ is kept whole. -> list of lines, each a list of ('t'|'m', str) segments."""
    if "$" not in text:
        return [[("t", ln)] for ln in (simpleSplit(text, "Body", SZ, width) or [""])]
    lines, cur, cw = [], [], 0
    for kind, body in _segs(text):
        for tok in ([body] if kind == "m" else re.findall(r"\S+\s*|\s+", body)):
            sg = (kind, tok); w = seg_w(sg)
            if cur and cw + w > width + 0.01 and (kind == "m" or tok.strip()):
                # trailing space on the previous token doesn't count
                lines.append(cur); cur, cw = [], 0
                if kind == "t": sg = ("t", tok.lstrip()); w = seg_w(sg)
            cur.append(sg); cw += w
    if cur: lines.append(cur)
    return lines or [[("t", "")]]

def line_ext(line):
    asc, desc = TXT_ASC, TXT_DESC
    for kind, body in line:
        if kind == "m":
            _, _, _, a, d = math_obj(body, SZ); asc, desc = max(asc, a), max(desc, d)
    return asc, desc

def line_width(line):
    return sum(seg_w(sg) for sg in line)

def draw_line(c, x, y, line, col=None):
    col = col or NAVY
    for kind, body in line:
        if kind == "t":
            c.setFillColor(col); c.setFont("Body", SZ); c.drawString(x, y, body)
        else:
            draw_math(c, x, y, body, SZ, col)
        x += seg_w((kind, body))

def pitch(prev_desc, asc, base):
    return max(base, prev_desc + asc + 3)

def lines_of(text, diagram=False):
    out = []
    for para in text.split("\n"):
        out.extend(simpleSplit(para, "Body", SZ, text_width(diagram)) or [""])
    return out

OPT_RE = __import__("re").compile(r"^\(?([A-Da-d])[\).]\s+(.*)$")
OPT_IND, OPT_LABW, OPT_LD, OPT_GAP = 12, 20, 19, 7

def split_question(text, diagram=False):
    """Split into stem lines + MCQ options (trailing lines like 'A) ...').
    Returns (stem, opts, rows, height). stem = [(line, baseline_drop)], opts = (items, two_col) with
    items = [(letter, lines, row_pitch)], where row_pitch is the baseline step to the next row."""
    paras = text.split("\n"); opts = []
    while paras and OPT_RE.match(paras[-1].strip()):
        m = OPT_RE.match(paras.pop().strip()); opts.insert(0, (m.group(1).upper(), m.group(2)))
    tw = text_width(diagram)
    lines = []
    for para in paras:
        lines.extend(wrap_rich(para, tw))
    stem, h = [], 0
    for i, ln in enumerate(lines):
        asc, desc = line_ext(ln)
        drop = max(LD, asc + 3) if i == 0 else pitch(line_ext(lines[i - 1])[1], asc, LD)
        stem.append((ln, drop)); h += drop
    if not opts:
        return stem, [], 0, h
    two_col = all(rich_width(t) <= (tw - OPT_IND) / 2 - OPT_LABW - 8 for _, t in opts)
    q_opts = [(l, wrap_rich(t, tw - OPT_IND - OPT_LABW) if not two_col else [[sg for sg in _segs(t)] or [("t", "")]]) for l, t in opts]
    items = []
    for l, ls in q_opts:
        ext = [line_ext(x) for x in ls]
        step = max(OPT_LD, max(a for a, _ in ext) + max(d for _, d in ext) + 3) if len(ls) == 1 else None
        items.append([l, ls, step])
    if two_col:   # both options of a row share one pitch
        for r in range(0, len(items), 2):
            st = max(it[2] for it in items[r:r + 2])
            for it in items[r:r + 2]: it[2] = st
        rows_h = sum(items[r][2] for r in range(0, len(items), 2))
    else:         # wrapped options may take several lines each
        rows_h = 0
        for it in items:
            ls = it[1]; ext = [line_ext(x) for x in ls]
            tot = OPT_LD + sum(pitch(ext[j - 1][1], ext[j][0], LD) for j in range(1, len(ls))) if len(ls) > 1 else it[2]
            it[2] = tot; rows_h += tot
    return stem, (items, two_col), len(items), h + OPT_GAP + rows_h + (4 if line_ext(lines[-1])[1] > 6 else 0)

# ------------------------------------------------------------------ page chrome
def banner_art(c, kind, x, y):
    """Decorative art for the page-1 banner; (x, y) = bottom-left of a 112 x 40 area."""
    c.saveState(); c.translate(x, y)
    if kind == "atom":
        atom_symbol(c, 56, 20, 2.0, HILITE, 1.2)
    elif kind == "wave":
        c.setStrokeColor(HILITE); c.setLineWidth(2)
        p = c.beginPath(); p.moveTo(0, 20)
        for i in range(1, 113): p.lineTo(i, 20 + 12 * math.sin(i / 112.0 * 4 * math.pi))
        c.drawPath(p, fill=0, stroke=1)
    elif kind == "flask":
        c.setStrokeColor(white); c.setFillColor(TEAL); c.setLineWidth(1.3)
        p = c.beginPath(); p.moveTo(48, 38); p.lineTo(48, 26); p.lineTo(34, 2); p.lineTo(78, 2); p.lineTo(64, 26); p.lineTo(64, 38)
        c.drawPath(p, fill=0, stroke=1)
        p = c.beginPath(); p.moveTo(40, 14); p.lineTo(72, 14); p.lineTo(78, 2); p.lineTo(34, 2); p.close(); c.drawPath(p, fill=1, stroke=0)
        arrow(c, 88, 14, 110, 14, ORANGE, 2.2, 5.5)
    else:  # block on a surface with an orange push arrow (mechanics default)
        c.setStrokeColor(HexColor("#7FB7C4")); c.setLineWidth(1.4); c.line(0, 0, 112, 0)
        c.setStrokeColor(white); c.setFillColor(TEAL); c.setLineWidth(1.2); c.rect(44, 0, 34, 24, fill=1, stroke=1)
        arrow(c, 80, 12, 108, 12, ORANGE, 2.4, 6)
    c.restoreState()

def head_first(c, spec):
    top = H - 28; hh = 74
    c.setFillColor(NAVY); c.roundRect(MX, top - hh, CW, hh, 10, fill=1, stroke=0)
    fs = 24
    while fs > 16 and pdfmetrics.stringWidth(spec["title"], "Head", fs) > CW - 20 - 150: fs -= 0.5   # keep clear of the art
    c.setFillColor(white); c.setFont("Head", fs); c.drawString(MX + 20, top - 38, spec["title"])
    c.setFont("Body", 11); c.setFillColor(SOFT); c.drawString(MX + 20, top - 58, spec["subtitle"])
    banner_art(c, spec.get("banner_icon", "block"), W - MX - 138, top - 50)
    return top - hh

def info_strip(c, y):
    x = MX + 10; ty = y - 16
    for nm, ln in [("Name", 150), ("Class", 56), ("Date", 66)]:
        c.setFillColor(NAVY); c.setFont("Body", 10.5); c.drawString(x, ty, nm); x += pdfmetrics.stringWidth(nm, "Body", 10.5) + 5
        c.setStrokeColor(GREY); c.setLineWidth(0.6); c.line(x, ty - 1.5, x + ln, ty - 1.5); x += ln + 18
    c.setFillColor(NAVY); c.drawString(x, ty, "Score"); x += pdfmetrics.stringWidth("Score", "Body", 10.5) + 5
    c.line(x, ty - 1.5, x + 34, ty - 1.5); c.drawString(x + 38, ty, "/10")
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(MX, y - 26, W - MX, y - 26)
    return y - 26

def ROW(k):
    return 16 * k + (1 if k >= 2 else 0)

def formula_geometry(spec):
    n = len(spec.get("formulas") or [])
    if n == 0: return 0, 0, 0
    left = n // 2; right = n - left
    rows = max(left, right, 3)
    return 74 + 16.5 * (rows - 3), left, right

def formula_box(c, y, spec):
    h, left, right = formula_geometry(spec)
    if not h: return y
    items = spec["formulas"]
    c.setFillColor(TEAL); c.roundRect(MX, y - h, CW, h, 9, fill=1, stroke=0)
    atom_symbol(c, MX + 24, y - 21, 1.0, white, 1.0)
    c.setFillColor(white); c.setFont("Head", 11.5); c.drawString(MX + 44, y - 25, spec.get("formula_title", "Quick Formula Box"))
    def row(it, x, ry):
        segs = []
        if it.get("label"): segs.append((it["label"] + ":  ", "b"))
        segs += parse_rich(it.get("expr", ""))
        rich(c, x, ry, segs, 9.8)
    bottom = y - h + 14                       # baseline of the lowest row
    lcol, rcol = items[:left], items[left:]
    for k, it in enumerate(reversed(lcol)): row(it, MX + 24, bottom + ROW(k))
    x2 = MX + CW * 0.58
    for k, it in enumerate(reversed(rcol)): row(it, x2, bottom + ROW(k))
    return y - h

def head_small(c, spec, page_no):
    top = H - 28; hh = 32
    c.setFillColor(NAVY); c.roundRect(MX, top - hh, CW, hh, 8, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Head", 12.5); c.drawString(MX + 14, top - 20, spec["title"])
    c.setFont("Body", 8.8); c.setFillColor(SOFT); c.drawRightString(W - MX - 44, top - 19.6, spec["subtitle"])
    sym = SMALL_ICONS[(page_no - 2) % len(SMALL_ICONS)]
    if sym == "atom": atom_symbol(c, W - MX - 22, top - 16, 1.0, HILITE, 1.0)
    elif sym == "gear": gear_symbol(c, W - MX - 22, top - 16, 1.2, HILITE)
    else: incline_symbol(c, W - MX - 23, top - 16.5, 1.0, HILITE)
    return top - hh

def badge_row(c, y, diff, cont=False):
    col, tcol, txt = DIFF[diff.lower()]
    bw = pdfmetrics.stringWidth(txt, "Head", 9.5) + 26; h = 17
    c.setStrokeColor(col); c.setLineWidth(1); c.line(MX + bw / 2, y - h / 2, W - MX, y - h / 2)
    c.setFillColor(col); c.setStrokeColor(NAVY); c.setLineWidth(1); c.roundRect(MX, y - h, bw, h, h / 2, fill=1, stroke=1)
    c.setFillColor(tcol); c.setFont("Head", 9.5); c.drawCentredString(MX + bw / 2, y - 12, txt)
    if cont:
        c.setFillColor(GREY); c.setFont("Body", 8.2); c.drawString(MX + bw + 10, y - h / 2 - 3, "continued")
    return y - h

def footer(c, spec, n, total):
    c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(MX, 44, W - MX, 44)
    atom_symbol(c, MX + 8, 29, 0.85, TEAL, 0.9)
    c.setFillColor(NAVY); c.setFont("BodyB", 8.8); c.drawString(MX + 24, 26.5, spec.get("footer_note", "Draw a free-body diagram first, then solve."))
    if spec.get("copy_label", ""):
        c.setFillColor(GREY); c.setFont("Body", 8); c.drawCentredString(W / 2 + 70, 26.5, spec.get("copy_label", ""))
    c.setFillColor(NAVY); c.setFont("BodyB", 9); c.drawRightString(W - MX, 26.5, f"Page {n} of {total}")

# ------------------------------------------------------------------ cards
def card(c, q, num, ytop, h):
    x = MX
    c.setFillColor(PALE); c.setStrokeColor(LINE); c.setLineWidth(0.8); c.roundRect(x, ytop - h, CW, h, 10, fill=1, stroke=1)
    c.setFillColor(NAVY); c.circle(x + 24, ytop - 25, 11, fill=1, stroke=0)
    c.setFillColor(white); c.setFont("Head", 11.5); c.drawCentredString(x + 24, ytop - 29, str(num))
    c.setFillColor(NAVY); c.setFont("Body", SZ)
    ty = ytop - 28 - (q["_stem"][0][1] - LD if q["_stem"] else 0)
    for i, (ln, drop) in enumerate(q["_stem"]):
        if i: ty -= drop
        draw_line(c, x + 46, ty, ln)
    if q["_opts"]:
        items, two_col = q["_opts"]
        tw = text_width(q["_diagram"]); colw = (tw - OPT_IND) / 2
        ext = line_ext(items[0][1][0])
        ty -= max(LD + 5, (line_ext(q["_stem"][-1][0])[1] if q["_stem"] else 3) + ext[0] + 8)
        for k, (l, ls, st) in enumerate(items):
            if two_col:
                row_top = ty - sum(items[r][2] for r in range(0, k - (k % 2), 2))
                ox = x + 46 + OPT_IND + (k % 2) * colw; oy = row_top
            else:
                ox = x + 46 + OPT_IND; oy = ty; ty -= st
            c.setFillColor(TEAL); c.setFont("BodyB", SZ); c.drawString(ox, oy, l + ")")
            for j, ln in enumerate(ls):
                yy = oy - j * LD if len(ls) > 1 else oy
                draw_line(c, ox + OPT_LABW, yy, ln)
    dg = q["_diagram"]
    ih = min(h - 18, DIAG_H if dg else 96)
    cw_ = DIAG_W if dg else ILLW
    icons.draw_icon(c, q.get("icon"), x + CW - cw_ - 14, ytop - 10 - ih, cw_, ih)
    if q.get("tag"):
        c.setFillColor(GREY); c.setFont("Body", 8.2); c.drawRightString(x + CW - 18, ytop - h + 8, "[" + q["tag"] + "]")

def card_min(q):
    """Compact card: just the question (no working-space row); tall enough for its text and art."""
    tg = 12 if q.get("tag") else 0
    if q["_diagram"]:
        return max(34 + q["_th"] + 6 + tg, 10 + DIAG_H + 12)
    return max(28 + q["_th"] + 8 + tg, 100)

def layout_page(c, items, ytop, ybot):
    """items: ('badge', diff, cont) | ('card', q, num). Cards share the leftover space."""
    cards = [it for it in items if it[0] == "card"]
    fixed = sum(BADGE_H for it in items if it[0] == "badge")
    total = ytop - ybot - fixed
    if cards:
        hs = [card_min(it[1]) for it in cards]
        g = GAP
    y = ytop; ci = 0
    for it in items:
        if it[0] == "badge":
            badge_row(c, y, it[1], it[2]); y -= BADGE_H
        else:
            h = hs[ci]; card(c, it[1], it[2], y, h); y -= h + g; ci += 1

# ------------------------------------------------------------------ pagination
def paginate(spec, qs):
    h_form = formula_geometry(spec)[0]
    top1 = H - 28 - 74 - 6 - 26 - 10 - (h_form + 14 if h_form else 0)
    top_n = H - 28 - 32 - 16
    use_diff = any(q.get("difficulty") for q in qs)
    pages, cur, cards_on, used = [], [], 0, 0
    last = None
    def cap(): return PAGE1_CARDS if not pages else NEXT_CARDS
    def avail(): return (top1 if not pages else top_n) - BOTTOM
    for i, q in enumerate(qs, 1):
        d = (q.get("difficulty") or "").lower() if use_diff else None
        need = card_min(q) + (GAP if cards_on else 0)
        new_group = use_diff and d != last
        must_break = cards_on >= cap() or used + need > avail() - (BADGE_H if (new_group or not cur) else 0)
        if new_group and cards_on >= 2: must_break = True
        if must_break and cur:
            pages.append(cur); cur, cards_on, used = [], 0, 0
            if use_diff and d == last and d:   # group continues onto the new page
                cur.append(("badge", d, True)); used += BADGE_H
        if use_diff and d and (new_group):
            cur.append(("badge", d, False)); used += BADGE_H
        elif use_diff and d and not cur:
            cur.append(("badge", d, True)); used += BADGE_H
        cur.append(("card", q, i)); cards_on += 1; used += card_min(q) + (GAP if cards_on > 1 else 0)
        last = d
    if cur: pages.append(cur)
    return pages, top1, top_n

# ------------------------------------------------------------------ build
def build(spec, out_path):
    register_fonts()
    qs = []
    for q in spec["questions"]:
        q = dict(q); q["text"] = clean_text(q["text"]); q["tag"] = (q.get("tag") or "").strip().strip("[]").strip()
        q["_diagram"] = icons.is_diagram(q.get("icon")); q["_stem"], q["_opts"], _r, q["_th"] = split_question(q["text"], q["_diagram"]); qs.append(q)
    for q in qs:
        if not icons.get(q.get("icon")): q.setdefault("_warn", f"icon '{q.get('icon')}' not found; using generic")
    pages, top1, top_n = paginate(spec, qs)
    c = canvas.Canvas(out_path, pagesize=A4)
    c.setTitle(spec["title"] + (" — " + spec["copy_label"].title() if spec.get("copy_label") else "")); c.setAuthor(spec.get("author", "HSC Physics"))
    c.setSubject(spec["subtitle"])
    for pn, items in enumerate(pages, 1):
        if pn == 1:
            y = head_first(c, spec) - 6
            y = info_strip(c, y) - 10
            y = formula_box(c, y, spec)
            y = y - 14 if spec.get("formulas") else y
        else:
            y = head_small(c, spec, pn) - 16
        layout_page(c, items, y, BOTTOM)
        footer(c, spec, pn, len(pages))
        c.showPage()
    c.save()
    return len(pages), [q["_warn"] for q in qs if q.get("_warn")]
