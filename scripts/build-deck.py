#!/usr/bin/env python3
"""
build-deck.py - generate a reveal.js slide deck for the class site.

Usage:
  1. Edit the `sections` list at the bottom of this file.
     - Each top-level list becomes a horizontal section (navigate with <-/->).
     - Each item inside a top-level list becomes a vertical sub-slide
       (navigate with up/down).
  2. Change `OUT` if you want a different deck path, e.g.
     OUT = "static/slides/rfs-2/index.html".
  3. Run: python3 scripts/build-deck.py
  4. Verify with: zola build && zola serve

Slide item format:
  (data_id, title, body_html)

- `data_id` must be unique; it becomes the slide's `data-id` attribute.
- `title` may contain inline HTML such as <code>, <em>, <strong>.
- `body_html` is raw HTML. Use the helpers `bullets(...)` and `code(lang, src)`
  for common patterns.

The generated deck uses the shared `clean.css` theme and follows the system
light/dark preference.
"""
import html

OUT = "static/slides/rfs-1/index.html"

# -- Helper to build a single slide -------------------------------------------

def slide(idx, title, body, kicker=None, data_id=None):
    sid = (data_id or f"{idx:02d}").lower().replace(" ", "-")
    label = kicker or f"{idx:02d}"
    tag = "h1" if idx == 1 else "h2"
    # Title may contain inline HTML (<code>, <em>, etc.). Do NOT escape it.
    title_html = f"<{tag}>{title}</{tag}>" if title else ""
    parts = [f'<span class="slide-id">{html.escape(label)}</span>', title_html]
    if body:
        parts.append(body)
    return f'        <section data-id="{html.escape(sid)}">\n          ' + "\n          ".join(filter(None, parts)) + "\n        </section>\n"

def bullets(items):
    return "<ul>\n" + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ul>"

def code(lang, src):
    return f'<pre><code class="language-{lang}" data-trim>{html.escape(src.rstrip())}</code></pre>'

# -- Slides grouped into reveal.js sections -----------------------------------
# Each top-level list is one horizontal section; nested lists are the vertical
# slides inside that section. Single-slide sections can be a flat list.

sections = []

