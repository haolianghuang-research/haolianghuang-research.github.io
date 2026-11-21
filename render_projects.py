"""Render static, accessible project pages using the shared portfolio style."""
from html import escape as e
from navigation import render_navigation, asset_url


def render_figure(f):
    img = '../../assets/projects/' + e(f['file'])
    return f'<figure><a href="{img}" aria-label="Open full-size image: {e(f["alt"])}"><img src="{img}" alt="{e(f["alt"])}" width="{f.get("width",1400)}" height="{f.get("height",900)}" loading="lazy"></a><figcaption>{e(f["caption"])}</figcaption></figure>'


def render_timeline(info, slug):
    items = ''
    for item in info['entries']:
        focused = item.get('project') == slug
        item_class = ' class="timeline-focus"' if focused else ''
        period = e(item['period'])
        if item.get('date_iso'):
            period = f'<time datetime="{e(item["date_iso"])}">{period}</time>'
        title = e(item['title'])
        if item.get('url'):
            target = '#contribution' if focused else item['url']
            title = f'<a href="{e(target)}">{title}</a>'
        label = item.get('label') or ('This project' if focused else '')
        badge = f'<span class="timeline-label">{e(label)}</span>' if label else ''
        items += f'<li{item_class}><p class="timeline-period">{period}</p><div class="timeline-entry"><h3>{title}</h3>{badge}<p>{e(item["description"])}</p></div></li>'
    note = f'<p class="timeline-note">{e(info["note"])}</p>' if info.get('note') else ''
    return f'<section class="project-timeline" id="timeline" aria-labelledby="timeline-heading"><p class="eyebrow">Research timeline</p><h2 id="timeline-heading">{e(info["title"])}</h2><p class="timeline-intro">{e(info["intro"])}</p><ol class="timeline-list">{items}</ol>{note}</section>'


def render_system_diagram(root, info):
    svg = (root / 'assets' / 'projects' / info['file']).read_text()
    controls = ''.join(f'<button type="button" data-architecture-view="{e(v["id"])}" aria-pressed="{str(i == 0).lower()}" aria-controls="architecture-panel-{e(v["id"])}">{e(v["label"])}</button>' for i,v in enumerate(info['views']))
    panels = ''
    for i,v in enumerate(info['views']):
        steps = ''.join(f'<li><strong>{e(s["title"])}</strong><p>{e(s["text"])}</p></li>' for s in v['steps'])
        hidden = ' hidden' if i else ''
        panels += f'<section class="architecture-panel" id="architecture-panel-{e(v["id"])}" data-architecture-panel="{e(v["id"])}" aria-labelledby="architecture-view-{e(v["id"])}"{hidden}><h3 id="architecture-view-{e(v["id"])}">{e(v["title"])}</h3><p>{e(v["description"])}</p><ol>{steps}</ol></section>'
    return f'''<section class="system-architecture" id="system-architecture" data-architecture-focus="system" aria-labelledby="system-architecture-heading"><div class="architecture-heading"><div><p class="eyebrow">System at a glance</p><h2 id="system-architecture-heading">{e(info['title'])}</h2></div><a class="text-link architecture-fullsize" href="../../assets/projects/{e(info['file'])}">Open full-size diagram</a></div><p class="architecture-intro">{e(info['intro'])}</p><div class="architecture-controls" role="group" aria-label="Choose an architecture view" hidden>{controls}</div><figure class="architecture-canvas">{svg}<figcaption>{e(info['caption'])}</figcaption></figure><div class="architecture-legend" aria-label="Diagram colors"><span class="architecture-key-agent">Agent reasoning</span><span class="architecture-key-control">VLA and action loop</span><span class="architecture-key-shared">Shared subtask state</span></div><div class="architecture-panels">{panels}</div></section>'''


def render_retrospective(info):
    cards = ''
    for item in info['editions']:
        href = '../../assets/reports/' + e(item['file'])
        cover = '../../assets/projects/' + e(item['cover'])
        size = f'{item["bytes"] / 1024 / 1024:.1f} MB'
        cards += f'''<article class="retrospective-card"><a class="retrospective-cover" href="{href}#view=FitH" target="_blank" rel="noopener" aria-label="Read {e(item['title'])}"><img src="{cover}" alt="{e(item['title'])} cover" width="420" height="594" loading="lazy"></a><div><p class="retrospective-edition">{e(item['language'])} · {item['pages']} pages · {size}</p><h3 lang="{e(item['lang'])}">{e(item['title'])}</h3><p class="retrospective-description">{e(item['description'])}</p><div class="retrospective-actions"><a href="{href}#view=FitH" target="_blank" rel="noopener" type="application/pdf">Read PDF</a><a href="{href}" download type="application/pdf">Download</a></div></div></article>'''
    eyebrow = info.get('eyebrow', 'Illustrated project report · November 2026')
    return f'''<section class="project-retrospective" id="project-report" aria-labelledby="retrospective-heading"><p class="eyebrow">{e(eyebrow)}</p><h2 id="retrospective-heading">{e(info['title'])}</h2><p class="retrospective-intro">{e(info['description'])}</p><div class="retrospective-editions">{cards}</div></section>'''


