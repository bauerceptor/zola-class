# Rust: First Steps — Lecture 7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the reveal.js slide deck, chapter webpage, and supporting documentation for Rust: First Steps Lecture 7 (Modules and Code Organization), continuing the media catalog from Lecture 6.

**Architecture:** Reuse the existing generator pattern from `scripts/build-deck-rfs6.py`. Create `scripts/build-deck-rfs7.py` with the Lecture 7 content, run it to produce `static/slides/rfs-7/index.html`, and write a matching Zola lecture page. Update the course overview and documentation.

**Tech stack:** Python 3, reveal.js 5.1.0, Zola 0.19.2, the shared `clean.css` slide theme.

---

## File structure

- `scripts/build-deck-rfs7.py` — Python generator for the rfs-7 slide deck.
- `static/slides/rfs-7/index.html` — generated reveal.js deck.
- `content/rust-first-steps/module1/lec07-modules.md` — Zola lecture page.
- `content/rust-first-steps/_index.md` — course overview (add Lecture 7).
- `README.md` — add `build-deck-rfs7.py` to the generator list.
- `guide-for-ai.md` — add `build-deck-rfs7.py` to §3.4 generator list.

---

## Task 1: Update course overview

**Files:**
- Modify: `content/rust-first-steps/_index.md`

- [ ] **Step 1: Add Lecture 7 summary paragraph**
  After the Lecture 6 paragraph, add:
  ```markdown
  Chapter 7 - **Modules and Code Organization** - takes the media catalog
  from the previous lecture and refactors it into a `content` module with
  `media` and `catalog` submodules, covering `mod`, `pub`, `use`, `super`,
  and nested-module rules.
  ```

---

## Task 2: Create the slide deck generator

**Files:**
- Create: `scripts/build-deck-rfs7.py`

