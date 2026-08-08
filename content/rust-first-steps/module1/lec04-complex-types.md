+++
title       = "Lecture 4 - Complex Types"
date        = 2026-06-21
description = "A project-style summary of Rust arrays, vectors, tuples, and control flow. Builds a simplified Pokemon type-advantage and battle helper."
weight      = 4

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 4
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-4 -->

## Slides

{{ slides(src="/slides/rfs-4/index.html", title="Lec 4 - Complex Types", note="40 slides · ~50 min") }}

## At a glance

This lecture introduces Rust's collection and control-flow types. The running example is a simplified Pokemon battle helper that answers two questions: which type has the advantage, and who wins a one-on-one fight?

Real Pokemon games have speed, accuracy, status effects, held items, and many more types. This lecture intentionally uses a simplified model so we can focus on the Rust constructs.

### Arrays

An array holds a fixed number of items of the same type.

```rust
fn main() {
    let types = ["Fire", "Water", "Grass", "Electric"];
    println!("{:?}", types);
}
```

The type of an array includes its length. `[&str; 2]` and `[&str; 3]` are different types. This is why you cannot assign an array of length 2 to a variable that previously held an array of length 3.

You can repeat a value to fill an array:

```rust
fn main() {
    let buffer = [0u8; 640];
    println!("{}", buffer.len()); // 640
}
```

This pattern is common for byte buffers in networking and file code.

### Slicing arrays and vectors

A slice is a borrowed view into part of a collection. Ranges are exclusive on the right by default.

```rust
fn main() {
    let numbers = [0, 1, 2, 3, 4, 5];

    let middle = &numbers[2..5]; // 2, 3, 4
    let tail   = &numbers[3..];  // 3, 4, 5
    let head   = &numbers[..3];  // 0, 1, 2
    let all    = &numbers[..];   // everything
}
```

Use `..=` for an inclusive range:

```rust
fn main() {
    let numbers = [0, 1, 2, 3];
    let first_three = &numbers[0..=2]; // 0, 1, 2
}
```

### Byte strings

The `b"..."` prefix creates an array of bytes, not a string slice.

```rust
fn main() {
    let greeting = b"Hello";
    println!("{:?}", greeting); // [72, 101, 108, 108, 111]
}
```

The type is `[u8; 5]`. This matters whenever you work with raw binary data.

### Vectors

A vector is a growable, heap-allocated collection.

```rust
fn main() {
    let mut team = Vec::new();
    team.push("Charmander");
    team.push("Squirtle");

    println!("{:?}", team);
}
```

Most people use the `vec!` macro:

```rust
fn main() {
    let team = vec!["Charmander", "Squirtle", "Bulbasaur"];
}
```

Vectors can be sliced just like arrays. They also have a capacity, which is the amount of memory reserved for future items. When a vector fills up, it reallocates: it asks for a larger chunk of memory and copies the existing items over.

```rust
fn main() {
    let mut v = Vec::new();
    println!("{}", v.capacity()); // 0

    v.push('a');
    println!("{}", v.capacity()); // 4

    for _ in 0..4 {
        v.push('a');
    }
    println!("{}", v.capacity()); // 8
}
```

If you know the final size, you can avoid extra reallocations:

```rust
fn main() {
    let mut v = Vec::with_capacity(8);
    for _ in 0..5 {
        v.push('a');
    }
    println!("{}", v.capacity()); // still 8
}
```

You can turn an array into a vector with `.into()`. You can even let Rust infer the element type with `Vec<_>`.

```rust
fn main() {
    let numbers: Vec<u8> = [1, 2, 3].into();
    let inferred: Vec<_> = [9, 0, 10].into();
}
```

### Tuples

A tuple groups values of different types. Access each slot with a dot and a number.

```rust
fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);

    println!("Name: {}", charmander.0);
    println!("Type: {}", charmander.1);
    println!("HP:   {}", charmander.2);
}
```

The type is `(&str, &str, u16)`.

#### Why tuples use dot notation and arrays use brackets

Arrays are homogeneous. Every element has the same type, so `arr[i]` has a known type even when `i` is only known at runtime.

Tuples are heterogeneous. A tuple like `(String, i32, char)` has a different type in each slot. If Rust let you write `tuple[i]`, the result type would depend on a runtime value. The compiler cannot allow that. So tuple access is fixed at compile time: `.0` always means the first slot, `.1` always means the second slot, and so on. Tuples act more like anonymous structs, so they use dot notation like structs do.

#### Destructuring

You can pull a tuple apart in one line:

```rust
fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);
    let (name, pokemon_type, hp) = charmander;

    println!("{name} is a {pokemon_type} type with {hp} HP");
}
```

The pattern on both sides must match. Use `_` to ignore a slot:

```rust
fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);
    let (_, pokemon_type, _) = charmander;
    println!("Type: {pokemon_type}");
}
```

If a tuple contains a non-Copy type like `String`, destructuring moves the values out:

```rust
fn main() {
    let entry = ("error".to_string(), 404);
    let (message, code) = entry;

    // println!("{:?}", entry); // error: entry has been moved
    println!("{message}: {code}");
}
```

When every element is Copy, the whole tuple is Copy and the original stays usable.

#### The unit type

An empty tuple `()` is called the unit type. It is the default return type when a function returns nothing.

```rust
fn do_nothing() {} // same as fn do_nothing() -> () {}
```

A semicolon at the end of an expression turns it into a statement, and statements return `()`. That is why adding a semicolon to the last line of a function changes its return type.

### Control flow

#### if, else if, else

Conditions do not need parentheses.

