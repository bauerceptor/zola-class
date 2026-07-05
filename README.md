# zola-class

Hassan Aziz's class site: lectures, course notes, slides, talks.

Built with [Zola](https://www.getzola.org/) on a vendored
[Super-Botman/neovim-theme](https://github.com/Super-Botman/neovim-theme),
heavily customized with a theme switcher, WebGL aurora backdrop, foldable
sidebar, and an enhanced `:` command prompt.

**Live**: <https://bauerceptor.github.io/zola-class/>

---

## Quickstart

```bash
git clone git@github.com:bauerceptor/zola-class.git
cd zola-class

# Install Zola 0.19.2 (must match CI)
brew install zola              # macOS
# or download from https://github.com/getzola/zola/releases

zola serve                     # http://127.0.0.1:1111
```

The Neovim theme is vendored under `themes/neovim-theme/`, so no submodule
fetch is required. To re-vendor a newer version, see
[Re-vendoring the theme](#re-vendoring-the-theme).

---

## Project layout

```
.
├── config.toml                  Site config (base_url, theme, [extra])
├── content/                     All site content (Markdown)
│   ├── _index.md                Root section frontmatter
│   ├── readme.md                Homepage body (rendered by theme index.html)
│   ├── cs101/
│   │   ├── _index.md            Course metadata
│   │   └── module1/
│   │       ├── _index.md        Module metadata
│   │       └── lec01-intro.md   A lecture
│   └── speeches/
│       └── demo-talk.md
├── static/                      Copied verbatim to site root
│   ├── css/                     Project overrides (class, menu, copy-btn)
│   ├── js/                      Theme switcher, aurora, prompt, menu, …
│   └── slides/                  Standalone slide decks (reveal.js)
├── templates/
│   ├── _head_extend.html        Injected into the theme's <head>
│   └── shortcodes/
│       └── slides.html          `{{ slides(src=…) }}` shortcode
└── themes/neovim-theme/         Vendored; safe to patch in place
```

---

## Adding content

### A new course

```bash
mkdir -p content/cs350
cat > content/cs350/_index.md <<'EOF'
+++
title = "CS 350 — Operating Systems"
sort_by = "weight"
+++

Course overview goes here.
EOF
```

The sidebar picks it up on the next build.

### A new module within a course

```bash
mkdir -p content/cs350/module1
cat > content/cs350/module1/_index.md <<'EOF'
+++
title = "Module 1 — Processes"
weight = 1
+++
EOF
```

### A new lecture page

```markdown
+++
title = "Lecture 4 — Scheduling"
date  = 2026-05-20
weight = 4
+++

Lecture body in Markdown.

`code` and code blocks render via Zola syntax highlighting.
```

### A new slide deck

Slides are standalone HTML files under `static/slides/<path>/index.html`
(any deck framework works; current ones use reveal.js). The `slides`
shortcode renders a clickable card that opens the deck in a new browser
tab — this avoids iframe-vs-theme keyboard conflicts and lets the deck
own the full viewport.

```markdown
{{ slides(src="/slides/cs350/module1/lec04/index.html", title="Lec 4 — Scheduling") }}
{{ slides(src="/slides/cs350/module1/lec04/index.html", title="Lec 4", note="42 slides · 25 min") }}
```

Parameters:

| Name    | Default        | Purpose                                |
|---------|----------------|----------------------------------------|
| `src`   | required       | Absolute-style path under `static/`   |
| `title` | `"Slide deck"` | Card label                             |
| `note`  | auto           | Small line below the title (slide count, duration, anything) |

The shortcode passes `src` through `get_url()`, so leading `/` is fine
under the GitHub Pages subpath deploy.

To copy the demo deck from repo1 as a starting template:

```bash
cp -r /path/to/repo1/static/slides/demo static/slides/<your-path>/
```

### Generating a deck with `scripts/build-deck.py`

For decks with many slides, edit `scripts/build-deck.py` and run it instead of
hand-writing HTML. The script builds a reveal.js deck with horizontal sections
(←/→) and vertical sub-sections (↑/↓):

```bash
python3 scripts/build-deck.py
```

How it works:

- The `sections` list near the bottom of the file defines the deck.
- Each top-level list is one **horizontal section** — a single key idea.
- Each item inside that list is a **vertical sub-slide** — an incremental detail.
- A slide item is `(data_id, title, body_html)`.
  - `data_id` must be unique and becomes the slide’s `data-id` attribute.
  - `title` may contain inline HTML such as `<code>`, `<em>`, `<strong>`.
  - `body_html` is raw HTML; use `bullets([...])` and `code("rust", "...")` helpers.
- Change `OUT` at the top of the file to write to a different deck path, e.g.
  `static/slides/rfs-2/index.html`.
- The generated deck links `static/slides/_themes/clean.css` and respects the
  system light/dark preference.

After running the script, wire the deck into the lecture page with the `slides`
shortcode and run `zola build`.

### Slide themes

Both repos ship the same three themes under `static/slides/_themes/`:

| Theme        | File          | Look                                                                 |
|--------------|---------------|----------------------------------------------------------------------|
| `clean`      | `clean.css`   | **Default.** Editorial serif (Newsreader) + Inter; auto-switches by system theme. |
| `night`      | `night.css`   | Tokyo-night dark, Playfair Display titles, Nanum Gothic body, lime accent. |
| `terminal`   | `terminal.css`| All JetBrains Mono, neovim-aligned, `# / ## / ###` heading prefixes. |

Every deck links one theme:

```html
<!-- adjust the ../ count to match your deck's directory depth -->
<link rel="stylesheet" href="../../../_themes/clean.css">
<script src="../../../_themes/deck-utils.js" defer></script>
```

`deck-utils.js` adds copy-to-clipboard on every `<pre>`, renders mermaid
fences as SVG, draws a bottom-right arrow-key indicator, and wires `?`
to open a slide-deck keyboard help overlay. It's a no-op if the deck
already injected its own copy buttons.

Mermaid in slides: put a ` ```mermaid` fence or a `<pre class="mermaid">`
block anywhere; `deck-utils.js` lazy-loads mermaid only when at least
one block exists.

---

## Theme system (light / dark / system)

The hamburger menu (top-right) has a **System / Light / Dark** cycle
button. Choice is persisted in `localStorage` under `site-theme`.

- All palette is defined as OKLCH CSS variables in `static/css/class.css`
  (`--nv-bg-base`, `--nv-fg`, `--nv-accent`, …).
- `html.light` and `html.dark` classes swap the values.
- `theme-toggle.js` runs **synchronously** (not deferred) so the right
  theme paints on first frame — no flash of wrong palette.
- The WebGL aurora background reads `--nv-aur-a/b/c` and retints when
  the theme changes via the `themechange` custom event.

To re-skin a theme, edit the OKLCH tokens in `class.css`. The aurora,
menu, sidebar, content, and code blocks all follow.

---

## Keyboard shortcuts

Inherited from the Neovim theme:

| Keys                | Action                                     |
|---------------------|--------------------------------------------|
| `shift+h` / `shift+l` | Move focus: file tree ↔ content viewer    |
| `j` / `k`            | Scroll content; move selection in tree    |
| `enter`              | Open the selected file in current tab     |
| `shift+t` + `enter`  | Open the selected file in a new tab       |
| `tab`                | Cycle through open tabs                   |
| `shift+q`            | Close the current tab                     |
| `esc` then `:`       | Open the command prompt                   |

Added by this project:

| Keys                | Action                                     |
|---------------------|--------------------------------------------|
| `↑` / `↓` in prompt  | Cycle command history (when no dropdown)  |
| `↑` / `↓` in prompt  | Move selection in fuzzy dropdown          |
| `tab` in prompt      | Autocomplete to top fuzzy match           |
| `esc` in prompt      | Dismiss the fuzzy dropdown                |
| Click chevron in sidebar | Fold / unfold a directory             |

---

## Command prompt (`:` mode)

| Command           | What it does                                 |
|-------------------|----------------------------------------------|
| `:help`           | Jump to the homepage (which doubles as help) |
| `:q`              | Exit the site                                |
| `:set mouse=true` | Show the cursor (default)                    |
| `:set mouse=false`| Hide the cursor (presentation mode)          |
| `:find <query>`   | Fuzzy-search all pages; ↑/↓ select; ⏎ opens  |
| `:f <query>`      | Alias for `:find`                            |
| `:edit <query>`   | Open the top fuzzy match directly            |
| `:e <query>`      | Alias for `:edit`                            |
| `:ls`             | List the first 8 pages in the dropdown       |

History persists in `localStorage` under `nv-prompt-history` (last 50).

---

## Customizing the chrome

### Navigation links

`static/js/menu.js` → `NAV_LINKS` array. Each entry:

```js
{ label: "Home", url: "https://…", external: false }
```

### Social links in the menu footer

Same file → `SOCIAL_LINKS` array.

### Aurora intensity / colors

`static/css/class.css` → `--nv-aur-a/b/c` tokens (separate values inside
`html.light` and `:root` for dark). Or set `--nv-aur-intensity: 0` to
disable visually while keeping the canvas mounted.

### Fonts

`templates/_head_extend.html` loads Barlow (body) and JetBrains Mono
(code). Change there.

### Code copy button

`static/js/copy-code.js` injects a "Copy" button on every `<pre><code>`
block. Toggle in the hamburger menu (state persists).

---

## Deploy

Push to `main` triggers `.github/workflows/deploy.yml`, which:

1. Installs Zola 0.19.2 via `taiki-e/install-action`.
2. Runs `zola build`.
3. Uploads the `public/` directory as a GitHub Pages artifact.
4. Deploys to the `github-pages` environment.

No submodule fetch — the Neovim theme is vendored.

---

## Re-vendoring the theme

```bash
git clone https://github.com/Super-Botman/neovim-theme /tmp/neovim-theme
cd /tmp/neovim-theme && git rev-parse HEAD          # record the hash

# Wipe and replace (keeps our patches lost — see below)
rm -rf themes/neovim-theme/{templates,sass,static,content,LICENSE,README.md,theme.toml}
cp -r /tmp/neovim-theme/{templates,sass,static,content,LICENSE,README.md,theme.toml} themes/neovim-theme/
rm -rf themes/neovim-theme/.git
```

**Patches this project applies to the vendored theme** — re-apply after
re-vendoring:

- `themes/neovim-theme/templates/base.html`
  - All asset URLs use `get_url(path=…)` (subpath-deploy compatible).
  - Body has no inline `background-image` style when `config.extra.background_image` is unset — lets the project CSS gradient + aurora canvas show through.
  - `{% include "_head_extend.html" ignore missing %}` before `</head>`.
- `themes/neovim-theme/sass/css/base.scss`
  - `@font-face` font URL is `../JetBrainsMonoNLNerdFont-Regular.ttf` (relative).
- `themes/neovim-theme/static/js/commands.js`
  - `:help` uses `window.HELP_URL` (set in `_head_extend.html`) instead of hardcoded `/readme`.

Record the new commit hash in `config.toml` under `[extra]`.

---

## Browser support

- **Modern Chromium / Safari 17+ / Firefox 121+**: everything works.
- **Cross-document View Transitions**: Chromium and Safari only. Firefox
  falls back to instant navigation. CSS `@view-transition` block has
  no effect in unsupporting browsers.
- **WebGL aurora**: any browser with WebGL. No WebGL → CSS gradient
  fallback only.
- **`prefers-reduced-motion`**: aurora pauses, View Transitions disabled,
  yank pulse suppressed.

---

## File-by-file reference

| File | Purpose |
|---|---|
| `config.toml` | Site title, base URL, theme name, syntax highlighting style. `[extra]` block holds `blog_name` (required by theme), `site_name` (menu overlay), `author`, optional `background_image`. |
| `content/_index.md` | Root section frontmatter. Sidebar pulls from here downward. |
| `content/readme.md` | The homepage body (the theme's `index.html` renders this via `get_page(path="readme.md")`). |
| `templates/_head_extend.html` | Injected into theme's `<head>`. Loads fonts, project CSS, all JS, exposes `window.HELP_URL` + `window.SITE_PAGES` for the prompt. |
| `templates/shortcodes/slides.html` | `{{ slides(src=…, height=…, title=…) }}` shortcode. |
| `static/css/class.css` | Theme tokens (light/dark), sidebar widening, typography, fold styles, prompt dropdown, View Transitions. |
| `static/css/menu.css` | Hamburger overlay menu. |
| `static/css/copy-btn.css` | Per-codeblock copy button. |
| `static/js/theme-toggle.js` | Cycles system / light / dark; dispatches `themechange` event. |
| `static/js/menu.js` | Builds and injects the hamburger overlay. |
| `static/js/aurora.js` | WebGL backdrop. Reads CSS tokens; pauses when hidden or reduced-motion. |
| `static/js/tree-fold.js` | Adds chevron toggles to sidebar folders; persists state. |
| `static/js/prompt-enhance.js` | Adds `:find`/`:edit`/`:ls` + history to the theme's command prompt. |
| `static/js/copy-code.js` | Injects "Copy" buttons into code blocks. |
| `scripts/build-deck.py` | Python generator for reveal.js slide decks with horizontal sections and vertical sub-sections (rfs-1 example). |
| `scripts/build-deck-rfs2.py` | Python generator for the rfs-2 / Lecture 2 deck. |
| `scripts/build-deck-rfs3.py` | Python generator for the rfs-3 / Lecture 3 deck. |
| `scripts/build-deck-rfs4.py` | Python generator for the rfs-4 / Lecture 4 deck. |
| `themes/neovim-theme/` | Vendored upstream theme + the patches listed above. |

---

## License

Content © Hassan Aziz. Site code MIT.
Vendored neovim-theme: MIT (Super-Botman).
