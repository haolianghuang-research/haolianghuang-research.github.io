"""A compact primary navigation and a sliding outline for each document."""
from html import escape as e
from hashlib import sha256
from pathlib import Path


def asset_url(path):
    """Revalidate changed CSS and JS while keeping public document URLs stable."""
    digest = sha256((Path(__file__).parent / path).read_bytes()).hexdigest()[:10]
    return f'{path}?v={digest}'


def render_navigation(content, prefix='', current='about', outline=None, page_title=None):
    home = prefix or '#about'
    primary = [('featured','Research'),('projects','Projects'),('experience','Experience'),('cv','CV')]
    top = ''.join(f'<a href="{prefix}#{slug}" data-nav-section="{slug}"' + (' aria-current="location"' if slug == current else '') + f'>{title}</a>' for slug,title in primary)
    if outline is None:
        short = {'rolewam':'RoleWAM','ricl':'RICL / Zero-WAM','agentic-planner':'Agentic Planner','d4rtvla':'D4rtVLA / InstructD4RT','maniparena':'ManipArena · CVPR','category-pose':'6D Pose · ICCV'}
        children = [{'id':'research-'+p['id'],'title':short.get(p['id'],p['title'])} for p in content['featured_projects']]
        outline = [
            {'id':'about','title':'About'},
            {'id':'awards','title':'Awards','count':str(len(content['awards']))},
            {'id':'featured','title':'Selected research','count':str(len(children)),'children':children},
            {'id':'experience','title':'Experience'},
            {'id':'projects','title':'Project archive','count':str(len(content['projects']))},
            {'id':'education','title':'Education'},
            {'id':'skills','title':'Skills & languages'},
            {'id':'cv','title':'CV downloads','count':str(len(content['cv_downloads']))},
            {'id':'contact','title':'Contact'},
        ]
    def outline_links(items, child=False):
        html = '<ul class="outline-children">' if child else '<ul class="outline-list">'
        for item in items:
            badge = f'<span class="outline-count">{e(item["count"])}</span>' if item.get('count') else ''
            html += f'<li><a href="#{e(item["id"])}" data-outline-target="{e(item["id"])}"><span>{e(item["title"])}</span>{badge}</a>'
            if item.get('children'): html += outline_links(item['children'],True)
            html += '</li>'
        return html+'</ul>'
    items = outline_links(outline)
    fallback = ''.join(f'<a href="#{e(item["id"])}">{e(item["title"])}</a>' for item in outline)
    subtitle = page_title or 'Haoliang Huang’s portfolio'
    context = 'project' if page_title else 'home'
    return f'''<header class="site-header" data-site-navigation>
      <div class="header-inner"><a class="brand" href="{home}"><span class="brand-mark" aria-hidden="true">HH</span><span>Haoliang Huang</span></a>
      <div class="header-navigation"><nav class="top-links" aria-label="Main navigation">{top}</nav>
      <button class="contents-toggle" type="button" aria-haspopup="dialog" aria-expanded="false" aria-controls="page-outline" hidden><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M3 5h2m3 0h9M3 10h2m3 0h9M3 15h2m3 0h9"/></svg><span>Contents</span></button></div></div>
    </header>
    <dialog class="page-outline" id="page-outline" aria-labelledby="outline-heading" data-outline-context="{context}">
      <div class="outline-heading"><div><h2 id="outline-heading">{'In this project' if page_title else 'On this page'}</h2><p>{e(subtitle)}</p></div><button class="outline-close" type="button" aria-label="Close contents"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="m5 5 10 10M15 5 5 15"/></svg></button></div>
      <nav class="outline-scroll" aria-label="{'Project' if page_title else 'Page'} contents">{items}</nav>
      <div class="outline-progress"><div><span>Page progress</span><span data-reading-percent aria-hidden="true">0%</span></div><progress max="100" value="0" aria-label="Page reading progress"></progress></div>
    </dialog>
    <noscript><nav class="fallback-contents" aria-label="Page contents">{fallback}</nav></noscript>'''
