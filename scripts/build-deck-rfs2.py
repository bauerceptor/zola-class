#!/usr/bin/env python3
"""
build-deck-rfs2.py - generate the reveal.js slide deck for Rust: First Steps,
Lecture 2: Memory and Ownership.

Run with:
  python3 scripts/build-deck-rfs2.py
"""
import html

OUT = "static/slides/rfs-2/index.html"

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
     '<p class="kicker">Lecture 2 - Memory and Ownership</p>\n<p class="lede">Stack, heap, references, strings, mutable borrows, Copy types, and the ownership rules that keep Rust safe.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: Stack, heap, pointers, references
sections.append([
    ("memory-intro",
     "Two places for data",
     bullets([
         "The <strong>stack</strong> is fast. Memory is added and removed like a pile of dishes: last in, first out.",
         "The <strong>heap</strong> is more flexible. It can hold data of any size, but finding and freeing it takes more work.",
         "Rust needs to know the size of a value at compile time to put it on the stack.",
         "Python hides this from you; Rust makes it part of the contract.",
     ])),
    ("stack",
     "The stack",
     bullets([
         "Simple values with a known size live on the stack.",
         "An <code>i32</code> is always 4 bytes, so it can go on the stack.",
         "When a function returns, its stack space is reclaimed automatically.",
     ]) +
     code("rust", '''fn main() {
    let x = 8;      // i32 on the stack
    let y = 100.5;  // f64 on the stack
}''')),
    ("heap",
     "The heap and pointers",
     bullets([
         "Data with an unknown size at compile time goes on the heap.",
         "The program asks the OS for a chunk of heap memory.",
         "A <strong>pointer</strong> goes on the stack; it stores the address of the heap data.",
     ]) +
     code("rust", '''fn main() {
    let s = String::from("I live on the heap");
    // s is a pointer/length/capacity on the stack;
    // the text itself lives on the heap.
}''')),
    ("pointers",
     "Pointers are like a table of contents",
     '<p>A table of contents tells you where each chapter lives. It does not own the chapter.</p>\n' +
     bullets([
         "A pointer stores an address. The data lives somewhere else.",
         "In Rust, the pointer you use most often is called a <strong>reference</strong>.",
         "A reference borrows memory; it does not own it.",
     ]) +
     code("rust", '''fn main() {
    let my_variable = 8;
    let my_reference = &my_variable;
}''')),
    ("references",
     "Reading references",
     bullets([
         "<code>let x = 8;</code> makes a regular variable.",
         "<code>let r = &x;</code> makes a reference to that variable.",
         "Read it as 'r is a reference to x' or 'r borrows x'.",
         "The owner (<code>x</code>) keeps the data. The reference just looks at it.",
     ]) +
     code("rust", '''fn main() {
    let my_number = 15;
    let single_reference = &my_number;          // &i32
    let double_reference = &single_reference;   // &&i32
    let five_references = &&&&&my_number;        // &&&&&i32
}''')),
])