def render_documents(documents, description=None, aliases=()):
    if not documents:
        return ''
    cards = ''
    for item in documents:
        href = '../../assets/reports/' + e(item['file'])
        download_name = e(item['file'].replace('/', '-'))
        size = f'{item["bytes"] / 1024 / 1024:.1f} MB' if item['bytes'] >= 1024 * 1024 else f'{round(item["bytes"] / 1024)} KB'
        pages = f'{item["pages"]} page' + ('s' if item['pages'] != 1 else '')
        format_label = 'Original PDF' if item['format'] == 'Original PDF' else 'PDF export'
        note = f'<p class="document-note">{e(item["note"])}</p>' if item.get('note') else ''
        if item.get('public_copy'):
            note += '<p class="document-note">Public copy: personal identifiers removed.</p>'
        cards += f'''<article class="document-card"><div class="document-heading"><span class="document-format" aria-hidden="true">PDF</span><div><p class="document-kind">{e(item['kind'])} · {e(format_label)}</p><h3>{e(item['title'])}</h3><p class="document-meta">{e(pages)} · {e(size)} · {e(item['language'])}</p>{note}</div></div><div class="document-actions"><a href="{href}#view=FitH" target="_blank" rel="noopener" type="application/pdf" aria-label="View PDF: {e(item['title'])}">View PDF</a><a href="{href}" download="{download_name}" type="application/pdf" aria-label="Download PDF: {e(item['title'])}">Download</a></div></article>'''
    intro = description or 'Project reports, theses and retained presentations in their original language. Presentations are provided as static PDF exports; personal identifiers are removed where necessary.'
    anchors = ''.join(f'<span class="document-anchor" id="{e(alias)}" aria-hidden="true"></span>' for alias in aliases)
    return f'''<section class="detail-section project-documents" id="documents" aria-labelledby="documents-heading">{anchors}<h2 id="documents-heading">Original documents</h2><p class="documents-intro">{e(intro)}</p><div class="document-list">{cards}</div></section>'''