```rust
fn main() {
    let hp = 30;

    if hp == 0 {
        println!("fainted");
    } else if hp < 50 {
        println!("critical");
    } else {
        println!("healthy");
    }
}
```

Use `==` to compare, `=` to assign, `&&` for and, and `||` for or.

#### match

`match` checks a value against patterns and runs the first matching arm.

```rust
fn main() {
    let status = "degraded";

    match status {
        "healthy"  => println!("all good"),
        "degraded" => println!("watch closely"),
        "down"     => println!("alert!"),
        _          => println!("unknown"),
    }
}
```

Rust requires every `match` to be exhaustive. If a value is not covered, the program will not compile. You can use `_` as a wildcard for everything else.

A `match` can also return a value:

```rust
fn main() {
    let status = "degraded";

    let priority = match status {
        "down"     => 1,
        "degraded" => 2,
        "healthy"  => 3,
        _          => 4,
    };
}
```

Every arm must return the same type.

Matching tuples is especially useful:

```rust
fn multiplier(attacker: &str, defender: &str) -> f64 {
    match (attacker, defender) {
        ("Fire", "Grass")  => 2.0,
        ("Water", "Fire")  => 2.0,
        ("Grass", "Water") => 2.0,
        ("Fire", "Water")  => 0.5,
        _                  => 1.0,
    }
}
```

#### Match guards

Add an `if` condition to a match arm for extra filtering.

```rust
fn describe(hp: u16) -> &'static str {
    match hp {
        0           => "fainted",
        n if n < 50 => "critical",
        _           => "healthy",
    }
}
```

#### Binding with @

Use `@` to match a pattern and bind the matched value to a name.

```rust
fn lucky_number(n: i32) {
    match n {
        value @ 4 | value @ 13   => println!("{value} is special"),
        value @ 10..=19          => println!("{value} is a teen"),
        _                        => println!("nothing special"),
    }
}
```

#### Loops

Rust has three loop keywords.

```rust
fn main() {
    // loop runs until break
    let mut n = 0;
    loop {
        n += 1;
        if n == 3 { break; }
    }

    // while checks a condition
    while n > 0 {
        n -= 1;
    }

    // for iterates over a range or collection
    for i in 0..3 {
        println!("{i}");
    }
}
```

You can name a loop and break out of an outer loop:

```rust
fn main() {
    'outer: loop {
        println!("outer");

        loop {
            println!("inner");
            break 'outer;
        }
    }
}
```

A `loop` can also return a value:

```rust
fn main() {
    let mut counter = 0;
    let answer = loop {
        counter += 1;
        if counter * counter == 64 {
            break counter;
        }
    };
    println!("{answer}"); // 8
}
```

### The project: a simplified Pokemon battle helper

#### Step 1: type advantage lookup

```rust
fn multiplier(attacker: &str, defender: &str) -> f64 {
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
}
```

This is intentionally small. A real type chart would have more types, but the Rust syntax stays the same.

#### Step 2: represent a Pokemon

```rust
fn main() {
    let charmander = ("Charmander", "Fire", 100_u16);
    let squirtle = ("Squirtle", "Water", 110_u16);

    println!("{} has {} HP", charmander.0, charmander.2);
}
```

We use `&str` and `u16` so the tuple is Copy. That keeps the early examples simple.

#### Step 3: build a team

```rust
fn main() {
    let red_team = vec![
        ("Charmander", "Fire", 100_u16),
        ("Pidgey", "Normal", 80_u16),
    ];

    println!("{:#?}", red_team);
}
```

The vector holds tuples. Every tuple has the same shape, so the vector is homogeneous.

#### Step 4: simulate an attack

```rust
fn attack(attacker: &(&str, &str, u16), defender: &mut (&str, &str, u16)) {
    let base_power = 20;
    let mult = multiplier(attacker.1, defender.1);
    let damage = (base_power as f64 * mult) as u16;
    defender.2 = defender.2.saturating_sub(damage);
}
```

- `attacker` is an immutable reference because we only read from it.
- `defender` is a mutable reference because we change its HP.
- `saturating_sub` prevents HP from going below zero.

#### Step 5: run a battle

```rust
fn battle(mut first: (&str, &str, u16), mut second: (&str, &str, u16)) -> &str {
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
}
```

The battle model is simplified. It ignores speed, accuracy, status effects, and switching. Those would come in a more advanced program.

## Python to Rust notes

### Mixed collections

In Python, a list can hold anything:

```python
[1, "two", 3.0]
```

In Rust, a vector must hold a single type. If you need mixed types, use a tuple or a struct. A vector of Pokemon tuples is fine because every tuple has the same shape.

### Tuple and array indexing

Python lets you index tuples with a variable: `t[i]`. Rust does not, because the type of `t[i]` would depend on the runtime value of `i`. Array indexing in Rust is checked at runtime; going out of bounds panics instead of returning a nonsense value.

### match is exhaustive

Python does not have an exact equivalent of Rust's `match`. A Rust `match` must cover every possible value, or the program will not compile. This feels strict at first, but it catches bugs where you forget to handle an unexpected case.

### Loops and ranges

Python ranges are exclusive on the right by default. Rust has the same default with `..`, and also an inclusive version with `..=`. Rust also lets a `loop` return a value with `break value;`, which Python does not do.

## Takeaway

- Arrays are for fixed-size, same-type data.
- Vectors are for growable collections and manage their own capacity.
- Tuples are for grouped, mixed-type values.
- Slices are borrowed views into arrays and vectors.
- `match` is exhaustive and works beautifully with tuples.
- Loops can be labeled and can return values.
- The Pokemon helper is intentionally simplified. The point is to see how arrays, vectors, tuples, and control flow fit together in a real program.
