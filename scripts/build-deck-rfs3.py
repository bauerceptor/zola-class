#!/usr/bin/env python3
"""
build-deck-rfs3.py - generate the reveal.js slide deck for Rust: First Steps,
Lecture 3: The Building Blocks.

Run with:
  python3 scripts/build-deck-rfs3.py
"""
import html

OUT = "static/slides/rfs-3/index.html"

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
     '<p class="kicker">Lecture 3 - The Building Blocks</p>\n<p class="lede">Structs, implementations, methods, crates, and a small Pokemon team program that ties everything together.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: Starting a Rust program
sections.append([
    ("main",
     "Every program starts at main",
     '<p>When a Rust program starts, it calls <code>main</code> automatically.</p>\n' +
     code("rust", '''fn main() {
    println!("Hello, world!");
}''') +
     bullets([
         "<code>fn</code> declares a function.",
         "<code>main</code> is the entry point.",
         "<code>println!</code> is a macro. The <code>!</code> is your hint.",
     ])),
    ("strings-chars",
     "Strings and chars",
     '<p>Double quotes make a string slice. Single quotes make a single character.</p>\n' +
     code("rust", '''fn main() {
    let name = "Pikachu";     // &str
    let initial = 'P';        // char

    // let bad = 'Pikachu';   // error: char must be one character
}''') +
     '<p>Coming from Python, think of <code>&str</code> as an immutable text slice and <code>String</code> as the owned, growable version.</p>'),
])

# Section 3: Structs
sections.append([
    ("structs-why",
     "Grouping data with a struct",
     '<p>A struct is like a lightweight class. It groups related data together and lets us attach behavior to it.</p>\n' +
     '<p>For this lecture we will build a <code>Team</code> that holds a list of Pokemon.</p>'),
    ("team-struct",
     "Defining Team",
     code("rust", '''struct Team {
    members: Vec<String>,
}''') +
     bullets([
         "<code>struct</code> introduces a new type.",
         "The name starts with a capital letter by convention.",
         "Inside the curly braces we list fields and their types.",
         "<code>Vec&lt;String&gt;</code> is a growable list of owned strings.",
     ])),
    ("team-instance",
     "Creating an instance",
     code("rust", '''fn main() {
    let team = Team {
        members: vec![],
    };

    println!("{:?}", team);
}''') +
     bullets([
         "A struct literal creates an instance.",
         "<code>vec![]</code> is the macro for an empty vector.",
         "Your editor may show a gray <code>: Team</code> hint. That is Rust Analyzer telling you the inferred type.",
     ])),
    ("derive-debug",
     "Making Team printable",
     '<p>If you try to print the team with <code>{}</code>, the compiler complains. It does not know how to turn a custom struct into text.</p>\n' +
     code("rust", '''#[derive(Debug)]
struct Team {
    members: Vec<String>,
}

fn main() {
    let team = Team { members: vec![] };
    println!("{:#?}", team);
}''') +
     bullets([
         "<code>#[derive(Debug)]</code> asks the compiler to write a debug formatter for us.",
         "<code>{:?}</code> prints compact debug output.",
         "<code>{:#?}</code> pretty-prints it across several lines.",
         "In Python, <code>print(obj)</code> calls <code>__str__</code>. In Rust, printing is opt-in through traits.",
     ])),
])

