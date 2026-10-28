# create-homework-sheet 📝

> **Agent Skill**: Generate print-ready A4 student homework practice worksheets and PDFs with diagrams and custom vector illustrations for every question.

Compatible with **Claude Code**, **Google Antigravity**, **Cursor**, **Codex**, **OpenCode**, and any AI agent supporting the open Agent Skills standard.

---

## ⚡ Instant Install (Recommended)

Install directly using the skills package manager:

### Project Install:
```bash
npx skills add muhaiminulsadat/create-homework-sheet
```

### Global Install (Available across all projects & agents):
```bash
npx skills add muhaiminulsadat/create-homework-sheet -g
```

---

## 🚀 Manual Install (Git Clone)

### 1. Claude Code
```bash
# macOS / Linux
git clone https://github.com/muhaiminulsadat/create-homework-sheet.git ~/.claude/skills/create-homework-sheet

# Windows (PowerShell)
git clone https://github.com/muhaiminulsadat/create-homework-sheet.git "$HOME\.claude\skills\create-homework-sheet"
```

### 2. Antigravity / Gemini
```bash
# macOS / Linux
git clone https://github.com/muhaiminulsadat/create-homework-sheet.git ~/.gemini/config/skills/create-homework-sheet

# Windows (PowerShell)
git clone https://github.com/muhaiminulsadat/create-homework-sheet.git "$HOME\.gemini\config\skills\create-homework-sheet"
```

### 3. Project Workspace (Cursor / Windsurf / Codex)
```bash
git clone https://github.com/muhaiminulsadat/create-homework-sheet.git .agents/skills/create-homework-sheet
```

---

## ⚙️ Prerequisites

The skill scripts run locally to draw diagrams and compile your worksheets to vector PDF:

- **Python 3.8+**
  ```bash
  pip install reportlab matplotlib
  ```

- **For Bangla Worksheets (Optional)**:
  ```bash
  pip install uharfbuzz fonttools
  ```
  *(Uses Windows `Nirmala UI` or standard Bangla complex-text shaping).*

---

## 📖 How to Use

Once installed, simply paste your numbered questions and ask your agent or invoke `/create-homework-sheet`:

```text
/create-homework-sheet

1. A block of mass 5 kg rests on a rough horizontal surface with coefficient of friction 0.3. A horizontal force of 20 N is applied. Find the acceleration. [BUET'11-12]
2. A particle moves along a straight line such that its displacement is given by x = 3t^2 + 2t. What is its velocity at t = 2s?
```

### What You Supply:
- **Questions**: Plain-text questions (numbered).
- **Optional Tags**: Exam/source tags in brackets like `[BUET'11-12]`, `(DU 15-16)`.
- **Optional Difficulty**: `[Easy]`, `[Medium]`, or `[Hard]` labels.
- **Optional Overrides**: Chapter title or subject subtitle.

### ✨ Features:
- **Every Question Gets an Illustration**: Automatically generates a dedicated diagram, circuit, graph, apparatus sketch, or force/free-body diagram for each problem.
- **LaTeX Math Equations**: Seamless inline and display math via Mathtext (`$F = ma$`, `$\int_0^1 x^2\,dx$`, `$\theta = 30^\circ$`).
- **Multiple Choice Questions (MCQ)**: Automatically detected and typeset in clean 2×2 indented grid cards.
- **Compact & Modern Design**:
  - Color-coded badges for difficulty (EASY, MEDIUM, HARD).
  - Compact header with Student Name, Class, Date, and Score blanks.
  - Slim subsequent page headers with automated pagination (`Page n of N`).
- **Bangla Support**: Fully handles Bangla Unicode questions, symbols, and formatting.

---

## 📂 Repository Structure

- `SKILL.md` – Core skill instructions and design specifications for AI agents
- `scripts/`
  - `sheet.py` – Core layout and PDF generation engine (ReportLab canvas)
  - `make_sheet.py` – CLI runner for compiling a JSON specification to PDF
  - `make_sheet_bn.py` – Bengali text shaping and compilation runner
  - `drawkit.py` – Vector drawing toolkit (blocks, springs, carts, angles, arrows, labels)
  - `icons.py` – Standard illustration primitives and icon library
  - `mathtex.py` – High-precision vector math typesetting engine
  - `preview_art.py` – Tool for rendering and previewing individual diagrams as PNGs
  - `bn_patch.py` – HarfBuzz text shaping integration for Bangla script
- `art/` – Library of pre-built domain diagrams:
  - `work_energy_power.py`
  - `simple_harmonic_motion.py`
  - `organic_chemistry.py`
  - `higher_math_integration.py`
  - `reference_diagrams.py`
- `examples/` – Sample question specification (`friction_example.json`)
- `agents/` – Agent metadata (`openai.yaml`)

---

## 👤 Author

Created by [Sadat](https://github.com/muhaiminulsadat).
Contributions and improvements are welcome!
