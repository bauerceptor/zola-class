+++
title       = "Lecture 5 - Building Your Own Types"
date        = 2026-06-23
description = "Structs, enums, implementations, destructuring, and the dot operator. Built around a DevOps server lifecycle tracker."
weight      = 5

[extra]
lang        = "en"
course      = "Rust: First Steps"
lecture_num = 5
mermaid     = false
copy        = true
+++

<!-- Chapter codename: rfs-5 -->

## Slides

{{ slides(src="/slides/rfs-5/index.html", title="Lec 5 - Building Your Own Types", note="58 slides · ~55 min") }}

## At a glance

This lecture introduces the main ways to build your own types in Rust: structs,
enums, and `impl` blocks. The running example is a small DevOps server lifecycle
tracker. We model a server as a struct and its status as an enum, then attach
methods that provision, maintain, and decommission it.

A server can only be in one state at a time, so status is a natural fit for an
enum. A server also has many properties at once: hostname, region, CPU, memory,
and status. That grouping is a natural fit for a struct.

## Structs

A struct bundles several values into one named type. Rust has three kinds.

### Unit struct

A unit struct has no fields. It is often used as a marker or type-level token.

```rust
struct DatabaseNode;

fn main() {
    let _node = DatabaseNode;
}
```

It takes up no space at runtime, but it is still a distinct type. That
distinction matters when you use traits or generic code later.

### Tuple struct

A tuple struct has fields but no names. Access them by position.

```rust
struct Rgb(u8, u8, u8);

fn main() {
    let color = Rgb(50, 0, 50);
    println!("Green channel: {}", color.1);
}
```

Tuple structs are good when the type name carries the meaning and the individual
field names are not important.

### Named struct

A named struct is the most common kind. Each field has a name and a type.

```rust
struct Server {
    hostname: String,
    region: String,
    cpu_percent: u8,
    memory_percent: u8,
}

fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
        memory_percent: 64,
    };

    println!("{} in {}", server.hostname, server.region);
}
```

Use a trailing comma after the last field. It makes reordering fields safer
because every line ends the same way.

### Field init shorthand

If a variable has the same name as a struct field, write the name once.

```rust
fn main() {
    let hostname = String::from("web-01");
    let region = String::from("us-east");

    let server = Server {
        hostname,
        region,
    };

    println!("{} {}", server.hostname, server.region);
}
```

This is just a shorthand. It keeps constructors readable when the local variable
names already match the field names.

## Enums

Use a struct when you want one thing **and** another thing. Use an enum when you
want one thing **or** another thing.

### Basic enum

```rust
enum ServerStatus {
    Provisioning,
    Online,
    Maintenance,
    Decommissioned,
}

fn main() {
    let status = ServerStatus::Online;

    match status {
        ServerStatus::Online => println!("Server is online"),
        _ => println!("Server is not online"),
    }
}
```

Choose a variant with `::`. A `match` on an enum must cover every variant, or
the program will not compile.

### Importing variants with use

```rust
fn check(status: &ServerStatus) {
    use ServerStatus::*;

    match status {
        Online => println!("online"),
        Maintenance => println!("maintenance"),
        _ => println!("other"),
    }
}
```

`use ServerStatus::*` imports every variant into the current scope. You can also
import individual variants.

### Enums that carry data

Rust enums can hold data inside each variant.

```rust
enum ServerStatus {
    Provisioning,
    Online,
    Maintenance(String),
    Decommissioned { reason: String },
}

fn main() {
    let status = ServerStatus::Maintenance(String::from("kernel upgrade"));

    match &status {
        ServerStatus::Maintenance(reason) => {
            println!("under maintenance: {reason}");
        }
        ServerStatus::Decommissioned { reason } => {
            println!("decommissioned: {reason}");
        }
        _ => println!("operational"),
    }
}
```

The data can be a tuple, named fields, or nothing. You extract it through pattern
matching.

### Casting simple enums to integers

If an enum variant has no data, Rust assigns it a number starting from 0. You can
cast it to an integer.

```rust
enum Priority {
    Low,
    Medium,
    High,
}

fn main() {
    let p = Priority::High;
    println!("{}", p as u32); // 2
}
```

This only works for simple enums. If a variant holds data, you cannot cast it.

### Custom discriminants

You can choose your own numbers. Variants without an explicit number count up
from the previous one.

```rust
enum HttpStatus {
    Ok = 200,
    NotFound = 404,
    ServerError = 500,
    Teapot = 418,
}

fn main() {
    println!("{}", HttpStatus::NotFound as u16); // 404
}
```

