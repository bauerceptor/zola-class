+++
title       = "Lecture 3 - The Building Blocks"
date        = 2026-06-19
description = "A project-style summary of Rust building blocks: structs, implementations, methods, external crates, Vec vs arrays, Debug derive, and mutable references. Uses a Pokemon team example."
weight      = 3

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 3
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-3 -->

## Code files

You can find all the relevant [code files for this lecture here](https://github.com/bauerceptor/rust-first-steps/blob/main/03%20-%20The%20Building%20Blocks/src/main.rs).

## Slides

{{ slides(src="/slides/rfs-3/index.html", title="Lec 3 - The Building Blocks", note="30 slides · ~40 min") }}

## At a glance

This lecture builds a small Pokemon team program. Along the way it introduces the pieces you will use in almost every Rust project: structs, implementations, methods, external crates, and the borrowing rules that govern mutation.

### main, strings, and chars

Every Rust program starts in `fn main()`. `println!` is a macro, which is why its name ends with `!`.

```rust
fn main() {
    println!("Hello, world!");
}
```

Double quotes make a `&str`. Single quotes make a `char`.

```rust
fn main() {
    let name = "Pikachu";   // &str
    let initial = 'P';      // char
}
```

If you try to put more than one character inside single quotes, the compiler rejects it.

### Structs

A struct groups related data and gives it a name. Think of it as a lightweight class whose fields are fixed at compile time.

```rust
struct Team {
    members: Vec<String>,
}
```

- The struct name starts with a capital letter.
- Each field has a name, a colon, and a type.
- `Vec<String>` is a growable list of owned strings.

To create an instance, use a struct literal:

```rust
fn main() {
    let team = Team {
        members: vec![],
    };
}
```

### Vec vs array

Use a `Vec` when the number of items can change. Use an array when the size is fixed.

```rust
fn main() {
    let mut team = vec!["Pikachu"];
    team.push("Charmander");        // allowed

    let types = ["Fire", "Water"];   // fixed-size array
    // types.push("Grass");          // error
}
```

Arrays are only very slightly faster than vectors. The real reason to choose an array is to tell the reader that this list will not change.

### Generating the roster

Instead of typing every name, we generate the team from two fixed arrays using nested loops and the `format!` macro.

```rust
fn main() {
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
}
```

`format!` works like `println!` but returns a `String` instead of printing it.

Because we keep adding members, the vector must be mutable. Without `mut`, `push` is rejected.

### Printing a struct

Rust does not know how to print a custom struct unless you tell it how. The easiest way during development is `#[derive(Debug)]`.

```rust
#[derive(Debug)]
struct Team {
    members: Vec<String>,
}

fn main() {
    let team = Team { members: vec![] };
    println!("{:#?}", team);
}
```

- `{:?}` prints compact debug output.
- `{:#?}` pretty-prints it.

This is different from Python, where `print(obj)` automatically calls `__str__` or `__repr__`. In Rust, printing is opt-in through traits.

### Implementations

An `impl` block attaches functions to a struct. Functions that do not take `self` are associated functions. Functions that take `&self` or `&mut self` are methods.

```rust
impl Team {
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
```

- `impl Team` is an inherent implementation.
- `Self` is shorthand for `Team` inside this block.
- `Team::new()` is an associated function, similar to a class method or static method.
- The last expression is returned automatically because there is no semicolon.

### Implicit return

Rust returns the last expression of a function if you leave off the semicolon.

```rust
fn is_even(n: i32) -> bool {
    n % 2 == 0
}
```

Python always needs an explicit `return`. Rust treats the tail expression as the return value.

### Methods

A method operates on a specific instance.

```rust
impl Team {
    fn shuffle(&mut self) {
        // shuffle the members vector
    }

    fn release(&mut self, num: usize) -> Vec<String> {
        self.members.split_off(self.members.len() - num)
    }
}
```

- `&self` gives read-only access to the instance.
- `&mut self` gives mutable access.
- If a method changes data, the caller must also have declared the instance as `mut`.

### External crates

Random number generation is not in the standard library, so we add the `rand` crate.

```bash
cargo add rand
```

Then bring what we need into scope:

```rust
use rand::{thread_rng, seq::SliceRandom};

impl Team {
    fn shuffle(&mut self) {
        let mut rng = thread_rng();
        self.members.shuffle(&mut rng);
    }
}
```

- A crate is Rust's word for a package or library.
- `use` creates a shortcut so we do not have to type the full path every time.
- External crates do not need a `mod` declaration; internal modules do.

This is one of the common Python gotchas. In Python, every file is an importable module automatically. In Rust, internal modules must be declared with `mod` before you use them.

### usize

`usize` is an unsigned integer the same size as a memory address. Use it for counts, lengths, and indices.

```rust
fn release(&mut self, num: usize) -> Vec<String> {
    self.members.split_off(self.members.len() - num)
}
```

### A note on error handling

If `release` asks for more members than the team has, `split_off` panics. This lecture skips proper error handling so we can focus on the building blocks. We will come back to error handling soon.

## Python to Rust notes

### Structs are not Python classes

- Fields are fixed at compile time. You cannot add new fields at runtime like you can with Python object attributes.
- Methods live in `impl` blocks, not inside the struct body.
- Every field must have a declared type.

### Mutation is explicit on both sides

In Python, passing a list into a function lets that function change the list. Rust makes the contract visible:

```rust
fn add_member(team: &mut Team, name: String) {
    team.members.push(name);
}

fn main() {
    let mut team = Team::new();
    add_member(&mut team, String::from("Mewtwo"));
}
```

The caller says `&mut team`, the parameter says `&mut Team`, and the method says `&mut self`. All three must agree.

### Imports and crates

- Use `cargo add crate_name` to add an external crate, similar to `pip install`.
- Access items with `crate_name::item` or bring them in with `use`.
- External crates do not need a `mod` declaration.
- Internal modules need `mod module_name;` before use.

### Printing

Rust only prints types it knows how to format. During development, `#[derive(Debug)]` and `{:?}` are your friends. For user-facing output, implement `Display` or use a custom formatter.

## Takeaway

- Structs group data. Implementations attach behavior.
- Associated functions create values. Methods operate on existing values.
- `Vec` grows; arrays do not. Pick the one that matches your intent.
- `#[derive(Debug)]` gives you quick, readable output while you learn.
- External crates extend Rust just like packages extend Python.
- Mutation requires `mut` at every level: the binding, the reference, and the method signature.