# Section 4: Vec vs array
sections.append([
    ("vec-array",
     "Vec or array?",
     bullets([
         "A <code>Vec</code> can grow and shrink. Use it when the number of items changes.",
         "An <code>array</code> has a fixed length. Use it when the size never changes.",
         "Arrays are very slightly faster, but the real reason to use them is communication: this list is fixed.",
     ]) +
     code("rust", '''fn main() {
    let mut team = vec!["Pikachu"];   // vector
    team.push("Charmander");          // allowed

    let types = ["Fire", "Water"];     // array of 2 items
    // types.push("Grass");            // error: no push on arrays
}''')),
    ("generate-team",
     "Building the roster",
     '<p>Instead of typing every name, we generate the team from two fixed arrays.</p>\n' +
     code("rust", '''fn main() {
    let types = ["Fire", "Water", "Grass", "Electric"];
    let species = ["Charmander", "Squirtle", "Bulbasaur", "Pikachu"];

    let mut members = vec![];
    for t in types {
        for s in species {
            let name = format!("{} {}", t, s);
            members.push(name);
        }
    }

    let team = Team { members };
    println!("{:#?}", team);
}''') +
     '<p><code>format!</code> works like <code>println!</code> but returns a <code>String</code> instead of printing it.</p>'),
    ("mutability-reminder",
     "Why mut matters here",
     '<p>We need <code>mut</code> because we keep adding members to the vector.</p>\n' +
     code("rust", '''fn main() {
    let members = vec![];
    members.push("Pikachu");   // error: cannot borrow as mutable
}''') +
     '<p>Without <code>mut</code>, Rust refuses to let us change the value or reassign the binding. This applies to anything nested inside the value too.</p>'),
])

# Section 5: Inherent implementations
sections.append([
    ("impl-why",
     "Adding behavior to Team",
     '<p>Right now the creation logic lives in <code>main</code>. We want a function tied to <code>Team</code> that builds a default roster.</p>\n' +
     '<p>In Rust we use an <code>impl</code> block to attach functions to a struct.</p>'),
    ("impl-new",
     "An associated function: Team::new",
     code("rust", '''impl Team {
    fn new() -> Self {
        let types = ["Fire", "Water", "Grass", "Electric"];
        let species = ["Charmander", "Squirtle", "Bulbasaur", "Pikachu"];

        let mut members = vec![];
        for t in types {
            for s in species {
                members.push(format!("{} {}", t, s));
            }
        }

        Self { members }
    }
}

fn main() {
    let team = Team::new();
    println!("{:#?}", team);
}''') +
     bullets([
         "<code>impl Team</code> is an inherent implementation.",
         "<code>Self</code> is shorthand for the type in the surrounding <code>impl</code> block. Here it means <code>Team</code>.",
         "<code>Team::new()</code> calls an associated function. It does not take <code>self</code>.",
         "The last expression is returned automatically because there is no semicolon.",
     ])),
    ("implicit-return",
     "Implicit return",
     '<p>Rust returns the last expression of a function if you leave off the semicolon.</p>\n' +
     code("rust", '''fn is_even(n: i32) -> bool {
    n % 2 == 0   // returned
}

fn is_even_longer(n: i32) -> bool {
    if n % 2 == 0 {
        true      // returned from the if branch
    } else {
        false     // returned from the else branch
    }
}''') +
     '<p>Python always needs <code>return</code>. Rust treats the tail expression as the return value.</p>'),
    ("methods-vs-associated",
     "Methods vs associated functions",
     bullets([
         "An associated function has no <code>self</code> argument. Use it for constructors or factories.",
         "A method takes <code>&self</code> or <code>&mut self</code> as its first argument. Use it to operate on one instance.",
         "This is close to static methods and instance methods in other languages, but Rust makes the borrowing explicit.",
     ])),
])