Two variants cannot share the same discriminant. This is useful when mapping enum
values to external constants like HTTP status codes.

### Enums in collections

A Vec can only hold one element type. An enum lets you wrap different types so
the Vec stays homogeneous.

```rust
enum Metric {
    Cpu(u8),
    Memory(u8),
    Message(String),
}

fn main() {
    let metrics = vec![
        Metric::Cpu(12),
        Metric::Memory(64),
        Metric::Message(String::from("healthy")),
    ];

    for metric in &metrics {
        match metric {
            Metric::Cpu(value) => println!("cpu: {value}%"),
            Metric::Memory(value) => println!("memory: {value}%"),
            Metric::Message(text) => println!("msg: {text}"),
        }
    }
}
```

This pattern appears often when reading heterogeneous events or log lines into a
single collection.

## Implementing types

An `impl` block attaches functions to a struct or enum.

- **Methods** take `self`, `&self`, or `&mut self`. Call them with a dot.
- **Associated functions** do not take `self`. Call them with `::`.

### Printing structs and enums

Rust does not let you print a custom type with `{}` unless you implement the
Display trait. For debugging, use `#[derive(Debug)]` and `{:?}`.

```rust
#[derive(Debug)]
struct Server {
    hostname: String,
    cpu_percent: u8,
}

fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        cpu_percent: 12,
    };

    println!("{:?}", server);
}
```

`#[derive(Debug)]` asks the compiler to generate a Debug implementation for you.
It is the quickest way to inspect a custom type during development.

### self vs Self

Inside an impl block, `Self` with a capital S is the type. `self` with a
lowercase s is the variable that refers to the instance.

```rust
impl Server {
    fn new(hostname: &str) -> Self {
        Self {
            hostname: String::from(hostname),
        }
    }

    fn hostname(&self) -> &str {
        &self.hostname
    }
}
```

`Self` is convenient because if you rename the struct, the impl block does not
need to change.

### Associated functions vs methods

Use an associated function when the value does not exist yet. Use a method when
the value already exists.

```rust
impl Server {
    // Associated function: no self, called with Server::new
    fn new(hostname: &str) -> Self {
        Self { hostname: String::from(hostname) }
    }

    // Method: takes &self, called with server.hostname()
    fn hostname(&self) -> &str {
        &self.hostname
    }
}
```

`String::from` and `Vec::new` are associated functions you have already used.

### Implementing methods on enums

Enums can have impl blocks too.

```rust
impl ServerStatus {
    fn is_operational(&self) -> bool {
        match self {
            ServerStatus::Online => true,
            ServerStatus::Maintenance(_) => false,
            ServerStatus::Provisioning => false,
            ServerStatus::Decommissioned { .. } => false,
        }
    }
}
```

Methods on enums often return a value based on which variant is active.

## The project: server lifecycle tracker

### Step 1: define the types

```rust
#[derive(Debug)]
enum ServerStatus {
    Provisioning,
    Online,
    Maintenance(String),
    Decommissioned { reason: String },
}

#[derive(Debug)]
struct Server {
    hostname: String,
    region: String,
    status: ServerStatus,
    cpu_percent: u8,
    memory_percent: u8,
}
```

Both types derive Debug so we can print them while learning.

### Step 2: add a constructor

```rust
impl Server {
    fn new(hostname: &str, region: &str) -> Self {
        Self {
            hostname: String::from(hostname),
            region: String::from(region),
            status: ServerStatus::Provisioning,
            cpu_percent: 0,
            memory_percent: 0,
        }
    }
}
```

New servers start in the Provisioning state.

### Step 3: add lifecycle methods

```rust
impl Server {
    fn start(&mut self) {
        self.status = ServerStatus::Online;
    }

    fn schedule_maintenance(&mut self, reason: &str) {
        self.status = ServerStatus::Maintenance(String::from(reason));
    }

    fn decommission(&mut self, reason: &str) {
        self.status = ServerStatus::Decommissioned {
            reason: String::from(reason),
        };
    }

    fn set_metrics(&mut self, cpu: u8, memory: u8) {
        self.cpu_percent = cpu;
        self.memory_percent = memory;
    }
}
```

Methods that mutate the server take `&mut self`. Methods that only read take
`&self`.

### Step 4: add a summary method

```rust
impl Server {
    fn health_summary(&self) -> String {
        let status_badge = match &self.status {
            ServerStatus::Online => "online",
            ServerStatus::Provisioning => "provisioning",
            ServerStatus::Maintenance(_) => "maintenance",
            ServerStatus::Decommissioned { .. } => "decommissioned",
        };

        format!(
            "{} [{}] CPU {}% MEM {}% - {}",
            self.hostname, self.region,
            self.cpu_percent, self.memory_percent,
            status_badge
        )
    }
}
```