# Section 3: Strings
sections.append([
    ("strings-intro",
     "String and &str",
     bullets([
         "<code>&str</code> is a string slice: a pointer plus a length. It is a view into data owned by something else.",
         "<code>String</code> is an owned, growable buffer on the heap.",
         "Both are UTF-8 encoded.",
         "Python strings feel like one thing; Rust separates borrowed views from owned buffers.",
     ])),
    ("str-sized",
     "Why &str and not str?",
     bullets([
         "A <code>str</code> can be any length, so the compiler does not know its size.",
         "A reference has a fixed size, so <code>&str</code> can live on the stack.",
         "The reference points to the bytes and carries the length.",
     ]) +
     code("rust", '''fn main() {
    let size_of_string = std::mem::size_of::<String>();
    let size_of_i8 = std::mem::size_of::<i8>();
    let size_of_jaurim = std::mem::size_of_val("자우림");

    println!("A String is always {size_of_string} bytes.");
    println!("An i8 is always {size_of_i8} bytes.");
    println!("But '&str' can be {size_of_jaurim} bytes - it is not Sized.");
}''') +
     '<p>Trying to write <code>let my_name: str = "My name";</code> gives a compile error: the size for values of type <code>str</code> cannot be known at compilation time.</p>'),
    ("utf8",
     "UTF-8 everywhere",
     bullets([
         "Both <code>&str</code> and <code>String</code> store UTF-8 bytes.",
         "ASCII uses one byte per character. Korean, emoji, and many other scripts use more.",
         "Rust is fine with any Unicode. Your terminal may not display it.",
     ]) +
     code("rust", '''fn main() {
    let name = "안녕하세요";
    let other_name = String::from("Adrian Fahrenheit Ţepeş");
    println!("My name is {}", name);
}''')),
    ("bytes-vs-chars",
     "Bytes vs characters",
     bullets([
         "<code>.len()</code> returns the number of <em>bytes</em>, not characters.",
         "Use <code>.chars().count()</code> for the number of Unicode characters.",
     ]) +
     code("rust", '''fn main() {
    let s1 = "Hello!";
    let s2 = "안녕!";
    println!("{}: {} bytes, {} chars", s1, s1.len(), s1.chars().count());
    println!("{}: {} bytes, {} chars", s2, s2.len(), s2.chars().count());
}''') +
     code("text", '''Hello!: 6 bytes, 6 chars
안녕!: 7 bytes, 3 chars''')),
    ("creating-strings",
     "Creating strings",
     bullets([
         '<code>String::from("...")</code> builds an owned String from a slice.',
         '<code>"...".to_string()</code> does the same thing.',
         '<code>format!("...")</code> works like <code>println!</code> but returns a String.',
         '<code>.into()</code> can convert a slice into a String, but you usually need a type hint.',
     ]) +
     code("rust", '''fn main() {
    let a = String::from("This is the string text");
    let b = "This is the string text".to_string();

    let name = "Billybrobby";
    let country = "USA";
    let together = format!("I am {name} from {country}.");

    let c: String = "Try to make this a String".into();
}''')),
])

# Section 4: const and static
sections.append([
    ("const-static",
     "const and static",
     bullets([
         "<code>const</code> is a value that does not change and is created at compile time.",
         "<code>static</code> is similar but has a fixed memory location.",
         "Both are written in ALL_CAPS and usually live outside <code>main</code>.",
         "They are available everywhere and do not get dropped.",
     ]) +
     code("rust", '''const NUMBER_OF_MONTHS: u32 = 12;
static SEASONS: [&str; 4] = ["Spring", "Summer", "Fall", "Winter"];

fn print_months() {
    println!("Number of months in the year: {NUMBER_OF_MONTHS}");
}

fn main() {
    print_months();
}''')),
])

# Section 5: More on references
sections.append([
    ("many-immutable",
     "Many immutable references",
     bullets([
         "You can have as many immutable references as you want.",
         "They are read-only views; nobody can change the data.",
     ]) +
     code("rust", '''fn main() {
    let country = String::from("Austria");
    let ref_one = &country;
    let ref_two = &country;
    println!("{}", ref_one);
    println!("{}", ref_two);
}''')),
    ("return-local-ref",
     "You cannot return a reference to a local",
     bullets([
         "A local variable dies when its function ends.",
         "A reference to that variable would point to freed memory.",
         "Rust refuses to let you return it.",
     ]) +
     code("rust", '''fn return_str() -> &String {
    let country = String::from("Austria");
    let country_ref = &country;
    country_ref
}

fn main() {
    let country = return_str();
}''') +
     code("rust", '''error[E0515]: cannot return value referencing local variable `country`
  |
3 |     let country_ref = &country;
  |                       -------- `country` is borrowed here
4 |     country_ref
  |     ^^^^^^^^^^^ returns a value referencing data owned by the current function''')),
])

