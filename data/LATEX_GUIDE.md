# LaTeX CV Generation Guide

## Overview

The LaTeX CV is automatically generated from `cv-data.json` using the same data source as the HTML website. This ensures consistency across both formats.

## Generating LaTeX CV

### Quick Start

```bash
# Generate both HTML and LaTeX
npm run build

# Generate only LaTeX
npm run build:latex

# Generate LaTeX and compile to PDF automatically
npm run build:pdf

# Generate HTML, LaTeX, and PDF all at once
npm run build:all
```

### Compiling LaTeX to PDF

**Automatic (Recommended):**
```bash
npm run build:pdf
```
This will generate the LaTeX file and compile it to PDF automatically.

**Manual:**
If you prefer to compile manually:
```bash
pdflatex cv.tex
pdflatex cv.tex  # Run twice for proper cross-references
```

Or use your LaTeX editor (TeXstudio, Overleaf, etc.) to compile.

**Note:** Automatic PDF generation requires `pdflatex` to be installed and in your PATH. See "PDF Generation Requirements" below.

## Structure and Labels

The generator maintains the exact LaTeX structure from your original CV:

### Label Conventions

- **Honors & Awards**: `HA:ROTARY2025`, `HA:KARAMITZOU2025`, `HA:EPFL2025`, etc.
- **Education**: `ED:MSC`, `ED:BSC`
- **Publications**: `PUB:P3`, `PUB:P2`, `PUB:P1` (numbered newest first)
- **Technical Reports**: `TR:TR1`, `TR:TR2`, etc.
- **Software Projects**: 
  - Research/Professional: `RPP:SP2`, `RPP:SP1`
  - Hackathon: `HCP:SP1`
  - Course Projects: `CP:CP7` down to `CP:CP1`
- **Work Experience**: `WE:INGENIUM2025`, `WE:TA2023`, `WE:FORTH`
- **Schools**: `SS:CCI2025`, `SS:INGENIUM2025`
- **Volunteering**: `AV:...`, `OV:...`
- **References**: `REF:TZITZIKAS`, `REF:MAGOUTIS`, etc.

### Cross-References

The generator automatically creates hyperref links in the Short Bio section:
- Links to education entries
- Links to awards and honors
- Links to publications
- Links to software projects

These links are automatically maintained based on the label conventions.

## Date Formatting

Dates are automatically formatted for LaTeX:
- Full month names → Abbreviated (e.g., "November" → "Nov")
- Date ranges use en-dash (e.g., "Jul 2023 – Jan 2024")
- Special handling for multiple years (e.g., "Sep 2025, 2024")

## Special Formatting

### Publications
- Publications are numbered P3, P2, P1 (newest first)
- Special handling for Bachelor Thesis (P2)
- Status information is automatically formatted

### Software Projects
- Research projects numbered SP2, SP1
- Course projects numbered CP7 down to CP1
- GitHub links automatically included

### Work Experience
- Teaching Assistant entries include itemized course lists
- FORTH work includes nested itemized lists with hyperref links

## Customization

### Adding New Sections

To add new sections, you'll need to:
1. Add data to `cv-data.json`
2. Update `scripts/generate-latex.js` to handle the new section
3. Add appropriate labels to the `LABELS` mapping

### Modifying Formatting

Edit `scripts/generate-latex.js` to change:
- Date formats
- Section ordering
- Label conventions
- LaTeX commands used

## Tips

1. **Always run pdflatex twice** - Cross-references need two passes
2. **Check hyperref links** - Verify links work in the PDF
3. **Maintain label consistency** - Labels must match between sections
4. **Escape special characters** - The generator handles LaTeX escaping automatically
5. **Bold your name** - Use `**Valantis Zervos**` in author lists to auto-bold

## Troubleshooting

### Hyperref links not working
- Ensure labels match exactly
- Run pdflatex twice
- Check for typos in label names

### Date formatting issues
- Check date format in JSON matches expected patterns
- Verify month abbreviations are correct

### Special characters appearing incorrectly
- The generator should handle escaping automatically
- Check if new special characters need to be added to `escapeLatex()`

## PDF Generation Requirements

To use automatic PDF generation (`npm run build:pdf`), you need a LaTeX distribution installed:

- **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
- **macOS**: Install [MacTeX](https://www.tug.org/mactex/)
- **Linux**: Install `texlive-full` (e.g., `sudo apt-get install texlive-full`)

After installation, ensure `pdflatex` is in your PATH. You can verify by running:
```bash
pdflatex --version
```

If `pdflatex` is not found, the script will provide helpful error messages and instructions.

## File Locations

- **Source data**: `data/cv-data.json`
- **Generator script**: `scripts/generate-latex.js`
- **PDF generator script**: `scripts/generate-pdf.js`
- **Output file**: `cv.tex` (in project root)
- **Compiled PDF**: `cv.pdf` (in project root, after compilation)

