#!/usr/bin/env python3
"""
build-deck-rfs6.py - generate the reveal.js slide deck for Rust: First Steps,
Lecture 6: Enums in Detail.

Run with:
  python3 scripts/build-deck-rfs6.py
"""
import html

OUT = "static/slides/rfs-6/index.html"

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
     '<p class="kicker">Lecture 6 - Enums in Detail</p>\n<p class="lede">Algebraic data types, pattern matching, and Option. We will build a media catalog as the running example.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: The project
sections.append([
    ("project-problem",
     "The problem",
     '<p>We want a catalog that can hold different kinds of media:</p>\n' +
     bullets([
         "Books have a title and an author.",
         "Movies have a title and a director.",
         "Audiobooks have only a title.",
         "Podcasts have an episode number.",
     ]) +
     '<p>They are similar but not identical. An enum is a natural fit.</p>'),
    ("project-structs",
     "Could we use structs?",
     '<p>We could define a separate struct for each media type. That works, but then every function or collection has to pick one type.</p>\n' +
     '<p>An enum lets us treat all media as a single type while keeping their distinct data.</p>'),
])

# Section 3: Defining the media enum
sections.append([
    ("enum-definition",
     "A media enum",
     '<p>Each variant holds the data that makes sense for that kind of media.</p>\n' +
     code("rust", '''#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Movie { title: String, director: String },
    Audiobook { title: String },
}''') +
     '<p>Every value is still of type <code>Media</code>.</p>'),
    ("enum-values",
     "Creating values",
     code("rust", '''fn main() {
    let book = Media::Book {
        title: String::from("The Rust Book"),
        author: String::from("Rust Contributors"),
    };

    let movie = Media::Movie {
        title: String::from("Inception"),
        director: String::from("Christopher Nolan"),
    };

    println!("{:?}", book);
}''') +
     '<p>We choose the variant with <code>::</code> and fill in its fields.</p>'),
])

# Section 4: Implementing methods on enums
sections.append([
    ("impl-intro",
     "Adding behavior to enums",
     '<p>Enums can have <code>impl</code> blocks. We can define one method that behaves differently for each variant.</p>'),
    ("impl-if-let",
     "Checking the variant with if let",
     '<p>Before accessing fields, we must find out which variant we have.</p>\n' +
     code("rust", '''impl Media {
    fn description(&self) -> String {
        if let Media::Book { title, author } = self {
            return format!("Book: {} by {}", title, author);
        }
        if let Media::Movie { title, director } = self {
            return format!("Movie: {} directed by {}", title, director);
        }
        String::from("Some other media")
    }
}''') +
     '<p><code>if let</code> checks one variant at a time.</p>'),
    ("impl-match",
     "Checking the variant with match",
     '<p><code>match</code> is usually cleaner because it forces us to handle every variant.</p>\n' +
     code("rust", '''impl Media {
    fn description(&self) -> String {
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
        }
    }
}''') +
     '<p>Rust requires the match to be exhaustive.</p>'),
    ("impl-match-note",
     "Why exhaustive matching matters",
     '<p>If we add a new variant later, the compiler tells us every place we forgot to update.</p>\n' +
     '<p>This catches real bugs. In many other languages, adding a new enum case silently breaks logic elsewhere.</p>'),
])

# Section 5: Structs vs enums
sections.append([
    ("struct-vs-enum",
     "When to use structs vs enums",
     '<p>Use an enum when every variant needs the same set of methods.</p>\n' +
     '<p>Use structs when different types need different methods that should not be shared.</p>'),
    ("struct-vs-enum-example",
     "An example",
     '<p>A <code>read()</code> method makes sense for a book but not a movie. A <code>play()</code> method makes sense for a movie but not a book.</p>\n' +
     '<p>If methods diverge like that, separate structs are usually clearer.</p>'),
    ("struct-vs-enum-fields",
     "Another consideration: fields",
     '<p>If each variant has many unique fields, match statements become tedious.</p>\n' +
     '<p>That is a sign that structs might be a better fit.</p>'),
])

# Section 6: Building the catalog
sections.append([
    ("catalog-struct",
     "The catalog",
     '<p>A catalog owns a vector of media items.</p>\n' +
     code("rust", '''#[derive(Debug)]
struct Catalog {
    items: Vec<Media>,
}

impl Catalog {
    fn new() -> Self {
        Self { items: vec![] }
    }
}''') +
     '<p>The vector holds one type, <code>Media</code>, but that type can represent many different things.</p>'),
    ("catalog-add",
     "Adding items",
     code("rust", '''impl Catalog {
    fn add(&mut self, media: Media) {
        self.items.push(media);
    }
}''') +
     '<p><code>add</code> takes <code>&mut self</code> because it changes the catalog.</p>'),
    ("catalog-use",
     "Using the catalog",
     code("rust", '''fn main() {
    let mut catalog = Catalog::new();

    catalog.add(Media::Audiobook {
        title: String::from("A Brief History"),
    });
    catalog.add(Media::Book {
        title: String::from("Dune"),
        author: String::from("Frank Herbert"),
    });

    println!("{:?}", catalog);
}''') +
     '<p><code>catalog</code> must be mutable because we call <code>add</code>.</p>'),
])

