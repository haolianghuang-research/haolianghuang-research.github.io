"""Render the portfolio's project detail pages with the shared site style."""
from html import escape as e
from pathlib import Path


def rich_text(value):
    """Content is plain text; references are explicit separate links."""
    return e(value)


def render_section(section):
    result = f'<section class="detail-section" id="{e(section["id"])}"><h2>{e(section["title"])}</h2>'
    for paragraph in section.get("paragraphs", []):
        result += f'<p>{rich_text(paragraph)}</p>'
    if section.get("bullets"):
        result += '<ul>' + ''.join(f'<li>{rich_text(item)}</li>' for item in section["bullets"]) + '</ul>'
    if section.get("table"):
        table = section["table"]
        result += '<div class="table-scroll"><table><thead><tr>' + ''.join(f'<th scope="col">{e(x)}</th>' for x in table["headers"]) + '</tr></thead><tbody>'
        for row in table["rows"]:
            result += '<tr>' + ''.join(f'<td>{e(str(x))}</td>' for x in row) + '</tr>'
        result += '</tbody></table></div>'
    return result + '</section>'


def render_all(root, content, details):
    catalog = {p['id']: p for p in content['projects']}
    catalog.update({p['id']: p for p in details.get('additional_projects', [])})
    rendered = []
    for slug, detail in details['pages'].items():
        p = catalog[slug]
        title = p['title']
        status = f'<p class="detail-status">{e(detail["status"])}</p>' if detail.get('status') else ''
        strengths = '<div class="detail-strengths">' + ''.join(f'<span>{e(x)}</span>' for x in detail.get('strengths', [])) + '</div>' if detail.get('strengths') else ''
        back_target = '../../#featured' if detail.get('featured') else '../../#projects'
        back_label = 'Selected research' if detail.get('featured') else 'All projects'
        canonical = f'https://haolianghuang-research.github.io/projects/{slug}/'
        facts = ''.join(f'<div><dt>{e(x["label"])}</dt><dd>{e(x["value"])}</dd></div>' for x in detail.get('facts', []))
        facts_class = 'project-facts facts-four' if len(detail.get('facts', [])) == 4 else 'project-facts'
        pipeline = ''
        if detail.get('pipeline'):
            pipeline = '<section class="pipeline-section" aria-labelledby="pipeline-title"><h2 id="pipeline-title">Method at a glance</h2><ol class="method-pipeline">'
            for node in detail['pipeline']:
                pipeline += f'<li><strong>{e(node["title"])}</strong><span>{e(node["text"])}</span></li>'
            pipeline += '</ol><p class="diagram-caption">Schematic summary of the project workflow.</p></section>'
        sections = ''.join(render_section(section) for section in detail['sections'])
        gallery = ''
        if detail.get('gallery'):
            gallery = '<section class="detail-section" id="visuals"><h2>Project visuals</h2><div class="project-gallery">'
            for f in detail['gallery']:
                img = f'../../assets/projects/{e(f["file"])}'
                gallery += f'<figure><a href="{img}" aria-label="Open full-size image: {e(f["alt"])}"><img src="{img}" alt="{e(f["alt"])}" loading="lazy" width="{f.get("width", 1400)}" height="{f.get("height", 900)}"></a><figcaption>{e(f["caption"])}</figcaption></figure>'
            gallery += '</div></section>'
        references = ''
        if detail.get('references'):
            references = '<section class="detail-section references" id="references"><h2>Related resources</h2><ul>'
            for ref in detail['references']:
                references += f'<li><a href="{e(ref["url"])}">{e(ref["title"])}</a>'
                if ref.get('note'): references += f'<span>{e(ref["note"])}</span>'
                references += '</li>'
            references += '</ul></section>'
        source_note = e(detail.get('source_note', 'Based on the project report and implementation.'))
        section_links = ''.join(f'<a href="#{e(s["id"])}">{e(s["title"])}</a>' for s in detail['sections'])
        if gallery: section_links += '<a href="#visuals">Project visuals</a>'
        if references: section_links += '<a href="#references">Related resources</a>'
        html = f'''<!doctype html>
<html lang="en"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{e(title)} | Haoliang Huang</title>
  <meta name="description" content="{e(detail['summary'])}">
  <meta name="author" content="Haoliang Huang"><link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{e(title)} | Haoliang Huang"><meta property="og:description" content="{e(detail['summary'])}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}">
  <meta name="theme-color" content="#174c72"><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../../assets/styles.css"><link rel="stylesheet" href="../../assets/project-details.css"><link rel="stylesheet" href="../../assets/featured.css">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="wordmark" href="../../">Haoliang Huang<span class="wordmark-dot">.</span></a><nav aria-label="Main navigation"><a href="../../#featured">Research</a><a href="../../#projects">Projects</a><a href="../../#experience">Experience</a><a href="../../assets/Haoliang-Huang-CV.pdf">CV <span class="pdf-label">PDF</span></a></nav></div></header>
<main id="main" class="detail-page"><div class="detail-hero"><a class="back-link" href="{back_target}">{back_label}</a><p class="eyebrow">{e(p['label'])} · {e(p['dates'])}</p>{status}<h1>{e(title)}</h1><p class="detail-lead">{e(detail['summary'])}</p><p class="detail-affiliation">{e(p['organization'])} · {e(p['type'])}</p>{strengths}<dl class="{facts_class}">{facts}</dl></div>
<div class="detail-layout"><aside><nav aria-label="On this page"><p>In this project</p>{section_links}</nav></aside><article class="detail-content">{pipeline}{sections}{gallery}{references}<p class="source-note">{source_note}</p></article></div>
<section class="detail-bottom"><a href="../../#featured">Explore selected research</a><a href="mailto:{e(content['email'])}">Discuss this project</a></section></main>
<footer class="footer"><div><span>© 2026 Haoliang Huang</span><span>Research portfolio</span><a href="../../">Home</a></div></footer>
</body></html>'''
        destination = root / 'projects' / slug
        destination.mkdir(parents=True, exist_ok=True)
        (destination / 'index.html').write_text(html)
        rendered.append(canonical)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{e(url)}</loc></url>' for url in ['https://haolianghuang-research.github.io/'] + rendered) + '</urlset>\n'
    (root / 'sitemap.xml').write_text(sitemap)
    return len(rendered)
