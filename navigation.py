"""Shared site navigation for the homepage and project detail pages."""
from html import escape as e


def render_navigation(content, prefix='', current='about'):
    items = [
        ('about', 'About', 'Profile & research focus'),
        ('awards', 'Awards', 'CVPR · ICCV · CommonRoad'),
        ('featured', 'Research', f"{len(content['featured_projects'])} selected projects"),
        ('experience', 'Experience', 'TUM · LMU · Huawei'),
        ('projects', 'Project archive', f"{len(content['projects'])} further projects"),
        ('education', 'Education', 'TUM · KIT · HFUT'),
        ('skills', 'Skills', 'Robotics · ML · Engineering'),
        ('cv', 'CV downloads', 'Full English · Robotics · 中文'),
    ]
    links = ''
    for slug, title, description in items:
        active = ' aria-current="location"' if slug == current else ''
        links += f'<a href="{prefix}#{slug}" data-section="{slug}"{active}><span class="nav-title">{e(title)}</span><span class="nav-description">{e(description)}</span></a>'
    home = f'{prefix}#about' if not prefix else prefix
    return f'''<header class="site-header" data-site-navigation>
    <div class="header-inner"><a class="wordmark" href="{home}">Haoliang Huang<span>.</span></a>
    <div class="header-actions"><a href="mailto:{e(content['email'])}">Email</a><a href="{e(content['github'])}">GitHub</a></div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-navigation" hidden><span class="menu-icon" aria-hidden="true"><i></i><i></i><i></i></span><span class="menu-label">Menu</span></button></div>
    <div class="nav-shell" id="site-navigation"><div class="nav-mobile-heading">Explore the website</div><nav class="header-nav" aria-label="Website sections">{links}</nav></div>
    </header>'''
