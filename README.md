# Maya Whitfield — Academic Site (Quarto + Python)

## What's in here

- `_quarto.yml` — site config: nav, footer, theme
- `index.qmd` — homepage
- `research.qmd` — research statement (+ a live Python/matplotlib chart)
- `references.bib` — your publications, one BibTeX entry each (the only
  file you need to touch to add a paper)
- `pubs_lib.py` — shared Python helpers that parse `references.bib`
  (author formatting, per-type "stamp" labels, BibTeX re-export)
- `publications.qmd` — renders each entry as a catalog card, with a "Cite"
  link that expands the raw BibTeX for that one paper, and a
  "Download all as BibTeX" link at the top
- `cv.qmd` — CV summary, PDF download link, and the same publications as a
  compact numbered list (initials style, CV-appropriate)
- `notes.qmd` + `notes/*.qmd` — a blog-style listing; each note is its own
  file and can contain executable Python code
- `contact.qmd` — contact info
- `styles/custom.scss` — theme (colors, fonts, Bootstrap overrides)
- `styles/extra.css` — the hero, index-card, catalog-stamp, and cite-box components
- `build.py` — Python wrapper around the `quarto` CLI (`python build.py render`,
  `preview`, `publish`, `check`) — handy for scripts, CI, or if you'd rather
  not type raw `quarto` commands

## 1. Install Quarto + Python deps (one time)

```bash
# Quarto CLI: download the installer for your OS from
# https://quarto.org/docs/get-started/

pip install -r requirements.txt
```

## 2. Preview locally (live-reloads as you edit)

```bash
quarto preview
# or, from Python:
python build.py preview
```

## 4. Build the static site

```bash
quarto render
# or, from Python:
python build.py render                       # whole site
python build.py render --file cv.qmd          # single page
python build.py check                         # verify quarto + deps installed
```

Output goes to `_site/` — that folder is a complete static website.

## 5. Deploy

**GitHub Pages (recommended, free):**
1. Push this folder to a GitHub repo.
2. `quarto publish gh-pages` (or `python build.py publish`) — builds and
   pushes `_site/` to a `gh-pages` branch and gives you a live URL.

**Netlify / Vercel:** connect the repo, set build command `quarto render`
and publish directory `_site`.

**Any static host:** just upload the contents of `_site/` after running
`quarto render`.