- [ ] **Step 1: Write `scripts/build-deck-rfs7.py`**
  Create the file with the following content. It follows the same pattern as
  `build-deck-rfs6.py` but adapts the deck to modules and the media-catalog
  refactor.

  ```python
  #!/usr/bin/env python3
  """
  build-deck-rfs7.py - generate the reveal.js slide deck for Rust: First Steps,
  Lecture 7: Modules and Code Organization.

  Run with:
    python3 scripts/build-deck-rfs7.py
  """
  import html

  OUT = "static/slides/rfs-7/index.html"

  # -- Helpers ------------------------------------------------------------------

  def slide(idx, title, body, kicker=None, data_id=None):
      sid = (data_id or f"{idx:02d}").lower().replace(" ", "-")
      label = kicker or f"{idx:02d}"
      tag = "h1" if idx == 1 else "h2"
      title_html = f"<{tag}>{title}</{tag}>" if title else ""
      parts = [f'<span class="slide-id">{html.escape(label)}</span>', title_html]
      if body:
          parts.append(body)
      return f'        <section data-id="{html.escape(sid)}">\n          ' + "\n          ".join(filter(None, parts)) + "\n        </section>\n"

  def bullets(items):
      return "<ul>\n" + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ul>"

  def code(lang, src):
      return f'<pre><code class="language-{lang}" data-trim>{html.escape(src.rstrip())}</code></pre>'

  # -- Slides -------------------------------------------------------------------

  sections = []

  # Section 1: Title
  sections.append([
      ("title",
       "Rust: First Steps",
       '<p class="kicker">Lecture 7 - Modules and Code Organization</p>\n<p class="lede">Grouping code, controlling privacy, and refactoring a growing project into modules.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
  ])

  # Section 2: Why modules
  sections.append([
      ("why-modules",
       "Why modules matter",
       '<p>As a project grows, <code>main.rs</code> collects structs, enums, functions, and implementations.</p>\n' +
       '<p>Modules let us group related code so the project stays readable.</p>'),
      ("why-modules-example",
       "A messy main.rs",
       '<p>Our media catalog from the last lecture currently lives in one file:</p>\n' +
       bullets([
           "The <code>Media</code> enum and its <code>impl</code> block.",
           "The <code>Catalog</code> struct and its <code>impl</code> block.",
           "The <code>main</code> function and helper functions.",
       ]) +
       '<p>We will split this into a <code>content</code> module with two submodules.</p>'),
  ])

  # Section 3: Three ways to make a module
  sections.append([
      ("module-inline",
       "Option 1: Inline module",
       '<p>Use <code>mod</code> inside an existing file when you want structure without creating new files.</p>\n' +
       code("rust", '''mod content {
      pub enum Media { Book, Movie }
      pub struct Catalog { items: Vec<Media> }
  }

  fn main() {
      let catalog = content::Catalog { items: vec![] };
  }''') +
       '<p>Access items with <code>module_name::item_name</code>.</p>'),
      ("module-file",
       "Option 2: Separate file",
       '<p>A file named <code>content.rs</code> becomes a module named <code>content</code>.</p>\n' +
       code("rust", '''// content.rs
  pub enum Media { Book, Movie }
  pub struct Catalog { items: Vec<Media> }''') +
       code("rust", '''// main.rs
  mod content;

  fn main() {
      let catalog = content::Catalog { items: vec![] };
  }''') +
       '<p><code>mod content;</code> tells Rust to look for <code>content.rs</code>.</p>'),
      ("module-folder",
       "Option 3: Nested folder",
       '<p>For larger modules, use a folder with a <code>mod.rs</code> file and sibling files.</p>\n' +
       code("text", '''src/
  ├── main.rs
  └── content/
      ├── mod.rs
      ├── media.rs
      └── catalog.rs''') +
       '<p>This is the pattern we will use for the media catalog.</p>'),
  ])

  # Section 4: Privacy and pub
  sections.append([
      ("privacy-default",
       "Everything is private by default",
       '<p>Items inside a module are hidden from the outside world unless marked <code>pub</code>.</p>\n' +
       code("rust", '''mod content {
      enum Media { Book, Movie }          // private
      pub struct Catalog { items: Vec<Media> } // public
  }''') +
       '<p>Without <code>pub</code>, <code>main.rs</code> cannot use <code>Media</code> or <code>Catalog</code>.</p>'),
      ("privacy-methods",
       "Public methods too",
       '<p>Functions and methods also need <code>pub</code> to be callable from outside.</p>\n' +
       code("rust", '''impl Catalog {
      pub fn new() -> Self {
          Self { items: vec![] }
      }
      pub fn add(&mut self, media: Media) {
          self.items.push(media);
      }
  }''') +
       '<p>If <code>new</code> is not <code>pub</code>, other modules cannot create a <code>Catalog</code>.</p>'),
  ])

  # Section 5: mod and use
  sections.append([
      ("mod-keyword",
       "mod declares a module",
       '<p><code>mod</code> tells the compiler that a module exists and should be compiled.</p>\n' +
       code("rust", '''// main.rs
  mod content;

  fn main() {
      let catalog = content::Catalog::new();
  }''') +
       '<p>Without <code>mod content;</code>, Rust ignores <code>content.rs</code> or the <code>content/</code> folder.</p>'),
      ("use-keyword",
       "use abbreviates paths",
       '<p>Long paths get tiring. <code>use</code> creates a shortcut.</p>\n' +
       code("rust", '''// main.rs
  mod content;
  use content::Catalog;

  fn main() {
      let catalog = Catalog::new();
  }''') +
       '<p><code>use</code> does not change privacy. It only shortens how we write a path.</p>'),
  ])

  # Section 6: Rules of nested modules
  sections.append([
      ("rule-files",
       "Every file is a module",
       '<p>In a nested folder, each file creates its own module.</p>\n' +
       code("text", '''content/
  ├── mod.rs      -> content module
  ├── media.rs    -> media module
  └── catalog.rs  -> catalog module''') +
       '<p>The folder name becomes a module because it contains <code>mod.rs</code>.</p>'),
      ("rule-modrs",
       "mod.rs is required for folders",
       '<p>A folder only becomes a module when it contains <code>mod.rs</code>.</p>\n' +
       code("rust", '''// content/mod.rs
  pub mod media;
  pub mod catalog;''') +
       '<p><code>pub mod media;</code> imports the <code>media</code> submodule and re-exports it publicly.</p>'),
      ("rule-no-deep",
       "No deeply nested imports",
       '<p>The root module cannot reach directly into <code>content/media.rs</code>.</p>\n' +
       '<p>Imports happen one level at a time:</p>\n' +
       bullets([
           "<code>content/mod.rs</code> imports <code>media</code> and <code>catalog</code>.",
           "<code>main.rs</code> imports <code>content</code>.",
           "Then <code>main.rs</code> can reach <code>content::media::Media</code>.",
       ])),
  ])

  # Section 7: Refactor the media catalog
  sections.append([
      ("refactor-media",
       "Move Media to content/media.rs",
       code("rust", '''// content/media.rs
  #[derive(Debug)]
  pub enum Media {
      Book { title: String, author: String },
      Movie { title: String, director: String },
      Audiobook { title: String },
      Podcast(u32),
      Placeholder,
  }

  impl Media {
      pub fn description(&self) -> String {
          // same body as Lecture 6
          format!("Media description")
      }
  }''') +
       '<p>Mark the enum and the method as <code>pub</code>.</p>'),
      ("refactor-catalog",
       "Move Catalog to content/catalog.rs",
       code("rust", '''// content/catalog.rs
  use super::media::Media;

  #[derive(Debug)]
  pub struct Catalog {
      items: Vec<Media>,
  }

  impl Catalog {
      pub fn new() -> Self {
          Self { items: vec![] }
      }
      pub fn add(&mut self, media: Media) {
          self.items.push(media);
      }
      pub fn get_by_index(&self, index: usize) -> Option<&Media> {
          self.items.get(index)
      }
  }''') +
       '<p>We will explain <code>super</code> in the next section.</p>'),
      ("refactor-modrs",
       "Wire up content/mod.rs",
       code("rust", '''// content/mod.rs
  pub mod media;
  pub mod catalog;''') +
       '<p>These two lines import the submodules and re-export them publicly.</p>'),
      ("refactor-main",
       "Update main.rs",
       code("rust", '''// main.rs
  mod content;
  use content::media::Media;
  use content::catalog::Catalog;

  fn main() {
      let mut catalog = Catalog::new();
      catalog.add(Media::Audiobook {
          title: String::from("A Brief History"),
      });
      println!("{:?}", catalog);
  }''') +
       '<p>With <code>use</code>, the code reads almost the same as before.</p>'),
  ])

  # Section 8: super
  sections.append([
      ("super-intro",
       "super means parent module",
       '<p>Inside <code>content/catalog.rs</code>, we need the <code>Media</code> enum from <code>content/media.rs</code>.</p>\n' +
       '<p>We use <code>super</code> to move up one module level:</p>\n' +
       code("rust", '''// content/catalog.rs
  use super::media::Media;''') +
       '<p><code>super</code> is <code>content</code>, so <code>super::media::Media</code> finds the enum.</p>'),
      ("super-diagram",
       "Visualizing the module tree",
       '<p>Think of modules as a tree:</p>\n' +
       code("text", '''crate (main.rs)
  └── content
      ├── media
      └── catalog''') +
       '<p>From <code>catalog</code>, <code>super</code> is <code>content</code>.</p>'),
  ])

  # Section 9: Python vs Rust notes
  sections.append([
      ("py-modules",
       "Python modules",
       '<p>In Python, modules are files. Privacy is by convention:</p>\n' +
       bullets([
           "<code>import content.media</code> imports a file or package.",
           "Names starting with <code>_</code> are considered private.",
           "There is no compiler enforcement of privacy.",
       ]) +
       '<p>You can still import and use <code>_private</code> things if you try.</p>'),
      ("rust-modules",
       "Rust modules",
       '<p>In Rust, modules are explicit and privacy is enforced:</p>\n' +
       bullets([
           "<code>mod content;</code> declares the module.",
           "Items are private unless marked <code>pub</code>.",
           "The compiler rejects code that uses private items.",
       ]) +
       '<p>This makes boundaries clear and prevents accidental dependencies.</p>'),
  ])

  # Section 10: Takeaways and finish
  sections.append([
      ("takeaway-1",
       "Takeaways",
       bullets([
           "Modules group related code: enums, structs, functions, and impl blocks.",
           "Everything inside a module is private by default.",
           "<code>pub</code> makes an item accessible from outside.",
           "<code>mod</code> declares a module; <code>use</code> abbreviates a path.",
       ])),
      ("takeaway-2",
       "More takeaways",
       bullets([
           "Nested folders need a <code>mod.rs</code> file.",
           "Imports happen one level at a time.",
           "<code>pub mod</code> imports and re-exports a submodule.",
           "<code>super</code> refers to the parent module.",
       ])),
      ("fin",
       "What comes next",
       '<p class="lede">Next we look at error handling with <code>Result</code> and how to propagate failures cleanly.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec07-modules/">return to the chapter page</a>.</p>'),
  ])

  # -- Build slide HTML with nested sections ------------------------------------

  slide_idx = 0
  section_html_parts = []

  for sec in sections:
      slide_idx += 1
      first = sec[0]
      if len(sec) == 1:
          section_html_parts.append(slide(slide_idx, title=first[1], body=first[2], kicker=first[0], data_id=first[0]))
      else:
          nested = [slide(slide_idx, first[1], first[2], kicker=first[0], data_id=first[0])]
          for item in sec[1:]:
              slide_idx += 1
              nested.append(slide(slide_idx, item[1], item[2], kicker=item[0], data_id=item[0]))
          section_html_parts.append("      <section>\n" + "".join(nested) + "      </section>\n")

  body_html = "".join(section_html_parts)
  slide_count = slide_idx

  html_doc = f'''<!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rust: First Steps - Lecture 7: Modules and Code Organization · Hassan Aziz</title>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reset.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/white.css" id="reveal-theme">

    <link rel="stylesheet" id="hljs-light" media="(prefers-color-scheme: light)"
          href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
    <link rel="stylesheet" id="hljs-dark"  media="(prefers-color-scheme: dark)"
          href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github-dark.min.css">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="../_themes/clean.css">
  </head>
  <body>

    <a href="../" id="back-to-site"><- site</a>

    <div class="reveal">
      <div class="slides">

  {body_html}

      </div>
    </div>

    <!-- Live arrow-key indicator -->
    <div id="nav-keys" aria-label="Navigation keys">
      <button type="button" class="key up"    data-dir="up"    aria-label="Up: go to previous subsection">↑</button>
      <button type="button" class="key left"  data-dir="left"  aria-label="Left: go to previous section">←</button>
      <button type="button" class="key down"  data-dir="down"  aria-label="Down: go to next subsection">↓</button>
      <button type="button" class="key right" data-dir="right" aria-label="Right: go to next section">→</button>
    </div>

    <div id="slide-counter" aria-hidden="true">1</div>

    <!-- ? help overlay -->
    <div id="help" role="dialog" aria-label="Keyboard shortcuts" aria-hidden="true">
      <pre>Keyboard
  ->  Next section
  <-  Previous section
  ↓  Next subsection
  ↑  Previous subsection
  F  Fullscreen
  S  Speaker view
  ESC Slide overview
  ?  Toggle this panel</pre>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/highlight/highlight.js"></script>
    <script>
      Reveal.initialize({{
        hash: true,
        controls: false,
        progress: true,
        slideNumber: 'c/t',
        center: false,
        transition: 'slide',
        navigationMode: 'default',
        keyboard: true,
        highlight: {{
          beforeHighlight: function (hljs) {{ hljs.configure({{ ignoreUnescapedHTML: true }}); }},
        }},
        plugins: [ RevealHighlight ],
      }});

      /* -- Copy-to-clipboard button on every <pre> -- */
      function addCopyButtons() {{
        document.querySelectorAll('.reveal pre').forEach(function (pre) {{
          if (pre.querySelector('.copy-btn')) return;
          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'copy-btn';
          btn.textContent = 'Copy';
          btn.setAttribute('aria-label', 'Copy code to clipboard');
          btn.addEventListener('click', function () {{
            var code = pre.querySelector('code');
            var text = code ? code.innerText : pre.innerText;
            if (navigator.clipboard && navigator.clipboard.writeText) {{
              navigator.clipboard.writeText(text).then(showCopied);
            }} else {{
              var ta = document.createElement('textarea');
              ta.value = text;
              document.body.appendChild(ta);
              ta.select();
              try {{ document.execCommand('copy'); showCopied(); }} catch (_) {{}}
              document.body.removeChild(ta);
            }}
          }});
          function showCopied() {{
            btn.textContent = 'Copied';
            btn.classList.add('copied');
            setTimeout(function () {{
              btn.textContent = 'Copy';
              btn.classList.remove('copied');
            }}, 1400);
          }}
          pre.appendChild(btn);
        }});
      }}
      Reveal.on('ready', addCopyButtons);
      Reveal.on('slidechanged', addCopyButtons);

      var keys = {{
        up:    document.querySelector('#nav-keys .key.up'),
        down:  document.querySelector('#nav-keys .key.down'),
        left:  document.querySelector('#nav-keys .key.left'),
        right: document.querySelector('#nav-keys .key.right'),
      }};

      var counterEl = document.getElementById('slide-counter');

      function updateKeys() {{
        var routes = Reveal.availableRoutes();
        ['up','down','left','right'].forEach(function (dir) {{
          keys[dir].classList.toggle('active', !!routes[dir]);
        }});
        var idx = Reveal.getIndices();
        var n = (idx.h + 1).toString().padStart(2, '0');
        if (idx.v && idx.v > 0) n += '.' + idx.v;
        counterEl.textContent = n;
      }}

      Reveal.on('ready', updateKeys);
      Reveal.on('slidechanged', updateKeys);

      Object.keys(keys).forEach(function (dir) {{
        keys[dir].addEventListener('click', function () {{
          if (!keys[dir].classList.contains('active')) return;
          if (dir === 'left')  Reveal.left();
          if (dir === 'right') Reveal.right();
          if (dir === 'up')    Reveal.up();
          if (dir === 'down')  Reveal.down();
        }});
      }});

      var help = document.getElementById('help');
      document.addEventListener('keydown', function (e) {{
        if (e.key === '?' && e.shiftKey) {{
          e.preventDefault();
          help.classList.toggle('open');
          help.setAttribute('aria-hidden', help.classList.contains('open') ? 'false' : 'true');
        }} else if (e.key === 'Escape' && help.classList.contains('open')) {{
          help.classList.remove('open');
          help.setAttribute('aria-hidden', 'true');
        }}
      }});
      help.addEventListener('click', function () {{
        help.classList.remove('open');
        help.setAttribute('aria-hidden', 'true');
      }});
    </script>
  </body>
  </html>
  '''

  with open(OUT, "w", encoding="utf-8") as f:
      f.write(html_doc)

  print(f"Wrote {slide_count} slides to {OUT}")
  ```