def render_section(s):
    technical = s.get('technical', False)
    if technical:
        out = f'<details class="detail-section technical-detail" id="{e(s["id"])}"><summary>{e(s["title"])}</summary><div class="technical-body">'
    else:
        section_class = 'detail-section project-overview-demo' if s.get('overview') else 'detail-section'
        out = f'<section class="{section_class}" id="{e(s["id"])}"><h2>{e(s["title"])}</h2>'
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
    if s.get('figures'):
        layout = ' figure-pair' if s.get('figure_layout') == 'pair' else ''
        out += f'<div class="section-figures{layout}">' + ''.join(render_figure(f) for f in s['figures']) + '</div>'
    if s.get('videos'):
        video_layout = ' video-pair' if s.get('video_layout') == 'pair' else ''
        comparison = ' data-video-comparison' if s.get('comparison') else ''
        if comparison:
            out += f'<div class="video-comparison"{comparison}>'
            out += '<div class="comparison-controls"><button type="button" data-play-comparison>Play both</button><span>Each clip keeps its original export timing.</span></div>'
        out += f'<div class="section-figures project-videos{video_layout}">'
        for v in s['videos']:
            src = '../../assets/projects/' + e(v['file'])
            poster = '../../assets/projects/' + e(v['poster'])
            width, height = v.get('width', 1920), v.get('height', 1080)
            video_class = ' class="portrait-video"' if height > width else ''
            download = f'<a class="video-download" href="{src}" download aria-label="Download video: {e(v["title"])}">Download video</a>' if v.get('download') else ''
            heading = f'<h3 class="video-heading">{e(v["heading"])}</h3>' if v.get('heading') else ''
            out += f'<figure{video_class}>{heading}<video controls playsinline preload="none" poster="{poster}" width="{width}" height="{height}" style="aspect-ratio:{width}/{height}" aria-label="{e(v["title"])}"><source src="{src}" type="video/mp4">Your browser does not support video. <a href="{src}">Download the replay</a>.</video><figcaption>{e(v["caption"])}{download}</figcaption></figure>'
        out += '</div>' + ('</div>' if comparison else '')
    if s.get('video_embed'):
        v = s['video_embed']
        out += f'<div class="section-figures"><figure class="project-video-embed"><div class="video-embed-player"><iframe src="{e(v["url"])}" title="{e(v["title"])}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe></div><figcaption>{e(v["caption"])} <a class="video-download" href="{e(v["watch_url"])}" target="_blank" rel="noopener">Watch on YouTube</a></figcaption></figure></div>'
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
        timeline_info = d.get('timeline') or details.get('research_timelines', {}).get(d.get('research_timeline'))
        timeline = render_timeline(timeline_info, slug) if timeline_info else ''
        timeline_assets = f'<link rel="stylesheet" href="../../{asset_url("assets/project-timeline.css")}">' if timeline else ''
        system = render_system_diagram(root, d['system_diagram']) if d.get('system_diagram') else ''
        architecture_assets = f'<link rel="stylesheet" href="../../{asset_url("assets/system-architecture.css")}"><script src="../../{asset_url("assets/system-architecture.js")}" defer></script>' if system else ''
        body_sections = ([d['overview_demo']] if d.get('overview_demo') else []) + d.get('intro_sections', []) + d['sections']
        report_info = d.get('retrospective')
        project_report = report_info if report_info and report_info.get('scope', 'project') == 'project' else None
        module_report = report_info if report_info and report_info.get('scope') == 'module' else None
        report = render_retrospective(project_report) if project_report else ''
        report_after = project_report.get('after_section') if project_report else None
        report_at_top = report if not report_after else ''
        report_outline = project_report.get('outline_title', 'Illustrated report') if project_report else ''
        resource_note = f'<p class="detail-resource-note">{e(d["resource_note"])}</p>' if d.get('resource_note') else ''
        report_assets = f'<link rel="stylesheet" href="../../{asset_url("assets/project-retrospective.css")}">' if report else ''
        archived_documents = list(d.get('documents', []))
        archive_intro = None
        archive_aliases = ()
        if module_report:
            for edition in module_report['editions']:
                archived_documents.append({
                    'file':edition['file'], 'title':edition['title'], 'language':edition['language'],
                    'kind':module_report.get('eyebrow', 'Module report'), 'format':'Original PDF',
                    'pages':edition['pages'], 'bytes':edition['bytes'], 'note':edition['description']
                })
            archive_intro = module_report.get('archive_intro')
            archive_aliases = ('project-report',)
        documents = render_documents(archived_documents, archive_intro, archive_aliases)
        document_assets = f'<link rel="stylesheet" href="../../{asset_url("assets/project-documents.css")}">' if documents else ''
        # Only reviewed whole-project summaries belong in the hero. Module
        # documents stay in the archive; videos stay in their body sections.
        summary_documents = [item for item in d.get('documents', []) if item.get('scope') == 'project' and item.get('resource_label')]
        summary_editions = project_report['editions'] if project_report else []
        website_link = ''
        for item in summary_editions + summary_documents:
            href = '../../assets/reports/' + e(item['file'])
            label = item.get('resource_label') or item['title']
            button_style = 'button-secondary' if website_link else 'button-primary'
            website_link += f'<a class="button {button_style}" href="{href}#view=FitH" target="_blank" rel="noopener" type="application/pdf">{e(label)}</a>'
        if documents:
            button_style = 'button-secondary' if website_link else 'button-primary'
            website_link += f'<a class="button {button_style}" href="#documents">Original documents</a>'
        if website_link:
            website_link = f'<nav class="detail-project-links" aria-label="Project resources">{website_link}</nav>'
        website_assets = f'<link rel="stylesheet" href="../../{asset_url("assets/project-links.css")}">' if website_link else ''
        if any(s.get('videos') or s.get('video_embed') for s in body_sections):
            website_assets += f'<link rel="stylesheet" href="../../{asset_url("assets/robot-demos.css")}">'
        if any(s.get('comparison') for s in body_sections):
            website_assets += f'<script src="../../{asset_url("assets/project-media.js")}" defer></script>'
        method = ''
        if d.get('pipeline') and not system:
            nodes = ''.join(f'<li><span class="step-number">0{i+1}</span><strong>{e(n["title"])}</strong><span>{e(n["text"])}</span></li>' for i,n in enumerate(d['pipeline']))
            method = f'<section class="pipeline-section" id="method-at-a-glance" aria-labelledby="pipeline-heading"><p class="eyebrow">Method at a glance</p><h2 id="pipeline-heading">{e(d.get("pipeline_title", "How it works"))}</h2><ol class="method-pipeline">{nodes}</ol><p class="diagram-caption">Project workflow schematic.</p></section>'
        section_links = ''.join(f'<a href="#{e(s["id"])}">{e(s["title"])}</a>' for s in d['sections'])
        outline = [{"id":"overview","title":"Overview"}]
        if timeline: outline.append({'id':'timeline','title':'Research timeline'})
        if report and not report_after: outline.append({'id':'project-report','title':report_outline})
        if system: outline.append({"id":"system-architecture","title":"System architecture"})
        if method: outline.append({"id":"method-at-a-glance","title":"Method at a glance"})
        for section in body_sections:
            outline.append({'id':section['id'],'title':section['title']})
            if report_after == section['id']:
                outline.append({'id':'project-report','title':report_outline})
        sections = ''.join(render_section(section) + (report if report_after == section['id'] else '') for section in body_sections)
        gallery = ''
        if d.get('gallery'):
            gallery = '<section class="detail-section" id="visuals"><h2>Project visuals</h2><div class="project-gallery">'
            for f in d['gallery']:
                gallery += render_figure(f)
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
        if gallery: outline.append({'id':'visuals','title':'Project visuals'})
        if documents: outline.append({'id':'documents','title':'Original documents'})
        if refs: outline.append({'id':'references','title':'Related resources'})
        back_target = '../../#experience' if d.get('experience') else ('../../#featured' if d.get('featured') else '../../#projects')
        back_label = 'Back to experience' if d.get('experience') else 'Back to projects'
        nav_section = 'experience' if d.get('experience') else ('featured' if d.get('featured') else 'projects')
        og_image = f'<meta property="og:image" content="https://haolianghuang-research.github.io/assets/projects/{e(image["file"])}">' if image else ''
        html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<title>{e(p['title'])} | Haoliang Huang</title><meta name="description" content="{e(d['summary'])}"><meta name="author" content="Haoliang Huang"><link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(p['title'])} | Haoliang Huang"><meta property="og:description" content="{e(d['summary'])}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}">{og_image}
