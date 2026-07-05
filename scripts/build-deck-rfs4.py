#!/usr/bin/env python3
"""
build-deck-rfs4.py - generate the reveal.js slide deck for Rust: First Steps,
Lecture 4: Complex Types.

Run with:
  python3 scripts/build-deck-rfs4.py
"""
import html

OUT = "static/slides/rfs-4/index.html"

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
     '<p class="kicker">Lecture 4 - Complex Types</p>\n<p class="lede">Arrays, vectors, tuples, and control flow. We will use a simplified Pokemon battle helper as the running example.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: The project
sections.append([
    ("project-problem",
     "The problem",
     '<p>Imagine you are building a small assistant for a Pokemon tournament. Trainers want to know two things quickly:</p>\n' +
     bullets([
         "Which type has the advantage in a matchup?",
         "Who wins a simple one-on-one battle?",
     ]) +
     '<p>Real Pokemon games have speed, accuracy, status effects, held items, and dozens of types. We are intentionally building a simplified model so we can focus on Rust arrays, vectors, tuples, and control flow.</p>'),
    ("project-constructs",
     "Why these constructs?",
     bullets([
         "An <strong>array</strong> holds the fixed list of matchups we care about.",
         "A <strong>vector</strong> holds a trainer's team, because teams can grow or shrink.",
         "A <strong>tuple</strong> holds each Pokemon's name, type, and hit points together.",
         "<strong>Match</strong> and loops let us look up type advantages and run battle rounds.",
     ])),
])

# Section 3: Arrays
sections.append([
    ("arrays-basics",
     "Arrays: fixed size, single type",
     '<p>An array is the simplest collection. Every element has the same type, and the size never changes.</p>\n' +
     code("rust", '''fn main() {
    let types = ["Fire", "Water", "Grass", "Electric"];
    println!("{:?}", types);
}''') +
     bullets([
         "Square brackets create an array.",
         "All items must be the same type.",
         "The length is fixed when the array is created.",
     ])),
    ("array-type",
     "The type includes the length",
     '<p>This is a subtle but important detail. <code>[&amp;str; 2]</code> and <code>[&amp;str; 3]</code> are different types.</p>\n' +
     code("rust", '''fn main() {
    let pair = ["Fire", "Water"];      // type is [&str; 2]
    let trio = ["Fire", "Water", "Grass"]; // type is [&str; 3]

    // They cannot be assigned to the same variable without conversion.
}''') +
     '<p>If you ever want to know the type of an array, the compiler will tell you in error messages. It prints something like <code>[&amp;str; 4]</code>.</p>'),
    ("array-repeat",
     "Creating an array from one value",
     '<p>Use a semicolon to repeat a value a fixed number of times.</p>\n' +
     code("rust", '''fn main() {
    let buffer = [0u8; 640];
    println!("Length: {}", buffer.len()); // 640
}''') +
     '<p>This is common for byte buffers. A <code>u8</code> is one byte, so <code>[0u8; 640]</code> gives you 640 bytes of zeroes. Real networking and file code use this pattern.</p>'),
    ("array-bytes",
     "Byte strings are arrays",
     '<p>The <code>b"..."</code> prefix turns a string literal into an array of bytes.</p>\n' +
     code("rust", '''fn main() {
    let greeting = b"Hello";
    println!("{:?}", greeting); // [72, 101, 108, 108, 111]
}''') +
     '<p>The type of <code>greeting</code> is <code>[u8; 5]</code>, not <code>&amp;str</code>. This matters when you work with raw binary data.</p>'),
    ("array-slice",
     "Slicing an array",
     '<p>A slice is a view into part of an array. Slices are written with <code>&amp;</code> and a range.</p>\n' +
     code("rust", '''fn main() {
    let numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

    let middle = &numbers[2..5];  // 2, 3, 4 (index 5 is not included)
    let tail   = &numbers[6..];   // 6, 7, 8, 9
    let head   = &numbers[..3];   // 0, 1, 2
    let all    = &numbers[..];    // the whole array

    println!("middle: {:?}", middle);
}''') +
     '<p><code>2..5</code> is exclusive on the right. <code>2..=5</code> is inclusive and would include index 5.</p>'),
    ("dot-vs-bracket",
     "Why tuples use dot and arrays use brackets",
     '<p>Arrays are homogeneous. Every element has the same type, so <code>arr[i]</code> has a type the compiler already knows even if <code>i</code> is only known at runtime.</p>\n' +
     '<p>Tuples are heterogeneous. A tuple like <code>(String, i32, char)</code> has a different type in every slot. If Rust let you write <code>tuple[i]</code>, the result type would depend on a runtime value. The compiler cannot allow that.</p>\n' +
     '<p>So tuple access is fixed at compile time: <code>.0</code> always means the first slot, <code>.1</code> always means the second slot, and each has a specific type. Tuples act more like anonymous structs, so they use dot notation like structs do.</p>'),
])

