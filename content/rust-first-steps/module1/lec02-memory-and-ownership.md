+++
title       = "Lecture 2 - Memory and Ownership"
date        = 2026-06-19
description = "A comprehensive summary of Rust Chapter 2. Covers the stack and heap, pointers and references, String and &str, UTF-8, const and static, mutable references, shadowing, functions and ownership, Copy types, uninitialized variables, advanced printing, and Python-vs-Rust gotchas."
weight      = 2

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 2
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-2 -->

## Slides

{{ slides(src="/slides/rfs-2/index.html", title="Lec 2 - Memory and Ownership", note="42 slides · ~55 min") }}

## At a glance

This lecture focuses on memory. Rust forces you to think about where data lives,
who owns it, and who is allowed to change it. The payoff is safety without a garbage
collector.

### The stack and the heap

Rust uses two places to store data:

- The **stack** holds values with a known, fixed size. It is fast because allocation
  and cleanup follow a strict last-in, first-out order.
- The **heap** holds data whose size is not known at compile time. The program asks
  the OS for memory, and a pointer on the stack records where that memory lives.

```rust
fn main() {
    let x = 8;                         // i32 on the stack
    let s = String::from("on heap");   // pointer on stack, text on heap
}
```

### Pointers and references

A pointer stores an address. The most common pointer in Rust is a **reference**,
written with `&`:

```rust
fn main() {
    let my_number = 15;
    let r = &my_number;        // r borrows my_number
    println!("{}", r);         // prints 15
}
```

A reference borrows a value without owning it. The owner keeps the data, and the
reference is only valid while the owner is alive. You cannot return a reference to a
local variable from a function, because the local is dropped when the function ends.

### String and &str

Rust has two main string types:

- `String` is an owned, growable buffer on the heap.
- `&str` is a borrowed slice: a pointer and a length into existing UTF-8 bytes.

Both are UTF-8 encoded. `&str` is not `Sized`; you cannot write `let s: str = "...";`
because the compiler would not know how much stack space to reserve. The reference
`&str` has a fixed size, so it works.

```rust
fn main() {
    let owned = String::from("owned");
    let borrowed: &str = "borrowed";
    let together = format!("{} {}", owned, borrowed);
}
```

Use `.len()` for the number of bytes and `.chars().count()` for the number of
characters:

```rust
fn main() {
    let s = "안녕!";
    println!("{} bytes, {} chars", s.len(), s.chars().count());
}
```

### const and static

Global values use `const` or `static`:

```rust
const NUMBER_OF_MONTHS: u32 = 12;
static SEASONS: [&str; 4] = ["Spring", "Summer", "Fall", "Winter"];

fn main() {
    println!("{}", NUMBER_OF_MONTHS);
}
```

- `const` values are computed at compile time.
- `static` values have a fixed memory location and last for the whole program.
- Both are written in ALL_CAPS and usually live outside `main`.

### Mutable references

To change data through a reference, use `&mut`:

```rust
fn main() {
    let mut n = 8;
    let r = &mut n;
    *r += 10;
    println!("{}", n); // 18
}
```

The two reference rules are:

1. You can have any number of immutable references.
2. You can have only one mutable reference, and you cannot mix it with immutable
   references at the same time.

These rules prevent data races. The compiler tracks when each borrow ends, so later
borrows are allowed once the earlier ones are no longer used.

### Functions and ownership

A function that takes `String` takes ownership. If it does not return the value, the
caller loses it:

```rust
fn print_country(country_name: String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(country);
    // print_country(country); // error: use of moved value
}
```

Pass a reference to borrow instead:

```rust
fn print_country(country_name: &String) {
    println!("{}", country_name);
}

fn main() {
    let country = String::from("Austria");
    print_country(&country);
    print_country(&country); // fine
}
```

A parameter like `mut s: String` is not a reference. It takes ownership and makes
the value mutable inside the function. The caller's original variable is gone.

### Shadowing again

Shadowing with `let` creates a new binding. The old binding is hidden, not destroyed:

```rust
fn main() {
    let country = String::from("Austria");
    let country_ref = &country;
    let country = 8;
    println!("{country_ref} {country}"); // Austria 8
}
```

### Copy types

Small stack types are `Copy`. They copy automatically when passed to a function:

```rust
fn print_number(n: i32) {
    println!("{}", n);
}

fn main() {
    let x = 8;
    print_number(x);
    print_number(x); // fine: i32 is Copy
}
```

`String` is not `Copy`. If you need an independent copy, call `.clone()`:

```rust
fn main() {
    let a = String::from("hi");
    let b = a.clone();
    println!("{} {}", a, b);
}
```

Cloning can be expensive for large data. Borrowing is usually the better choice.

### Uninitialized variables

You can declare a variable without a value, but you must assign it before use:

```rust
fn main() {
    let n: i32;
    {
        n = 57;
    }
    println!("{n}");
}
```

### More about printing

Rust's `println!` macro supports a lot of formatting:

```rust
fn main() {
    println!("Line one\nLine two");
    println!(r#"Raw string with \"quotes\" and \ backslashes."#);
    println!("{:?}", b"bytes");

    let n = 555;
    println!("binary: {:b}, hex: {:x}, octal: {:o}", n, n, n);

    let r = &n;
    println!("address: {:p}", r);

    println!("{:-^30}", "TITLE");
}
```

You can also use positional or named arguments, padding, and alignment.

### Python vs Rust gotchas

- **GC vs ownership.** Python keeps objects alive as long as any name points to them.
  Rust has no GC. Every value has one owner, and references are explicit borrows.
- **References are explicit.** In Python, names are references managed by the runtime.
  In Rust, `&` and `&mut` are part of the type system with compile-time rules.
- **.clone() vs deepcopy.** Python's `copy.deepcopy` recursively copies objects. Rust's
  `.clone()` calls the `Clone` trait and makes an explicit duplicate. Prefer borrowing.
- **mut parameter takes ownership.** `fn f(mut s: String)` is not a reference. It moves
  the value into the function and makes it mutable there.
- **Returning references from locals.** A function cannot return `&String` to data it
  created. Return an owned value, or tie the returned reference to an input parameter.
- **Slices are views.** `&str` is a slice into existing bytes. It does not own the data.
  If the owner is dropped, the slice becomes invalid. Rust catches this at compile time.

## Takeaway

- The stack holds fixed-size data; the heap holds data whose size is unknown at
  compile time.
- `String` owns its heap data; `&str` borrows a view into UTF-8 bytes.
- References borrow; mutable references let you change data, but only one at a time.
- Functions take ownership by default. Borrow with `&` or `&mut` to avoid moves.
- Copy types are cheap to duplicate; everything else moves unless you clone or borrow.
- `const` and `static` create global values.
- `println!` supports escapes, raw strings, byte strings, bases, pointers, and rich
  formatting.
- From Python, the biggest shift is moving from a garbage-collected name model to an
  explicit ownership and borrowing model.
