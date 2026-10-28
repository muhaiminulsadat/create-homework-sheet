"""CLI: python make_sheet.py spec.json out.pdf   ->  prints page count and any warnings.

Run from anywhere; this file puts its own folder on sys.path.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
import sheet

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: make_sheet.py spec.json out.pdf")
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    for k in ("title", "subtitle", "questions"):
        if not spec.get(k): raise SystemExit(f"spec is missing '{k}'")
    for i, q in enumerate(spec["questions"], 1):
        if not q.get("text", "").strip(): raise SystemExit(f"question {i} has no text")
    sheet.register_fonts()
    bn = sys.modules.get("bn_patch")
    bn_cmap = bn._font(False)[0].getBestCmap() if bn else {}
    def has_glyph(ch):
        if bn and bn._BN_RE.fullmatch(ch):
            return ord(ch) in bn_cmap
        return sheet.font_has(ch)
    missing = sorted({ch for q in spec["questions"] for ch in q["text"] if ord(ch) > 127 and not has_glyph(ch)})
    pages, warns = sheet.build(spec, sys.argv[2])
    print(f"OK  {sys.argv[2]}  pages={pages}  questions={len(spec['questions'])}")
    for w in warns: print("WARN", w)
    if missing: print("WARN glyphs missing from font (may print as boxes):", " ".join(missing))

if __name__ == "__main__":
    main()
