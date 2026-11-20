# Haoliang Huang — Research Homepage

Personal research portfolio and CV, hosted at https://haolianghuang-research.github.io/.

## Update content

Edit `content.json` for the homepage and `project-details.json` for project pages, then run:

```sh
python3 build.py
```

Commit the JSON content, regenerated `index.html`, `projects/` pages, and `sitemap.xml`, then push to `main`. GitHub Pages serves the repository root. No build service, package installation, or JavaScript framework is required. To preview locally, run `python3 -m http.server 8000` and open http://localhost:8000.

Each project detail contains a task summary, workflow schematic, technical sections, selected figures, and related public resources. Put approved images under `assets/projects/`, add their dimensions and captions in the JSON, and retain attribution in [ASSET-CREDITS.md](ASSET-CREDITS.md). Original private reports, raw configurations, and the local evidence index are kept outside this public repository.

`about_affiliations.current` defines the three current research affiliations and their links. The complete prose introduction keeps a small 16px-high university logo inline beside each team name, including LMU’s green wordmark. `organization_logos` supplies the shared asset metadata, and `project_logos` explicitly assigns a logo to every project. Both selected-research and archive cards show a small mark beside their existing metadata. Official assets live in `assets/organizations/`; source attribution is retained in `ASSET-CREDITS.md`.

`content.json` also defines the ordered `featured_projects` list. Those entries reference the project metadata in the main catalog or `additional_projects` and appear after the compact award highlights and before experience and the project archive. Featured detail pages use `status`, `strengths`, and an explicit contribution section. Ongoing research, discontinued prototypes, and competition placements have distinct labels. Recorded results stay attached to their specific checkpoint, data split, and evaluation protocol.

The `cv_downloads` list links three public November 2026 PDFs: the full English CV, the focused AI & Robotics English CV, and its Chinese version. Keep private addresses and phone numbers out of the public repository. These copies have the private phone number physically removed; the original local documents remain unchanged.

## Design credits

The current visual design adapts [Academic Portfolio by Kody](https://github.com/kody1126/academic-portfolio) (MIT): system typography, the large profile heading, rounded portrait frame, blue CV action, and image-led project cards. The upstream copyright and permission notice are retained in [assets/Academic-Portfolio-LICENSE.txt](assets/Academic-Portfolio-LICENSE.txt). All photographs, project content, and CVs are Haoliang Huang’s existing reviewed material; none of the template author’s personal content is copied.

The original portfolio foundation also credited [Jon Barron’s academic website](https://github.com/jonbarron/jonbarron.github.io). Retained figures and illustrations are documented in [ASSET-CREDITS.md](ASSET-CREDITS.md). The stored Lato font files retain their SIL Open Font License; the current visual design uses system fonts.

## Images and detail pages

Each page can define `thumbnail` and `hero_image` objects with `file`, `alt`, and `caption`. Cover images should show attributable project material; captions identify synthetic data, intermediate outputs, archived views, and conceptual illustrations. Set `technical: true` on a section to place implementation detail in an expandable block. The `related` list links connected project pages. Project category filters work without a build dependency; all projects remain visible when JavaScript is unavailable.

Sections can also define a `figures` list using the same image fields plus intrinsic `width` and `height`. Images then appear alongside the method or result they explain. Set `figure_layout: "pair"` for two related comparisons; the pair stacks on small screens. Figures open at full size through ordinary accessible links. CSS and JavaScript asset URLs include content hashes so published updates refresh reliably.

## Site navigation

`navigation.py` renders the four primary links and a document outline. The homepage outline lists every major section and the six selected projects; each project detail page supplies its own method, data, evaluation, and visual sections. `assets/navigation.css` provides the pinned left desktop panel and a native-dialog drawer that slides in from the left. At widths of at least 1480px, the outline opens alongside the content; narrower screens open it with **Contents**. Desktop collapse preference lasts for the browser session.

The full-width sticky header keeps the brand at the left edge regardless of the outline state. The pinned outline is 220px wide and starts below the measured header height; only the main content and footer reserve a left column. The narrower modal drawer is 280px wide, and its backdrop starts below the header.

`assets/navigation.js` maintains the current section, reading progress, keyboard closing, native modal focus behavior, and measured header height used for the outline and anchor offsets. Project cards use stable `research-<slug>` anchors; regular project and CV URLs are preserved. Optional technical sections open when their anchors are followed. The navigation has a static no-JavaScript fallback.
