"""Build the static GitHub Pages portfolio from the reviewed content files."""
import json
from html import escape as e
from pathlib import Path
from render_projects import render_all
from navigation import render_navigation, asset_url

ROOT = Path(__file__).resolve().parent
c = json.loads((ROOT / 'content.json').read_text())
d = json.loads((ROOT / 'project-details.json').read_text())
SITE = 'https://haolianghuang-research.github.io/'
catalog = {p['id']: p for p in c['projects'] + d.get('additional_projects', [])}


def logo_mark(logo_id):
    logo = c['organization_logos'][logo_id]
    return f'<span class="affiliation-logo affiliation-logo-{e(logo["style"])}" aria-hidden="true"><img src="assets/organizations/{e(logo["file"])}" width="{logo["width"]}" height="{logo["height"]}" alt=""></span>'


def project_logo(slug):
    logo_id = c['project_logos'][slug]
    name = c['organization_logos'][logo_id]['name']
    return f'<span class="project-card-logo" role="img" aria-label="{e(name)}" title="{e(name)}">{logo_mark(logo_id)}</span>'


def affiliation_link(item):
    first, _, rest = item['name'].partition(' ')
    mark = logo_mark(item['logo'])
    return f'<a href="{e(item["url"])}"><span class="affiliation-prefix">{mark}{e(first)}</span> {e(rest)}</a>'


about_labs = ''.join(
    f'<p class="lab-affiliations">At {affiliation_link(item)}, {e(item["research"])}</p>'
    for item in c['about_affiliations']['current']
)
previous = c['about_previous']
about_previous = f'<p class="lab-affiliations">{e(previous["prefix"])} {affiliation_link(previous)}, {e(previous["research"])}</p>'


def image_media(slug, css='project-media'):
    p = catalog[slug]
    image = d['pages'][slug].get('thumbnail')
    if image:
        src = 'assets/projects/' + image['file']
        alt = image['alt']
        caption = image.get('caption', 'Project visualization')
    else:
        src = 'assets/' + p.get('visual', 'robotics') + '.svg'
        alt = 'Conceptual illustration: ' + p['title']
        caption = 'Method schematic · Conceptual illustration'
    return f'''<a class="{css}" href="projects/{e(slug)}/" tabindex="-1" aria-hidden="true"><img src="{e(src)}" alt="{e(alt)}" width="1000" height="625" loading="lazy"><span class="media-caption">{e(caption)}</span></a>'''


def project_actions(slug, title, label='Project details'):
    links = f'<a class="project-more" href="projects/{e(slug)}/">{e(label)}<span class="visually-hidden">: {e(title)}</span></a>'
    page = d['pages'][slug]
    demo, website = page.get('demo_link'), page.get('project_website')
    report_info = page.get('retrospective', {})
    report = report_info.get('card_link')
    report_anchor = 'documents' if report_info.get('scope') == 'module' else 'project-report'
    if demo:
        links += f'<a class="project-website" href="projects/{e(slug)}/#{e(demo["section"])}" aria-label="Watch demo: {e(title)}">Watch demo</a>'
    if website:
        links += f'<a class="project-website" href="{e(website["url"])}" target="_blank" rel="noopener" aria-label="Project website: {e(title)}">Project website</a>'
    if report:
        links += f'<a class="project-website" href="projects/{e(slug)}/#{report_anchor}">{e(report)}</a>'
    return f'<div class="project-links">{links}</div>' if demo or website or report else links


featured = ''
for f in c['featured_projects']:
    slug = f['id']
    tags = ''.join(f'<span>{e(t)}</span>' for t in f.get('skills', []))
    result = f'<p class="featured-evidence"><strong>{e(f["evidence"]["value"])}</strong><span>{e(f["evidence"]["label"])}</span></p>' if f.get('evidence') else ''
    featured += f'''<article class="featured-card" id="research-{e(slug)}">{image_media(slug, 'featured-media')}
      <div class="featured-body"><div class="card-meta-row"><p class="feature-status {e(f.get('status_kind','research'))}">{e(f['status'])}</p>{project_logo(slug)}</div>
      <h3><a href="projects/{e(slug)}/">{e(f['title'])}</a></h3><p class="featured-summary">{e(f['summary'])}</p>
      <p class="featured-contribution"><span>My work</span>{e(f['contribution'])}</p>{result}
      <div class="feature-skills">{tags}</div>{project_actions(slug, f['title'], 'Read the project')}</div></article>'''