# Section 1: Title
sections.append([
    ("title",
     "Rust: First Steps",
     '<p class="kicker">Lecture 1 - The Basics</p>\n<p class="lede">A first look at the compiler, types, variables, printing, mutability, and shadowing.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: The compiler's teaching style
sections.append([
    ("intro-what",
     "What is Rust?",
     bullets([
         "Released in 2015; by 2024 it powers Windows, Android, the Linux kernel, AWS, Discord, Cloudflare, and more.",
         "Speed and control close to C/C++, plus memory safety like newer languages.",
         "A rich type system catches bugs before the program runs.",
         "The compiler is famously strict <em>and</em> famously helpful.",
         "Some ideas are new, so you have to think before you code. You cannot just figure it out as you go.",
     ])),
    ("intro-hangover",
     "The hangover first",
     bullets([
         "In many languages the party starts first: code compiles, looks great, then you debug at runtime.",
         "In Rust you get the hangover first: the compiler refuses to run code that might be wrong.",
         "You must satisfy the compiler about types, errors, missing values, and memory safety up front.",
         "The payoff: once it compiles, it usually works.",
     ])),
    ("intro-teacher",
     "The compiler as a teacher",
     bullets([
         "Error messages often include the exact fix: add <code>mut</code>, use single quotes, insert a comma, etc.",
         "The compiler feels like a co-programmer or teacher rather than an adversary.",
         "Fixing errors teaches you how memory and types work.",
         "Rust is not just a tool for building software; it is a tool for understanding computers.",
     ])),
    ("intro-pep",
     "A pep talk",
     bullets([
         "Rust is complex, but the frustrating phase does not last forever.",
         "Once it clicks, the compiler starts doing a lot of the thinking for you.",
         "Junior developers can refactor existing code with confidence: if it compiles, it is usually safe.",
         "The cycle of 'make changes -> see compiler feedback -> fix one by one' is fast and reliable.",
     ])),
    ("intro-spouse",
     "Rust is like a critical spouse",
     '<p>Rust will not let you out the door unprepared.</p>\n' +
     bullets([
         "It complains about the heavy suit, the mismatched socks, the windy hair, and the missing parking change.",
         "Each complaint feels annoying until you see your reflection, and then you realize you look great.",
         "Other languages smile and wave, then let you discover the problems at the interview.",
         "Rust is strict at compile time, where programmers live, so runtime surprises are rare.",
     ]) +
     '<blockquote style="margin-top:1.2rem;">"In Rust, you get the hangover first."</blockquote>'),
    ("try-broken",
     "A first try",
     '<p>This program looks reasonable, but Rust rejects it:</p>\n' +
     code("rust", '''fn main() {
    let my_name: String = "Dave";
    my_name.push("!");
    println!("{}" my_name);
}''') +
     '<p style="margin-top:0.6rem;color:var(--fg-3);font-size:1rem;">The compiler will walk us through three issues before we reach the next one.</p>'),
    ("fix-1",
     "Fix #1: a missing comma",
     '<p>The first error is about the <code>println!</code> call:</p>\n' +
     code("rust", '''error: expected `,`, found `my_name`
  |
4 |     println!("{}" my_name);
  |               ^^^^^^^ expected `,`''') +
     '<p>Format arguments in <code>println!</code> must be separated by commas.</p>'),
    ("fix-2",
     "Fix #2: <code>&str</code> vs <code>String</code>",
     '<p><code>"Dave"</code> is a string slice (<code>&str</code>), not an owned <code>String</code>:</p>\n' +
     code("rust", '''error[E0308]: mismatched types
 --> src/main.rs:2:27
  |
2 |     let my_name: String = "Dave";
  |                   ------   ^^^^^^
  |                   |        |
  |                   |        expected struct `String`, found `&str`
  |                   expected due to this
  |
  = help: try using a conversion method: `.to_string()`''') +
     '<p>Add <code>.to_string()</code> to create an owned <code>String</code>.</p>'),
    ("fix-3",
     "Fix #3: <code>char</code> vs <code>&str</code>",
     '<p><code>push</code> expects a single character, but <code>"!"</code> is a string slice:</p>\n' +
     code("rust", '''error[E0308]: mismatched types
 --> src/main.rs:3:18
  |
3 |     my_name.push("!");
  |             ---- ^^^ expected `char`, found `&str`
  |
  = help: if you meant to write a `char` literal, use single quotes''') +
     '<p>Use single quotes for a <code>char</code>: <code>\'!\'</code>.</p>'),
    ("fix-after3",
     "After the first three fixes",
     '<p>The code now looks like this:</p>\n' +
     code("rust", '''fn main() {
    let my_name: String = "Dave".to_string();
    my_name.push('!');
    println!("{}", my_name);
}''') +
     '<p>But Rust has one more lesson to teach.</p>'),
    ("fix-4",
     "Fix #4: mutability",
     '<p><code>push</code> changes the string, so the variable must be mutable:</p>\n' +
     code("rust", '''error[E0596]: cannot borrow `my_name` as mutable, as it is not declared as mutable
 --> src/main.rs:3:5
  |
2 |     let my_name: String = "Dave".to_string();
  |         ------- help: consider changing this to be mutable: `mut my_name`
3 |     my_name.push('!');
  |     ^^^^^^^^^^^^^^^^^ cannot borrow as mutable''') +
     '<p>Add <code>mut</code> after <code>let</code>.</p>'),
    ("fix-working",
     "A working program",
     '<p>The final, compiling program:</p>\n' +
     code("rust", '''fn main() {
    let mut my_name: String = "Dave".to_string();
    my_name.push('!');
    println!("{}", my_name);
}''') +
     '<p>Output: <code>Dave!</code></p>'),
    ("fix-unused",
     "Unused variables",
     '<p>Rust warns about variables you create but never use:</p>\n' +
     code("rust", '''fn main() {
    let my_number = 9;
}''') +
     code("rust", '''warning: unused variable: `my_number`
 --> src/main.rs:2:9
  |
2 |     let my_number = 9;
  |         ^^^^^^^^^ help: if this is intentional, prefix it with an underscore: `_my_number`''') +
     '<p>Prefix with <code>_</code> to silence the warning.</p>'),
])

# Section 3: Comments
sections.append([
    ("comments-line",
     "Line comments",
     '<p>Comments are for humans; the compiler ignores them.</p>\n' +
     code("rust", '''fn main() {
    // Rust programs start with fn main()
    // You put the code inside a block: { ... }
    let some_number = 100; // the rest of the line is ignored
}''') +
     '<p>Use <code>//</code> for everything to the right of the slashes.</p>'),
    ("comments-block",
     "Block comments",
     '<p>Use <code>/*</code> and <code>*/</code> for multi-line comments or comments in the middle of a line:</p>\n' +
     code("rust", '''fn main() {
    let some_number/*: i16*/ = 100;

    let x = 100; /* Let me tell you
    a little about this number.
    It's 100, which is my favorite number. */
}''') +
     '<p>To the compiler, both examples look like <code>let some_number = 100;</code>.</p>'),
    ("comments-doc",
     "Doc comments",
     '<p><code>///</code> creates documentation that tools can turn into web pages.</p>\n' +
     code("rust", '''/// Converts a string slice in a given base to an integer.
/// Leading and trailing whitespace represent an error.
fn parse(input: &str) -> Result<i32, ()> {
    todo!()
}''') +
     '<ul>\n<li><code>//</code> = informal comment inside the code.</li>\n<li><code>///</code> = official documentation for readers of your API.</li>\n<li>Try <code>cargo doc --open</code> to see the generated docs.</li>\n</ul>'),
])

# Section 4: Integers
sections.append([
    ("primitives",
     "Primitive types",
     '<p>The simplest built-in types are called <em>primitive</em> types.</p>\n' +
     bullets([
         "Integers: <code>i8</code>, <code>i16</code>, <code>i32</code>, <code>i64</code>, <code>i128</code>, <code>isize</code> (signed) and <code>u8</code> ... <code>usize</code> (unsigned).",
         "Floats: <code>f32</code> and <code>f64</code>.",
         "Characters: <code>char</code>.",
         "Booleans: <code>bool</code>.",
         "Text slices and owned strings: <code>&str</code> and <code>String</code>.",
     ])),
    ("integers",
     "Integers",
     '<p>Signed integers can be negative; unsigned integers cannot.</p>\n' +
     code("rust", '''// signed:   i8, i16, i32, i64, i128, isize
// unsigned: u8, u16, u32, u64, u128, usize

fn main() {
    let a: i32 = -8;   // signed
    let b: u32 = 8;    // unsigned
    let c = 8;         // Rust chooses i32 by default
}''') +
     '<p>The number in the name is the bit width: <code>u8</code> = 1 byte, <code>i64</code> = 8 bytes.</p>'),
    ("binary",
     "Binary in a byte",
     '<p>Each bit is twice the previous one. An 8-bit number uses these places:</p>\n' +
     code("text", '''128 | 64 | 32 | 16 | 8 | 4 | 2 | 1''') +
     '<p>Decimal 226 in binary is <code>11100010</code>:</p>\n' +
     code("text", '''128 + 64 + 32 + 0 + 0 + 0 + 2 + 0 = 226''') +
     '<p>That is why a <code>u8</code> maxes out at 255: <code>11111111</code> = 1+2+4+8+16+32+64+128.</p>'),
    ("ranges",
     "Signed vs unsigned ranges",
     '<p>With the same number of bits, signed types sacrifice half the positive range for negatives.</p>\n' +
     code("rust", '''fn main() {
    println!("u8 range:  {} to {}", u8::MIN, u8::MAX);   // 0 to 255
    println!("i8 range:  {} to {}", i8::MIN, i8::MAX);   // -128 to 127
    println!("u16 range: {} to {}", u16::MIN, u16::MAX); // 0 to 65535
}''') +
     '<p><code>isize</code>/<code>usize</code> match your computer\'s architecture: 32 bits on 32-bit machines, 64 bits on 64-bit machines.</p>'),
    ("minmax",
     "Smallest and largest numbers",
     '<p>Every integer type has associated <code>MIN</code> and <code>MAX</code> constants.</p>\n' +
     code("rust", '''fn main() {
    println!("i8:  {} to {}", i8::MIN, i8::MAX);
    println!("u8:  {} to {}", u8::MIN, u8::MAX);
    println!("i32: {} to {}", i32::MIN, i32::MAX);
    println!("u32: {} to {}", u32::MIN, u32::MAX);
}''') +
     '<p>They are uppercase because they are <code>const</code>s attached to the type with <code>::</code>.</p>'),
])

# Section 5: Characters and strings
sections.append([
    ("chars",
     "Characters",
     '<p>A <code>char</code> is a single Unicode scalar value and uses 4 bytes.</p>\n' +
     code("rust", '''fn main() {
    let first_letter = 'A';        // ASCII
    let space = ' ';               // even a space is a char
    let korean = '안';              // 3 bytes as UTF-8
    let cat_face = '🐱';            // 4 bytes as UTF-8
}''') +
     '<p>Single quotes <code>\'\'</code> create a <code>char</code>; double quotes <code>""</code> create a string slice.</p>'),
    ("casting",
     "Casting with <code>as</code>",
     '<p><code>as</code> converts one numeric type to another. Only <code>u8</code> can become a <code>char</code>.</p>\n' +
     code("rust", '''fn main() {
    let my_number = 100;
    // println!("{}", my_number as char); // error: only u8 -> char
    println!("{}", my_number as u8 as char); // prints 'd'
}''') +
     '<p>Rust is strict: it will not silently convert <code>i32</code> to <code>u8</code> for you.</p>'),
    ("cast-overflow",
     "Casting can overflow",
     '<p>Casting a large number into a smaller type wraps around:</p>\n' +
     code("rust", '''fn main() {
    let a = 256;
    println!("{}", a as u8);  // 0

    let b = 600;
    println!("{}", b as u8);  // 88  (600 - 256 - 256 = 88)
}''') +
     '<p>Always make sure the original value fits in the target type.</p>'),
    ("string-len",
     "String length: bytes vs characters",
     '<p><code>.len()</code> returns the number of <em>bytes</em>, not the number of letters.</p>\n' +
     code("rust", '''fn main() {
    let str1 = "Hello!";
    let str2 = "안녕!";
    println!("str1: {} bytes, {} chars", str1.len(), str1.chars().count());
    println!("str2: {} bytes, {} chars", str2.len(), str2.chars().count());
}''') +
     code("text", '''str1: 6 bytes, 6 chars
str2: 7 bytes, 3 chars''')),
    ("bytes",
     "Seeing the bytes",
     '<p><code>.as_bytes()</code> shows the raw UTF-8 encoding:</p>\n' +
     code("rust", '''fn main() {
    println!("{:?}", "a".as_bytes());   // [97]
    println!("{:?}", "ß".as_bytes());   // [195, 159]
    println!("{:?}", "안".as_bytes());   // [236, 149, 132]
    println!("{:?}", "🐱".as_bytes());   // [240, 159, 144, 177]
}''') +
     '<p>One byte for ASCII, two for many European letters, three for most CJK, four for emoji and ancient scripts.</p>'),
])

# Section 6: Type system
sections.append([
    ("inference",
     "Type inference",
     '<p>Rust usually figures out the type from the value.</p>\n' +
     code("rust", '''fn main() {
    let my_number = 8;        // i32
    let my_float = 5.0;       // f64
    let letter = 'A';         // char

    let small: u8 = 10;       // explicit
    let small_too = 10u8;     // suffix
    let readable = 1_000_000_i32; // underscores ignored
}''') +
     '<p>You only need to be explicit when the compiler cannot decide or you want a different type.</p>'),
    ("floats",
     "Floats",
     '<p>Numbers with a decimal point are floats: <code>f32</code> or <code>f64</code>.</p>\n' +
     code("rust", '''fn main() {
    let a = 5.0;          // f64 (default)
    let b: f32 = 5.0;     // f32
    let c = 5.;           // also f64

    // let bad = a + b;   // error: cannot add f64 and f32
    let ok = a + b as f64; // cast, or remove the :f32 above
}''') +
     '<p>Like integers, floats of different widths do not mix automatically.</p>'),
])

# Section 7: Functions and blocks
sections.append([
    ("hello",
     "Hello, world!",
     '<p>Every Rust program starts in <code>fn main()</code>.</p>\n' +
     code("rust", '''fn main() {
    println!("Hello, world!");
}''') +
     bullets([
         "<code>fn</code> declares a function.",
         "<code>main()</code> is the entry point: where the program starts.",
         "<code>()</code> means no arguments this time.",
         "<code>{}</code> is a code block: the body of the function.",
         "<code>println!</code> is a macro. Notice the <code>!</code>.",
     ])),
    ("blocks",
     "Code blocks and lifetimes",
     '<p>A pair of braces <code>{}</code> defines a block. Variables live until the end of the block that contains them.</p>\n' +
     code("rust", '''fn main() {
    let a = 5.0;
    {
        let b = 8.5;
    } // b is dropped here

    // println!("{}", b); // error: not found
}''') +
     '<p>This is the foundation of Rust\'s ownership system.</p>'),
    ("block-return",
     "Returning values from blocks",
     '<p>If the last expression has no semicolon, the block returns it:</p>\n' +
     code("rust", '''fn main() {
    let n = {
        let x = 8;
        x + 9 // returns 17
    };
    println!("{}", n);
}''') +
     '<p>Add a semicolon and the block returns <code>()</code>, the unit type.</p>'),
    ("printing",
     "Printing with placeholders",
     '<p><code>{}</code> inside <code>println!</code> is replaced by the matching argument.</p>\n' +
     code("rust", '''fn main() {
    let x = 8;
    let y = 9;
    println!("Hello, world number {}!", x);
    println!("Hello, worlds number {} and {}!", x, y);
    println!("Hello, world number {x}!"); // named capture, Rust 2021+
}''') +
     '<p><code>print!</code> is the same but does not add a newline.</p>'),
    ("functions",
     "Functions",
     '<p>Functions can take inputs and return values.</p>\n' +
     code("rust", '''fn multiply(number_one: i32, number_two: i32) -> i32 {
    number_one * number_two
}

fn main() {
    let result = multiply(8, 9);
    println!("The two numbers multiplied are: {}", result);
}''') +
     '<p>The return type comes after <code>-></code>. The last expression is returned.</p>'),
    ("semicolon",
     "The semicolon rule",
     '<p>A semicolon turns an expression into a statement. Statements do not return a value.</p>\n' +
     code("rust", '''fn give_number() -> i32 {
    8;  // statement, returns ()
}

fn main() {
    println!("{}", give_number());
}''') +
     code("rust", '''error[E0308]: mismatched types
 --> src/main.rs:1:21
  |
1 | fn give_number() -> i32 {
  |    -----------      ^^^ expected `i32`, found `()`
  |
  = help: remove this semicolon to return this value''') +
     '<p>Remove the <code>;</code> to return <code>8</code>.</p>'),
    ("return",
     "Early return",
     '<p>You can use <code>return</code> to leave a function before the last line:</p>\n' +
     code("rust", '''fn give_number() -> i32 {
    return 8;
    10; // unreachable
}

fn main() {
    println!("{}", give_number()); // 8
}''') +
     '<p>Rust warns about unreachable code, but it still compiles.</p>'),
])

# Section 8: Display / Debug
sections.append([
    ("display-debug",
     "Display and Debug",
     '<p>Not every type can print with <code>{}</code>.</p>\n' +
     code("rust", '''fn main() {
    let unit = ();
    println!("{}", unit); // error: `()` doesn't implement Display
}''') +
     '<p>The compiler suggests <code>{:?}</code> (Debug) or <code>{:#?}</code> (pretty Debug).</p>\n' +
     code("rust", '''fn main() {
    let unit = ();
    println!("{:?}", unit);   // ()
    println!("{:#?}", unit);  // ()  (pretty, when there is more to show)
}''')),
    ("traits",
     "Traits at a glance",
     '<p>A <em>trait</em> is "what a type can do."</p>\n' +
     bullets([
         "<code>Display</code> ({}) is for user-facing output.",
         "<code>Debug</code> ({:?}) is for programmer-facing output.",
         "If a type does not implement a trait, the compiler tells you and suggests alternatives.",
         "Traits are one of Rust\'s most powerful ideas; we will return to them throughout the course.",
     ])),
])

# Section 9: Mutability and shadowing
sections.append([
    ("mutability",
     "Mutability",
     '<p>Variables are immutable by default.</p>\n' +
     code("rust", '''fn main() {
    let my_number = 8;
    my_number = 10; // error: cannot assign twice to immutable variable
}''') +
     '<p>Add <code>mut</code> to allow change. But you still cannot change the <em>type</em>:</p>\n' +
     code("rust", '''fn main() {
    let mut x = 8;
    x = 10;              // ok
    // x = "hello";       // error: expected integer, found &str
}''') +
     bullets([
         "In Python, <code>x = 8; x = 10</code> rebinds the name. In Rust, <code>let x = 8; x = 10</code> is an error unless you write <code>let mut x</code>.",
         "<code>mut</code> goes on the binding: <code>let mut x</code>, not on the type.",
         "Even with <code>mut</code>, the type is fixed.",
     ])),
    ("shadowing",
     "Shadowing",
     '<p>Shadowing creates a new variable with the same name. It is <em>not</em> mutability.</p>\n' +
     code("rust", '''fn main() {
    let my_number = 8;
    println!("{}", my_number); // 8

    let my_number = 9.2;       // shadows the first one
    println!("{}", my_number); // 9.2
}''') +
     '<p>The new binding can have a different type. The old value is blocked, not destroyed.</p>\n' +
     bullets([
         "In Python, <code>x = 8; x = 9.2</code> makes the same name point somewhere else.",
         "In Rust, <code>let x = 8; let x = 9.2</code> creates a second binding that hides the first.",
         "The first binding is still alive in memory until its scope ends.",
     ])),
    ("shadowing-scope",
     "Shadowing and scope",
     '<p>A shadow only lasts inside its own block:</p>\n' +
     code("rust", '''fn main() {
    let my_number = 8;
    {
        let my_number = 9.2;
        println!("inside: {}", my_number); // 9.2
    }
    println!("outside: {}", my_number);    // 8
}''') +
     '<p>Useful when you want to transform a value through several steps without inventing a new name for every step.</p>'),
])

# Section 10: Python vs Rust gotchas
sections.append([
    ("python-gotchas",
     "Python vs Rust gotchas",
     '<p class="lede">A few habits from Python that do not carry over.</p>'),
    ("python-move",
     "Assignment moves, not copies",
     bullets([
         "Python: <code>a = [1, 2]; b = a</code> makes both names point to the same list.",
         "Rust: <code>let a = String::from(\"hi\"); let b = a;</code> moves the String into <code>b</code>. <code>a</code> is no longer valid.",
         "This is why a function that takes <code>String</code> consumes it unless you pass <code>&String</code>.",
     ]) +
     code("rust", '''fn main() {
    let a = String::from("hello");
    let b = a;
    println!("{}", a); // error: borrow of moved value
}''')),
    ("python-mut",
     "Mutability lives on the binding",
     bullets([
         "In Python you can rebind a name to anything at any time.",
         "In Rust, <code>mut</code> controls whether the value behind the binding can change in place.",
         "Write <code>let mut x: i32</code>, not <code>let x: mut i32</code>.",
     ]) +
     code("rust", '''fn main() {
    let mut count = 0;
    count += 1; // ok: the value changes in place
    // count = "one"; // error: expected integer, found &str
}''')),
    ("python-shadow",
     "Shadowing is not rebinding",
     bullets([
         "Python <code>x = 8; x = \"eight\"</code> changes what the name refers to.",
         "Rust <code>let x = 8; let x = \"eight\"</code> creates a second binding with a different type.",
         "The first binding stays alive until its scope ends; it is just hidden.",
     ]) +
     code("rust", '''fn main() {
    let x = 8;
    let x = "eight";
    println!("{}", x); // prints "eight"
}''')),
    ("python-format",
     "Format strings are checked at compile time",
     bullets([
         "Python f-strings are evaluated at runtime.",
         "Rust checks <code>println!</code> placeholders at compile time.",
         "Missing or mismatched arguments are caught before the program runs.",
     ]) +
     code("rust", '''fn main() {
    let name = "Dave";
    // println!("{}", x); // error: cannot find value `x`
    println!("Hello, {name}!"); // ok
}''')),
    ("python-unit",
     "The unit type is not None",
     bullets([
         "Python <code>None</code> means 'no value'.",
         "Rust <code>()</code> is the unit type: a real value that carries no information.",
         "A function with no return expression returns <code>()</code>.",
     ]) +
     code("rust", '''fn no_value() {}

fn main() {
    let x = no_value();
    println!("{:?}", x); // ()
}''')),
])

# Section 11: Summary
sections.append([
    ("summary",
     "Summary",
     bullets([
         "Comments: <code>//</code>, <code>/* */</code>, and doc comments <code>///</code>.",
         "You can annotate types, but Rust usually infers them; default integers are i32 and default floats are f64.",
         "Understanding binary helps you choose the right integer size.",
         "Variables live inside <code>{}</code> blocks unless they are returned into a larger scope.",
         "Use <code>mut</code> to change a value; shadowing with <code>let</code> creates a new binding instead.",
         "The compiler is strict at compile time so your program is safer at runtime.",
         "From Python: remember moves, binding-level mutability, shadowing, compile-time format checks, and the unit type <code>()</code>.",
     ])),
    ("fin",
     "What comes next",
     '<p class="lede">In the next chapter we explore ownership: how Rust decides who is allowed to use each piece of memory, and for how long.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec01-the-basics/">return to the chapter page</a>.</p>'),
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
  <title>Rust: First Steps - Lecture 1: The Basics · Hassan Aziz</title>

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
