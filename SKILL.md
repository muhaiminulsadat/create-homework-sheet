---
name: create-homework-sheet
description: Create a print-ready A4 student homework sheet PDF from questions, using the established Friction Homework Practice design with an illustration or diagram for every question. Use for requests such as "homework sheet", "make the sheet", or "worksheet PDF". The user can supply just the questions.
---

# Create Homework Sheet

Produces one finished PDF per request. The design is the approved default; do not ask the user to describe or confirm layout, colours, fonts or icons. Explicit user changes take precedence. Resolve all bundled paths relative to this `SKILL.md`, so the skill works from any current directory. The Python scripts require a local execution environment; if one is unavailable, explain that the PDF cannot be generated in that chat.

## What the user gives you
Plain-text questions, usually pasted numbered. Optionally: chapter name, "Easy/Medium/Hard" headings, source tags in `[brackets]`, a title/subtitle override. Nothing else is required. Do not ask follow-up questions unless there is literally no question text.

## Steps

0. **Check for gaps first; ask only what you cannot infer.** Before building, scan the request. If an essential item below is missing and cannot be worked out from the questions, the folder path or the user's wording, ask once using the chat's available question mechanism; group related questions together. If everything is inferable, or the user said "just make it", continue. Never ask about design, layout, fonts, colours or icons.
   - **Chapter / paper** — not given, and the folder path and questions don't make it clear (or HSC 1st vs 2nd paper is uncertain). Offer your best guess first.
   - **Difficulty** — when questions have no Easy/Medium/Hard labels, use no badges and one flowing list unless the user requests grouping. Do not ask solely about this.
   - **Formula box** — not wanted (user preference): never ask and never add one. Include it only if the user explicitly asks for a formula box or supplies formulas.
   - **Unclear question text** — a question looks cut off, has a likely typo, a missing value or unit, or mentions a figure/diagram that is not provided. Quote the question number and the problem and ask how to proceed (print as written / user corrects it). Never silently fix or drop it.
   - **Source tags** — only if some questions have tags and others do not and it looks unintentional. Missing tags everywhere is normal: do not ask.
   - **Existing file** — the target PDF name already exists and the user did not say to replace it: keep both by adding a version suffix.
   After the answers arrive, continue without further questions.

1. **Parse the questions into a spec** (JSON, written to an available temporary directory outside the project when possible):
   - `text`: the question **exactly as written**. Never reword, shorten, fix, solve or add answers. Strip only the leading number ("1." / "Q1)") and wrapping quotation marks. Keep line breaks (e.g. sub-parts) as `\n`.
   - **Mathematical terms in ANY subject (maths, physics, chemistry, ICT...)**: the user's standing preference is LaTeX-quality typesetting wherever a mathematical term appears, not only in maths papers. Convert every equation, variable, symbol, Greek letter, vector, fraction, power/subscript, root, trig/log function, integral/sum/limit, and value-with-exponent-or-unit (e.g. `$9.8\ \mathrm{m/s^2}$`, `$F=ma$`, `$\mu_s$`, `$\vec{v}$`, `$\theta=30^\circ$`) to `$...$` LaTeX (see "Maths (LaTeX)" at the bottom), in the stem *and* each option, and typeset any symbol labels in art with `mlab`. Plain words and plain numbers without symbols stay as normal text. Subtitle uses the real subject, e.g. `"HSC Higher Mathematics | Integration"`, with a fitting footer note instead of the free-body-diagram line when it doesn't apply. For graphs of functions draw the curve (shade the area when limits are given) and never show the answer.
   - `tag`: trailing `[BUET'11-12]` / `(DU 15-16)` source tag, without brackets; `""` if none.
   - `difficulty`: `Easy` / `Medium` / `Hard` if the user grouped or labelled them. If they gave none, leave it `null` for **every** question (no badges are drawn). Only assign difficulty yourself if the user asks for grouping and gave no labels, and say so in the reply.
   - `icon`: the name of the art you draw for this question (see "Art for every question"). Do this after drawing it (step 2b), then put its name here.
   - Question order is kept as given; numbering is automatic.

