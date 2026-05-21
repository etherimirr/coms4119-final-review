# Reuse This App For Another Course

This started as a COMS 4119 final review app. It's now mostly course-agnostic.
To repurpose it for another course, you only need to swap **one config file**
and the **course-specific data files**.

---

## Quick Start (5 minutes)

```bash
# 1. Fork / copy this directory
cp -R /path/to/4119 /path/to/your-course

# 2. Replace the course config
nano your-course/app/data/course.json
# — set course.title, files[], special[], lec_topics{}

# 3. Drop your slide images + text into:
#    app/pages/<file-id>/p-<NN>.jpg
#    app/text/<file-id>.txt

# 4. Run server
cd your-course/app && python3 server.py 8788
```

Then open `http://localhost:8788/`.

---

## File Layout

```
app/
  index.html                  # framework HTML (course-agnostic)
  app.js                      # framework JS — reads data/course.json
  style.css                   # framework styling
  server.py                   # static + /api/ask + /api/upload + /api/patch-cheatsheet
  cheatsheet.html             # COURSE-SPECIFIC: 4-sheet A4 cheatsheet content
  cheatsheet-assets/          # COURSE-SPECIFIC: embedded slide images
  data/
    course.json               # ★ COURSE CONFIG — files, special tabs, lec_topics
    explanations.json         # COURSE-SPECIFIC: per-page AI explanations
    explanations_detail.json  # COURSE-SPECIFIC: hand-written overrides
    concepts.json             # COURSE-SPECIFIC: concept graph nodes + edges
    midterm.json              # COURSE-SPECIFIC: midterm Q&A (gitignored if personal)
    finalpreview.json         # COURSE-SPECIFIC: final preview Q&A
    premid-summary.md         # COURSE-SPECIFIC: pre-mid summary
    postmid-summary.md        # COURSE-SPECIFIC: post-mid summary
    postmid-checks.json       # USER STATE: checkbox progress
  pages/<file-id>/p-<NN>.jpg  # COURSE-SPECIFIC: slide screenshots
  text/<file-id>.txt          # COURSE-SPECIFIC: slide text dumps
```

---

## data/course.json reference

```json
{
  "course": {
    "id":       "<short-id>",
    "title":    "Sidebar title",
    "subtitle": "Sidebar subtitle"
  },
  "files": [
    { "id": "lec1", "label": "Lecture 1", "pages": 24, "premid": true },
    ...
  ],
  "special": [
    { "id": "overview", "label": "📚 Overview", "pages": 0 },
    ...
  ],
  "lec_topics": {
    "lec1": ["keyword1", "keyword2", ...],
    ...
  }
}
```

- **`files[]`** — each lecture / PDF. `id` matches the folder name under `pages/<id>/`. `pages` is the page count. Optional flags: `premid: true` for pre-midterm scope, `nyu: true` for reference material.
- **`special[]`** — the non-lecture tabs (overview, stars, cheat sheet, etc.). Built-in render functions exist for: `overview`, `stars`, `final`, `midterm`, `postmid`, `concepts`, `cheat`. Custom IDs need code; see `selectTab()` in `app.js`.
- **`lec_topics{}`** — used by **Cheat Sheet → Pull notes**: when a user stars a slide, the system finds the matching cheatsheet section by these keywords. Add ~5 keywords per lecture matching the section titles in `cheatsheet.html`.

---

## Building course content from scratch

### Generate slide images + text from PDFs

```bash
# from PDFs in the project root
pdftoppm -jpeg -r 150 lec1.pdf app/pages/lec1/p
pdftotext -layout lec1.pdf app/text/lec1.txt
```

### Generate AI explanations skeleton

```bash
cd app/data
python3 build_explanations.py
# → fills explanations.json with one entry per slide (title from PDF)
# → manual entries in explanations_detail.json are merged in
```

### Concepts graph

Hand-write `data/concepts.json` (nodes + edges). Format:
```json
{
  "nodes": [{"id":"tcp","label":"TCP","group":"transport","desc":"..."}, ...],
  "edges": [{"from":"tcp","to":"udp"}, ...]
}
```
Groups for color: `pre_mid`, `app`, `transport`, `network`, `link`, `wireless`, `general`.

### Cheatsheet

`app/cheatsheet.html` — A4 4-column layout. Each `<section data-key="...">` is one card. Edit in the browser via the **Cheat Sheet** tab; auto-saves back to file via `/api/patch-cheatsheet` (section-level patch, doesn't clobber other edits).

---

## What stays the same (framework)

These behave the same for any course:

- ⭐ Star slides (`S` key on a lecture page)
- 💬 Per-page Q&A via OpenAI proxy (set key via ⚙️)
- 🖍️ Highlight AI explanation text (`Y` key)
- 📥 Pull stars/Q&A/highlights into matching cheatsheet section
- 🧠 Concept graph autoplay (BFS tree traversal)
- 📝 Post-midterm summary tab with per-concept checkboxes
- 🖨️ Print to A4 / Save as PDF
- 📄 Download HTML / 📝 Word backups

---

## Optional: multi-course in one repo

To host multiple courses in the same checkout, restructure to:
```
/courses/coms4119/{course.json, cheatsheet.html, data/, pages/, text/, ...}
/courses/cs6701/{...}
/app/{app.js, style.css, server.py, index.html}
```
and add a `?course=<id>` query handler in `app.js boot()`.
Not implemented currently — single-course per checkout.