# Section 7: Unlabeled fields and unit variants
sections.append([
    ("unlabeled-fields",
     "Unlabeled fields",
     '<p>Variants can hold a single value without naming it.</p>\n' +
     code("rust", '''#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Movie { title: String, director: String },
    Audiobook { title: String },
    Podcast(u32),
}''') +
     '<p><code>Podcast(10)</code> is less explicit than a named field, but fine when the meaning is obvious.</p>'),
    ("unlabeled-pattern",
     "Matching unlabeled fields",
     code("rust", '''impl Media {
    fn description(&self) -> String {
        match self {
            Media::Podcast(episode) => {
                format!("Podcast episode {}", episode)
            }
            _ => String::from("other media"),
        }
    }
}''') +
     '<p>We bind the value inside the parentheses to a variable.</p>'),
    ("unit-variants",
     "Unit variants",
     '<p>A variant with no data is called a unit variant.</p>\n' +
     code("rust", '''#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Placeholder,
}

fn main() {
    let placeholder = Media::Placeholder;
    println!("{:?}", placeholder);
}''') +
     '<p>Unit variants are useful as placeholders or markers.</p>'),
])

# Section 8: Option
sections.append([
    ("option-intro",
     "No null in Rust",
     '<p>Rust does not have <code>null</code>, <code>nil</code>, or <code>undefined</code>.</p>\n' +
     '<p>Instead, Rust uses the <code>Option</code> enum to represent a value that may or may not be present.</p>'),
    ("option-definition",
     "The Option enum",
     '<p><code>Option</code> is built into the standard library.</p>\n' +
     code("rust", '''enum Option<T> {
    Some(T),
    None,
}''') +
     '<p><code>Some</code> wraps a value. <code>None</code> means there is no value.</p>'),
    ("option-get",
     "A real example: Vec::get",
     '<p><code>Vec::get</code> returns an <code>Option</code> because the index might be out of bounds.</p>\n' +
     code("rust", '''fn main() {
    let catalog = Catalog::new();
    let item = catalog.items.get(0);

    match item {
        Some(media) => println!("{:?}", media),
        None => println!("no item at that index"),
    }
}''') +
     '<p>We must handle both cases.</p>'),
])

# Section 9: Building our own Option-like enum
sections.append([
    ("custom-option",
     "Why Option works this way",
     '<p>To see why <code>Option</code> is designed like this, we can build our own version.</p>'),
    ("custom-option-enum",
     "A custom Maybe enum",
     code("rust", '''enum MaybeValue<'a> {
    HasValue(&'a Media),
    NoValue,
}''') +
     '<p>This is conceptually identical to <code>Option<&Media></code>.</p>'),
    ("custom-option-impl",
     "Using the custom enum",
     code("rust", '''impl Catalog {
    fn get_media(&self, index: usize) -> MaybeValue {
        if index < self.items.len() {
            MaybeValue::HasValue(&self.items[index])
        } else {
            MaybeValue::NoValue
        }
    }
}''') +
     '<p>The lifetime annotation <code>\'a</code> is required because we return a reference.</p>'),
    ("custom-option-use",
     "Matching the custom enum",
     code("rust", '''fn main() {
    let catalog = Catalog::new();

    match catalog.get_media(0) {
        MaybeValue::HasValue(media) => println!("{:?}", media),
        MaybeValue::NoValue => println!("nothing here"),
    }
}''')),
    ("replace-with-option",
     "Replacing with the real Option",
     code("rust", '''impl Catalog {
    fn get_media(&self, index: usize) -> Option<&Media> {
        if index < self.items.len() {
            Some(&self.items[index])
        } else {
            None
        }
    }
}''') +
     '<p>Real code uses <code>Option</code> instead of reinventing it.</p>'),
])

# Section 10: Other ways to handle Option
sections.append([
    ("unwrap",
     "unwrap",
     '<p><code>unwrap</code> extracts the value from <code>Some</code>.</p>\n' +
     code("rust", '''fn main() {
    let item = catalog.items.get(0);
    println!("{:?}", item.unwrap());
}''') +
     '<p>If the value is <code>None</code>, the program panics and crashes.</p>'),
    ("unwrap-warning",
     "Be careful with unwrap",
     '<p><code>unwrap</code> is fine for quick scripts and prototypes.</p>\n' +
     '<p>In production code, prefer <code>match</code> or <code>if let</code> so you handle <code>None</code> safely.</p>'),
    ("expect",
     "expect",
     '<p><code>expect</code> is like <code>unwrap</code> but lets you provide a panic message.</p>\n' +
     code("rust", '''fn main() {
    let item = catalog.items.get(0);
    println!("{:?}", item.expect("catalog should not be empty"));
}''') +
     '<p>Useful when a missing value means the program is fundamentally misconfigured.</p>'),
    ("unwrap-or",
     "unwrap_or",
     '<p><code>unwrap_or</code> returns the value inside <code>Some</code>, or a fallback value if it is <code>None</code>.</p>\n' +
     code("rust", '''fn main() {
    let item = catalog.items.get(100);
    let placeholder = Media::Placeholder;
    println!("{:?}", item.unwrap_or(&placeholder));
}''') +
     '<p>This avoids a panic by providing a default.</p>'),
    ("match-recommended",
     "match is still the default",
     '<p>For most code, use <code>match</code> or <code>if let</code>.</p>\n' +
     '<p><code>unwrap</code>, <code>expect</code>, and <code>unwrap_or</code> are shortcuts for specific situations.</p>'),
])