The `Maintenance(_)` pattern ignores the reason. The `Decommissioned { .. }`
pattern ignores all named fields.

### Step 5: put it together

```rust
fn main() {
    let mut server = Server::new("web-01", "us-east");
    server.start();
    server.set_metrics(12, 64);
    println!("{}", server.health_summary());

    server.schedule_maintenance("kernel upgrade");
    println!("{}", server.health_summary());

    server.decommission("hardware end-of-life");
    println!("{}", server.health_summary());
}
```

This is intentionally simple. A real inventory tool would persist state, query
APIs, and handle many more fields. The Rust constructs stay the same.

### Step 6: track a fleet

```rust
fn main() {
    let mut fleet = vec![
        Server::new("web-01", "us-east"),
        Server::new("web-02", "eu-west"),
    ];

    for server in &mut fleet {
        server.start();
        println!("{}", server.health_summary());
    }
}
```

Because `Server` owns its `String` fields, the vector owns the servers.
Iterating with `&mut fleet` lets us call mutating methods.

## Destructuring

Destructuring creates variables from the fields of a struct or enum. It looks
like construction in reverse.

```rust
let Server { hostname, region, cpu_percent } = server;
```

### Renaming fields

```rust
let Server {
    hostname: name,
    region: datacenter,
    cpu_percent: cpu,
} = server;
```

### Ignoring fields with ..

```rust
let Server { hostname, .. } = server;
```

This is helpful when a struct has many fields but you only care about a few.

### Destructuring in function parameters

```rust
fn show(Server { hostname, cpu_percent, .. }: &Server) {
    println!("{} is at {}% CPU", hostname, cpu_percent);
}
```

Patterns can appear anywhere a value is bound, including function arguments.

### Destructuring moves non-Copy fields

If a field is not Copy, destructuring moves it. You cannot use the original
struct afterward.

```rust
fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
        memory_percent: 64,
        status: ServerStatus::Online,
    };

    let Server { hostname, .. } = server;
    println!("{}", hostname);

    // println!("{:?}", server); // error: server.hostname has been moved
}
```

To keep the struct usable, destructure by reference: `let Server { ref hostname,
.. } = server;` or borrow the field later with `&server.hostname`.

## References and the dot operator

When you call a method with `.`, Rust automatically dereferences as many times
as needed.

```rust
fn main() {
    let name = String::from("Billy");
    let double_ref = &&name;

    println!("{}", double_ref.is_empty()); // works!
}
```

`is_empty` expects `&String`, but `double_ref` is `&&String`. The dot operator
adds the right number of `*` for us.

However, comparison operators like `==` do **not** auto-dereference.

```rust
fn main() {
    let a = String::from("Billy");
    let b = String::from("Billy");

    // println!("{}", a == &b); // error
    println!("{}", a == *(&b)); // ok
}
```

Remember: `.` handles derefs for method calls, but operators do not.

## Python to Rust notes

### Classes vs structs and impl blocks

Python puts data and methods together in a class. Rust separates the data
definition from the behavior. You can have multiple impl blocks for the same
type, and they can live in different modules. This separation helps large
codebases.

### Enums are not just integers

In Python, an enum is usually an integer with names attached. In Rust, enums can
carry data and are fully type-checked. `ServerStatus::Maintenance(String)` is a
different shape from `ServerStatus::Online`, and the compiler enforces that.

### Match is exhaustive

Rust requires every `match` to cover every possible variant. Python does not
have an exact equivalent. This catches bugs where you forget to handle a new
status.

### Mutability is explicit

In Python, any method can mutate an object unless you write defensive code. In
Rust, a method must take `&mut self` to mutate. Callers know from the signature
whether the method changes the server.

## Takeaway

- A **struct** groups related values. Pick unit, tuple, or named depending on
  how much naming you need.
- An **enum** represents a choice. Variants can carry data, which makes them
  much more expressive than simple integer enums.
- An **impl block** adds methods and associated functions. Use `::` before the
  value exists, and `.` after it exists.
- `Self` is the type; `self` is the instance variable.
- **Destructuring** pulls fields out of structs and enums. It moves non-Copy
  fields, so use references when you need to keep the original.
- The **dot operator** auto-dereferences for method calls, but operators like
  `==` do not.
- The server lifecycle tracker is intentionally simple, but it shows how structs,
  enums, and impl blocks fit together in a real program.