---

## Task 3: Generate the slide deck

**Files:**
- Create: `static/slides/rfs-7/index.html`

- [ ] **Step 1: Run the generator**
  ```bash
  python3 scripts/build-deck-rfs7.py
  ```
  Expected: `Wrote 24 slides to static/slides/rfs-7/index.html`.

---

## Task 4: Create the lecture webpage

**Files:**
- Create: `content/rust-first-steps/module1/lec07-modules.md`

- [ ] **Step 1: Write frontmatter**
  ```toml
  +++
  title       = "Lecture 7 - Modules and Code Organization"
  date        = 2026-06-27
  description = "Modules, privacy, mod, pub, use, super, and refactoring a growing Rust project into multiple files. Built around the media catalog from Lecture 6."
  weight      = 7

  [extra]
  lang        = "en"
  course      = "Rust: First Steps"
  lecture_num = 7
  mermaid     = false
  copy        = true
  +++
  ```

- [ ] **Step 2: Write body**
  Start with `<!-- Chapter codename: rfs-7 -->`.
  Include the slide deck card with the shortcode.
  Summarize modules, privacy, `mod`, `pub`, `use`, nested-module rules, `super`,
  and the refactor walkthrough.
  Add Python-vs-Rust notes and a takeaway list.

  ```markdown
  <!-- Chapter codename: rfs-7 -->

  ## Slides

  {{ slides(src="/slides/rfs-7/index.html", title="Lec 7 - Modules and Code Organization", note="24 slides · ~40 min") }}

  ## At a glance

  This lecture explains Rust's module system. We take the media catalog from
  Lecture 6 — where the `Media` enum, `Catalog` struct, and `main` function all
  lived in one file — and refactor it into a `content` module with `media` and
  `catalog` submodules. Along the way we cover `mod`, `pub`, `use`, `super`, and
  the rules that govern nested modules.

  ## Why modules matter

  A small program can live comfortably in `main.rs`. As it grows, related items
  start to pile up: enums, structs, implementations, helper functions. Modules
  group related code into named units, making the project easier to read,
  navigate, and maintain.

  ## Three ways to create a module

  Rust gives you three patterns. They share the same privacy rules; only the
  structure changes.

  ### Inline module

  Use `mod` inside an existing file when you want structure without creating new
  files.

  ```rust
  mod content {
      pub enum Media { Book, Movie }
      pub struct Catalog { items: Vec<Media> }
  }

  fn main() {
      let catalog = content::Catalog { items: vec![] };
  }
  ```

  ### Separate file

  A file named `content.rs` becomes a module named `content`.

  ```rust
  // content.rs
  pub enum Media { Book, Movie }
  pub struct Catalog { items: Vec<Media> }
  ```

  ```rust
  // main.rs
  mod content;

  fn main() {
      let catalog = content::Catalog { items: vec![] };
  }
  ```

  ### Nested folder

  For larger modules, use a folder with `mod.rs` and sibling files.

  ```text
  src/
  ├── main.rs
  └── content/
      ├── mod.rs
      ├── media.rs
      └── catalog.rs
  ```

  This is the pattern we use for the media catalog refactor.

  ## Privacy is the default

  Everything inside a module is private unless marked `pub`. This includes enums,
  structs, functions, and methods.

  ```rust
  mod content {
      enum Media { Book, Movie }          // private
      pub struct Catalog { items: Vec<Media> } // public
  }
  ```

  Without `pub`, code outside the module cannot use the item. The compiler
  enforces this, so privacy is not just a convention.

  ## `mod` and `use`

  `mod` tells the compiler that a module exists and should be compiled.

  ```rust
  // main.rs
  mod content;

  fn main() {
      let catalog = content::Catalog::new();
  }
  ```

  `use` abbreviates a path. It does not change what is accessible; it only
  shortens how you write it.

  ```rust
  // main.rs
  mod content;
  use content::Catalog;

  fn main() {
      let catalog = Catalog::new();
  }
  ```

  ## Rules of nested modules

  Nested modules have a few rules that often trip people up.

  - **Every file creates a module.** `content/media.rs` is the `media` module.
  - **Every folder needs a `mod.rs`.** The folder `content/` becomes the
    `content` module because it contains `content/mod.rs`.
  - **Imports happen one level at a time.** The root module cannot reach
    directly into `content/media.rs`. It must go through `content`.
  - **`pub mod` imports and re-exports.** In `content/mod.rs`,
    `pub mod media;` brings the `media` submodule into `content` and makes it
    public.

  ```rust
  // content/mod.rs
  pub mod media;
  pub mod catalog;
  ```

  ## Refactoring the media catalog

  We start with a single `main.rs` from Lecture 6 and end with this layout:

  ```text
  src/
  ├── main.rs
  └── content/
      ├── mod.rs
      ├── media.rs
      └── catalog.rs
  ```

  ### `content/media.rs`

  ```rust
  #[derive(Debug)]
  pub enum Media {
      Book { title: String, author: String },
      Movie { title: String, director: String },
      Audiobook { title: String },
      Podcast(u32),
      Placeholder,
  }

  impl Media {
      pub fn description(&self) -> String {
          match self {
              Media::Book { title, author } => {
                  format!("Book: {} by {}", title, author)
              }
              Media::Movie { title, director } => {
                  format!("Movie: {} by {}", title, director)
              }
              Media::Audiobook { title } => {
                  format!("Audiobook: {}", title)
              }
              Media::Podcast(episode) => {
                  format!("Podcast episode {}", episode)
              }
              Media::Placeholder => String::from("Placeholder"),
          }
      }
  }
  ```

  ### `content/catalog.rs`

  ```rust
  use super::media::Media;

  #[derive(Debug)]
  pub struct Catalog {
      items: Vec<Media>,
  }

  impl Catalog {
      pub fn new() -> Self {
          Self { items: vec![] }
      }

      pub fn add(&mut self, media: Media) {
          self.items.push(media);
      }

      pub fn get_by_index(&self, index: usize) -> Option<&Media> {
          self.items.get(index)
      }
  }
  ```

  ### `content/mod.rs`

  ```rust
  pub mod media;
  pub mod catalog;
  ```

  ### `main.rs`

  ```rust
  mod content;
  use content::media::Media;
  use content::catalog::Catalog;

  fn main() {
      let mut catalog = Catalog::new();

      catalog.add(Media::Audiobook {
          title: String::from("A Brief History"),
      });
      catalog.add(Media::Book {
          title: String::from("Dune"),
          author: String::from("Frank Herbert"),
      });

      match catalog.get_by_index(0) {
          Some(media) => println!("{}", media.description()),
          None => println!("no media at that index"),
      }

      println!("{:?}", catalog);
  }
  ```

  ## `super`

  Inside a nested module, `super` refers to the parent module. From
  `content/catalog.rs`, `super` is `content`.

  ```rust
  // content/catalog.rs
  use super::media::Media;
  ```

  This is how sibling modules talk to each other. `catalog.rs` cannot import
  `Media` directly from the root; it must go up to `content` and then into
  `media`.

  ## Python to Rust: modules

  In Python, a module is usually a file or package. Privacy is by convention:
  names starting with `_` are considered private, but the language does not stop
  you from importing them.

  In Rust, modules are explicit and privacy is enforced. You must declare a
  module with `mod`, mark public items with `pub`, and import through each layer.
  The compiler rejects code that tries to use private items. This makes
  dependencies visible and accidental coupling harder.

  ## Takeaway

  - Modules group related code: enums, structs, functions, and implementations.
  - Everything inside a module is private by default.
  - `pub` makes an item accessible from outside.
  - `mod` declares a module; `use` abbreviates a path.
  - Nested folders require a `mod.rs` file.
  - Imports happen one level at a time; use `pub mod` to re-export.
  - `super` refers to the parent module.
  - Rust's module privacy is enforced by the compiler, unlike Python's
    convention-based privacy.
  ```

