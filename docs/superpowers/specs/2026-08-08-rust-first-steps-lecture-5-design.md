# Design: Rust: First Steps — Lecture 5

## Goal

Create the slide deck and chapter webpage for *Rust: First Steps*, Lecture 5,
based on the "Building your own types" chapter. The lecture covers structs,
enums, `impl` blocks, destructuring, and the dot operator.

## Codename and date

- Slide deck codename: **rfs-5**
- Lecture date: **2026-06-23** (two days after Lecture 4)
- Lecture title: **Lecture 5 — Building Your Own Types**

## Running example: Server lifecycle tracker

We model a small fleet of servers. Each server is a `Server` struct with a
`ServerStatus` enum. The example shows how structs and enums work together.

### Types

```rust
enum ServerStatus {
    Provisioning,
    Online,
    Maintenance(String),            // reason for maintenance
    Decommissioned { reason: String },
}

struct Server {
    hostname: String,
    region: String,
    status: ServerStatus,
    cpu_percent: u8,
    memory_percent: u8,
}
```

### Methods

- `Server::new(hostname, region) -> Self` — associated function (constructor).
- `start(&mut self)` — bring a provisioning server online.
- `schedule_maintenance(&mut self, reason: &str)` — set status to `Maintenance`.
- `decommission(&mut self, reason: &str)` — set status to `Decommissioned`.
- `health_summary(&self) -> String` — read CPU and memory and return a short report.
- `status_badge(&self) -> &str` — match on the status enum.

## Slide deck structure

The deck uses the shared `clean.css` theme, auto light/dark, with horizontal
sections and vertical sub-slides.

1. **Title slide** — Lecture 5, topic, project preview.
2. **The project** — why model servers, what we will build.
3. **Structs** — unit, tuple, and named structs; field init shorthand.
4. **Enums** — basic enums, `::` syntax, `use`, enums with data.
5. **Casting enums** — casting simple enums to integers and custom discriminants.
6. **Enums in collections** — using an enum to hold different types in a `Vec`.
7. **Implementing types** — `impl` blocks, `Self` vs `self`, associated functions vs methods, `#[derive(Debug)]`.
8. **Building the server tracker** — incremental code steps using the running example.
9. **Destructuring** — pulling fields out of structs, renaming, `..`, destructuring in function parameters.
10. **References and the dot operator** — auto-dereferencing, why `==` still needs care.
11. **Python to Rust notes** — what Python devs should watch for.
12. **Review and finish** — return to chapter page link.

## Webpage structure

The chapter page at `content/rust-first-steps/module1/lec05-building-your-own-types.md` will:

- Start with the codename comment `<!-- Chapter codename: rfs-5 -->`.
- Embed the slide deck card.
- Summarize structs, enums, impl blocks, destructuring, and the dot operator.
- Include the server tracker code in runnable steps.
- Add Python-vs-Rust notes.
- Provide a takeaway list.

## Files to create or modify

- `scripts/build-deck-rfs5.py` — new generator for this deck.
- `static/slides/rfs-5/index.html` — generated slide deck.
- `content/rust-first-steps/module1/lec05-building-your-own-types.md` — new lecture page.
- `content/rust-first-steps/_index.md` — add Lecture 5 to the course overview.
- `README.md` and `guide-for-ai.md` — document the new generator and the two-day date convention.
- `content/rust-first-steps/module1/lec01-the-basics.md` — change date to 2026-06-15.
- `content/rust-first-steps/module1/lec02-memory-and-ownership.md` — change date to 2026-06-17.
- `content/rust-first-steps/module1/lec03-the-building-blocks.md` — change date to 2026-06-19.
- `content/rust-first-steps/module1/lec04-complex-types.md` — change date to 2026-06-21.

## Subtleties to highlight

- `Self` is the type; `self` is the variable. Inside `impl Server`, `Self` means `Server`.
- Associated functions use `::` because the value does not exist yet; methods use `.`.
- `#[derive(Debug)]` is not magic; it asks the compiler to generate a Debug implementation.
- Destructuring moves non-Copy fields. Use references or `Clone` when you want to keep the original.
- The dot operator auto-dereferences for method calls, but comparison operators like `==` do not auto-dereference.
- `match` on enums must be exhaustive.
- Unit structs are useful as markers and have zero size.

## Verification

- Run `zola build` and confirm no errors.
- Open the generated slide deck and check navigation.
- Confirm the chapter page links to the slide deck.
