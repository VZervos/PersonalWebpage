# Quick Start Guide - Editing Your CV

## The Easy Way to Update Your Website

Your CV is now completely data-driven! Just edit one JSON file and run simple commands.

### Step 1: Edit Your Data
Open `data/cv-data.json` and edit your information. It's organized by sections:
- Personal info, education, awards, publications, work experience, etc.

### Step 2: Generate HTML Sections
Run this command:
```bash
python generate_html.py
```
This generates all HTML section files in the `sections/` directory.

### Step 3: Generate LaTeX CV (Optional)
Run this command:
```bash
python generate_latex.py
```
This generates `cv.tex` that you can compile to PDF with `pdflatex`.

### Step 4: View Changes
Refresh your browser to see the updated HTML sections!

## Example: Adding a New Award

1. Open `data/cv-data.json`
2. Find the `honorsAwards.entries` array
3. Add a new entry:
```json
{
  "date": "January 2026",
  "title": "New Award Name",
  "institution": "Awarding Organization",
  "description": "What the award is for..."
}
```
4. Run `python generate_html.py`
5. Refresh your browser

That's it!

## How It Works

- **Simple Python scripts** - No npm, no Node.js, no build tools
- **Standard library only** - Uses only Python's built-in libraries
- **Single data source** - Edit `cv-data.json` and generate both HTML and LaTeX
- **Works everywhere** - Python is pre-installed on most systems

## Commands

- `python generate_html.py` - Generate all HTML sections from JSON
- `python generate_latex.py` - Generate LaTeX CV from JSON

## File Structure

- **`data/cv-data.json`** ← Edit this file (your CV data)
- **`generate_html.py`** ← Generates HTML sections (run this)
- **`generate_latex.py`** ← Generates LaTeX CV (run this)
- **`sections/*.html`** ← Generated HTML files (auto-generated)
- **`cv.tex`** ← Generated LaTeX file (auto-generated)

## LaTeX PDF Generation

1. Run `python generate_latex.py` to generate `cv.tex`
2. Compile it with `pdflatex cv.tex` (run twice for cross-references)
3. Or use an online LaTeX editor like Overleaf

## Need Help?

See `data/README.md` for detailed documentation on the data structure.