# Section 4: Vectors
sections.append([
    ("vectors-basics",
     "Vectors: growable collections",
     '<p>A vector is like a heap-allocated array that can grow and shrink.</p>\n' +
     code("rust", '''fn main() {
    let mut team = Vec::new();
    team.push("Charmander");
    team.push("Squirtle");

    println!("{:?}", team);
}''') +
     bullets([
         "<code>Vec::new()</code> creates an empty vector.",
         "<code>push</code> adds an item to the end.",
         "The vector must be mutable to grow.",
         "The compiler usually infers the element type from the first <code>push</code>.",
     ])),
    ("vectors-macro",
     "The vec! macro",
     '<p>Most people create vectors with the <code>vec!</code> macro because it is shorter.</p>\n' +
     code("rust", '''fn main() {
    let team = vec!["Charmander", "Squirtle", "Bulbasaur"];
    println!("{:?}", team);
}''') +
     '<p>You can also give an explicit type if the compiler cannot infer it:</p>\n' +
     code("rust", '''fn main() {
    let team: Vec<String> = Vec::new();
}''')),
    ("vector-slice",
     "Slicing a vector",
     '<p>Vectors can be sliced just like arrays.</p>\n' +
     code("rust", '''fn main() {
    let team = vec!["Charmander", "Squirtle", "Bulbasaur", "Pikachu"];

    let lead = &team[..1];     // first member
    let bench = &team[1..];    // everyone else

    println!("lead: {:?}, bench: {:?}", lead, bench);
}''')),
    ("vector-capacity",
     "Vector capacity and reallocation",
     '<p>Vectors allocate memory in chunks. When they fill up, they request a larger chunk and copy everything over. This is called reallocation.</p>\n' +
     code("rust", '''fn main() {
    let mut v = Vec::new();
    println!("{}", v.capacity()); // 0

    v.push('a');
    println!("{}", v.capacity()); // 4

    for _ in 0..4 {
        v.push('a');
    }
    println!("{}", v.capacity()); // 8
}''') +
     '<p>If you know how many items you need, you can avoid extra reallocations.</p>'),
    ("vector-with-capacity",
     "Reserving space with with_capacity",
     '<p><code>Vec::with_capacity</code> allocates once instead of growing in small steps.</p>\n' +
     code("rust", '''fn main() {
    let mut v = Vec::with_capacity(8);
    for _ in 0..5 {
        v.push('a');
    }
    println!("{}", v.capacity()); // still 8
}''') +
     '<p>This is useful when you are reading a known number of items from a file or an API and want to avoid repeated memory copies.</p>'),
    ("vector-from-array",
     "Turning an array into a vector",
     '<p>The <code>.into()</code> method can convert an array into a <code>Vec</code>. You can even let Rust infer the element type with <code>Vec&lt;_&gt;</code>.</p>\n' +
     code("rust", '''fn main() {
    let numbers: Vec<u8> = [1, 2, 3].into();
    let inferred: Vec<_> = [9, 0, 10].into();

    println!("{:?} {:?}", numbers, inferred);
}''')),
])