awards = ''.join(f'''<article class="award-card"><div class="award-topline"><p class="award-result">{e(a['result'])}</p><span class="award-logo" role="img" aria-label="{e(c['organization_logos'][a['logo']]['name'])}">{logo_mark(a['logo'])}</span></div><h3><a href="projects/{e(a['detail_id'])}/">{e(a['title'])}</a></h3><p class="meta">{e(a['venue'])} · {e(a['year'])}</p><p class="award-description">{e(a['description'])}</p></article>''' for a in c['awards'])
experience = ''
for item in c['experience']:
    fields = ' · '.join(item.get('fields', []))
    links = ''.join(f'<a href="projects/{e(link["id"])}/">{e(link["label"])}</a>' for link in item['links'])
    highlights = ''.join(f'<li>{e(text)}</li>' for text in item['highlights'])
    advisors = f'<p class="advisors">Advisors: {e(item["advisors"])}</p>' if item.get('advisors') else ''
    experience += f'''<article class="experience-card" id="experience-{e(item['id'])}"><div class="experience-topline"><p class="experience-kind">{e(item['role_type'])}</p><span class="experience-logo" role="img" aria-label="{e(c['organization_logos'][item['logo']]['name'])}">{logo_mark(item['logo'])}</span></div><p class="dates">{e(item['dates'])}</p><h3>{e(item['title'])}</h3><p class="organization">{e(item['organization'])}</p>{advisors}<p class="experience-fields">{e(fields)}</p><ul class="experience-highlights">{highlights}</ul><div class="experience-links">{links}</div></article>'''
projects = ''
for p in c['projects']:
    tags = ''.join(f'<span>{e(t)}</span>' for t in p['tags'][:3])
    actions = project_actions(p['id'], p['title'])
    projects += f'''<article class="project" id="{e(p['id'])}" data-category="{e(p['category'])}">{image_media(p['id'])}
    <div class="project-body"><div class="card-meta-row"><p class="project-meta">{e(p['label'])}</p>{project_logo(p['id'])}</div><h3><a href="projects/{e(p['id'])}/">{e(p['title'])}</a></h3>
    <p class="meta">{e(p['dates'])}</p><p class="organization">{e(p['organization'])}</p><p>{e(p['description'])}</p><div class="tags">{tags}</div>{actions}</div></article>'''