<meta name="theme-color" content="#173f58"><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="../../{asset_url('assets/styles.css')}"><link rel="stylesheet" href="../../{asset_url('assets/project-details.css')}"><link rel="stylesheet" href="../../{asset_url('assets/navigation.css')}">{architecture_assets}{document_assets}{website_assets}{report_assets}{timeline_assets}<script src="../../{asset_url('assets/navigation.js')}" defer></script><script src="../../{asset_url('assets/project-details.js')}" defer></script><link rel="stylesheet" href="../../{asset_url('assets/site-effects.css')}"><script src="../../{asset_url('assets/site-effects.js')}" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>{render_navigation(content, '../../', nav_section, outline, p['title'])}
<main class="detail-page" id="main"><a class="back-link" href="{back_target}">{back_label}</a><div class="detail-hero" id="overview"><div class="detail-heading"><p class="eyebrow">{e(p['label'])}</p>{status}<h1>{e(p['title'])}</h1><p class="detail-lead">{e(d['summary'])}</p><p class="detail-affiliation">{e(p['organization'])}<span>{e(p['dates'])} · {e(p['type'])}</span></p>{resource_note}{website_link}</div>{hero_image}</div><dl class="project-facts{facts_style}">{facts}</dl>
{timeline}{report_at_top}{system}<div class="detail-layout"><article class="detail-content">{method}{sections}{gallery}{documents}{refs}<p class="source-note">{e(d.get('source_note','Based on my project report and implementation.'))}</p></article></div>{related}
<section class="detail-bottom"><a href="../../#featured">Explore selected research</a><a href="mailto:{e(content['email'])}">Discuss this project</a></section></main><footer class="footer"><div><span>© 2026 Haoliang Huang</span><span>Research portfolio · November 2026</span><a href="../../">Home</a></div></footer></body></html>'''
        destination = root/'projects'/slug
        destination.mkdir(parents=True,exist_ok=True)
        (destination/'index.html').write_text(html)
        urls.append(canonical)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{e(u)}</loc></url>' for u in ['https://haolianghuang-research.github.io/']+urls) + '</urlset>\n'
    (root/'sitemap.xml').write_text(xml)
    return len(urls)
