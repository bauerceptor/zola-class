# Design: Rust: First Steps — Lecture 7

## Goal

Create the slide deck and chapter webpage for *Rust: First Steps*, Lecture 7,
based on the module-system transcripts. The lecture covers grouping code with
modules, the `mod` and `pub` keywords, three ways to create modules, nested
modules with `mod.rs`, re-exports, `use`, and `super`.

## Codename and date

- Slide deck codename: **rfs-7**
- Lecture date: **2026-06-27** (two days after Lecture 6)
- Lecture title: **Lecture 7 — Modules and Code Organization**

## Running example: Refactor the media catalog

We continue the media catalog from Lecture 6. The lecture starts with a
monolithic `main.rs` that contains the `Media` enum, its `impl` block, the
`Catalog` struct, and its `impl` block. We refactor this into a `content`
module with two submodules.

### Files after the refactor

- `src/content/mod.rs` — re-exports the submodules.
- `src/content/media.rs` — the `Media` enum and its `description` method.
- `src/content/catalog.rs` — the `Catalog` struct and its methods.
- `src/main.rs` — imports the `content` module and uses `Media` and `Catalog`.

### Types

```rust
enum Media {
    Book { title: String, author: String },
    Movie { title: String, director: String },
    Audiobook { title: String },
    Podcast(u32),
    Placeholder,
}

struct Catalog {
    items: Vec<Media>,
}
```

### Methods kept from Lecture 6

- `Media::description(&self) -> String`
- `Catalog::new() -> Self`
- `Catalog::add(&mut self, media: Media)`
- `Catalog::get_by_index(&self, index: usize) -> Option<&Media>`

## Slide deck structure

The deck uses the shared `clean.css` theme, auto light/dark, with horizontal
sections and vertical sub-slides.

1. **Title slide** — Lecture 7, topic, project preview.
2. **Why modules** — grouping related code, the messy `main.rs` problem.
3. **Section: Three ways to make a module**
   - Inline `mod content { ... }` inside an existing file.
   - Separate file `content.rs` in the same directory.
   - Nested folder `content/mod.rs` with sibling files.
4. **Section: Privacy and `pub`** — everything is private by default; `pub`
   opens access from outside the module.
5. **Section: `mod` and `use`** — `mod` declares a module; `use` abbreviates
   a path.
6. **Section: Rules of nested modules**
   - Every file and every folder creates a module.
   - A folder must contain `mod.rs`.
   - Imports happen one level at a time; no deeply nested imports.
   - `pub mod media;` imports a submodule and re-exports it.
7. **Section: Refactor the media catalog**
   - Move `Media` and its `impl` into `content/media.rs`.
   - Move `Catalog` and its `impl` into `content/catalog.rs`.
   - Add `pub` to public items.
   - Write `content/mod.rs` with `pub mod media;` and `pub mod catalog;`.
   - Update `main.rs` with `mod content;` and `use content::media::Media;`.
8. **Section: `super`** — reaching the parent module; how `catalog.rs` uses
   `super::media::Media`.
9. **Python to Rust notes** — Python modules are files with convention-based
   privacy; Rust modules are explicit, privacy is by default, and `pub` is
   required.
10. **Review and finish** — return to chapter page link.

## Webpage structure

The chapter page at `content/rust-first-steps/module1/lec07-modules.md` will:

- Start with the codename comment `<!-- Chapter codename: rfs-7 -->`.
- Embed the slide deck card.
- Summarize why modules matter, the three module patterns, `pub`, `mod`,
  `use`, nested module rules, and the refactor walkthrough.
- Include the final file layout and key code snippets.
- Add a Python-vs-Rust note on modules.
- Provide a takeaway list.

## Files to create or modify

- `scripts/build-deck-rfs7.py` — new generator for this deck.
- `static/slides/rfs-7/index.html` — generated slide deck.
- `content/rust-first-steps/module1/lec07-modules.md` — new lecture page.
- `content/rust-first-steps/_index.md` — add Lecture 7 to the course overview.
- `README.md` and `guide-for-ai.md` — document the new generator.

## Subtleties to highlight

- `mod` tells the compiler a module exists; it does not automatically make
  anything public.
- `pub` must be added to the item itself, and again when re-exporting with
  `pub mod`.
- A folder and its `mod.rs` merge into one module named after the folder.
- `use` only shortens paths; it does not change what is accessible.
- `super` is the parent module, not the file system parent.
- Rust does not allow deeply nested imports; you must pull items through each
  module layer.

## Verification

- Run `zola build` and confirm no errors.
- Open the generated slide deck and check navigation.
- Confirm the chapter page links to the slide deck.