# Section 6: Shuffling with an external crate
sections.append([
    ("shuffle-goal",
     "Randomizing the team",
     '<p>Every time we run the program, the team prints in the same order. We want a <code>shuffle</code> method that randomizes it.</p>\n' +
     '<p>Rust does not put randomness in the standard library, so we pull in the <code>rand</code> crate.</p>'),
    ("crates",
     "Crates are packages",
     bullets([
         "A <strong>crate</strong> is Rust's word for a package or library.",
         "The standard library crate is included automatically.",
         "External crates are added with <code>cargo add rand</code> and listed in <code>Cargo.toml</code>.",
         "You can browse crates at <code>crates.io</code> and read docs at <code>docs.rs</code>.",
     ]) +
     '<p style="margin-top:0.8rem;">In Python you might <code>pip install</code> a package and then <code>import</code> it. In Rust you add a crate and bring items into scope with <code>use</code>.</p>'),
    ("use-keyword",
     "Bringing items into scope",
     '<p>We need two things from <code>rand</code>: a random number generator and the ability to shuffle a slice.</p>\n' +
     code("rust", '''use rand::{thread_rng, seq::SliceRandom};

impl Team {
    fn shuffle(&mut self) {
        let mut rng = thread_rng();
        self.members.shuffle(&mut rng);
    }
}''') +
     bullets([
         "<code>use</code> creates a shortcut so we do not have to type <code>rand::thread_rng</code> every time.",
         "<code>thread_rng()</code> gives us a random number generator.",
         "<code>SliceRandom</code> is a trait that adds <code>shuffle</code> to vectors.",
         "External crates do not need a <code>mod</code> statement; internal modules do.",
     ])),
    ("mut-self",
     "Why &mut self?",
     '<p><code>shuffle</code> changes the team, so it needs a mutable reference.</p>\n' +
     code("rust", '''fn main() {
    let mut team = Team::new();
    team.shuffle();
    println!("{:#?}", team);
}''') +
     bullets([
         "The caller must declare <code>team</code> as <code>mut</code>.",
         "The method signature must take <code>&mut self</code>.",
         "Both ends of the call have to agree that the data may change.",
         "In Python, if you pass a list to a function, it can mutate the list. Rust makes that contract explicit.",
     ])),
    ("rand-010",
     "A note on rand 0.10",
     '<p>The code above uses <code>thread_rng</code>, which works up to <code>rand</code> 0.9. Starting with <code>rand</code> 0.10.0, the API changes slightly.</p>\n' +
     '<p>Option 1: use <code>rng()</code> instead of <code>thread_rng()</code>. Everything else stays the same.</p>\n' +
     code("rust", '''use rand::{rng, seq::SliceRandom};

impl Team {
    fn shuffle(&mut self) {
        let mut rng = rng();
        self.members.shuffle(&mut rng);
    }
}''') +
     '<p>Option 2: use <code>make_rng</code> with an explicit type such as <code>SmallRng</code>.</p>\n' +
     code("rust", '''use rand::{make_rng, rngs::SmallRng, seq::SliceRandom};

impl Team {
    fn shuffle(&mut self) {
        let mut rng: SmallRng = make_rng();
        self.members.shuffle(&mut rng);
    }
}''') +
     '<p>Both versions give you a random number generator. Pick whichever your project already uses.</p>'),
])

# Section 7: Removing members
sections.append([
    ("release-goal",
     "Sending members to a gym",
     '<p>We want a method that removes some members from the team and returns them in a new vector. We will call it <code>release</code>.</p>\n' +
     '<p>It takes the number of members to remove and returns a <code>Vec&lt;String&gt;</code>.</p>'),
    ("usize",
     "usize: sizes and counts",
     '<p>Counts, lengths, and indices usually use <code>usize</code>. It is large enough to index any collection on the current machine.</p>\n' +
     code("rust", '''impl Team {
    fn release(&mut self, num: usize) -> Vec<String> {
        // TODO: handle asking for too many members
        self.members.split_off(self.members.len() - num)
    }
}''') +
     bullets([
         "<code>usize</code> is an unsigned integer the same size as a memory address.",
         "<code>i32</code> or <code>u32</code> would also work here, but <code>usize</code> is the convention for counts.",
         "<code>split_off(at)</code> removes everything from index <code>at</code> onward and returns it as a new vector.",
     ])),
    ("release-call",
     "Calling release",
     code("rust", '''fn main() {
    let mut team = Team::new();
    team.shuffle();

    let gym_team = team.release(3);
    println!("Gym team: {:#?}", gym_team);
    println!("Remaining: {:#?}", team);
}''') +
     '<p>After the call, <code>gym_team</code> owns the removed strings and the original team owns whatever is left.</p>'),
    ("error-deferred",
     "A missing safety check",
     '<p>If we ask for more members than the team has, <code>split_off</code> panics. We are skipping proper error handling here so we can focus on the building blocks.</p>\n' +
     '<p>We will come back to error handling in a future lecture. For now, treat it as a known hole.</p>'),
])