# Section 6: Mutable references
sections.append([
    ("mut-ref-intro",
     "Mutable references",
     bullets([
         "Use <code>&mut</code> when you want to change data through a reference.",
         "The original variable must also be declared <code>mut</code>.",
         "Dereference with <code>*</code> to reach the value behind the reference.",
     ]) +
     code("rust", '''fn main() {
    let mut my_number = 8;
    let num_ref = &mut my_number;
    *num_ref += 10;
    println!("{}", my_number); // 18
}''')),
    ("ref-rules",
     "The two reference rules",
     bullets([
         "Rule 1: You can have any number of immutable references.",
         "Rule 2: You can have only one mutable reference, and no immutable references at the same time.",
         "This prevents data races and surprises at compile time.",
     ]) +
     code("rust", '''fn main() {
    let mut number = 10;
    let number_ref = &number;
    let number_change = &mut number; // error
    *number_change += 10;
    println!("{}", number_ref);
}''') +
     code("rust", '''error[E0502]: cannot borrow `number` as mutable because it is also borrowed as immutable
  |
3 |     let number_ref = &number;
  |                      ------- immutable borrow occurs here
4 |     let number_change = &mut number;
  |                         ^^^^^^^^^^^ mutable borrow occurs here''')),
    ("non-overlap",
     "Borrows can end",
     bullets([
         "The compiler tracks <em>when</em> each borrow is used.",
         "A mutable borrow ends after its last use, so an immutable borrow can start later.",
     ]) +
     code("rust", '''fn main() {
    let mut number = 10;
    let number_change = &mut number;
    *number_change += 10;

    let number_ref = &number; // fine now
    println!("{}", number_ref); // 20
}''')),
])

# Section 7: Shadowing again
sections.append([
    ("shadow-memory",
     "Shadowing does not destroy",
     bullets([
         "A new <code>let</code> with the same name hides the old binding.",
         "The old value is still alive in memory until its scope ends.",
         "A reference to the old value keeps working.",
     ]) +
     code("rust", '''fn main() {
    let country = String::from("Austria");
    let country_ref = &country;
    let country = 8;
    println!("{country_ref} {country}"); // Austria 8
}''')),
    ("shadow-functions",
     "Shadowing and ownership",
     '<p>Shadowing becomes even more useful once functions and references get involved. You can reuse a name when ownership has passed, or when a value has been transformed into a different type.</p>\n' +
     code("rust", '''fn main() {
    let country = String::from("Austria");
    let country = add_hungary(country);
    println!("{}", country);
}

fn add_hungary(name: String) -> String {
    format!("{}-Hungary", name)
}''')),
])

# Section 8: Giving references to functions
sections.append([
    ("fn-ownership",
     "Functions take ownership by default",
     bullets([
         "A function parameter that takes <code>String</code> owns the value.",
         "If the function does not return it, the value is dropped when the function ends.",
         "This is why the first call to <code>print_country(country)</code> works, but the second fails.",
     ]) +
     code("rust", '''fn print_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(country);
    print_country(country); // error: use of moved value
}''')),
    ("fn-borrow",
     "Borrowing with references",
     bullets([
         "Change the parameter to <code>&String</code> to borrow instead of own.",
         "Pass <code>&country</code> from the caller.",
         "The function can look at the data, but the caller keeps ownership.",
     ]) +
     code("rust", '''fn print_country(country_name: &String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(&country);
    print_country(&country); // fine
}''')),
    ("fn-mut-borrow",
     "Mutable references in functions",
     bullets([
         "Use <code>&mut String</code> when the function needs to change the string.",
         "The caller must also pass <code>&mut country</code>.",
     ]) +
     code("rust", '''fn add_hungary(country_name: &mut String) {
    country_name.push_str("-Hungary");
    println!("Now it says: {}", country_name);
}

fn main() {
    let mut country = String::from("Austria");
    add_hungary(&mut country);
}''')),
    ("fn-mut-param",
     "A mut parameter takes ownership",
     bullets([
         "<code>mut string: String</code> is not a reference. It takes ownership and makes it mutable.",
         "The original variable is gone; the function owns the data now.",
         "This is different from a mutable reference.",
     ]) +
     code("rust", '''fn main() {
    let country = String::from("Austria");
    adds_hungary(country);
}

fn adds_hungary(mut string_to_add_hungary_to: String) {
    string_to_add_hungary_to.push_str("-Hungary");
    println!("{}", string_to_add_hungary_to);
}''') +
     '<p>Notice the warning if you mark the original <code>country</code> as <code>mut</code>: the caller never mutates it, so the <code>mut</code> belongs on the parameter, not the caller.</p>'),
])

