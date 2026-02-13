# CV Data Management

This directory contains the JSON data file that stores all your CV information.

## How to Use

1. **Edit your information**: Open `cv-data.json` and edit the data directly. The structure is organized by sections:
   - `shortBio`: Your biography paragraphs
   - `education`: Your educational background
   - `honorsAwards`: Awards and honors
   - `publications`: Research publications
   - `workExperience`: Work history
   - `softwareProjects`: Software projects
   - `schoolsSeminars`: Schools and seminars attended
   - `volunteering`: Volunteering activities
   - `languages`: Languages you speak
   - `hobbies`: Your hobbies
   - `references`: Professional references
   - `contact`: Contact information and links

2. **Generate HTML sections**: After editing the JSON file, run:
   ```bash
   npm run build
   ```
   This will regenerate all HTML section files in the `sections/` directory.

3. **View your changes**: Open `index.html` in your browser to see the updated content.

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
    "url": "https://link-to-paper.pdf"  // optional
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
  "courses": ["Course 1", "Course 2"]  // optional, for teaching positions
}
```

## Tips

- Use `**Valantis Zervos**` in author lists to automatically bold your name
- Dates can include line breaks: use ` - ` for automatic `<br>` insertion
- All text is automatically HTML-escaped for security
- The generator preserves the exact HTML structure you had before

## File Structure

```
data/
  └── cv-data.json          # Your CV data (edit this!)
sections/                   # Generated HTML files (auto-generated)
scripts/
  └── generate-sections.js  # Generator script
```

**Important**: Only edit `cv-data.json`. The files in `sections/` are auto-generated and will be overwritten when you run `npm run build`.