# Section 8: Integer types
sections.append([
    ("integers",
     "The integer family",
     bullets([
         "Signed integers can be negative: <code>i8</code>, <code>i16</code>, <code>i32</code>, <code>i64</code>, <code>i128</code>, <code>isize</code>.",
         "Unsigned integers start at zero: <code>u8</code>, <code>u16</code>, <code>u32</code>, <code>u64</code>, <code>u128</code>, <code>usize</code>.",
         "Floats: <code>f32</code> and <code>f64</code>.",
         "Pick the smallest type that fits your data safely.",
     ])),
    ("integer-example",
     "Picking a type",
     code("rust", '''fn main() {
    let level: u8 = 42;        // plenty for a Pokemon level
    let hp: i32 = -25;         // damage can be negative in a calculation
    let count: usize = 1000;   // counts and indexes
    let health: f64 = 95.5;    // decimal stats
}''') +
     '<p>The number in the name is the bit width. A <code>u8</code> fits 0 to 255. A <code>u128</code> fits an astronomically large range.</p>'),
])

# Section 9: Python -> Rust gotchas
sections.append([
    ("py-classes",
     "Structs are not Python classes",
     bullets([
         "A struct's fields are fixed at compile time. You cannot add new fields later like you can with Python object attributes.",
         "Methods are added in <code>impl</code> blocks, not inside the struct definition.",
         "All types must be declared. There is no dynamic typing.",
     ]) +
     '<p>If you need flexible key-value data, Rust has other tools. A struct is for shaped, predictable data.</p>'),
    ("py-imports",
     "Crates, modules, and use",
     bullets([
         "External crates are used directly with <code>crate_name::item</code>. You do not write <code>mod</code> for them.",
         "Internal modules need a <code>mod</code> declaration before you use them.",
         "<code>use</code> is a shortcut, not exactly an import. You can still access items through their full path.",
         "This trips up a lot of Python newcomers because Python treats every file as an importable module automatically.",
     ])),
    ("py-mutation",
     "Mutation needs permission everywhere",
     '<p>In Python, passing a list into a function lets that function change the list. Rust makes both sides opt in.</p>\n' +
     code("rust", '''fn add_member(team: &mut Team, name: String) {
    team.members.push(name);
}

fn main() {
    let mut team = Team::new();
    add_member(&mut team, String::from("Mewtwo"));
}''') +
     '<p>The caller says <code>&mut team</code>, the parameter says <code>&mut Team</code>, and the method says <code>&mut self</code>. All three have to agree.</p>'),
    ("py-printing",
     "Printing is not automatic",
     '<p>Python calls <code>__str__</code> or <code>__repr__</code> for you. Rust only prints what it knows how to format.</p>\n' +
     bullets([
         "Use <code>#[derive(Debug)]</code> for debug output during development.",
         "Use <code>{}</code> for Display when you want user-facing output.",
         "You can implement Display manually for full control over the output.",
     ])),
])

# Section 10: Review and finish
sections.append([
    ("review",
     "What we built",
     bullets([
         "A <code>Team</code> struct that owns a <code>Vec&lt;String&gt;</code>.",
         "Fixed arrays for types and species, and a nested loop to generate names.",
         "<code>#[derive(Debug)]</code> so we can print the struct.",
         "An <code>impl</code> block with an associated function <code>new</code> and methods <code>shuffle</code> and <code>release</code>.",
         "The <code>rand</code> crate brought in through <code>cargo add</code> and brought into scope with <code>use</code>.",
         "Mutable references <code>&mut self</code> whenever a method changes data.",
     ])),
    ("fin",
     "What comes next",
     '<p class="lede">Next we look at error handling: how to write functions that can fail without crashing the program.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec03-the-building-blocks/">return to the chapter page</a>.</p>'),
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
  <title>Rust: First Steps - Lecture 3: The Building Blocks · Hassan Aziz</title>

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