2. **Fill the header fields** (infer, don't ask):
   - `title`: `"<Chapter> Homework Practice"`. Chapter comes from the user, else from the project folder path (e.g. `.../Newtonian Mechanics/Friction` -> "Friction"), else from the questions' topic.
   - `subtitle`: `"HSC Physics 1st Paper | <chapter group>"` or `"HSC Physics 2nd Paper | <chapter group>"`. Subject is HSC Physics unless the folder/user says otherwise.
     - 1st Paper chapters: Physical World & Measurement, Vectors, Dynamics, Newtonian Mechanics, Work Energy & Power, Gravitation & Gravity, Structural Properties of Matter, Periodic Motion, Waves, Ideal Gas & Kinetic Theory of Gases.
     - 2nd Paper chapters: Thermodynamics, Static Electricity, Current Electricity, Magnetic Effects of Current & Magnetism, Electromagnetic Induction & Alternating Current, Geometrical Optics, Physical Optics, Introduction to Modern Physics, Atomic Model & Nuclear Physics, Semiconductor & Electronics, Astronomy.
     - Use the chapter group as written in the folder path if it is one of those (e.g. "Newtonian Mechanics"); otherwise the chapter name.
   - `copy_label`: omit it (no "STUDENT COPY" text in the footer; user preference). `footer_note`: keep the default `"Draw a free-body diagram first, then solve."` for mechanics/problem-solving chapters; for chapters where a free-body diagram makes no sense (optics, circuits, modern physics...) use a fitting one-line study note such as `"Draw a labelled diagram first, then solve."`. When unsure, use that diagram line.
   - `banner_icon`: `block` (mechanics/force), `atom` (modern physics, electricity), `wave` (waves, sound, optics), `flask` (heat, gases, chemistry).
   - `formula_title`: omit.
   - `formulas`: omit entirely by default (no Quick Formula Box on the sheet; the script then skips the box). Only when the user explicitly asks for one: 3–6 items `{"label": "...", "expr": "..."}` or `{"expr": "..."}`, subscripts `_{...}`, superscripts `^{...}`, Unicode freely; no answers or worked values; double-check each formula.

2b. **Draw the art for every question** (see "Art for every question" below). Write reusable drawings to this skill's `art/<chapter-slug>.py` when the skill folder is writable. If it is read-only, make a writable working copy of the skill and generate from that copy. Preview each drawing, fix defects, then set each question's `icon` to its art name.

3. **Generate**:
   ```bash
   python "<skill-dir>/scripts/make_sheet.py" <spec.json> "<output.pdf>"
   ```
   - Needs Python with `reportlab` and `matplotlib`; install missing packages if the environment permits. The font loader uses Segoe UI on Windows and falls back to Arial or DejaVu where available. For Bangla sheets, use `make_sheet_bn.py`; it additionally needs `uharfbuzz`, `fonttools`, and Windows Nirmala UI.
   - Output goes in the user's project folder, or another user-specified output location, named `<Chapter>_Homework_Student.pdf` (e.g. `Friction_Homework_Student.pdf`); if that file exists, add `_v2` or the next free suffix unless replacement was requested.
   - The script prints page count and warnings. Fix every warning (missing art -> draw it (step 2b); missing glyph -> replace the character with a supported one only if it is a pure typo, otherwise tell the user).

4. **Check the result visually** before reporting: render each page to PNG (PyMuPDF: `fitz.open(pdf)[i].get_pixmap(dpi=90).save(...)`) and look at them. Verify: no text overlaps an icon or card edge, every question appears with its tag, icons match their questions, page count is sensible. If something is off, fix the spec (or icon) and regenerate; do not hand-edit layout code for one sheet.

5. **Reply briefly**: link to the PDF, page count, and any material issue the user should know. Do not paste the spec.

## Layout behaviour (automatic)
MCQ options (trailing lines starting `A)`, `B)`...) are detected automatically: the stem is followed by a small gap, then the options in an indented 2 x 2 grid with teal bold letters (one per line, wrapped with hanging indent, when any option is too long for half the column). Keep options as separate `
` lines at the end of `text`.
Page 1 = banner, Name/Class/Date/Score line, (formula box only if requested), as many compact question cards as fit; later pages = slim header. A new difficulty group starts on a new page when the current page already has 2+ cards; a group that runs over a page break repeats its badge with "continued". Card height grows with question length; a 6+ line question is fine. Any number of questions works; long sets just add pages ("Page n of N").

## Art for every question
The library in `scripts/icons.py` (25 ready-made icons) and `art/reference_diagrams.py` (3 full diagrams) are **style references and examples, not a menu**. Do not just pick the nearest one. For each question, draw a fresh illustration that shows **that question's own situation**: the specific objects, the specific arrangement, the quantities it names. Reuse a library icon only when it already depicts the question's situation exactly (e.g. the same sliding block), and still check it reads right next to the question.

### Decide: icon or diagram
- **Icon** (default, 100 x 64 box, small right-hand column): a symbolic picture of the situation, e.g. a car braking with skid marks, a bucket on a spring balance, a charged rod near a pith ball. Labels only for quantities/forces the question names, 3 words or fewer.
- **Diagram** (150 x 100 box, big right-hand column, `@icon("name", box=DIAGRAM_BOX)`): use when the question needs a figure to be understood or solved, or says "in the figure", or is inherently diagrammatic: circuits, ray diagrams, force/free-body diagrams on slopes or pulleys, graphs, wave/field pictures, lever and moment set-ups, vector addition, P-V diagrams, projectile paths, apparatus layouts. Draw the figure the question describes, accurately and to scale in proportion (angles, positions, which part is bigger), labelled with the symbols or **given values that appear in the question text** (e.g. "5 Ω", "30°", "2 kg" are fine because they are in the question). Never show answers, calculated results or intermediate working. If the question's wording is too vague to draw the figure faithfully, ask the user (step 0).
- A sheet may mix icons and diagrams; diagram cards are taller (about 195 pt), so a page holds 2-3 of them.

### How to write the art
1. Create or append to `art/<chapter-slug>.py` (e.g. `art/current_electricity.py`) in the writable skill folder or working copy. Files in `art/` auto-load; names starting with `_` are skipped. Start the file with `from drawkit import *` (the `icon` decorator, `ICON_BOX` and `DIAGRAM_BOX` are injected for you).
2. One function per question: `@icon("<slug>-q<n>")` for an icon, `@icon("<slug>-q<n>", box=DIAGRAM_BOX)` for a diagram. Draw in the local box, **y up**, origin bottom-left, and leave a few units of margin.
3. Visual language (same as the approved sheet): flat vector, **navy** outlines `stroke_style(c, 1.2-1.6)`, **teal** `TEAL` fills for main bodies, **orange** `ORANGE` for force/direction arrows and small accents, `TEAL_L`/`ORANGE_L`/`PALE`/white light fills, `GRASS` for grass, `HATCH`/`GREY` for hatching and guide lines. Rounded joins, no gradients, no shadows, no clutter.
4. Helpers in `scripts/drawkit.py`: `arrow`, `dim_arrow`, `angle_arc`, `zigzag` (springs/resistors), `block`, `ball`, `dot`, `dashed`, `hatch` (ground/wall/ceiling), `floor`, `car2`, `pent`, `lab`/`txt` (captions; diagrams use `txt` 7-9 pt bold), plus reportlab canvas calls (`c.circle`, `c.rect`, `c.beginPath()` ...). Read `icons.py` and `art/reference_diagrams.py` for the quality bar and idioms before drawing.
5. **Preview and iterate**: `python "<skill-dir>/scripts/preview_art.py" <art-name> <out.png> [scale]` renders one piece large; inspect the PNG. Check correct physics/geometry, readable labels, force arrows placed where they act, unclipped art, and consistent line weights. Fix and re-preview. `--all gallery.png` shows everything registered.
6. Everything you draw stays in `art/` and becomes future reference. Do not delete it.

## Fixed design (do not change)
Palette navy `#142D4E`, teal `#168D94`, orange `#F3A34B`, card `#F3F6FA`; green/orange/muted-red outlined badges with text EASY/MEDIUM/HARD (identifiable in black-and-white); Segoe UI Black headings, Segoe UI body 12 pt questions on A4; art is drawn fresh per question in the same flat style; cards with thin grey border, number circle at upper left, wide text column, illustration column at right, no working-space row (students write in a separate copy), source tag small at bottom right only when present; footer with atom glyph, note and "Page n of N" (no "STUDENT COPY" label). All of this lives in `scripts/drawkit.py` and `scripts/sheet.py`; leave them alone unless the user explicitly asks for a design change (then change it for all future sheets and re-run `examples/friction_example.json` to confirm nothing else moved).

## Not covered
Teacher/answer copies are not produced by this skill (the user gave only the student-sheet design). If asked for a teacher copy, say so and offer to make one separately.

## Maths (LaTeX) — for every subject with mathematical terms
Wrap any maths in `$...$` inside question/option text and it is typeset LaTeX-style (Computer Modern, vector) by `scripts/mathtex.py`: `"$\int_0^1 3x^2\,dx = \ ?$"`, options like `"A) $\dfrac{x^4}{4}+C$"`. Add `\,` after `\int`. Mathtext has no `\displaystyle`. In art use `mlab(c, x, y, r"$y=x^3$", TEAL, 8, "l")` instead of `lab`. Row heights adapt to fractions automatically. Plain-text questions (no `$`) render exactly as before.

