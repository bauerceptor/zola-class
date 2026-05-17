# zola-class — Class Site

Course materials, lectures, and talks built with
[Zola](https://www.getzola.org/) and the
[Neovim theme](https://github.com/Super-Botman/neovim-theme) (vendored).

Live at: `https://bauerceptor.github.io/zola-class`

The companion main site lives at `bauerceptor/bauerceptor.github.io`.

---

## Areas

| Path | Purpose |
|------|---------|
| `/cs101/` | CS 101 course — syllabus + module/lecture hierarchy |
| `/speeches/` | Conference talks and speaker notes |

Add more courses by creating `content/COURSE-CODE/_index.md`.

---

## First-time setup

### 1. Vendor the Neovim theme

See `themes/neovim-theme/VENDOR_INSTRUCTIONS.md` for the exact commands.
This must be done before `zola serve` will work.

### 2. Install Zola

```bash
brew install zola   # macOS
# or download from https://github.com/getzola/zola/releases
# Use version 0.19.2 — same as the CI workflow
```

### 3. Serve locally

```bash
zola serve
# → http://127.0.0.1:1111
```

---

## Adding content

### New course

1. Create `content/COURSE-CODE/_index.md` with the syllabus table
2. Create `content/COURSE-CODE/module1/_index.md`
3. Add lecture files: `content/COURSE-CODE/module1/lec01-title.md`

Lecture front matter:

```toml
+++
title = "Lecture N — Topic"
date = 2025-01-15
weight = 1
description = "One sentence summary."

[extra]
lang        = "en"
course      = "COURSE-CODE"
lecture_num = N
math        = false   # true = KaTeX
mermaid     = false
copy        = true
+++
```

### Embedding slides

Place your Reveal.js HTML under `static/slides/` at any depth:

```
static/slides/course-code/module1/lecN/index.html
```

Then in the lecture Markdown:

```
{{ slides(src="/slides/course-code/module1/lecN/index.html") }}
{{ slides(src="/slides/course-code/module1/lecN/index.html", height="600") }}
```

### New talk / speech

Create `content/speeches/YYYY-MM-DD-talk-title.md`. See `demo-talk.md`
for the front matter structure.

---

## Slide deck conventions

Every Reveal.js deck should:

1. Load fonts from Google Fonts CDN: **Playfair Display** (titles),
   **Nanum Gothic** (body/headings), **JetBrains Mono** (code)
2. Use the Moon base theme as a starting point
3. Be a fully self-contained HTML file (no external asset dependencies
   other than CDN links)

Copy the header from `static/slides/cs101/module1/lec01/index.html`
as your starting template.

---

## Fonts

| Context | Font |
|---------|------|
| Page body | Barlow |
| Code blocks | JetBrains Mono |
| Slide titles | Playfair Display (inside slide HTML) |
| Slide body | Nanum Gothic (inside slide HTML) |
| Slide code | JetBrains Mono (inside slide HTML) |

---

## Keeping the menu in sync

`static/js/menu.js` must stay identical to the main site's version
except for the `SITE_NAME` variable at the top (already set to
`"Class — Your Name"` in this repo).

When you add or rename nav links, update **both repos**.

---

## Deployment

Push to `main`. GitHub Actions builds with Zola 0.19.2 and deploys
to GitHub Pages automatically.

**One-time setup:** Go to repo Settings → Pages → Source: set to
"GitHub Actions".

---

## File structure

```
zola-class/
├── config.toml
├── themes/
│   └── neovim-theme/          ← vendored; see VENDOR_INSTRUCTIONS.md
├── templates/
│   ├── _head_extend.html      ← fonts, highlight sheets, menu CSS
│   └── shortcodes/
│       └── slides.html        ← {{ slides(src="...") }}
├── static/
│   ├── css/
│   │   ├── class.css          ← Barlow font override, lecture styles
│   │   ├── menu.css           ← hamburger overlay (keep in sync)
│   │   └── copy-btn.css       ← copy button (keep in sync)
│   ├── js/
│   │   ├── menu.js            ← hamburger menu (keep in sync)
│   │   ├── theme-toggle.js    ← light/dark/system cycle
│   │   └── copy-code.js       ← copy-to-clipboard toggle
│   └── slides/
│       └── cs101/module1/lec01/index.html   ← demo deck
├── content/
│   ├── _index.md
│   ├── cs101/
│   │   ├── _index.md          ← syllabus
│   │   ├── module1/
│   │   │   ├── _index.md
│   │   │   ├── lec01-intro.md
│   │   │   └── lec02-types.md
│   │   └── module2/
│   │       ├── _index.md
│   │       └── lec03-control.md
│   └── speeches/
│       ├── _index.md
│       └── demo-talk.md
└── .github/
    └── workflows/
        └── deploy.yml
```