# Section 9: Copy types
sections.append([
    ("copy-intro",
     "Copy types",
     bullets([
         "Small, fixed-size types live on the stack and are cheap to copy.",
         "When you pass them to a function, Rust copies the value automatically.",
         "Copy types use <em>copy semantics</em>; everything else uses <em>move semantics</em>.",
     ]) +
     code("rust", '''fn prints_number(number: i32) {
    println!("{}", number);
}

fn main() {
    let my_number = 8;
    prints_number(my_number);
    prints_number(my_number); // fine: i32 is Copy
}''')),
    ("copy-vs-clone",
     "Copy vs Clone",
     bullets([
         "<code>Copy</code> happens automatically for small stack types.",
         "<code>Clone</code> is explicit: you call <code>.clone()</code>.",
         "<code>String</code> implements <code>Clone</code> but not <code>Copy</code>.",
         "Cloning a large string can use a lot of memory; borrowing is usually better.",
     ]) +
     code("rust", '''fn prints_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Kiribati");
    prints_country(country.clone());
    prints_country(country); // fine because we cloned
}''')),
    ("references-are-cheap",
     "References are cheap",
     bullets([
         "If a function only needs to read, pass an immutable reference.",
         "This avoids both moves and clones.",
     ]) +
     code("rust", '''fn get_length(input: &String) {
    println!("It is {} words long.", input.split_whitespace().count());
}

fn main() {
    let mut s = String::new();
    for _ in 0..50 {
        s.push_str("Here are some more words ");
        get_length(&s); // zero clones
    }
}''')),
])

# Section 10: Variables without values
sections.append([
    ("uninit",
     "Uninitialized variables",
     bullets([
         "You can declare a variable without giving it a value.",
         "You must initialize it before you use it.",
         "This is useful when a value comes from inside a block but needs to live outside it.",
     ]) +
     code("rust", '''fn main() {
    let my_number: i32;
    {
        my_number = 57;
        println!("{my_number}");
    }
}''') +
     '<p>The variable is not <code>mut</code>. It is simply not given a value until it is assigned.</p>'),
])

# Section 11: More about printing
sections.append([
    ("print-escapes",
     "Escapes and raw strings",
     bullets([
         "<code>\\n</code> is a newline, <code>\\t</code> is a tab.",
         "To print a literal backslash, escape it with another backslash.",
         "Prefix a string with <code>r#</code> and end with <code>#</code> for a raw string.",
     ]) +
     code("rust", '''fn main() {
    println!("Line one\\nLine two");
    println!("Here are two escapes: \\\\n and \\\\t");
    println!(r#"This has \"quotes\" and \\ backslashes as-is."#);
}''')),
    ("print-bytes",
     "Byte strings",
     bullets([
         "Add <code>b</code> before a string to make a byte string literal.",
         "The result is an array of bytes, not text.",
     ]) +
     code("rust", '''fn main() {
    println!("{:?}", b"This will look like numbers");
}''') +
     code("text", '''[84, 104, 105, 115, 32, 119, 105, 108, 108, 32, 108, 111, 111, 107, 32, 108, 105, 107, 101, 32, 110, 117, 109, 98, 101, 114, 115]''')),
    ("print-pointers",
     "Pointer addresses",
     bullets([
         "Use <code>{:p}</code> to print the address a reference points to.",
     ]) +
     code("rust", '''fn main() {
    let number = 9;
    let number_ref = &number;
    println!("{:p}", number_ref); // e.g. 0x7ffd4a2bfcfc
}''')),
    ("print-bases",
     "Number bases",
     bullets([
         "<code>{:b}</code> prints binary.",
         "<code>{:x}</code> prints hexadecimal.",
         "<code>{:o}</code> prints octal.",
     ]) +
     code("rust", '''fn main() {
    let number = 555;
    println!("Binary: {:b}, hex: {:x}, octal: {:o}", number, number, number);
}''') +
     code("text", '''Binary: 1000101011, hex: 22b, octal: 1053''')),
    ("print-positional",
     "Positional and named arguments",
     bullets([
         "Use an index like <code>{0}</code> or a name like <code>{city}</code> to control ordering.",
     ]) +
     code("rust", '''fn main() {
    let father = "Vlad";
    let son = "Adrian Fahrenheit";
    let family = "Ţepeş";
    println!("This is {1} {2}, son of {0} {2}.", father, son, family);

    println!(
        "{city1} is in {country} and {city2} is also in {country}.",
        city1 = "Seoul",
        city2 = "Busan",
        country = "Korea"
    );
}''')),
    ("print-padding",
     "Padding and alignment",
     bullets([
         "Format: <code>{variable:pad alignment minimum.maximum}</code>.",
         "<code>^</code> centers, <code>&lt;</code> left-aligns, <code>&gt;</code> right-aligns.",
     ]) +
     code("rust", '''fn main() {
    let title = "TODAY'S NEWS";
    println!("{:-^30}", title);

    let bar = "|";
    println!("{: <15}{: >15}", bar, bar);

    let a = "SEOUL";
    let b = "TOKYO";
    println!("{city1:-<15}{city2:->15}", city1 = a, city2 = b);
}''') +
     code("text", '''---------TODAY'S NEWS---------
|                            |
SEOUL--------------------TOKYO''')),
])

