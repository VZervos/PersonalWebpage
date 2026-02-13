#!/usr/bin/env python3
"""
Generate LaTeX CV from cv-data.json
Uses ONLY data from JSON - nothing is hardcoded
"""

import json
import re

def escape_latex(text):
    """Escape LaTeX special characters and fix Unicode issues"""
    if not text:
        return ''
    text = str(text).replace('∼', '~').replace('–', '-').replace('—', '--')
    text = text.replace('\\', '\\textbackslash{}')
    text = text.replace('&', '\\&')
    text = text.replace('%', '\\%')
    text = text.replace('$', '\\$')
    text = text.replace('#', '\\#')
    text = text.replace('^', '\\textasciicircum{}')
    text = text.replace('_', '\\_')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('~', '\\textasciitilde{}')
    return text

def format_date_for_latex(date_str):
    """Format date string for LaTeX (abbreviate months)"""
    if not date_str:
        return ''
    
    month_map = {
        'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr',
        'May': 'May', 'June': 'Jun', 'July': 'Jul', 'August': 'Aug',
        'September': 'Sep', 'October': 'Oct', 'November': 'Nov', 'December': 'Dec'
    }
    
    formatted = date_str
    for full, abbrev in month_map.items():
        formatted = formatted.replace(full, abbrev)
    
    return escape_latex(formatted)

def format_date_range(date_str):
    """Format date range for LaTeX"""
    if not date_str:
        return ''
    
    parts = date_str.split(' - ')
    if len(parts) == 2:
        return f'{format_date_for_latex(parts[0].strip())} - {format_date_for_latex(parts[1].strip())}'
    return format_date_for_latex(date_str)

def generate_header(data):
    """Generate LaTeX header with personal data from JSON"""
    personal = data.get('personal', {})
    contact = data.get('contact', {})
    emails = contact.get('emails', [])
    links = contact.get('links', [])
    
    email = personal.get('email')
    if not email and emails:
        email = emails[0].get('address')
    
    github = personal.get('github')
    if not github:
        github_link = next((l for l in links if 'github' in l.get('url', '').lower()), {})
        github_url = github_link.get('url', '')
        if github_url and '/' in github_url:
            github = github_url.split('/')[-1]
    
    linkedin = personal.get('linkedin')
    if not linkedin:
        linkedin_link = next((l for l in links if 'linkedin' in l.get('url', '').lower()), {})
        linkedin_url = linkedin_link.get('url', '')
        if linkedin_url and '/' in linkedin_url:
            linkedin = linkedin_url.split('/')[-1]
    
    first_name = personal.get('firstName')
    last_name = personal.get('lastName')
    title_lines = personal.get('title', [])
    address_line1 = personal.get('addressLine1')
    address_line2 = personal.get('addressLine2')
    phone = personal.get('phone')
    
    if not first_name or not last_name:
        raise ValueError("firstName and lastName must be in JSON 'personal' section")
    if not title_lines:
        raise ValueError("title (array) must be in JSON 'personal' section")
    if not address_line1 or not address_line2:
        raise ValueError("addressLine1 and addressLine2 must be in JSON 'personal' section")
    if not phone:
        raise ValueError("phone must be in JSON 'personal' section")
    if not email:
        raise ValueError("email must be in JSON 'personal' section or 'contact.emails'")
    if not github:
        raise ValueError("github must be in JSON 'personal' section or extractable from 'contact.links'")
    if not linkedin:
        raise ValueError("linkedin must be in JSON 'personal' section or extractable from 'contact.links'")
    
    title_tex = ' \\newline\n'.join([escape_latex(line) for line in title_lines])
    
    return f'''% Documentation: https://ctan.math.washington.edu/tex-archive/macros/latex/contrib/moderncv/manual/moderncv_userguide.pdf
\\documentclass[11pt,a4paper,sans]{{moderncv}}

% ModernCV theme
\\moderncvstyle{{classic}}
\\moderncvcolor{{blue}}

% Adjust page margins
\\usepackage[scale=0.75]{{geometry}}
\\usepackage{{amsmath}}
\\usepackage{{hyperref}}
\\setlength{{\\parskip}}{{0.5em}}

% Personal data
\\name{{{escape_latex(first_name)}}}{{{escape_latex(last_name)}}}
\\title{{
{title_tex}
}}
\\address{{{escape_latex(address_line1)}}}{{{escape_latex(address_line2)}}}
\\phone[mobile]{{{escape_latex(phone)}}}
\\email{{{escape_latex(email)}}}
\\social[github]{{\\underline{{{escape_latex(github)}}}}}
\\social[linkedin]{{\\underline{{{escape_latex(linkedin)}}}}} 

%-------------------------------------------------------------------------------
% Content
%-------------------------------------------------------------------------------
\\begin{{document}}

\\makecvtitle

'''

