# CV Data Management

This directory contains the JSON data file that stores all your CV information.

## How to Use

1. **Edit your information**: Open `cv-data.json` and edit the data directly. The structure is organized by sections:
   - `personal`: Name, titles, and contact details used in metadata
   - `shortBio`: Your biography paragraphs
   - `education`: Your educational background
   - `honorsAwards`: Awards and honors
   - `publications`: Research publications
   - `technicalReports`: Technical reports
   - `workExperience`: Work history
   - `softwareProjects`: Software projects
   - `schoolsSeminars`: Schools and seminars attended
   - `volunteering`: Volunteering activities
   - `languages`: Languages you speak
   - `hobbies`: Your hobbies
   - `references`: Professional references
   - `contact`: Contact information and links

2. **Regenerate the site**: After editing the JSON file, run from the project root:
   ```bash
   python generate_html.py
   ```
   This regenerates `index.html` from `cv-data.json`.

3. **Optional LaTeX CV**: To regenerate the PDF-oriented LaTeX source as well:
   ```bash
   python generate_latex.py
   ```

4. **View your changes**: Open `index.html` in your browser to see the updated content.

## Data Structure Examples

### Adding a New Award
```json
{
  "date": "January 2026",
  "title": "Your Award Title",
  "institution": "Awarding Institution",
  "description": "Description of the award..."
}
```

### Adding a New Publication
Add to the appropriate year in `publications.byYear`:
```json
"2026": [
  {
    "authors": "Author1, Author2, Valantis Zervos, ...",
    "title": "Paper Title",
    "status": "Accepted at Conference 2026",
    "url": "https://link-to-paper.pdf"
  }
]
```

### Adding Work Experience
```json
{
  "date": "Jan 2026 - Present",
  "title": "Job Title",
  "institution": "Company/Organization",
  "description": "Job description...",
  "courses": ["Course 1", "Course 2"]
}
```

### Adding an Optional Entry Logo
Most entry objects can include an optional `logo` path (relative to project root):
```json
{
  "title": "BSc (2021-2025)",
  "school": "Computer Science Department, University of Crete (CSD, UoC)",
  "logo": "resources/logos/uoc.png"
}
```
Optional field:
- `logoAlt`: Custom alt text for the logo image

## Tips

- Use `Valantis Zervos` in author lists to automatically bold your name in generated HTML
- All text is automatically HTML-escaped for security
- Only edit `cv-data.json`; `index.html` is generated and should not be edited by hand

## File Structure

```
data/
  └── cv-data.json       # Your CV data (edit this)
generate_html.py         # Generates index.html
generate_latex.py        # Generates cv.tex
index.html               # Generated website (do not edit manually)
```

**Important**: Only edit `cv-data.json`. Running `python generate_html.py` will overwrite `index.html`.