# Section 5: Tuples
sections.append([
    ("tuples-basics",
     "Tuples hold mixed types",
     '<p>A tuple groups values of different types together. Use a dot and a number to access each slot.</p>\n' +
     code("rust", '''fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);

    println!("Name: {}", charmander.0);
    println!("Type: {}", charmander.1);
    println!("HP:   {}", charmander.2);
}''') +
     '<p>The type of <code>charmander</code> is <code>(&amp;str, &amp;str, u16)</code>.</p>'),
    ("unit-type",
     "The unit type",
     '<p>An empty tuple <code>()</code> is called the unit type. It is the default return type when a function returns nothing.</p>\n' +
     code("rust", '''fn do_nothing() {}      // same as fn do_nothing() -> () {}

fn main() {
    do_nothing();       // returns ()
}''') +
     '<p>A semicolon at the end of an expression turns it into a statement, and statements return <code>()</code>. That is why adding a semicolon to the last line of a function changes its return type.</p>'),
    ("tuple-destructure",
     "Destructuring a tuple",
     '<p>You can pull a tuple apart into separate variables in one line.</p>\n' +
     code("rust", '''fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);
    let (name, pokemon_type, hp) = charmander;

    println!("{name} is a {pokemon_type} type with {hp} HP");
}''') +
     '<p>Each variable gets the type of its corresponding slot. Here <code>name</code> is <code>&amp;str</code>, <code>pokemon_type</code> is <code>&amp;str</code>, and <code>hp</code> is <code>u16</code>.</p>'),
    ("tuple-pattern",
     "Patterns must match",
     '<p>Destructuring only works when the shape on both sides matches.</p>\n' +
     code("rust", '''fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);

    // let (name, t) = charmander; // error: expected 3 items, found 2

    let (_, pokemon_type, _) = charmander; // ok: three slots, we ignore two
    println!("Type: {pokemon_type}");
}''') +
     '<p>Use <code>_</code> when you do not care about a slot. Use <code>_name</code> when you might use it later and want to silence the unused-variable warning.</p>'),
    ("tuple-move",
     "Tuples move non-Copy values",
     '<p>If a tuple contains a non-Copy type like <code>String</code>, destructuring moves the values out.</p>\n' +
     code("rust", '''fn main() {
    let entry = ("error".to_string(), 404);
    let (message, code) = entry;

    // println!("{:?}", entry); // error: entry has been moved
    println!("{message}: {code}");
}''') +
     '<p>When every element is Copy, such as <code>(&amp;str, &amp;str, u16)</code>, the whole tuple is Copy and the original stays usable.</p>'),
])

