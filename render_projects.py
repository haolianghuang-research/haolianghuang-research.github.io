"""Render static, accessible project pages using the shared portfolio style."""
from html import escape as e
from navigation import render_navigation


def render_section(s):
    technical = s.get('technical', False)
    if technical:
        out = f'<details class="detail-section technical-detail" id="{e(s["id"])}"><summary>{e(s["title"])}</summary><div class="technical-body">'
    else:
        out = f'<section class="detail-section" id="{e(s["id"])}"><h2>{e(s["title"])}</h2>'
    out += ''.join(f'<p>{e(p)}</p>' for p in s.get('paragraphs', []))
    if s.get('bullets'):
        out += '<ul>' + ''.join(f'<li>{e(p)}</li>' for p in s['bullets']) + '</ul>'
    if s.get('table'):
        t = s['table']
        out += '<div class="table-scroll" tabindex="0" role="region" aria-label="' + e(s['title']) + ' data table"><table><thead><tr>'
        out += ''.join(f'<th scope="col">{e(x)}</th>' for x in t['headers']) + '</tr></thead><tbody>'
        for row in t['rows']:
            out += '<tr>' + ''.join(f'<td>{e(str(x))}</td>' for x in row) + '</tr>'
        out += '</tbody></table></div>'
    if s.get('link'):
        out += f'<a class="text-link" href="{e(s["link"]["url"])}">{e(s["link"]["title"])}</a>'
    return out + ('</div></details>' if technical else '</section>')


def render_all(root, content, details):
    catalog = {p['id']:p for p in content['projects'] + details.get('additional_projects', [])}
    urls = []
    for slug, d in details['pages'].items():
        p = catalog[slug]
        canonical = f'https://haolianghuang-research.github.io/projects/{slug}/'
        status = f'<p class="detail-status">{e(d["status"])}</p>' if d.get('status') else ''
        image = d.get('hero_image') or d.get('thumbnail')
        hero_image = ''
        if image:
            hero_image = f'<figure class="detail-cover"><img src="../../assets/projects/{e(image["file"])}" alt="{e(image["alt"])}" width="1000" height="625"><figcaption>{e(image.get("caption","Project visualization"))}</figcaption></figure>'
        facts = ''.join(f'<div><dt>{e(f["label"])}</dt><dd>{e(f["value"])}</dd></div>' for f in d.get('facts', []))
        facts_style = ' facts-four' if len(d.get('facts',[])) == 4 else ''
        method = ''
        if d.get('pipeline'):
            nodes = ''.join(f'<li><span class="step-number">0{i+1}</span><strong>{e(n["title"])}</strong><span>{e(n["text"])}</span></li>' for i,n in enumerate(d['pipeline']))
            method = f'<section class="pipeline-section" aria-labelledby="pipeline-heading"><p class="eyebrow">Method at a glance</p><h2 id="pipeline-heading">How it works</h2><ol class="method-pipeline">{nodes}</ol><p class="diagram-caption">Project workflow schematic.</p></section>'
        section_links = ''.join(f'<a href="#{e(s["id"])}">{e(s["title"])}</a>' for s in d['sections'])
        sections = ''.join(render_section(s) for s in d['sections'])
        gallery = ''
        if d.get('gallery'):
            gallery = '<section class="detail-section" id="visuals"><h2>Project visuals</h2><div class="project-gallery">'
            for f in d['gallery']:
                img = '../../assets/projects/' + e(f['file'])
                gallery += f'<figure><a href="{img}" aria-label="Open full-size image: {e(f["alt"])}"><img src="{img}" alt="{e(f["alt"])}" width="{f.get("width",1400)}" height="{f.get("height",900)}" loading="lazy"></a><figcaption>{e(f["caption"])}</figcaption></figure>'
            gallery += '</div></section>'
            section_links += '<a href="#visuals">Project visuals</a>'
        refs = ''
        if d.get('references'):
            refs = '<section class="detail-section references" id="references"><h2>Related resources</h2><ul>'
            for r in d['references']:
                refs += f'<li><a href="{e(r["url"])}">{e(r["title"])}</a>' + (f'<span>{e(r["note"])}</span>' if r.get('note') else '') + '</li>'
            refs += '</ul></section>'
            section_links += '<a href="#references">Related resources</a>'
        related = ''
        if d.get('related'):
            related = '<section class="related-projects"><p class="eyebrow">Continue exploring</p><h2>Connected projects</h2><div>'
            for related_slug in d['related']:
                q = catalog[related_slug]
                related += f'<a href="../{e(related_slug)}/"><span>{e(q["label"])}</span><strong>{e(q["title"])}</strong></a>'
            related += '</div></section>'
        back_target = '../../#featured' if d.get('featured') else '../../#projects'
        og_image = f'<meta property="og:image" content="https://haolianghuang-research.github.io/assets/projects/{e(image["file"])}">' if image else ''
        html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>{e(p['title'])} | Haoliang Huang</title><meta name="description" content="{e(d['summary'])}"><meta name="author" content="Haoliang Huang"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(p['title'])} | Haoliang Huang"><meta property="og:description" content="{e(d['summary'])}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}">{og_image}
<meta name="theme-color" content="#173f58"><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../../assets/styles.css"><link rel="stylesheet" href="../../assets/project-details.css"><link rel="stylesheet" href="../../assets/navigation.css"><script src="../../assets/navigation.js" defer></script><script src="../../assets/project-details.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>{render_navigation(content, '../../', 'featured' if d.get('featured') else 'projects')}
<main class="detail-page" id="main"><a class="back-link" href="{back_target}">Back to projects</a><div class="detail-hero"><div class="detail-heading"><p class="eyebrow">{e(p['label'])}</p>{status}<h1>{e(p['title'])}</h1><p class="detail-lead">{e(d['summary'])}</p><p class="detail-affiliation">{e(p['organization'])}<span>{e(p['dates'])} · {e(p['type'])}</span></p></div>{hero_image}</div><dl class="project-facts{facts_style}">{facts}</dl>
<div class="detail-layout"><aside><nav aria-label="On this page"><p>In this project</p>{section_links}</nav></aside><article class="detail-content">{method}{sections}{gallery}{refs}<p class="source-note">{e(d.get('source_note','Based on my project report and implementation.'))}</p></article></div>{related}
<section class="detail-bottom"><a href="../../#featured">Explore selected research</a><a href="mailto:{e(content['email'])}">Discuss this project</a></section></main><footer class="footer"><div><span>© 2026 Haoliang Huang</span><span>Research portfolio · November 2026</span><a href="../../">Home</a></div></footer></body></html>'''
        destination = root/'projects'/slug
        destination.mkdir(parents=True,exist_ok=True)
        (destination/'index.html').write_text(html)
        urls.append(canonical)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{e(u)}</loc></url>' for u in ['https://haolianghuang-research.github.io/']+urls) + '</urlset>\n'
    (root/'sitemap.xml').write_text(xml)
    return len(urls)