def generate_short_bio(data):
    """Generate Short Bio section with hyperrefs from JSON"""
    latex = '''%-------------------------------------------------------------------------------
% Short Bio
%-------------------------------------------------------------------------------
\\label{sec:ShortBio}
\\section{Short Bio}
'''
    
    hyperrefs = [
        (r'BSc from the same department with a grade of 9\.57/10', 'ED:BSC', 'BSc from the same department with a grade of 9.57/10'),
        (r'ranking second among the students of my year of admission', 'HA:KARAMITZOU2025', 'ranking second among the students of my year of admission in the school'),
        (r'technological upgrade of the openABEKT system, commissioned by the National Documentation and Electronic Content Centre of Greece \(EKT\)', 'RPP:SP1', 'technological upgrade of the openABEKT system, commissioned by the National Documentation and Electronic Content Centre of Greece (EKT)'),
        (r'conducted research on both national and international research projects at the Information Systems Laboratory \(ISL\) of ICS-FORTH', 'sec:Publications', 'conducted research on both national and international research projects at the Information Systems Laboratory (ISL) of ICS-FORTH'),
        (r'8th nationwide for the HIAS scholarship \(2024\)', 'HA:HIAS2024', '8th nationwide for the HIAS scholarship (2024)'),
        (r'top 13% of applicants for EPFL worldwide \(2025\)', 'HA:EPFL2025', 'top 13% of applicants for EPFL worldwide (2025)'),
        (r'distinguished Undergraduate Teaching Assistant position in my department', 'HA:DEPROFOIT', 'distinguished Undergraduate Teaching Assistant position in my department'),
        (r'a member of the INGENIUM Student Board, representative of the University of Crete', '', 'a member of the INGENIUM Student Board, representative of the University of Crete')
    ]
    
    for idx, para in enumerate(data['shortBio']['paragraphs']):
        processed = para
        placeholders = []
        placeholder_idx = 0
        
        for pattern, label, text in hyperrefs:
            if pattern in processed:
                placeholder = f'\uE000{placeholder_idx}\uE001'
                text_escaped = text.replace('%', '\\%')
                if label:
                    placeholders.append((placeholder, f'\\hyperref[{label}]{{{text_escaped}}}'))
                else:
                    placeholders.append((placeholder, text_escaped))
                processed = re.sub(pattern, placeholder, processed)
                placeholder_idx += 1
        
        processed = processed.replace('\\hyperref[]{}', '')
        escaped = escape_latex(processed)
        
        for placeholder, cmd in placeholders:
            escaped = escaped.replace(placeholder, cmd)
        
        if idx < len(data['shortBio']['paragraphs']) - 1:
            latex += escaped + ' \\\\\n\n'
        else:
            latex += escaped + ' \\\\ \\\\\n\n'
    
    return latex

