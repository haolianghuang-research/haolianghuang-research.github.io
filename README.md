# Haoliang Huang — Research Homepage

Personal research portfolio and CV, hosted at https://haolianghuang-research.github.io/.

## Update content

Edit `content.json` for the homepage and `project-details.json` for project pages, then run:

```sh
python3 build.py
```

Commit the JSON content, regenerated `index.html`, `projects/` pages, and `sitemap.xml`, then push to `main`. GitHub Pages serves the repository root. No build service, package installation, or JavaScript framework is required. To preview locally, run `python3 -m http.server 8000` and open http://localhost:8000.

Each project detail contains a task summary, workflow schematic, technical sections, selected figures, and related public resources. Put approved images under `assets/projects/`, add their dimensions and captions in the JSON, and retain attribution in [ASSET-CREDITS.md](ASSET-CREDITS.md). Original private reports, raw configurations, and the local evidence index are kept outside this public repository.

`content.json` also defines the ordered `featured_projects` list. Those entries reference the project metadata in the main catalog or `additional_projects` and appear before awards, experience, and the longer project list. Featured detail pages use `status`, `strengths`, and an explicit contribution section. Current research, incomplete prototypes, and competition placements have distinct labels. Recorded results stay attached to their specific checkpoint, data split, and evaluation protocol.

Replace `assets/Haoliang-Huang-CV.pdf` when updating the public CV. Keep private addresses and phone numbers out of this public repository. The current PDF is a public copy of the September 2026 CV; the original remains unchanged locally.

## Design credits

Adapted from [Jon Barron's academic website](https://github.com/jonbarron/jonbarron.github.io), whose README permits personal reuse. The page and project-row structure and base stylesheet are customized for this portfolio. Original source reference: `jonbarron/jonbarron.github.io`, `master`, retrieved 2026-11-18. No original research text, papers, analytics, photographs, or domain settings from that website are included.

The original SVG illustrations are conceptual diagrams. Project detail pages also use real figures extracted from project reports, experiment notebooks, and presentations, with provenance in their captions. Workflow schematics summarize the documented methods. The portrait is extracted from Haoliang Huang's CV. Lato font files are distributed under the SIL Open Font License; see `assets/OFL-Lato.txt`.
