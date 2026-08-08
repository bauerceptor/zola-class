+++
title       = "Lecture 1 - The Basics"
date        = 2026-06-15
description = "A comprehensive summary of Rust Chapter 1. Covers the compiler's teaching style, comments, integers and floats, chars and strings, type inference, printing, functions, code blocks, Display/Debug, mutability, shadowing, and Python-vs-Rust gotchas."
weight      = 1

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 1
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-1 -->

## Slides

{{ slides(src="/slides/rfs-1/index.html", title="Lec 1 - The Basics", note="49 slides · ~55 min") }}

## At a glance

This lecture is the first step into Rust. The main goal is to get comfortable with the
compiler's personality and to learn the small building blocks that every Rust program
uses: comments, scalar types, variables, printing, functions, mutability, and shadowing.

### The compiler as a teacher

Rust is strict at compile time. The compiler refuses to run code that might be wrong,
and it usually explains exactly what to fix. This can feel frustrating at first, but it means
runtime surprises are rare.

A first try at building a string shows the pattern:

```rust
fn main() {
    let my_name: String = "Dave";
    my_name.push("!");
    println!("{}" my_name);
}
```

The compiler walks you through the fixes one by one:

1. Add the missing comma in `println!("{}", my_name)`.
2. Convert `&str` to `String` with `"Dave".to_string()`.
3. Use a `char` literal for `push`: `'!'` instead of `"!"`.
4. Make the variable mutable with `let mut` so `push` can change it.

The final program looks like this:

```rust
fn main() {
    let mut my_name: String = "Dave".to_string();
    my_name.push('!');
    println!("{}", my_name);
}
```

Rust also warns about unused variables. Prefix with `_` (as in `_my_number`) if the
unused value is intentional.

### Comments

- `//` creates a line comment.
- `/* ... */` creates a block comment; it can span lines or sit in the middle of a line.
- `///` creates a doc comment, which `cargo doc` can turn into documentation.

```rust
fn main() {
    // This is a regular comment.
    let x = 100; /*: i16*/ // the type hint is commented out
}
```

### Primitive types

Rust's scalar types include integers, floats, characters, and booleans.

**Integers:**

- Signed: `i8`, `i16`, `i32`, `i64`, `i128`, `isize`.
- Unsigned: `u8`, `u16`, `u32`, `u64`, `u128`, `usize`.
- The number is the bit width. `u8` is 1 byte; `i64` is 8 bytes.
- Default integer type is `i32`. `isize`/`usize` match the machine word size.

A `u8` stores values 0 to 255 because its 8 bits represent powers of two:

```
128 | 64 | 32 | 16 | 8 | 4 | 2 | 1
```

Signed types split the range between negative and positive values:

```rust
fn main() {
    println!("u8 range:  {} to {}", u8::MIN, u8::MAX);   // 0 to 255
    println!("i8 range:  {} to {}", i8::MIN, i8::MAX);   // -128 to 127
}
```

**Characters:**

- A `char` is a single Unicode scalar value.
- It uses single quotes: `'A'`, `'안'`, `'🐱'`.
- Internally a `char` is 4 bytes so it can hold any Unicode character.

**Casting with `as`:**

```rust
fn main() {
    let n = 100;
    println!("{}", n as u8 as char); // prints 'd'
}
```

Casting to a smaller type can wrap:

```rust
fn main() {
    println!("{}", 256 as u8); // 0
    println!("{}", 600 as u8); // 88
}
```

**String length is measured in bytes:**

```rust
fn main() {
    let str1 = "Hello!";
    let str2 = "안녕!";
    println!("str1: {} bytes, {} chars", str1.len(), str1.chars().count());
    println!("str2: {} bytes, {} chars", str2.len(), str2.chars().count());
}
```

Output:

```
str1: 6 bytes, 6 chars
str2: 7 bytes, 3 chars
```

Use `.chars().count()` when you need the number of characters.

### Type inference

Rust usually figures out the type for you:

```rust
fn main() {
    let n = 8;        // i32
    let f = 5.0;      // f64
    let c = 'A';      // char
}
```

You can be explicit with a type annotation or a suffix:

```rust
fn main() {
    let a: u8 = 10;
    let b = 10u8;
    let c = 100_000_000_i32; // underscores are ignored
}
```

### Floats

Floats are `f32` and `f64`. The default is `f64`. You cannot mix the two without casting:

```rust
fn main() {
    let a = 5.0;      // f64
    let b: f32 = 8.5; // f32
    let c = a + b as f64;
}
```

### Hello, world! and printing

Every Rust program starts in `fn main()`:

```rust
fn main() {
    println!("Hello, world!");
}
```