# Section 12: Python vs Rust gotchas
sections.append([
    ("python-gotchas",
     "Python vs Rust gotchas",
     '<p class="lede">Ownership and borrowing look unusual if you are coming from Python. Here are the main traps.</p>'),
    ("gc-vs-ownership",
     "GC vs ownership",
     bullets([
         "Python uses garbage collection: objects live as long as any name points to them.",
         "Rust has no GC. Each value has exactly one owner, and the value is dropped when the owner goes out of scope.",
         "References let other code look at the data without taking ownership.",
     ]) +
     code("rust", '''fn main() {
    let s = String::from("owned");
    let r = &s;      // borrow
    println!("{}", r);
    println!("{}", s); // owner is still valid
}''')),
    ("references-not-names",
     "References are explicit borrows",
     bullets([
         "In Python, every name is a reference to an object, and the GC manages lifetimes.",
         "In Rust, a reference is an explicit <code>&</code> or <code>&mut</code> with rules attached.",
         "You cannot keep a reference after the owner has been dropped.",
     ])),
    ("clone-vs-deepcopy",
     ".clone() vs deepcopy",
     bullets([
         "Python <code>copy.deepcopy</code> recursively copies an object.",
         "Rust <code>.clone()</code> calls the <code>Clone</code> trait. For a String, it copies the heap data.",
         "Cloning is explicit and can be expensive; prefer borrowing when you can.",
     ]) +
     code("rust", '''fn main() {
    let a = String::from("hello");
    let b = a.clone();
    println!("{} {}", a, b);
}''')),
    ("mut-param-ownership",
     "mut parameter takes ownership",
     bullets([
         "A parameter like <code>mut s: String</code> is not a reference.",
         "It takes full ownership and makes the value mutable inside the function.",
         "The caller's original variable is gone after the call.",
     ])),
    ("return-local",
     "Returning references from locals",
     bullets([
         "A function cannot return a reference to data it created.",
         "The local data is dropped at the end of the function, so the reference would dangle.",
         "Return owned data instead, or accept a reference as input and return a reference tied to it.",
     ])),
    ("slices-as-views",
     "Slices are views",
     bullets([
         "A <code>&str</code> is a slice: a pointer and a length into existing data.",
         "It does not own the bytes. If the owner is dropped, the slice becomes invalid.",
         "This is similar to Python memory views or NumPy slices, but checked at compile time.",
     ])),
])

# Section 13: Summary
sections.append([
    ("summary",
     "Summary",
     bullets([
         "The stack holds fixed-size data; the heap holds data whose size is not known at compile time.",
         "A reference borrows memory without owning it. A mutable reference can change the data.",
         "String is owned and growable; &str is a borrowed slice. Both are UTF-8.",
         "const and static create global values that last for the whole program.",
         "You can have many immutable references or one mutable reference, but not both at once.",
         "Copy types copy automatically; everything else moves unless you borrow or clone.",
         "Uninitialized variables are allowed, but you must assign before using them.",
         "println! supports escapes, raw strings, byte strings, pointer addresses, bases, positional/named arguments, and padding.",
     ])),
])

# Section 14: Fin
sections.append([
    ("fin",
     "What comes next",
     '<p class="lede">In the next chapter we look at Rust\'s collection types: tuples, arrays, and vectors.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec02-memory-and-ownership/">return to the chapter page</a>.</p>'),
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

# -- Build full HTML ----------------------------------------------------------

body_html = "".join(section_html_parts)
slide_count = slide_idx

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rust: First Steps - Lecture 2: Memory and Ownership · Hassan Aziz</title>

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

    /* -- Copy-to-clipboard button on every <pre> ------------------------ */
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