# Section 11: Language comparison
sections.append([
    ("lang-compare-intro",
     "How other languages handle enums",
     '<p>Rust enums are different from enums in Python, C++, Java, and Go. Each language makes a different trade-off.</p>'),
    ("python-enums",
     "Python enums",
     '<p>Python has <code>enum.Enum</code>.</p>\n' +
     bullets([
         "Variants are names attached to values, often integers.",
         "No per-variant data fields.",
         "No exhaustive matching at compile time.",
         "Missing values use <code>None</code>, which can be forgotten at runtime.",
     ])),
    ("cpp-enums",
     "C++ enums",
     '<p>C++ has <code>enum</code> and <code>enum class</code>.</p>\n' +
     bullets([
         "Plain enums are basically integers.",
         "<code>enum class</code> adds type safety but still no per-variant data.",
         "No exhaustive switch checking.",
         "Missing values use <code>std::optional</code>, introduced in C++17.",
     ])),
    ("java-enums",
     "Java enums",
     '<p>Java enums can have fields and methods shared by all variants.</p>\n' +
     bullets([
         "All variants share the same fields.",
         "No per-variant data shapes.",
         "<code>switch</code> on enums can be exhaustive with modern tooling.",
         "Missing values use <code>Optional<T></code>.",
     ])),
    ("go-enums",
     "Go enums",
     '<p>Go does not have a dedicated enum type.</p>\n' +
     bullets([
         "Use typed constants with <code>iota</code>.",
         "No compile-time exhaustiveness checking.",
         "No per-variant data.",
         "Missing values use <code>nil</code>, like other reference types.",
     ])),
    ("rust-enums",
     "Rust enums",
     '<p>Rust enums are algebraic data types.</p>\n' +
     bullets([
         "Each variant can carry different data.",
         "<code>match</code> must be exhaustive.",
         "No null; missing values use <code>Option<T></code>.",
         "The compiler prevents many null-pointer-style bugs.",
     ])),
    ("lang-compare-strengths",
     "Where Rust is stronger",
     '<p>Rust combines three features that are usually separate in other languages:</p>\n' +
     bullets([
         "Sum types: one type, many possible shapes.",
         "Exhaustive pattern matching.",
         "Null-free option types.",
     ]) +
     '<p>This catches whole categories of bugs at compile time.</p>'),
    ("lang-compare-tradeoffs",
     "Where Rust asks more of you",
     '<p>The trade-off is verbosity.</p>\n' +
     bullets([
         "You must handle every variant in a <code>match</code>.",
         "You must explicitly unwrap <code>Option</code> values.",
         "Lifetime and ownership rules apply to references inside variants.",
     ]) +
     '<p>Other languages let you be sloppier, which is sometimes faster to write but easier to break.</p>'),
])

# Section 12: Python to Rust notes
sections.append([
    ("py-option",
     "Option vs None",
     '<p>In Python, a function can return <code>None</code> to mean "no value." The caller might forget to check.</p>\n' +
     '<p>In Rust, <code>Option</code> forces the check. You cannot accidentally use a <code>None</code> as if it were a real value.</p>'),
    ("py-match",
     "Exhaustive matching",
     '<p>Python has no compile-time exhaustiveness check for enum-like constants.</p>\n' +
     '<p>Rust refuses to compile if you add a variant and forget to update a <code>match</code>.</p>'),
    ("py-classes",
     "Enums vs classes",
     '<p>Python classes can simulate sum types with subclasses, but the language does not enforce exhaustive handling.</p>\n' +
     '<p>Rust enums make the shape of data part of the type system.</p>'),
])

# Section 13: Review and finish
sections.append([
    ("review-1",
     "What we built",
     bullets([
         "An enum can represent many related shapes as one type.",
         "Pattern matching extracts data and must be exhaustive.",
         "Methods on enums use <code>match</code> or <code>if let</code> to behave differently per variant.",
     ])),
    ("review-2",
     "What we built, continued",
     bullets([
         "Unit variants and unlabeled fields keep enums concise.",
         "<code>Option<T></code> replaces null with an explicit <code>Some</code>/<code>None</code> choice.",
         "<code>unwrap</code>, <code>expect</code>, and <code>unwrap_or</code> are shortcuts for specific cases.",
     ])),
    ("fin",
     "What comes next",
     '<p class="lede">Next we look at error handling: how to represent failures with <code>Result</code> and how to propagate errors cleanly.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec06-enums-in-detail/">return to the chapter page</a>.</p>'),
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
  <title>Rust: First Steps - Lecture 6: Enums in Detail · Hassan Aziz</title>

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
