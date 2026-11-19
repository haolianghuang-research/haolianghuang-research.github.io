"""Regenerate the static homepage after editing content.json. Python 3, no dependencies."""
import json
from html import escape as e
from pathlib import Path
from render_projects import render_all

ROOT = Path(__file__).resolve().parent
d = json.loads((ROOT / "content.json").read_text())
details = json.loads((ROOT / "project-details.json").read_text())
site = "https://haolianghuang-research.github.io/"
catalog = {p['id']: p for p in d['projects']}
catalog.update({p['id']: p for p in details.get('additional_projects', [])})
featured_cards = ''
for entry in d.get('featured_projects', []):
    meta = catalog[entry['id']]
    href = f"projects/{e(entry['id'])}/"
    thumb = details['pages'][entry['id']].get('thumbnail')
    media = f'<a class="featured-media" href="{href}" tabindex="-1" aria-hidden="true"><img src="assets/projects/{e(thumb["file"])}" alt="{e(thumb["alt"])}" width="660" height="400" loading="lazy"></a>' if thumb else ''
    evidence = f'<p class="featured-evidence"><strong>{e(entry["evidence"]["value"])}</strong><span>{e(entry["evidence"]["label"])}</span></p>' if entry.get('evidence') else ''
    tags = ''.join(f'<span>{e(tag)}</span>' for tag in entry.get('skills', []))
    featured_cards += f'''<article class="featured-card">
      {media}<div class="featured-body"><p class="feature-status {e(entry.get('status_kind', 'research'))}">{e(entry['status'])}</p>
      <h3><a href="{href}">{e(entry.get('title', meta['title']))}</a></h3>
      <p class="featured-summary">{e(entry['summary'])}</p>
      <p class="featured-contribution"><span>My contribution</span>{e(entry['contribution'])}</p>
      {evidence}<div class="feature-skills">{tags}</div><a class="project-more" href="{href}">Explore project<span class="visually-hidden">: {e(meta['title'])}</span></a></div>
    </article>'''
interests = ''.join(f'<span>{e(item)}</span>' for item in d.get('research_interests', ['Robot learning & manipulation', 'Vision-language-action models', '3D perception & reconstruction', 'Autonomous driving & foundation models']))

awards = "".join(f'''<article class="award-item">
  <div class="award-top"><span>{e(a['year'])}</span><strong>{e(a['result'])}</strong></div>
  <h3><a href="projects/{e(a['detail_id'])}/">{e(a['title'])}</a></h3><p class="meta">{e(a['venue'])}</p><p>{e(a['description'])}</p>
</article>''' for a in d["awards"])
experience = "".join(f'''<article class="experience-item">
  <div class="item-heading"><h3>{e(a['title'])}</h3><span class="dates">{e(a['dates'])}</span></div>
  <p class="organization">{e(a['organization'])}</p><p>{e(a['description'])}</p>
</article>''' for a in d["experience"])
projects = ""
for p in d["projects"]:
    detail = details['pages'][p['id']]
    href = f"projects/{e(p['id'])}/"
    if detail.get('thumbnail'):
        thumb = detail['thumbnail']
        media = f'<div class="project-media actual-media"><a href="{href}" tabindex="-1" aria-hidden="true"><img src="assets/projects/{e(thumb["file"])}" width="220" height="160" alt="{e(thumb["alt"])}" loading="lazy"></a></div>'
    else:
        media = f'''<div class="project-media"><a href="{href}" tabindex="-1" aria-hidden="true"><img src="assets/{e(p['visual'])}.svg" width="220" height="160" alt="Conceptual illustration: {e(p['title'])}" loading="lazy"></a></div>''' if p.get("visual") else ""
    tags = "".join(f"<span>{e(t)}</span>" for t in p["tags"])
    projects += f'''<article class="project {'with-media' if media else 'compact'}" id="{e(p['id'])}" data-category="{e(p['category'])}">
  {media}<div class="project-body"><div class="project-meta"><span class="topic">{e(p['label'])}</span><span>{e(p['dates'])}</span></div>
  <h3><a href="{href}">{e(p['title'])}</a></h3><p class="organization">{e(p['organization'])} <span class="separator">/</span> {e(p['type'])}</p>
  <p>{e(p['description'])}</p><div class="tags" aria-label="Technologies">{tags}</div><a class="project-more" href="{href}">Project details<span class="visually-hidden">: {e(p['title'])}</span></a></div>
</article>'''
education = "".join(f'''<article class="education-item"><span class="education-year">{e(a['year'])}</span><div><h3>{e(a['degree'])}</h3><p>{e(a['school'])}</p><p class="meta">{e(a['detail'])}</p></div></article>''' for a in d["education"])
skills = "".join(f"<span>{e(s)}</span>" for s in d["skills"])

html = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>Haoliang Huang | Embodied AI, World–Action Models &amp; Agentic Robotics</title>
  <meta name="description" content="Haoliang Huang's selected research: RoleWAM, RICL with Zero-WAM, agentic driving, D4rtVLA, and award-winning robot manipulation and 6D pose systems.">
  <meta name="author" content="Haoliang Huang">
  <link rel="canonical" href="{site}">
  <meta property="og:type" content="profile">
  <meta property="og:title" content="Haoliang Huang | Robotics &amp; Embodied AI">
  <meta property="og:description" content="Research, projects, experience, and CV. Robot learning, VLA models, 3D vision, and autonomous driving.">
  <meta property="og:url" content="{site}">
  <meta property="og:image" content="{site}assets/portrait.jpg">
  <meta name="twitter:card" content="summary">
  <meta name="theme-color" content="#174c72">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="assets/lato-regular.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="assets/styles.css">
  <link rel="stylesheet" href="assets/project-details.css">
  <link rel="stylesheet" href="assets/featured.css">
  <script src="assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header"><div class="header-inner">
    <a class="wordmark" href="#about">Haoliang Huang<span class="wordmark-dot">.</span></a>
    <nav aria-label="Main navigation"><a href="#featured">Research</a><a href="#projects">Projects</a><a href="#experience">Experience</a><a href="assets/Haoliang-Huang-CV.pdf">CV <span class="pdf-label">PDF</span></a></nav>
  </div></header>
  <main class="page" id="main">
    <section class="bio" id="about" aria-labelledby="name">
      <div class="bio-text">
        <p class="eyebrow">Embodied AI · World–Action Models · Agentic Robotics</p>
        <h1 id="name" class="name">Haoliang Huang</h1>
        <p class="intro">{e(d['intro'])}</p>
        <p>{e(d['focus'])}</p>
        <div class="bio-links"><a href="mailto:{e(d['email'])}">Email</a><span aria-hidden="true">/</span><a href="{e(d['github'])}">GitHub</a><span aria-hidden="true">/</span><a href="assets/Haoliang-Huang-CV.pdf">Download CV</a></div>
      </div>
      <div class="bio-photo"><img src="assets/portrait.jpg" alt="Portrait of Haoliang Huang" width="1050" height="1050"><p>Munich, Germany<br><span>Technical University of Munich</span></p></div>
    </section>
    <section class="section featured-section" id="featured" aria-labelledby="featured-heading">
      <div class="section-title"><h2 id="featured-heading">Selected research &amp; competitions</h2></div>
      <p class="featured-intro">Model design, demonstration transfer, and agentic systems—built through data, training, deployment, and controlled evaluation.</p>
      <div class="featured-grid">{featured_cards}</div>
    </section>
    <section id="research" class="research-summary" aria-labelledby="research-heading">
      <h2 id="research-heading">Research interests</h2>
      <p>Learning to perceive, reason, and act.</p>
      <div class="interest-list">{interests}</div>
    </section>
    <section class="section" id="awards" aria-labelledby="awards-heading">
      <div class="section-title"><h2 id="awards-heading">Highlights &amp; awards</h2><span>2024–2026</span></div>
      <div class="awards-grid">{awards}</div>
    </section>
    <section class="section" id="experience" aria-labelledby="experience-heading">
      <div class="section-title"><h2 id="experience-heading">Research &amp; industry experience</h2></div>
      <div class="experience-list">{experience}</div>
    </section>
    <section class="section" id="projects" aria-labelledby="projects-heading">
      <div class="section-title"><h2 id="projects-heading">More projects</h2><span id="project-count" aria-live="polite">{len(d['projects'])} projects</span></div>
      <p class="section-description">Further research projects, practical courses, and thesis work across robotics and AI.</p>
      <div class="filters" role="group" aria-label="Filter projects by research area" hidden><button type="button" data-filter="all" aria-pressed="true">All projects</button><button type="button" data-filter="robotics" aria-pressed="false">Robotics</button><button type="button" data-filter="vision" aria-pressed="false">Computer vision</button><button type="button" data-filter="learning" aria-pressed="false">Machine learning</button><button type="button" data-filter="systems" aria-pressed="false">Software systems</button></div>
      <div class="projects">{projects}</div>
    </section>
    <section class="section" id="education" aria-labelledby="education-heading">
      <div class="section-title"><h2 id="education-heading">Education</h2></div><div class="education-list">{education}</div>
    </section>
    <section class="section skills-section" aria-labelledby="skills-heading">
      <div><h2 id="skills-heading">Technical skills</h2><div class="skills">{skills}</div></div>
      <div><h2>Languages</h2><p>{e(d['languages'])}</p></div>
    </section>
    <section class="contact-section" aria-labelledby="contact-heading"><div><h2 id="contact-heading">Get in touch</h2><p>For research discussions and collaboration.</p></div><a href="mailto:{e(d['email'])}">{e(d['email'])}</a></section>
  </main>
  <footer class="footer"><div><span>© 2026 Haoliang Huang</span><span>Adapted from <a href="https://github.com/jonbarron/jonbarron.github.io">Jon Barron's academic website</a>.</span><a href="#about">Back to top</a></div></footer>
</body>
</html>
'''
(ROOT / "index.html").write_text(html)
page_count = render_all(ROOT, d, details)
print(f"Built homepage and {page_count} project detail pages.")