- `fn` declares a function.
- `main()` is the program entry point.
- `println!` is a macro (note the `!`).
- `{}` is a placeholder for a value.

```rust
fn main() {
    let x = 8;
    let y = 9;
    println!("Hello, world number {}!", x);
    println!("Hello, worlds number {} and {}!", x, y);
    println!("Hello, world number {x}!"); // named capture, Rust 2021+
}
```

### Functions

Functions can take arguments and return values:

```rust
fn multiply(number_one: i32, number_two: i32) -> i32 {
    number_one * number_two
}

fn main() {
    let result = multiply(8, 9);
    println!("The two numbers multiplied are: {}", result);
}
```

The last expression in a function is its return value. If you add a semicolon, the function
returns `()` (the unit type) instead:

```rust
fn give_number() -> i32 {
    8 // returns 8
}
```

You can use `return` for early returns, but idiomatic Rust leaves off the semicolon on
the last line.

### Code blocks and lifetimes

A pair of braces `{}` defines a block. Variables live until the end of the block that
contains them:

```rust
fn main() {
    let a = 5.0;
    {
        let b = 8.5;
    } // b is dropped here

    // println!("{}", b); // error: b is not in scope
}
```

A block can also return a value:

```rust
fn main() {
    let n = {
        let x = 8;
        x + 9 // returns 17
    };
    println!("{}", n);
}
```

### Display and Debug

- `{}` uses the `Display` trait.
- `{:?}` uses the `Debug` trait.
- `{:#?}` pretty-prints with `Debug`.

Not every type implements `Display`. The compiler will suggest `{:?}` when that
happens. A trait is Rust's way of describing what a type can do.

### MIN and MAX

Every integer type has `MIN` and `MAX` constants:

```rust
fn main() {
    println!("i8:  {} to {}", i8::MIN, i8::MAX);
    println!("u32: {} to {}", u32::MIN, u32::MAX);
}
```

### Mutability

Variables are immutable by default:

```rust
fn main() {
    let x = 8;
    // x = 10; // error: cannot assign twice to immutable variable
}
```

Add `mut` to allow reassignment. You can change the value, but not the type:

```rust
fn main() {
    let mut x = 8;
    x = 10;              // ok
    // x = "hello";       // error: expected integer, found &str
}
```

`mut` lives on the binding, not the type. Write `let mut x: i32`, never `let x: mut i32`.

### Shadowing

Shadowing creates a new variable with the same name. It is different from mutability:

```rust
fn main() {
    let my_number = 8;
    println!("{}", my_number); // 8

    let my_number = 9.2;       // shadows the first binding
    println!("{}", my_number); // 9.2
}
```

A shadow only lasts inside its own block, so the outer binding becomes visible again
when the inner block ends:

```rust
fn main() {
    let my_number = 8;
    {
        let my_number = 9.2;
        println!("inside: {}", my_number); // 9.2
    }
    println!("outside: {}", my_number);    // 8
}
```

Shadowing is useful when you want to transform a value through several steps without
inventing a new name for every step. The old binding is still alive in memory; it is just
hidden.

### Python vs Rust gotchas

A few Python habits that do not carry over:

- **Assignment moves, not copies.** In Python, `a = [1, 2]; b = a` makes both names point to the same list. In Rust, `let a = String::from("hi"); let b = a;` moves the string into `b`, and `a` is no longer valid.
- **Mutability lives on the binding.** Python lets you rebind a name to any type. Rust's `mut` controls in-place changes only, and the type stays fixed.
- **Shadowing is not rebinding.** Python `x = 8; x = "eight"` changes what the name refers to. Rust `let x = 8; let x = "eight"` creates a second binding that hides the first.
- **Format strings are checked at compile time.** Python f-strings are evaluated at runtime. Rust checks `println!` placeholders at compile time.
- **`()` is not `None`.** Python's `None` means "no value." Rust's unit type `()` is a real value that carries no information; functions with no return expression return it.

```rust
fn main() {
    let a = String::from("hello");
    let b = a;
    // println!("{}", a); // error: borrow of moved value

    let x = 8;
    let x = "eight";
    println!("{}", x); // "eight"
}
```

## Takeaway

- Rust teaches you at compile time, before anything runs.
- Comments, types, variables, and functions work similarly to other languages but with
  stricter rules.
- Default numeric types are `i32` for integers and `f64` for floats.
- Variables are immutable unless you write `let mut`.
- Shadowing is a new binding, not a mutation.
- If the last expression in a function or block has no semicolon, it becomes the return
  value.
- From Python, watch out for moves, binding-level mutability, shadowing, compile-time
  format checks, and the unit type `()`.