# Section 6: Control flow
sections.append([
    ("if",
     "if, else if, else",
     '<p>Rust checks a condition and runs the matching block. Conditions do not need parentheses.</p>\n' +
     code("rust", '''fn main() {
    let hp = 30;

    if hp == 0 {
        println!("fainted");
    } else if hp < 50 {
        println!("critical");
    } else {
        println!("healthy");
    }
}''') +
     '<p>Use <code>==</code> to compare, <code>=</code> to assign. Use <code>&amp;&amp;</code> for and and <code>||</code> for or.</p>'),
    ("match",
     "match statements",
     '<p><code>match</code> checks a value against several patterns and runs the first one that fits.</p>\n' +
     code("rust", '''fn main() {
    let status = "degraded";

    match status {
        "healthy"   => println!("all good"),
        "degraded"  => println!("watch closely"),
        "down"      => println!("alert!"),
        _           => println!("unknown"),
    }
}''') +
     bullets([
         "Each line is called an arm.",
         "Arms are separated by commas.",
         "The <code>_</code> arm catches everything else.",
         "Rust requires the match to cover every possible value. It checks exhaustiveness at compile time.",
     ])),
    ("match-value",
     "Match returns a value",
     '<p>You can use a match expression to assign a value to a variable.</p>\n' +
     code("rust", '''fn main() {
    let status = "degraded";

    let priority = match status {
        "down"      => 1,
        "degraded"  => 2,
        "healthy"   => 3,
        _           => 4,
    };

    println!("priority: {priority}");
}''') +
     '<p>Every arm must return the same type. You cannot return an <code>i32</code> in one arm and a <code>&amp;str</code> in another.</p>'),
    ("match-tuple",
     "Matching tuples",
     '<p>Match is especially useful with tuples because you can check several values at once.</p>\n' +
     code("rust", '''fn multiplier(attacker: &str, defender: &str) -> f64 {
    match (attacker, defender) {
        ("Fire", "Grass")   => 2.0,
        ("Water", "Fire")   => 2.0,
        ("Grass", "Water")  => 2.0,
        ("Fire", "Water")   => 0.5,
        ("Water", "Grass")  => 0.5,
        ("Grass", "Fire")   => 0.5,
        _                   => 1.0,
    }
}''') +
     '<p>This is the heart of our Pokemon project. It maps attacker and defender types to a damage multiplier.</p>'),
    ("match-guard",
     "Match guards",
     '<p>You can add an <code>if</code> condition to a match arm for extra filtering.</p>\n' +
     code("rust", '''fn describe(hp: u16) -> &'static str {
    match hp {
        0          => "fainted",
        n if n < 50 => "critical",
        _          => "healthy",
    }
}''') +
     '<p>The variable <code>n</code> binds the matched value so we can use it in the guard. Guards are useful when a simple pattern is not enough.</p>'),
    ("match-at",
     "Binding values with @",
     '<p>The <code>@</code> symbol lets you match a pattern and also give the matched value a name.</p>\n' +
     code("rust", '''fn lucky_number(n: i32) {
    match n {
        value @ 4 | value @ 13 => println!("{value} is special"),
        value @ 10..=19       => println!("{value} is a teen"),
        _                     => println!("nothing special"),
    }
}''') +
     '<p>Without <code>@</code>, you would match the range but would not have a variable holding the actual number.</p>'),
    ("loops",
     "Loops",
     '<p>Rust has three loop keywords.</p>\n' +
     code("rust", '''fn main() {
    // loop runs forever until you break
    let mut n = 0;
    loop {
        n += 1;
        if n == 3 { break; }
    }

    // while checks a condition each time
    while n > 0 {
        n -= 1;
    }

    // for iterates over a range or collection
    for i in 0..3 {
        println!("{i}");
    }
}''') +
     '<p><code>0..3</code> gives 0, 1, 2. <code>0..=3</code> gives 0, 1, 2, 3.</p>'),
    ("labeled-loops",
     "Labeled loops",
     '<p>You can name a loop so a <code>break</code> inside a nested loop exits the outer one.</p>\n' +
     code("rust", '''fn main() {
    'outer: loop {
        println!("outer");

        loop {
            println!("inner");
            break 'outer;
        }
    }
}''') +
     "<p>The tick mark <code>'</code> before the name is part of the label syntax. Without the label, <code>break</code> would only exit the inner loop.</p>"),
    ("break-value",
     "Returning a value from a loop",
     '<p>A <code>loop</code> can return a value when it breaks.</p>\n' +
     code("rust", '''fn main() {
    let mut counter = 0;
    let answer = loop {
        counter += 1;
        if counter * counter == 64 {
            break counter;
        }
    };

    println!("{answer}"); // 8
}''') +
     '<p>This is a neat way to compute a value when the number of iterations is not known in advance.</p>'),
])

