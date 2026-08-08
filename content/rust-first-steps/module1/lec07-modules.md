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

```
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

```
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