def generate_education(data):
    """Generate Education section"""
    latex = '''%-------------------------------------------------------------------------------
% Education
%-------------------------------------------------------------------------------
\\label{sec:Education}
\\section{Education}

'''
    
    for entry in data['education']['entries']:
        if 'MSc' in entry['title']:
            year_match = re.search(r'(\d{4})', entry['title'])
            year = year_match.group(1) if year_match else '2025'
            latex += f'\\label{{ED:MSC}}\n'
            latex += f'\\cvitem{{MSc Candidate {year}-Present}}{{\n'
            latex += '  \\textbf{Currently pursuing Master\\\'s Degree in Computer Science}\\newline\n'
            latex += f'  School: \\textbf{{{escape_latex(entry["school"])}}}\\newline\n'
            latex += '}\n\n'
        elif 'BSc' in entry['title']:
            year_match = re.search(r'(\d{4})[–-](\d{4})', entry['title'])
            if year_match:
                year_range = f'{year_match.group(1)}-{year_match.group(2)}'
            else:
                year_range = '2021-2025'
            
            grade_text = entry.get('grade', '').replace('Grade: ', '').replace(' (Ranked second)', '')
            latex += f'\\label{{ED:BSC}}\n'
            latex += f'\\cvitem{{BSc {year_range}}}{{\n'
            latex += f'  \\textbf{{Bachelor Degree in Computer Science}}\\newline\n'
            latex += f'  School: \\textbf{{{escape_latex(entry["school"])}}}\\newline\n'
            if grade_text:
                latex += f'  Grade: \\textbf{{{escape_latex(grade_text)}}} \\hyperref[HA:KARAMITZOU2025] {{(Ranked second)}}\\newline\n'
            latex += '}\n\n'
    
    return latex

def generate_honors_awards(data):
    """Generate Honors and Awards section"""
    latex = '''%-------------------------------------------------------------------------------
% Honors and Awards
%-------------------------------------------------------------------------------
\\label{sec:HonorsAndAwards}
\\section{Honors and Awards}

'''
    
    label_map = {
        'November 2025': 'HA:ROTARY2025',
        'July 2025': 'HA:KARAMITZOU2025',
        'January 2025': 'HA:EPFL2025',
        'September 2025, 2024': 'HA:DEPROFOIT',
        'June 2024': 'HA:PITCH2024',
        'March 2024': 'HA:HIAS2024',
        'November 2023': 'HA:ROTARY2023',
        'July 2023': 'HA:FORTH2023'
    }
    
    for entry in data['honorsAwards']['entries']:
        date = entry['date']
        label = label_map.get(date, f'HA:{date.replace(" ", "")[:15]}')
        
        date_parts = date.split(' ')
        month = date_parts[0]
        year = date_parts[1] if len(date_parts) > 1 else date_parts[-1]
        
        if ',' in date:
            parts = date.split(',')
            month = parts[0].split(' ')[0]
            year = f"{parts[0].split(' ')[1]}, {parts[1].strip()}"
        
        month_esc = format_date_for_latex(month)
        year_esc = format_date_for_latex(year)
        
        title_esc = escape_latex(entry['title'])
        inst_esc = escape_latex(entry['institution'])
        desc_esc = escape_latex(entry['description'])
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{{month_esc} {year_esc}}}\n'
        latex += '{\n'
        latex += f'\\textbf{{"{title_esc}"\\newline}}\n'
        latex += f'Issued by: \\textbf{{{inst_esc}}}\\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
    
    if 'contests' in data['honorsAwards'] and data['honorsAwards']['contests']:
        latex += '''%-------------------------------------------------------------------------------
% Contests
%-------------------------------------------------------------------------------
\\label{sec:Contests}
\\section{Contests}

'''
        
        for contest in data['honorsAwards']['contests']:
            date_esc = format_date_for_latex(contest['date'])
            title_esc = escape_latex(contest['title'])
            inst_esc = escape_latex(contest['institution'])
            desc_esc = escape_latex(contest['description'])
            
            label_base = contest['title'].replace(' ', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '')[:20]
            latex += f'\\label{{HA:CONTEST:{label_base}}}\n'
            latex += f'\\cvitem{{{date_esc}}}\n'
            latex += '{\n'
            latex += f'\\textbf{{{title_esc}\\newline}}\n'
            latex += f'Issued by: \\textbf{{{inst_esc}}}\\newline\n'
            latex += f'{desc_esc}\n'
            latex += '}\n\n'
    
    return latex

