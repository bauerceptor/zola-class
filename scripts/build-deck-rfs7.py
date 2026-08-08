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
        match self {
            Media::Book { title, author } => format!("Book: {} by {}", title, author),
            Media::Movie { title, director } => format!("Movie: {} by {}", title, director),
            Media::Audiobook { title } => format!("Audiobook: {}", title),
            Media::Podcast(episode) => format!("Podcast episode {}", episode),
            Media::Placeholder => String::from("Placeholder"),
        }
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