---

## Task 5: Update documentation

**Files:**
- Modify: `README.md`
- Modify: `guide-for-ai.md`

- [ ] **Step 1: Document the new generator in README.md**
  In the file-by-file reference table, add a row after `scripts/build-deck-rfs6.py`:
  ```markdown
  | `scripts/build-deck-rfs7.py` | Python generator for the rfs-7 / Lecture 7 deck. |
  ```

- [ ] **Step 2: Document the new generator in guide-for-ai.md**
  In §3.4, add `scripts/build-deck-rfs7.py` to the generator list after
  `build-deck-rfs6.py`.

---

## Task 6: Build and verify

- [ ] **Step 1: Run Zola build**
  ```bash
  zola build
  ```
  Expected: success, no errors.

- [ ] **Step 2: Sanity-check generated files**
  Confirm `static/slides/rfs-7/index.html` exists and the lecture page is at
  `content/rust-first-steps/module1/lec07-modules.md`.

---

## Task 7: Commit and push

- [ ] **Step 1: Stage all changes**
  ```bash
  git add -A
  ```

- [ ] **Step 2: Commit**
  ```bash
  git commit -m "lec: rust-first-steps lecture 7 (modules and code organization)"
  ```

- [ ] **Step 3: Push**
  ```bash
  git push
  ```
  Expected: pushed to origin/main.

---

## Self-review

- **Spec coverage:** Every section of the design doc maps to a task: course
  overview, generator, deck, webpage, docs, build, commit/push.
- **Placeholder scan:** No TBDs or vague steps; exact file paths and commands
  provided.
- **Type consistency:** `Media` and `Catalog` types match Lecture 6. Slide count
  (24) matches the note in the webpage shortcode.