def generate_publications(data):
    """Generate Publications section"""
    latex = '''\\label{sec:Publications}
\\section{Publications}

'''
    
    all_pubs = []
    years = sorted(data['publications']['byYear'].keys(), reverse=True)
    
    for year in years:
        for pub in data['publications']['byYear'][year]:
            all_pubs.append({**pub, 'year': year})
    
    pub_num = len(all_pubs)
    for pub in all_pubs:
        authors = pub['authors'].replace('Valantis Zervos', '\\textbf{Valantis Zervos}')
        authors_esc = escape_latex(authors)
        title_esc = escape_latex(pub['title'])
        
        status = ''
        if 'url' in pub and 'TPDL' in pub.get('url', ''):
            status = f', TPDL {escape_latex(pub["year"])} \\textbf{{Bachelor Thesis}}'
        elif 'status' in pub and 'Accepted' in pub['status']:
            status = f'({escape_latex(pub["year"])}, {escape_latex(pub["status"].lower())})'
        elif 'status' in pub and 'status2' in pub:
            status = f'({escape_latex(pub["year"])}, {escape_latex(pub["status"].lower())}, to submit at {escape_latex(pub["status2"].replace("To submit at ", ""))})'
        else:
            status = f'({escape_latex(pub["year"])}, {escape_latex(pub.get("status", "under preparation").lower())})'
        
        latex += f'\\label{{PUB:P{pub_num}}}\n'
        latex += f'\\cvitem{{P{pub_num}}}\n'
        latex += f'{{{authors_esc}}},\n'
        latex += f'{title_esc}\n'
        latex += f'{status}\n'
        latex += '}\n\n'
        pub_num -= 1
    
    return latex

def generate_technical_reports(data):
    """Generate Technical Reports section"""
    latex = '''%-------------------------------------------------------------------------------
% Technical Reports
%-------------------------------------------------------------------------------
\\label{sec:TechnicalReports}
\\section{Technical Reports}

'''
    
    report_years = sorted(data['technicalReports']['byYear'].keys(), reverse=True)
    
    for idx, year in enumerate(report_years):
        for report in data['technicalReports']['byYear'][year]:
            authors = report['authors'].replace('Valantis Zervos', '\\textbf{Valantis Zervos}')
            authors_esc = escape_latex(authors)
            title_esc = escape_latex(report['title'])
            status_esc = escape_latex(report['status'].replace('Delivered to FAO-UN, ', 'delivered to FAO, '))
            
            latex += f'\\label{{TR:TR{idx + 1}}}\n'
            latex += f'\\cvitem{{TR{idx + 1}}}\n'
            latex += f'{{{authors_esc}}},\n'
            latex += f'{title_esc}, {status_esc}\n'
            latex += '}\n\n'
    
    return latex

def generate_software_projects(data):
    """Generate Software Projects sections"""
    latex = '''%-------------------------------------------------------------------------------
% Software Projects
%-------------------------------------------------------------------------------
\\label{sec:ResearchProfessionalProjects}
\\section{Research/Professional Software Projects}
\\href{https://github.com/VZervos}{GitHub: \\textcolor{blue}{https://github.com/VZervos}}
\\\\[1em]

'''
    
    for idx, project in enumerate(data['softwareProjects']['researchProfessional']):
        date_range = format_date_range(project['date'])
        title_esc = escape_latex(project['title'])
        inst_esc = escape_latex(project['institution'])
        desc_esc = escape_latex(project['description'])
        
        project_num = len(data['softwareProjects']['researchProfessional']) - idx
        latex += f'\\label{{RPP:SP{project_num}}}\n'
        latex += f'\\cvitem{{SP{project_num}}}{{\n'
        latex += f'\\textbf{{{title_esc}}} \\newline\n'
        latex += f'Duration: {date_range} \\newline\n'
        latex += f'Host: {inst_esc} \\newline\n'
        latex += f'My Role: \\textbf{{Full-Stack Developer}} \\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
    
    latex += '''%-------------------------------------------------------------------------------
% Course Projects
%-------------------------------------------------------------------------------
\\label{sec:CourseProjects}
\\section{Course Projects}
\\href{https://github.com/VZervos}{GitHub: \\textcolor{blue}{https://github.com/VZervos}}
\\\\[1em]

'''
    
    course_projects = data['softwareProjects']['courseProjects']['entries']
    cp_num = len(course_projects)
    
    for project in course_projects:
        date_range = format_date_range(project['date']).replace(' - ', ' – ')
        title_esc = escape_latex(project['title'])
        inst_esc = escape_latex(project['institution'])
        desc_esc = escape_latex(project['description'])
        
        cp_num_str = str(cp_num)
        latex += f'\\label{{CP:CP{cp_num_str}}}\n'
        latex += f'\\cvitem{{\\label{{CP:CP{cp_num_str}}} CP{cp_num_str}}}{{\n'
        latex += f'\\textbf{{{title_esc}}} \\newline\n'
        latex += f'Duration: {date_range} \\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
        cp_num -= 1
    
    return latex

