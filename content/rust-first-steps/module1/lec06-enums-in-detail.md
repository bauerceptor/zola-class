+++
title       = "Lecture 6 - Enums in Detail"
date        = 2026-06-25
description = "Algebraic data types, pattern matching, Option, and a comparison with enums in Python, C++, Java, and Go. Built around a media catalog."
weight      = 6

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 6
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-6 -->

## Slides

{{ slides(src="/slides/rfs-6/index.html", title="Lec 6 - Enums in Detail", note="45 slides · ~55 min") }}

## At a glance

This lecture dives deeper into enums. We build a media catalog that can hold
books, movies, audiobooks, podcasts, and placeholders, all as variants of a
single `Media` enum. Along the way we cover pattern matching, methods on enums,
`Option`, and how Rust's enums compare to enums in Python, C++, Java, and Go.

## Defining an enum with data

An enum is perfect when you have several related things that are similar but not
identical.

```rust
#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Movie { title: String, director: String },
    Audiobook { title: String },
}
```

Every value is still of type `Media`. A function that accepts `Media` can accept
any variant.

```rust
fn print_media(media: &Media) {
    println!("{:?}", media);
}

fn main() {
    let book = Media::Book {
        title: String::from("Dune"),
        author: String::from("Frank Herbert"),
    };

    print_media(&book);
}
```

## Methods on enums

Inside an `impl` block, we must first discover which variant we have before we
can access its fields.

### if let

```rust
impl Media {
    fn description(&self) -> String {
        if let Media::Book { title, author } = self {
            return format!("Book: {} by {}", title, author);
        }
        if let Media::Movie { title, director } = self {
            return format!("Movie: {} by {}", title, director);
        }
        String::from("other media")
    }
}
```

### match

`match` is usually preferred because it is exhaustive.

```rust
impl Media {
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
}
```

If you add a new variant, the compiler tells you every `match` that needs
updating.

## Structs vs enums

Use an enum when every variant supports the same set of methods. Use structs when
different types need different methods that should not be shared.

If a book needs a `read()` method, a movie needs a `play()` method, and an
audiobook needs a `listen()` method, separate structs are usually clearer.

## The catalog project

A `Catalog` struct owns a `Vec<Media>`.

```rust
#[derive(Debug)]
struct Catalog {
    items: Vec<Media>,
}

impl Catalog {
    fn new() -> Self {
        Self { items: vec![] }
    }

    fn add(&mut self, media: Media) {
        self.items.push(media);
    }
}
```

The vector holds one type, `Media`, but that type can represent many different
shapes.

```rust
fn main() {
    let mut catalog = Catalog::new();

    catalog.add(Media::Audiobook {
        title: String::from("A Brief History"),
    });
    catalog.add(Media::Book {
        title: String::from("Dune"),
        author: String::from("Frank Herbert"),
    });

    println!("{:?}", catalog);
}
```

## Unlabeled fields and unit variants

Variants can hold a single unnamed value.

```rust
#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Podcast(u32),
}
```

A variant with no data is called a unit variant.

```rust
#[derive(Debug)]
enum Media {
    Book { title: String, author: String },
    Placeholder,
}
```

## Option

Rust has no null. Instead, it uses the `Option` enum.

```rust
enum Option<T> {
    Some(T),
    None,
}
```

`Vec::get` returns an `Option` because the index might be invalid.

```rust
fn main() {
    let catalog = Catalog::new();
    let item = catalog.items.get(0);

    match item {
        Some(media) => println!("{:?}", media),
        None => println!("no item at that index"),
    }
}
```

### Why Option works

`Option` forces you to handle both cases. You cannot accidentally use a missing
value as if it were present.

### unwrap, expect, unwrap_or

These are shortcuts for specific situations.

```rust
// Panics if None
item.unwrap();

// Panics with a custom message if None
item.expect("catalog should not be empty");

// Returns a fallback value if None
let placeholder = Media::Placeholder;
item.unwrap_or(&placeholder);
```

For most production code, prefer `match` or `if let`.

## Language comparison

### Python

Python's `enum.Enum` attaches names to values, often integers. Variants cannot
carry different per-variant data. Missing values use `None`, and the compiler
does not enforce that you check for it.

### C++

C++ enums are essentially integers. `enum class` adds type safety but still does
not allow per-variant data. Missing values use `std::optional`, available since
C++17.

### Java

Java enums can have shared fields and methods, but every variant has the same
shape. Per-variant data is not supported directly. Missing values use
`Optional<T>`.

### Go

Go has no dedicated enum type. Use typed constants with `iota`. There is no
compile-time exhaustiveness checking and no per-variant data. Missing values use
`nil`.

### Rust

Rust enums are algebraic data types. Each variant can carry different data,
`match` is exhaustive, and missing values use `Option<T>`. The compiler prevents
many null-pointer-style bugs.

## Python to Rust notes

### Option vs None

Python functions can return `None` for missing values, and callers can forget to
check. Rust's `Option` makes the check unavoidable.

### Exhaustive matching

Python has no compile-time check that you handled every enum case. Rust refuses
to compile if a `match` is incomplete.

### Enums vs classes

Python classes can simulate sum types with subclasses, but the language does not
enforce exhaustive handling. Rust enums make data shapes part of the type system.

## Takeaway

- Enums can carry different data in each variant.
- Pattern matching extracts data and must be exhaustive.
- Methods on enums use `match` or `if let` to behave differently per variant.
- Unit variants and unlabeled fields keep enums concise.
- `Option<T>` replaces null with an explicit `Some`/`None` choice.
- `unwrap`, `expect`, and `unwrap_or` are shortcuts; prefer `match` and `if let`
  in production code.
- Rust enums combine sum types, exhaustive matching, and null-free option types
  in a way that Python, C++, Java, and Go do not.