# Section 7: Building the project
sections.append([
    ("project-type-chart",
     "Step 1: the type chart",
     '<p>We start with a function that looks up type advantage. It returns a damage multiplier.</p>\n' +
     code("rust", '''fn multiplier(attacker: &str, defender: &str) -> f64 {
    match (attacker, defender) {
        ("Fire", "Grass")   |
        ("Water", "Fire")   |
        ("Grass", "Water")  |
        ("Electric", "Water") => 2.0,

        ("Fire", "Water")   |
        ("Water", "Grass")  |
        ("Grass", "Fire")   => 0.5,

        _ => 1.0,
    }
}''') +
     '<p>This is intentionally small. A real type chart would have more types and matchups, but the Rust syntax stays the same.</p>'),
    ("project-pokemon",
     "Step 2: represent a Pokemon",
     '<p>Each Pokemon is a tuple of name, type, and hit points.</p>\n' +
     code("rust", '''fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);
    let squirtle = ("Squirtle", "Water", 110_u16);

    println!("{} has {} HP", charmander.0, charmander.2);
}''') +
     '<p>We use <code>&amp;str</code> and <code>u16</code> so the tuple is Copy. That keeps the early examples simple.</p>'),
    ("project-team",
     "Step 3: build a team",
     '<p>A trainer has a team. Teams can change, so we use a vector.</p>\n' +
     code("rust", '''fn main() {
    let red_team = vec![
        ("Charmander", "Fire", 100_u16),
        ("Pidgey", "Normal", 80_u16),
    ];

    println!("{:#?}", red_team);
}''') +
     '<p>The vector holds tuples. Every tuple has the same shape, so the vector is homogeneous.</p>'),
    ("project-attack",
     "Step 4: simulate an attack",
     "<p>An attack function reduces the defender's hit points by a base amount times the type multiplier.</p>\n" +
     code("rust", '''fn attack(attacker: &(&str, &str, u16), defender: &mut (&str, &str, u16)) {
    let base_power = 20;
    let mult = multiplier(attacker.1, defender.1);
    let damage = (base_power as f64 * mult) as u16;
    defender.2 = defender.2.saturating_sub(damage);
}''') +
     bullets([
         "<code>attacker</code> is an immutable reference because we only read from it.",
         "<code>defender</code> is a mutable reference because we change its HP.",
         "<code>saturating_sub</code> prevents HP from going below zero.",
     ])),
    ("project-battle",
     "Step 5: run a battle",
     "<p>We keep attacking until one Pokemon faints. The loop returns the winner's name.</p>\n" +
     code("rust", '''fn battle(mut first: (&str, &str, u16), mut second: (&str, &str, u16)) -> &str {
    loop {
        attack(&first, &mut second);
        if second.2 == 0 {
            break first.0;
        }

        attack(&second, &mut first);
        if first.2 == 0 {
            break second.0;
        }
    }
}

fn main() {
    let winner = battle(
        ("Charmander", "Fire", 100),
        ("Squirtle", "Water", 110),
    );
    println!("{winner} wins!");
}''') +
     '<p>This is the simplified battle model. It ignores speed, accuracy, status effects, and switching. Those would come in a more advanced program.</p>'),
])

# Section 8: Python -> Rust notes
sections.append([
    ("py-mixed-collections",
     "Mixed collections",
     '<p>In Python, a list can hold anything: <code>[1, "two", 3.0]</code>. In Rust, a vector must hold a single type. If you need mixed types, use a tuple or a custom struct.</p>\n' +
     '<p>This is why our Pokemon is a tuple, not a vector. A vector of Pokemon tuples is fine because every tuple has the same shape.</p>'),
    ("py-indexing",
     "Tuple and array indexing",
     '<p>Python lets you index tuples with a variable: <code>t[i]</code>. Rust does not, because the type of <code>t[i]</code> would depend on the runtime value of <code>i</code>.</p>\n' +
     '<p>Array indexing in Rust is checked at runtime. If you go out of bounds, the program panics instead of returning a nonsense value.</p>'),
    ("py-match",
     "match is exhaustive",
     "<p>Python does not have an exact equivalent of Rust's <code>match</code>. A Rust <code>match</code> must cover every possible value, or the program will not compile.</p>\n" +
     '<p>This feels strict at first, but it catches bugs where you forget to handle an unexpected case.</p>'),
    ("py-loops",
     "Loops and ranges",
     '<p>Python ranges are exclusive on the right by default: <code>range(0, 3)</code> gives 0, 1, 2. Rust has the same default with <code>..</code>, but also an inclusive version with <code>..=</code>.</p>\n' +
     '<p>Rust also lets a <code>loop</code> return a value with <code>break value;</code>, which Python does not do.</p>'),
])

# Section 9: Review and finish
sections.append([
    ("review",
     "What we built",
     bullets([
         "Arrays for fixed data like type names and byte buffers.",
         "Vectors for growable data like a trainer's team.",
         "Tuples for grouped, mixed-type values like a Pokemon's stats.",
         "Slices as borrowed views into arrays and vectors.",
         "Match for type-chart lookup and exhaustive branching.",
         "Loops for repeated attacks until a battle ends.",
     ])),
    ("fin",
     "What comes next",
     '<p class="lede">Next we look at error handling: how to write functions that can fail and how to propagate those failures cleanly.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec04-complex-types/">return to the chapter page</a>.</p>'),
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
  <title>Rust: First Steps - Lecture 4: Complex Types · Hassan Aziz</title>

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