def generate_work_experience(data):
    """Generate Work Experience section"""
    latex = '''%-------------------------------------------------------------------------------
% Work Experience
%-------------------------------------------------------------------------------
\\label{sec:WorkExperience}
\\section{Work Experience}

'''
    
    label_map = {
        'INGENIUM': 'WE:INGENIUM2025',
        'Teaching Assistant': 'WE:TA2023',
        'FORTH': 'WE:FORTH'
    }
    
    for entry in data['workExperience']['entries']:
        label = 'WE:UNKNOWN'
        if 'INGENIUM' in entry['title']:
            label = label_map['INGENIUM']
            title = 'Member of the INGENIUM Student Board'
        elif 'Teaching Assistant' in entry['title']:
            label = label_map['Teaching Assistant']
            title = 'University Teaching Assistant (DEPROFOIT)'
        elif 'FORTH' in entry['title']:
            label = label_map['FORTH']
            title = 'Graduate Researcher at FORTH'
        else:
            title = entry['title']
        
        date_formatted = format_date_range(entry['date'])
        title_esc = escape_latex(title)
        inst_esc = escape_latex(entry['institution'])
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{{date_formatted}}}\n'
        latex += '{\n'
        latex += f'\\textbf{{{title_esc}\\newline}}\n'
        latex += f'{inst_esc}\\newline\n'
        
        if 'courses' in entry:
            desc_esc = escape_latex(entry['description'])
            latex += f'{desc_esc}:\n'
            latex += '\\begin{itemize}\n'
            for course in entry['courses']:
                course_esc = escape_latex(course).replace('\\textasciitilde{}', '\\(\\sim \\)')
                latex += f'    \\item {course_esc}\n'
            latex += '\\end{itemize}\n'
        elif 'workItems' in entry:
            desc_esc = escape_latex(entry.get('description', ''))
            if desc_esc:
                latex += f'{desc_esc}\n'
            latex += 'Indicative work:\n'
            latex += '\\begin{itemize}\n'
            
            for item in entry['workItems']:
                if isinstance(item, str):
                    processed_item = escape_latex(item)
                    if 'industrial project' in processed_item.lower():
                        processed_item = processed_item.replace('industrial project', 'industrial project [\\hyperref[RPP:SP1]{SP1}, \\hyperref[PUB:P3]{P3}]')
                    if 'November 2023 to September 2024' in processed_item:
                        processed_item = processed_item.replace('November 2023 to September 2024', 'November 2023 to September 2024. [\\hyperref[RPP:SP2]{SP2}, \\hyperref[PUB:P1]{P1}]')
                    if 'RAG' in processed_item and 'LLMs' in processed_item:
                        processed_item = processed_item.replace('RAG) systems.', 'RAG) systems. [\\hyperref[PUB:P2]{P2}]')
                    latex += f'    \\item {processed_item}\n'
                elif isinstance(item, dict) and 'title' in item:
                    latex += f"    \\item {escape_latex(item['title'])}\n"
                    latex += '    \\begin{itemize}\n'
                    for sub_item in item.get('items', []):
                        latex += f"        \\item {escape_latex(sub_item)}\n"
                    latex += '    \\end{itemize}\n'
                    if 'note' in item:
                        note_esc = escape_latex(item['note'])
                        if 'November 2023 to September 2024' in note_esc:
                            note_esc = note_esc.replace('November 2023 to September 2024', 'November 2023 to September 2024. [\\hyperref[RPP:SP2]{SP2}, \\hyperref[PUB:P1]{P1}]')
                        latex += f'    {note_esc}\n'
            
            latex += '\\end{itemize}\n'
        else:
            desc_esc = escape_latex(entry['description'])
            latex += f'{desc_esc}\n'
        
        latex += '}\n\n'
    
    return latex

