#!/usr/bin/env python3
"""
Generate complete index.html from cv-data.json
Simple Python script - no dependencies required
"""

import json
from html import escape

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ''
    return escape(str(text))

def clean_latex_artifacts(text):
    """Remove LaTeX commands from text"""
    import re
    if not text:
        return ''
    text = re.sub(r'\\hyperref\[\]{}', '', text)
    return text

def bold_author_name(text):
    """Bold 'Valantis Zervos' in author lists"""
    if not text:
        return ''
    text = text.replace('Valantis Zervos', '<b>Valantis Zervos</b>')
    text = text.replace('&lt;b&gt;Valantis Zervos&lt;/b&gt;', '<b>Valantis Zervos</b>')
    return text

def load_data():
    """Load CV data from JSON file"""
    with open('data/cv-data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_short_bio(data):
    """Generate Short Bio section"""
    paragraphs = []
    for p in data['shortBio']['paragraphs']:
        cleaned = clean_latex_artifacts(p)
        paragraphs.append(f'<p>{escape_html(cleaned)}</p>')
    
    paragraphs_html = '\n        '.join(paragraphs)
    
    return f'''<section id="short">
    <h2>Short Bio</h2>
    <div class="section-content">
        {paragraphs_html}
    </div>
</section>'''

def generate_education(data):
    """Generate Education section"""
    entries = []
    for entry in data['education']['entries']:
        html = f'''                <div class="entry">
                    <div class="title">{escape_html(entry['title'])}</div>
                    <div class="details">
                        <p class="school">{escape_html(entry['school'])}</p>'''
        if 'grade' in entry:
            html += f'\n                        <p class="grade">{escape_html(entry["grade"])}</p>'
        if 'note' in entry:
            html += f'\n                        <p class="note">{escape_html(entry["note"])}</p>'
        html += '''\n                    </div>
                </div>'''
        entries.append(html)
    
    entries_html = '\n'.join(entries)
    return f'''<section id="education">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <h2><i class="fa-solid fa-graduation-cap"> </i> Studies</h2>
{entries_html}
            </div>
        </div>
    </div>
</section>'''

def generate_honors_awards(data):
    """Generate Honors & Awards section"""
    html = '''<section id="honorsawards">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <h2><i class="fa-solid fa-award"></i> Honors & Awards</h2>'''
    
    entries = []
    for entry in data['honorsAwards']['entries']:
        entry_html = f'''                <div class="entry">
                    <div class="left-col">
                        <div class="date">{escape_html(entry['date'])}</div>
                    </div>
                    <div class="right-col">
                        <div class="title">
                            {escape_html(entry['title'])}
                        </div>
                        <div class="institution">
                            {escape_html(entry['institution'])}
                        </div>
                        <div class="details">
                            <p>{escape_html(entry['description'])}
                            </p>
                        </div>
                    </div>
                </div>'''
        entries.append(entry_html)
    
    entries_html = '\n\n'.join(entries)
    html += f'\n{entries_html}'
    html += '''\n            </div>
        </div>'''
    
    if 'contests' in data['honorsAwards'] and data['honorsAwards']['contests']:
        html += '''\n        <div class="row">
            <div class="section-content col-12 col-md">
                <h2><i class="fa-solid fa-trophy"></i> Contests</h2>'''
        
        contest_entries = []
        for contest in data['honorsAwards']['contests']:
            contest_html = f'''                <div class="entry">
                    <div class="left-col">
                        <div class="date">{escape_html(contest['date'])}</div>
                    </div>
                    <div class="right-col">
                        <div class="title">
                            {escape_html(contest['title'])}
                        </div>
                        <div class="institution">
                            {escape_html(contest['institution'])}
                        </div>
                        <div class="details">
                            <p>{escape_html(contest['description'])}
                            </p>
                        </div>
                    </div>
                </div>'''
            contest_entries.append(contest_html)
        
        contests_html = '\n\n'.join(contest_entries)
        html += f'\n{contests_html}'
        html += '''\n            </div>
        </div>'''
    
    html += '''\n    </div>
</section>'''
    return html

def generate_publications(data):
    """Generate Publications section"""
    html = '''<section id="publicationsresearch">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <h2><i class="fa-solid fa-book"></i> Publications</h2>'''

    years = sorted(data['publications']['byYear'].keys(), reverse=True)
    for year in years:
        html += f'\n                <div class="year-section">\n                    <h3>{year}</h3>'
        for pub in data['publications']['byYear'][year]:
            authors_escaped = escape_html(pub['authors'])
            authors_html = bold_author_name(authors_escaped)
            has_link = 'url' in pub and pub['url']
            
            html += '\n                    <div class="entry">\n                        <div class="left-col-rev">\n                            <div class="publication">'
            if has_link:
                html += f'\n                                <a target="_blank" href="{escape_html(pub["url"])}">'
            html += f'\n                                    <div class="paper-authors">{authors_html}</div>\n                                    <div class="paper-title">\n                                        {escape_html(pub["title"])}\n                                    </div>'
            if has_link:
                html += '\n                                </a>'
            html += '\n                            </div>\n                        </div>\n                        <div class="right-col-rev">'
            if 'status' in pub:
                html += f'\n                            <div class="status-accepted">\n                                {escape_html(pub["status"])}\n                            </div>'
            if 'status2' in pub:
                html += f'\n                            <div class="status-to_submit">\n                                {escape_html(pub["status2"])}\n                            </div>'
            if has_link and 'status' not in pub:
                html += '\n                            <i class="fa-solid fa-arrow-up-right-from-square"></i>'
            html += '\n                        </div>\n                    </div>'
        html += '\n                </div>'
    
    html += '''\n            </div>
        </div>
        <div class="row">
            <div class="section-content col-12 col-md">
                <h2><i class="fa-solid fa-pen-nib"></i> Technical Reports</h2>'''
    
    report_years = sorted(data['technicalReports']['byYear'].keys(), reverse=True)
    for year in report_years:
        html += f'\n                <div class="year-section">\n                    <h3>{year}</h3>'
        for report in data['technicalReports']['byYear'][year]:
            authors_escaped = escape_html(report['authors'])
            authors_html = bold_author_name(authors_escaped)
            html += f'''\n                    <div class="entry">
                        <div class="left-col-rev">
                            <div class="publication">
                                <div class="paper-authors">{authors_html}</div>
                                <div class="paper-title">
                                    {escape_html(report['title'])}
                                </div>
                            </div>
                        </div>
                        <div class="right-col-rev">
                            <div class="status-accepted">
                                {escape_html(report['status'])}
                            </div>
                        </div>
                    </div>'''
        html += '\n                </div>'
    
    html += '''\n            </div>
        </div>
    </div>
</section>'''
    return html

def generate_work_experience(data):
    """Generate Work Experience section"""
    entries = []
    for entry in data['workExperience']['entries']:
        date_html = escape_html(entry['date'])
        html = f'''                    <div class="entry">
                        <div class="left-col">
                            <div class="date">{date_html}</div>
                        </div>
                        <div class="right-col">
                            <div class="title">
                                {escape_html(entry['title'])}
                            </div>
                            <div class="institution">
                                {escape_html(entry['institution'])}
                            </div>
                            <div class="details">
                                <p>{escape_html(entry['description'])}'''
        if 'courses' in entry:
            html += '\n                                    <ul>'
            for course in entry['courses']:
                html += f'\n                                        <li>{escape_html(course)}</li>'
            html += '\n                                    </ul>'
        if 'workItems' in entry:
            html += '\n                                    <ul>'
            for item in entry['workItems']:
                if isinstance(item, str):
                    html += f'\n                                        <li>{escape_html(item)}</li>'
                elif isinstance(item, dict) and 'title' in item:
                    html += f'\n                                        <li>{escape_html(item["title"])}\n                                            <ul>'
                    for sub_item in item.get('items', []):
                        html += f'\n                                                <li>{escape_html(sub_item)}</li>'
                    html += f'\n                                            </ul>\n                                            {escape_html(item.get("note", ""))}\n                                        </li>'
            html += '\n                                    </ul>'
        html += '''\n                                </p>
                            </div>
                        </div>
                    </div>'''
        entries.append(html)
    
    entries_html = '\n'.join(entries)
    return f'''<section id="workexperience">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-building"></i> Work Experience</h2>
{entries_html}
                </div>
            </div>
        </div>
    </div>
</section>'''

def generate_software_projects(data):
    """Generate Software Projects section"""
    html = '''<section id="softwareprojects">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-laptop-code"></i> Research/Professional Software Projects</h2>'''
    
    for project in data['softwareProjects']['researchProfessional']:
        date_html = escape_html(project['date'])
        html += f'''\n                    <div class="entry">
                        <div class="left-col">
                            <div class="date">{date_html}</div>
                        </div>
                        <div class="right-col">
                            <div class="title">
                                {escape_html(project['title'])}
                            </div>
                            <div class="institution">
                                {escape_html(project['institution'])}
                            </div>
                            <div class="details">
                                <p>{escape_html(project['description'])}
                                </p>
                            </div>
                        </div>
                    </div>'''
    
    html += '''\n                </div>
            </div>
        </div>
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-pen"></i> Course Projects</h2>'''
    
    if 'courseProjects' in data['softwareProjects']:
        html += f'\n                    <div class="institution">\n                        {escape_html(data["softwareProjects"]["courseProjects"]["note"])}\n                    </div>'
        
        for project in data['softwareProjects']['courseProjects']['entries']:
            date_html = escape_html(project['date'])
            html += f'''\n                    <div class="entry">
                        <div class="left-col">
                            <div class="date">{date_html}</div>
                        </div>
                        <div class="right-col">
                            <div class="title">
                                {escape_html(project['title'])}
                            </div>
                            <div class="institution">
                                {escape_html(project['institution'])}
                            </div>
                            <div class="details">
                                <p>{escape_html(project['description'])}
                                </p>
                            </div>
                        </div>
                    </div>'''
    
    html += '''\n                </div>
            </div>
        </div>
    </div>
</section>'''
    return html

def generate_schools_seminars(data):
    """Generate Schools & Seminars section"""
    entries = []
    for entry in data['schoolsSeminars']['entries']:
        date_html = escape_html(entry['date'])
        html = f'''                    <div class="entry">
                        <div class="left-col">
                            <div class="date">{date_html}</div>
                        </div>
                        <div class="right-col">'''
        if 'subtitle' in entry:
            html += f'\n                            <div class="subtitle">\n                                {escape_html(entry["subtitle"])}\n                            </div>'
        html += f'''\n                            <div class="title">
                                {escape_html(entry['title'])}
                            </div>
                            <div class="institution">
                                {escape_html(entry['institution'])}
                            </div>
                            <div class="details">
                                <p>{escape_html(entry['description'])}
                                </p>
                            </div>
                        </div>
                    </div>'''
        entries.append(html)
    
    entries_html = '\n'.join(entries)
    return f'''<section id="schoolsseminars">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-school"></i> Schools</h2>
{entries_html}
                </div>
            </div>
        </div>
    </div>
</section>'''

def generate_volunteering(data):
    """Generate Volunteering section"""
    html = '''<section id="volunteering">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-person-chalkboard"></i> Academic Volunteering</h2>'''
    
    for entry in data['volunteering']['academic']:
        html += f'''\n                    <div class="entry">
                        <div class="left-col">
                            <div class="date">{escape_html(entry['date'])}</div>
                        </div>
                        <div class="right-col">'''
        if 'subtitle' in entry:
            html += f'\n                            <div class="subtitle">\n                                {escape_html(entry["subtitle"])}\n                            </div>'
        html += f'''\n                            <div class="title">
                                {escape_html(entry['title'])}
                            </div>
                            <div class="institution">
                                {escape_html(entry['institution'])}
                            </div>
                            <div class="details">
                                <p>{escape_html(entry['description'])}
                                </p>
                            </div>
                        </div>
                    </div>'''
    
    html += f'''\n                </div>
            </div>
            <div class="row">
                <div class="section-content col-12 col-md">
                    <div>
                        <h2><i class="fa-solid fa-tree"></i> Other Volunteering</h2>
                        <div class="institution">
                            {escape_html(data['volunteering']['other']['note'])}
                        </div>'''
    
    for entry in data['volunteering']['other']['entries']:
        html += f'''\n                        <div class="entry">
                            <div class="left-col">
                                <div class="date">{escape_html(entry['date'])}</div>
                            </div>
                            <div class="right-col">
                                <div class="title">
                                    {escape_html(entry['title'])}
                                </div>
                                <div class="institution">
                                    {escape_html(entry['institution'])}
                                </div>
                                <div class="details">
                                    <p>{escape_html(entry['description'])}
                                    </p>
                                </div>
                            </div>
                        </div>'''
    
    html += '''\n                    </div>
                </div>
            </div>
        </div>
    </div>
</section>'''
    return html

def generate_languages_hobbies_references(data):
    """Generate Languages, Hobbies & References section"""
    html = '''<section id="languageshobbiesreferences">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-language"></i> Languages</h2>'''
    
    for lang in data['languages']['entries']:
        html += f'''\n                    <div class="entry">
                        <div class="title">
                            {escape_html(lang['name'])}
                        </div>
                        <div class="institution">
                            {escape_html(lang['level'])}
                        </div>
                    </div>'''
    
    html += '''\n                </div>
            </div>
        </div>
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-gamepad"></i> Hobbies</h2>'''
    
    for hobby in data['hobbies']['entries']:
        html += f'''\n                    <div class="entry">
                        <div class="title">
                            {escape_html(hobby['title'])}
                        </div>
                        <div class="institution">
                            {escape_html(hobby['description'])}
                        </div>
                    </div>'''
    
    html += '''\n                </div>
            </div>
        </div>
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-square-check"></i> References</h2>'''
    
    for ref in data['references']['entries']:
        html += f'''\n                    <div class="entry">
                        <div class="left-col">
                            <div class="title"> {escape_html(ref['name'])}</div>
                            <div class="subtitle"><a target="_blank" href="mailto:{escape_html(ref['email'])}"> {escape_html(ref['email'].replace('@', ' (at) '))} <i class="fa-solid fa-envelope"></i></a></div>
                        </div>
                        <div class="right-col">
                            <div class="details">
                                <p>'''
        if len(ref['positions']) == 1:
            html += f'\n                                        {escape_html(ref["positions"][0])} '
        else:
            html += '\n                                        <ul>'
            for pos in ref['positions']:
                html += f'\n                                            <li>{escape_html(pos)}</li>'
            html += '\n                                        </ul>'
        html += '''\n                                </p>
                            </div>
                        </div>
                    </div>'''
    
    html += '''\n                </div>
            </div>
        </div>
    </div>
</section>'''
    return html

def generate_contact_me(data):
    """Generate Contact Me section"""
    html = '''<section id="contactme">
    <div class="container-fluid">
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-envelope"></i> Contact Me</h2>'''
    
    for email in data['contact']['emails']:
        email_display = email['address'].replace('@', ' (at) ')
        html += f'''\n                    <a target="_blank" href="mailto:{escape_html(email['address'])}">
                        <div class="entry">
                            <div class="title">
                                {escape_html(email_display)}
                            </div>
                            <div class="institution">
                                {escape_html(email['label'])} <i class="fa-solid fa-envelope"></i>
                            </div>
                        </div>
                    </a>'''
    
    html += '''\n                </div>
            </div>
        </div>
        <div class="row">
            <div class="section-content col-12 col-md">
                <div>
                    <h2><i class="fa-solid fa-link"></i> Useful Links</h2>'''
    
    for link in data['contact']['links']:
        html += f'''\n                    <a target="_blank" href="{escape_html(link['url'])}">
                        <div class="entry">
                            <div class="title">
                                {escape_html(link['name'])}
                            </div>
                            <div class="institution">
                                {escape_html(link['url'])} <i class="fa-solid fa-arrow-up-right-from-square"></i>
                            </div>
                        </div>
                    </a>'''
    
    html += '''\n                </div>
            </div>
        </div>
    </div>
</section>'''
    return html

def generate_index_html(data):
    """Generate complete index.html file"""
    
    short_bio = generate_short_bio(data)
    education = generate_education(data)
    honors_awards = generate_honors_awards(data)
    publications = generate_publications(data)
    work_experience = generate_work_experience(data)
    software_projects = generate_software_projects(data)
    schools_seminars = generate_schools_seminars(data)
    volunteering = generate_volunteering(data)
    languages_hobbies_references = generate_languages_hobbies_references(data)
    contact_me = generate_contact_me(data)
    
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="Author" content="Valantis Zervos">
    <meta name="Description" content="Valantis's biography page">
    <meta name="keywords" lang="en-us" content="valantis, zervos, csd4878, bio, biography">

    <title>Valantis Zervos</title>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

    <link rel="stylesheet" href="css/default.css">
    <!--    <link rel="stylesheet" href="css/tablet.css">-->
    <!--    <link rel="stylesheet" href="css/mobile.css">-->

    <script src="js/fb_share.js"></script>
    <script src="js/open_secret.js"></script>
    <script src="js/navigation.js"></script>
    <script src="index.js"></script>

</head>
<body class="bg-body-secondary">
<header>
    <div class="container">
        <div class="row align-items-center">
            <div class="col-md-5 text-center mb-4 mb-md-0">
                <img src="resources/me.png" alt="Valantis Zervos Photo" class="logo img-fluid rounded-circle mb-3">
                <h1>Valantis Zervos</h1>
                <h2 class="h5 fw-normal">MSc Student at Computer Science Department, University of Crete</h2>
                <h2 class="h5 fw-normal">Graduate Research Fellow, Information Systems Laboratory, ICS-FORTH</h2>
                <h2 class="h5 fw-normal">Member of the INGENIUM Student Board for the University of Crete</h2>
                <div class="social-icons" aria-label="Quick access social links">
                    <a class="social-icon" target="_blank" href="https://www.linkedin.com/in/vzervos/" aria-label="LinkedIn">
                        <i class="fa-brands fa-linkedin"></i>
                    </a>
                    <a class="social-icon" target="_blank" href="https://github.com/VZervos" aria-label="GitHub">
                        <i class="fa-brands fa-github"></i>
                    </a>
                    <a class="social-icon" target="_blank" href="https://scholar.google.com/citations?user=NiPG7QIAAAAJ" aria-label="Google Scholar">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Scholar_logo.svg" alt="Google Scholar">
                    </a>
                </div>
            </div>

            <div class="col-md-7" id="short-bio-container">
'''
    html += '                ' + short_bio.replace('\n', '\n                ') + '\n'
    html += '''            </div>
        </div>
    </div>
</header>


<nav class="navbar navbar-expand-lg enhanced-nav" id="mainNavigation">
    <div class="container-fluid navBarContent">
        <!-- Mobile hamburger button -->
        <button class="navbar-toggler d-lg-none" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navigation items -->
        <div class="navbar-collapse collapse" id="navbarNav">
            <div class="navbar-nav nav-items-container">
                <a class="nav-link nav-item" href="#education" data-section="education">
                    <i class="fa-solid fa-graduation-cap"></i>
                    <span class="nav-text">Education</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#publicationsresearch" data-section="publicationsresearch">
                    <i class="fa-solid fa-book"></i>
                    <span class="nav-text">Publications & Research</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#honorsawards" data-section="honorsawards">
                    <i class="fa-solid fa-award"></i>
                    <span class="nav-text">Honors & Awards</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#workexperience" data-section="workexperience">
                    <i class="fa-solid fa-building"></i>
                    <span class="nav-text">Work Experience</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#softwareprojects" data-section="softwareprojects">
                    <i class="fa-solid fa-laptop-code"></i>
                    <span class="nav-text">Software Projects</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#schoolsseminars" data-section="schoolsseminars">
                    <i class="fa-solid fa-school"></i>
                    <span class="nav-text">Schools & Seminars</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#volunteering" data-section="volunteering">
                    <i class="fa-solid fa-handshake-angle"></i>
                    <span class="nav-text">Volunteering</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item" href="#languageshobbiesreferences"
                   data-section="languageshobbiesreferences">
                    <i class="fa-solid fa-language"></i>
                    <span class="nav-text">Languages & Hobbies</span>
                    <div class="nav-indicator"></div>
                </a>
                <a class="nav-link nav-item contact-nav" href="#contactme" data-section="contactme">
                    <i class="fa-solid fa-envelope"></i>
                    <span class="nav-text">Contact Me</span>
                    <div class="nav-indicator"></div>
                </a>
            </div>
        </div>
    </div>
</nav>

<main>
'''
    html += education + '\n\n'
    html += publications + '\n\n'
    html += honors_awards + '\n\n'
    html += work_experience + '\n\n'
    html += software_projects + '\n\n'
    html += schools_seminars + '\n\n'
    html += volunteering + '\n\n'
    html += languages_hobbies_references + '\n\n'
    html += contact_me + '\n\n'
    html += '''</main>

<footer>
    <div class="footer-content">
        <div class="container">
            <div class="row d-flex justify-content-between align-items-center">
                <div class="col-12 col-sm-auto text-center text-sm-start">
                    <div class="col-12 col-sm-auto text-center text-sm-start">
                        Contact me:
                    </div>
                    <div class="col-12 col-sm-auto text-center text-sm-start">
                        <a target="_blank" href="mailto:zervosvalantis@gmail.com" style="color: white">
                            zervosvalantis (at) gmail.com
                        </a>
                    </div>
                    <div class="col-12 col-sm-auto text-center text-sm-start">
                        <a target="_blank" href="mailto:vzervos@csd.uoc.gr" style="color: white">
                            vzervos (at) csd.uoc.gr
                        </a>
                    </div>
                    <div class="col-12 col-sm-auto text-center text-sm-start">
                        <a target="_blank" href="mailto:vzervos@ics.forth.gr" style="color: white">
                            vzervos (at) ics.forth.gr
                        </a>
                    </div>
                </div>
                <div class="col-12 col-sm-auto text-center">
                    <p class="copyright">Spyridon Chrysovalantis Zervos <br> Personal Page</p>
                </div>
                <div class="col-12 col-sm-auto text-center text-sm-end">
                    <a target="_blank" href="https://www.linkedin.com/in/vzervos/" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor"
                             class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z"/>
                        </svg>
                    </a>
                    <a target="_blank" href="https://github.com/vzervos" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor"
                             class="bi bi-github github-icon" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.54 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.13 0 0 .67-.21 2.2.82a7.548 7.548 0 012.01-.27c.68.003 1.36.092 2.01.27 1.53-1.04 2.2-.82 2.2-.82.44 1.11.16 1.93.08 2.13.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                    </a>
                    <a target="_blank" href="https://scholar.google.com/citations?user=NiPG7QIAAAAJ">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Scholar_logo.svg"
                             alt="Google Scholar" width="32" height="32">
                    </a>
                </div>
            </div>
        </div>
    </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>

</body>
</html>'''
    
    return html

def main():
    """Main function to generate complete index.html"""
    print('Loading CV data...')
    data = load_data()
    
    print('Generating complete index.html...')
    
    html = generate_index_html(data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('Generated index.html successfully!')

if __name__ == '__main__':
    main()