education = ''.join(f'''<article class="education-item"><p class="education-year">{e(a['year'])}</p><h3>{e(a['degree'])}</h3><p>{e(a['school'])}</p><p class="meta">{e(a['detail'])}</p></article>''' for a in c['education'])
skills = ''.join(f'<span>{e(s)}</span>' for s in c['skills'])
interests = ''.join(f'<li>{e(s)}</li>' for s in c['research_interests'])
cvs = ''.join(f'''<a class="cv-download" href="assets/{e(v['file'])}"><strong>{e(v['title'])}</strong><span>{e(v['detail'])} · PDF</span></a>''' for v in c['cv_downloads'])
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light"><title>Haoliang Huang | Embodied AI &amp; Robotics</title>
<meta name="description" content="Haoliang Huang — VLA, world–action models, agentic manipulation, robot in-context learning, and 3D vision. Research at TUM and LMU Munich.">
<meta name="author" content="Haoliang Huang"><link rel="canonical" href="{SITE}">
<meta property="og:type" content="profile"><meta property="og:title" content="Haoliang Huang | Embodied AI &amp; Robotics"><meta property="og:description" content="Selected research, robot systems, competition projects, and CV."><meta property="og:url" content="{SITE}"><meta property="og:image" content="{SITE}assets/portrait-personal.webp">
<meta name="twitter:card" content="summary"><meta name="theme-color" content="#173f58"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{asset_url('assets/styles.css')}"><link rel="stylesheet" href="{asset_url('assets/featured.css')}"><link rel="stylesheet" href="{asset_url('assets/navigation.css')}"><script src="{asset_url('assets/navigation.js')}" defer></script><script src="{asset_url('assets/site.js')}" defer></script>
<link rel="stylesheet" href="{asset_url('assets/project-links.css')}">
<link rel="stylesheet" href="{asset_url('assets/profile-sections.css')}">
<link rel="stylesheet" href="{asset_url('assets/site-effects.css')}"><script src="{asset_url('assets/site-effects.js')}" defer></script>
</head><body><a class="skip-link" href="#main">Skip to content</a>
{render_navigation(c)}
<main class="page" id="main">
<section class="bio" id="about" aria-labelledby="name"><div class="bio-text"><p class="eyebrow">AI &amp; Robotics</p><h1 id="name">Haoliang Huang</h1><p class="research-line">Embodied AI, VLA &amp; World–Action Models<br>Agentic Manipulation</p><p class="intro">{e(c['intro'])}</p>{about_labs}{about_previous}<p class="bio-summary">{e(c['focus'])}</p><p class="bio-summary">{e(c['focus_outlook'])}</p><div class="bio-links"><a class="button button-primary" href="#cv">View CVs</a><a href="{e(c['github'])}">GitHub</a><a href="mailto:{e(c['email'])}">Email</a></div></div><figure class="bio-photo" aria-label="Photos of Haoliang Huang"><div class="portrait-image"><img id="profile-photo" src="assets/portrait-personal.webp" alt="Haoliang Huang wearing a black hat" width="1200" height="1599" fetchpriority="high"></div><figcaption><div class="portrait-caption">Based in Munich<span>TUM · LMU TRESP Lab</span></div><div class="portrait-picker" role="group" aria-label="Choose a portrait photo" hidden><button type="button" data-portrait-src="assets/portrait-personal.webp" data-portrait-alt="Haoliang Huang wearing a black hat" aria-label="Show personal photo" aria-pressed="true"><img src="assets/portrait-personal.webp" alt="" width="44" height="52"></button><button type="button" data-portrait-src="assets/portrait.jpg" data-portrait-alt="Formal portrait of Haoliang Huang" aria-label="Show formal portrait" aria-pressed="false"><img src="assets/portrait.jpg" alt="" width="44" height="52"></button></div></figcaption></figure></section>
<section class="awards-section" id="awards" aria-labelledby="awards-heading"><div class="awards-intro"><p class="eyebrow">{e(c['awards_intro']['eyebrow'])}</p><h2 id="awards-heading">{e(c['awards_intro']['title'])}</h2><p>{e(c['awards_intro']['description'])}</p></div><div class="awards-grid">{awards}</div></section>
<section class="section featured-section" id="featured" aria-labelledby="featured-heading"><div class="section-title"><div><p class="eyebrow">Selected work</p><h2 id="featured-heading">Research &amp; competitions</h2></div></div><p class="section-description">From visual representations and demonstration data to models that act. Six projects across ongoing research, completed systems, and lessons from exploration.</p><div class="featured-grid">{featured}</div></section>
<section class="research-summary" aria-labelledby="research-heading"><div><p class="eyebrow">Research interests</p><h2 id="research-heading">Learning to perceive,<br>reason, and act.</h2></div><ul class="interest-list">{interests}</ul></section>
<section class="section" id="experience" aria-labelledby="experience-heading"><div class="section-title"><div><p class="eyebrow">Research &amp; industry</p><h2 id="experience-heading">Experience</h2></div></div><p class="section-description">Student research roles, an industry internship, and ongoing collaborations at TUM and LMU.</p><div class="experience-grid">{experience}</div></section>
<section class="section" id="projects" aria-labelledby="projects-heading"><div class="section-title"><div><p class="eyebrow">Further work</p><h2 id="projects-heading">Project archive</h2></div><span id="project-count" aria-live="polite">{len(c['projects'])} projects</span></div><p class="section-description">Research projects, practical courses, and thesis work in robotics, vision, and machine learning. Each project includes its methods, data, and my role.</p><div class="filters" role="group" aria-label="Filter projects by research area" hidden><button type="button" data-filter="all" aria-pressed="true">All projects</button><button type="button" data-filter="robotics" aria-pressed="false">Robotics</button><button type="button" data-filter="vision" aria-pressed="false">Computer vision</button><button type="button" data-filter="learning" aria-pressed="false">Machine learning</button><button type="button" data-filter="systems" aria-pressed="false">Software systems</button></div><div class="projects">{projects}</div></section>
<section class="section" id="education" aria-labelledby="education-heading"><div class="section-title"><div><p class="eyebrow">Academic background</p><h2 id="education-heading">Education</h2></div></div><div class="education-list">{education}</div></section>
<section class="section skills-section" id="skills" aria-labelledby="skills-heading"><div><h2 id="skills-heading">Technical skills</h2><div class="skills">{skills}</div></div><div><h2>Languages</h2><p>{e(c['languages'])}</p></div></section>
<section class="section cv-section" id="cv" aria-labelledby="cv-heading"><div class="section-title"><div><p class="eyebrow">November 2026</p><h2 id="cv-heading">Curriculum vitae</h2></div></div><p class="section-description">A complete research and project CV, plus focused English and Chinese versions for embodied AI and robotics roles.</p><div class="cv-downloads">{cvs}</div></section>
<section class="contact-section" id="contact" aria-labelledby="contact-heading"><div><p class="eyebrow">Research &amp; collaboration</p><h2 id="contact-heading">Let’s talk robotics.</h2></div><a href="mailto:{e(c['email'])}">{e(c['email'])}</a></section>
</main><footer class="footer"><div><span>© 2026 Haoliang Huang · Updated November 2026</span><span>Design adapted from <a href="https://github.com/kody1126/academic-portfolio">Academic Portfolio</a>.</span><a href="#about">Back to top</a></div></footer></body></html>'''
(ROOT/'index.html').write_text(html)
print(f'Built homepage and {render_all(ROOT,c,d)} project pages.')