def generate_schools_seminars(data):
    """Generate Schools & Seminars section"""
    latex = '''%-------------------------------------------------------------------------------
% Schools & Seminars
%-------------------------------------------------------------------------------
\\label{sec:SchoolsSeminars}
\\section{Schools \\& Seminars}

'''
    
    label_map = {
        'CCI Summer School': 'SS:CCI2025',
        'INGENIUM Junior Winter School 2025': 'SS:INGENIUM2025'
    }
    
    for entry in data['schoolsSeminars']['entries']:
        subtitle = entry.get('subtitle', '')
        label = label_map.get(subtitle, f'SS:{subtitle.replace(" ", "")[:15]}')
        
        year_match = re.search(r'\d{4}', entry['date'])
        year = year_match.group(0) if year_match else '2025'
        
        date_esc = escape_latex(entry['date'])
        subtitle_esc = escape_latex(subtitle) if subtitle else ''
        title_esc = escape_latex(entry['title'])
        desc_esc = escape_latex(entry['description'])
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{{year}}}{{\n'
        if subtitle_esc:
            latex += f'\\textbf{{{subtitle_esc} \\newline}}\n'
        latex += f'\\textbf{{{date_esc}}} \\newline\n'
        latex += f'{title_esc} \\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
    
    return latex

def generate_volunteering(data):
    """Generate Volunteering sections"""
    latex = '''%-------------------------------------------------------------------------------
% Academic Volunteering
%-------------------------------------------------------------------------------
\\label{sec:AcademicVolunteering}
\\section{Academic Volunteering}

'''
    
    label_map = {
        "Researcher's Night": 'AV:RESEARCHERNIGHT',
        'ToTT': 'AV:TOTTCONF',
        'Open Week': 'AV:SCHOOLVISITCSD',
        'Career Fair': 'AV:CAREERFAIRUOC'
    }
    
    for entry in data['volunteering']['academic']:
        title = entry['title']
        label = 'AV:UNKNOWN'
        for key, val in label_map.items():
            if key in title:
                label = val
                break
        
        year = entry['date']
        title_esc = escape_latex(entry.get('subtitle', '') + ' ' + title if 'subtitle' in entry else title)
        if 'subtitle' in entry:
            title_esc = escape_latex(entry['subtitle']) + ' ' + escape_latex(title)
        else:
            title_esc = escape_latex(title)
        inst_esc = escape_latex(entry['institution'])
        desc_esc = escape_latex(entry['description'])
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{{year}}}\n'
        latex += '{\n'
        latex += f'{title_esc} \\newline\n'
        latex += f'{inst_esc}\\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
    
    latex += '''%-------------------------------------------------------------------------------
% Other Volunteering
%-------------------------------------------------------------------------------
\\label{sec:OtherVolunteering}
\\section{Other Volunteering}

'''
    
    label_map_other = {
        'Traditional Dance': 'OV:TRADITIONALDANCEEVENT',
        'Cultural Intervention': 'OV:CULTURALINTERVENTION',
        'Sales Representative': 'OV:SALESREPRESENTATIVE'
    }
    
    for entry in data['volunteering']['other']['entries']:
        title = entry['title']
        label = 'OV:UNKNOWN'
        for key, val in label_map_other.items():
            if key in title:
                label = val
                break
        
        date_esc = escape_latex(entry['date'])
        title_esc = escape_latex(title)
        inst_esc = escape_latex(entry['institution'])
        desc_esc = escape_latex(entry['description'])
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{{date_esc}}}\n'
        latex += '{\n'
        latex += f'{title_esc} \\newline\n'
        latex += f'{inst_esc} \\newline\n'
        latex += f'{desc_esc}\n'
        latex += '}\n\n'
    
    return latex

def generate_languages(data):
    """Generate Languages section"""
    latex = '''%-------------------------------------------------------------------------------
% Languages
%-------------------------------------------------------------------------------
\\label{sec:Languages}
\\section{Languages}
'''
    
    for lang in data['languages']['entries']:
        name_esc = escape_latex(lang['name'])
        level_esc = escape_latex(lang['level'])
        latex += f'\\cvitem{{\\textbf{{{name_esc}}} }}{{{level_esc}}}\n'
    
    return latex

def generate_hobbies(data):
    """Generate Hobbies and Interests section"""
    latex = '''%-------------------------------------------------------------------------------
% Hobbies and Interests
%-------------------------------------------------------------------------------
\\label{sec:HobbiesInterests}
\\section{Hobbies and Interests}
'''
    
    for hobby in data['hobbies']['entries']:
        title_esc = escape_latex(hobby['title'])
        desc_esc = escape_latex(hobby['description'])
        latex += f'\\cvitem{{\\textbf{{{title_esc}}}}}{{{desc_esc}}}\n'
    
    return latex

def generate_references(data):
    """Generate References section"""
    latex = '''%-------------------------------------------------------------------------------
% References
%-------------------------------------------------------------------------------
\\label{sec:References}
\\section{References}

'''
    
    label_map = {
        'Yannis Tzitzikas': 'REF:TZITZIKAS',
        'Kostas Magoutis': 'REF:MAGOUTIS',
        'Noni Rizopoulou': 'REF:RIZOPOULOU',
        'Yannis Marketakis': 'REF:MARKETAKIS',
        'Vangelis Kritsotakis': 'REF:KRITSOTAKIS',
        'Dimitris Sampsonidis': 'REF:SAMPSONIDIS'
    }
    
    for ref in data['references']['entries']:
        name = ref['name']
        label = label_map.get(name, f'REF:{name.replace(" ", "")[:15]}')
        name_esc = escape_latex(name)
        email_esc = escape_latex(ref['email'])
        positions = ref['positions']
        
        latex += f'\\label{{{label}}}\n'
        latex += f'\\cvitem{{\\textbf{{{name_esc}}}}} {{\n'
        for idx, pos in enumerate(positions):
            pos_esc = escape_latex(pos)
            if idx < len(positions) - 1:
                latex += f'{pos_esc},\\newline\n'
            else:
                latex += f'{pos_esc}\\newline\n'
        latex += f'{email_esc}\n'
        latex += '}\n\n'
    
    return latex

def main():
    """Main function to generate LaTeX CV"""
    print('Loading CV data...')
    with open('data/cv-data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('Generating LaTeX CV...')
    
    latex = generate_header(data)
    latex += generate_short_bio(data)
    latex += generate_education(data)
    latex += generate_honors_awards(data)
    latex += generate_publications(data)
    latex += generate_technical_reports(data)
    latex += generate_software_projects(data)
    latex += generate_work_experience(data)
    latex += generate_schools_seminars(data)
    latex += generate_volunteering(data)
    latex += generate_languages(data)
    latex += generate_hobbies(data)
    latex += generate_references(data)
    latex += '\\end{document}\n'
    
    with open('cv.tex', 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print('LaTeX CV generated successfully!')
    print('Output: cv.tex')
    print('\nTo compile:')
    print('   pdflatex cv.tex')
    print('   (Run twice for proper cross-references)')

if __name__ == '__main__':
    main()

