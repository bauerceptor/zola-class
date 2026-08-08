#!/usr/bin/env python3
"""
build-deck-rfs5.py - generate the reveal.js slide deck for Rust: First Steps,
Lecture 5: Building Your Own Types.

Run with:
  python3 scripts/build-deck-rfs5.py
"""
import html

OUT = "static/slides/rfs-5/index.html"

# -- Helpers ------------------------------------------------------------------

def slide(idx, title, body, kicker=None, data_id=None):
    sid = (data_id or f"{idx:02d}").lower().replace(" ", "-")
    label = kicker or f"{idx:02d}"
    tag = "h1" if idx == 1 else "h2"
    title_html = f"<{tag}>{title}</{tag}>" if title else ""
    parts = [f'<span class="slide-id">{html.escape(label)}</span>', title_html]
    if body:
        parts.append(body)
    return f'        <section data-id="{html.escape(sid)}">\n          ' + "\n          ".join(filter(None, parts)) + "\n        </section>\n"

def bullets(items):
    return "<ul>\n" + "\n".join(f"<li>{x}</li>" for x in items) + "\n</ul>"

def code(lang, src):
    return f'<pre><code class="language-{lang}" data-trim>{html.escape(src.rstrip())}</code></pre>'

# -- Slides -------------------------------------------------------------------

sections = []

# Section 1: Title
sections.append([
    ("title",
     "Rust: First Steps",
     '<p class="kicker">Lecture 5 - Building Your Own Types</p>\n<p class="lede">Structs, enums, implementations, destructuring, and the dot operator. We will model a server lifecycle tracker as the running example.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>-></code> to begin. Press <code>?</code> for shortcuts.</p>')
])

# Section 2: The project
sections.append([
    ("project-problem",
     "The problem",
     '<p>Imagine you are building a small tool to track a fleet of servers. Each server has a hostname, a region, a status, and some current metrics. You want to:</p>\n' +
     bullets([
         "Create new servers with sensible defaults.",
         "Change their status as they are provisioned, maintained, or decommissioned.",
         "Print a human-readable summary of any server.",
     ]) +
     '<p>This is a perfect fit for structs and enums. The server is a struct, and its status is an enum because a server can only be in one state at a time.</p>'),
    ("project-constructs",
     "Why these constructs?",
     bullets([
         "A <strong>struct</strong> groups the hostname, region, CPU, memory, and status into one type.",
         "An <strong>enum</strong> represents the current status, because a server is either provisioning, online, in maintenance, or decommissioned.",
         "An <strong>impl block</strong> adds methods like <code>start</code>, <code>schedule_maintenance</code>, and <code>health_summary</code>.",
         "<strong>Destructuring</strong> lets us pull fields apart when printing or processing a server.",
     ])),
])

# Section 3: Structs
sections.append([
    ("structs-overview",
     "Structs group related values",
     '<p>A struct is a custom type that bundles several values together. Rust has three kinds.</p>\n' +
     bullets([
         "<strong>Unit struct</strong>: has no fields. Useful as a marker or type-level token.",
         "<strong>Tuple struct</strong>: has fields but no names. Access by position.",
         "<strong>Named struct</strong>: has named fields. This is the most common kind.",
     ])),
    ("unit-struct",
     "Unit struct",
     '<p>A unit struct has no data. It is often used as a marker type.</p>\n' +
     code("rust", '''struct DatabaseNode;

fn main() {
    let _node = DatabaseNode;
}''') +
     '<p>It takes up no space at runtime, but it is still a distinct type. That distinction matters when you use traits or generic code later.</p>'),
    ("tuple-struct",
     "Tuple struct",
     '<p>A tuple struct is like a tuple with a custom name. You access its fields by position.</p>\n' +
     code("rust", '''struct Rgb(u8, u8, u8);

fn main() {
    let color = Rgb(50, 0, 50);
    println!("Green channel: {}", color.1);
}''') +
     '<p>Tuple structs are good when the meaning of the type matters more than the names of the individual fields.</p>'),
    ("named-struct",
     "Named struct",
     '<p>A named struct is the most common. Each field has a name and a type.</p>\n' +
     code("rust", '''struct Server {
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
}''') +
     '<p>Use a comma after the last field if you like. It makes reordering fields safer because every line then ends the same way.</p>'),
    ("field-init-shorthand",
     "Field init shorthand",
     '<p>If a variable has the same name as a struct field, you can write the field name once.</p>\n' +
     code("rust", '''struct Server {
    hostname: String,
    region: String,
}

fn main() {
    let hostname = String::from("web-01");
    let region = String::from("us-east");

    let server = Server {
        hostname,
        region,
    };

    println!("{} {}", server.hostname, server.region);
}''') +
     '<p>This is not special syntax for structs; it is just a shorthand when the names line up. It keeps constructors readable.</p>'),
    ("structs-nest",
     "Structs can contain other structs and enums",
     '<p>A struct field can be another struct or an enum. We will use this to put a status enum inside our Server struct.</p>\n' +
     code("rust", '''enum ServerStatus {
    Online,
    Offline,
}

struct Server {
    hostname: String,
    status: ServerStatus,
}

fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        status: ServerStatus::Online,
    };
}''') +
     '<p>This nesting is one reason Rust types feel composable. You build bigger types out of smaller ones.</p>'),
])

# Section 4: Enums
sections.append([
    ("enums-overview",
     "Enums represent a choice",
     '<p>Use a struct when you want one thing <em>and</em> another thing. Use an enum when you want one thing <em>or</em> another thing.</p>\n' +
     bullets([
         "A struct groups many values together.",
         "An enum lists the possible values, and only one can be active at a time.",
     ])),
    ("enum-basic",
     "Basic enum",
     '<p>Declare the variants inside an enum block. Use <code>::</code> to choose a variant.</p>\n' +
     code("rust", '''enum ServerStatus {
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
}''') +
     '<p>The compiler knows that <code>status</code> must be one of the four variants. A <code>match</code> on an enum must cover every variant.</p>'),
    ("enum-use",
     "Importing variants with use",
     '<p>Typing the enum name every time gets repetitive. You can import the variants with <code>use</code>.</p>\n' +
     code("rust", '''enum ServerStatus {
    Provisioning,
    Online,
    Maintenance,
    Decommissioned,
}

fn check(status: &ServerStatus) {
    use ServerStatus::*;

    match status {
        Online => println!("online"),
        Maintenance => println!("maintenance"),
        _ => println!("other"),
    }
}

fn main() {
    check(&ServerStatus::Maintenance);
}''') +
     '<p><code>use ServerStatus::*</code> imports every variant into the current scope. You can also import individual variants.</p>'),
    ("enum-data",
     "Enums that carry data",
     '<p>Rust enums can hold data inside each variant. This makes them much more powerful than enums in some other languages.</p>\n' +
     code("rust", '''enum ServerStatus {
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
}''') +
     '<p>The data can be a tuple, named fields, or nothing. You extract it through pattern matching.</p>'),
    ("enum-vs-struct",
     "Enum vs struct: a quick rule",
     '<p>If you are unsure which to use, ask whether the type represents:</p>\n' +
     bullets([
         "Many things <strong>together</strong> -> struct.",
         "Many possible <strong>choices</strong>, one active -> enum.",
     ]) +
     '<p>Our Server is a struct because it has hostname, region, CPU, and memory all at once. Its status is an enum because it can only be one state at a time.</p>'),
])

# Section 5: Casting enums
sections.append([
    ("enum-cast",
     "Casting simple enums to integers",
     '<p>If an enum variant has no data, Rust assigns it a number starting from 0. You can cast it to an integer.</p>\n' +
     code("rust", '''enum Priority {
    Low,
    Medium,
    High,
}

fn main() {
    let p = Priority::High;
    println!("{}", p as u32); // 2
}''') +
     '<p>This only works for simple enums. If a variant holds data like <code>Maintenance(String)</code>, you cannot cast it.</p>'),
    ("enum-discriminant",
     "Custom discriminants",
     '<p>You can choose your own numbers. Variants without an explicit number count up from the previous one.</p>\n' +
     code("rust", '''enum HttpStatus {
    Ok = 200,
    NotFound = 404,
    ServerError = 500,
    Teapot = 418,
}

fn main() {
    println!("{}", HttpStatus::NotFound as u16); // 404
}''') +
     '<p>Two variants cannot share the same discriminant. This is useful when you need to map enum values to external constants like HTTP status codes.</p>'),
])

# Section 6: Enums in collections
sections.append([
    ("enum-mixed",
     "Using enums to hold different types in a collection",
     '<p>A Vec can only hold one element type. An enum lets you wrap different types so the Vec stays homogeneous.</p>\n' +
     code("rust", '''enum Metric {
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
}''') +
     '<p>This pattern appears often when reading heterogeneous events or log lines into a single collection.</p>'),
])

# Section 7: Implementing types
sections.append([
    ("impl-overview",
     "Adding behavior with impl blocks",
     '<p>An <code>impl</code> block lets you attach functions to a struct or enum. These functions are called methods and associated functions.</p>\n' +
     bullets([
         "<strong>Methods</strong> take <code>self</code>, <code>&self</code>, or <code>&mut self</code>. Call them with a dot.",
         "<strong>Associated functions</strong> do not take <code>self</code>. Call them with <code>::</code>.",
     ])),
    ("derive-debug",
     "Printing structs and enums",
     '<p>Rust does not let you print a custom type with <code>{}</code> unless you implement the Display trait. For debugging, use <code>#[derive(Debug)]</code> and <code>{:?}</code>.</p>\n' +
     code("rust", '''#[derive(Debug)]
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
}''') +
     '<p><code>#[derive(Debug)]</code> asks the compiler to generate a Debug implementation for you. It is the quickest way to inspect a struct or enum during development.</p>'),
    ("self-vs-Self",
     "self vs Self",
     '<p>Inside an impl block, <code>Self</code> with a capital S is the type. <code>self</code> with a lowercase s is the variable that refers to the instance.</p>\n' +
     code("rust", '''#[derive(Debug)]
struct Server {
    hostname: String,
}

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

fn main() {
    let server = Server::new("web-01");
    println!("{}", server.hostname());
}''') +
     '<p><code>Self</code> is convenient because if you rename the struct, the impl block does not need to change.</p>'),
    ("associated-functions",
     "Associated functions vs methods",
     '<p>Use an associated function when the value does not exist yet. Use a method when the value already exists.</p>\n' +
     code("rust", '''#[derive(Debug)]
struct Server {
    hostname: String,
}

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

fn main() {
    let server = Server::new("web-01");
    println!("{}", server.hostname());
}''') +
     '<p><code>String::from</code> and <code>Vec::new</code> are associated functions you have already used.</p>'),
    ("impl-enum",
     "Implementing methods on enums",
     '<p>Enums can have impl blocks too. This is useful when behavior belongs to the choice itself.</p>\n' +
     code("rust", '''#[derive(Debug)]
enum ServerStatus {
    Online,
    Maintenance(String),
}

impl ServerStatus {
    fn is_operational(&self) -> bool {
        match self {
            ServerStatus::Online => true,
            ServerStatus::Maintenance(_) => false,
        }
    }
}

fn main() {
    let status = ServerStatus::Maintenance(String::from("kernel upgrade"));
    println!("{:?}", status.is_operational()); // false
}''') +
     '<p>Methods on enums often return a value based on which variant is active.</p>'),
])

# Section 8: Building the server tracker
sections.append([
    ("tracker-types",
     "Step 1: define the types",
     '<p>We start with the enum for status and the struct for the server.</p>\n' +
     code("rust", '''#[derive(Debug)]
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
}''') +
     '<p>Both types derive Debug so we can print them while learning.</p>'),
    ("tracker-constructor",
     "Step 2: add a constructor",
     '<p>An associated function creates a new server with a default status.</p>\n' +
     code("rust", '''impl Server {
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

fn main() {
    let server = Server::new("web-01", "us-east");
    println!("{:?}", server);
}''') +
     '<p>New servers start in the Provisioning state with zero CPU and memory usage.</p>'),
    ("tracker-methods",
     "Step 3: add lifecycle methods",
     '<p>Methods change the server status and update metrics.</p>\n' +
     code("rust", '''impl Server {
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
}''') +
     '<p>Methods that mutate the server take <code>&mut self</code>. Methods that only read take <code>&self</code>.</p>'),
    ("tracker-summary",
     "Step 4: add a summary method",
     '<p>A summary method reads the fields and returns a formatted string.</p>\n' +
     code("rust", '''impl Server {
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
}''') +
     '<p>The <code>Maintenance(_)</code> pattern ignores the reason. The <code>Decommissioned { .. }</code> pattern ignores all named fields.</p>'),
    ("tracker-main",
     "Step 5: put it together",
     '<p>Now we can create servers, change their status, and print summaries.</p>\n' +
     code("rust", '''fn main() {
    let mut server = Server::new("web-01", "us-east");
    server.start();
    server.set_metrics(12, 64);
    println!("{}", server.health_summary());

    server.schedule_maintenance("kernel upgrade");
    println!("{}", server.health_summary());

    server.decommission("hardware end-of-life");
    println!("{}", server.health_summary());
}''') +
     '<p>This is intentionally simple. A real inventory tool would persist state, query APIs, and handle many more fields. The Rust constructs stay the same.</p>'),
    ("tracker-fleet",
     "Step 6: track a fleet",
     '<p>A Vec of servers lets us manage more than one machine.</p>\n' +
     code("rust", '''fn main() {
    let mut fleet = vec![
        Server::new("web-01", "us-east"),
        Server::new("web-02", "eu-west"),
    ];

    for server in &mut fleet {
        server.start();
        println!("{}", server.health_summary());
    }
}''') +
     '<p>Because <code>Server</code> owns its <code>String</code> fields, the vector owns the servers. Iterating with <code>&mut fleet</code> lets us call mutating methods.</p>'),
])

# Section 9: Destructuring
sections.append([
    ("destructure-overview",
     "Destructuring: taking types apart",
     '<p>Destructuring creates variables from the fields of a struct or enum. It looks like construction in reverse.</p>\n' +
     bullets([
         "<code>let server = Server { ... }</code> constructs.",
         "<code>let Server { hostname, region } = server</code> destructures.",
     ])),
    ("destructure-struct",
     "Destructuring a struct",
     '<p>You can pull fields out into local variables.</p>\n' +
     code("rust", '''#[derive(Debug)]
struct Server {
    hostname: String,
    region: String,
    cpu_percent: u8,
}

fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
    };

    let Server { hostname, region, cpu_percent } = server;

    println!("{} {} {}", hostname, region, cpu_percent);
}''') +
     '<p>This moves the fields out of the struct. After destructuring, <code>server</code> is no longer usable unless every field is Copy.</p>'),
    ("destructure-rename",
     "Renaming while destructuring",
     '<p>You can give the new variables different names.</p>\n' +
     code("rust", '''fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
    };

    let Server {
        hostname: name,
        region: datacenter,
        cpu_percent: cpu,
    } = server;

    println!("{} {} {}%", name, datacenter, cpu);
}''') +
     '<p>Renaming is useful when the field name is long or when the local variable name needs to fit surrounding code.</p>'),
    ("destructure-ignore",
     "Ignoring fields with ..",
     '<p>Use <code>..</code> to ignore the rest of the fields.</p>\n' +
     code("rust", '''fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
    };

    let Server { hostname, .. } = server;
    println!("{}", hostname);
}''') +
     '<p>This is especially helpful when a struct has many fields but you only care about a few.</p>'),
    ("destructure-function",
     "Destructuring in function parameters",
     '<p>You can destructure directly in a function signature.</p>\n' +
     code("rust", '''fn show(Server { hostname, cpu_percent, .. }: &Server) {
    println!("{} is at {}% CPU", hostname, cpu_percent);
}

fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
    };

    show(&server);
}''') +
     '<p>This works because patterns can appear anywhere a value is bound, including function arguments.</p>'),
    ("destructure-move",
     "Destructuring moves non-Copy fields",
     '<p>If a field is not Copy, destructuring moves it. You cannot use the original struct afterward.</p>\n' +
     code("rust", '''fn main() {
    let server = Server {
        hostname: String::from("web-01"),
        region: String::from("us-east"),
        cpu_percent: 12,
    };

    let Server { hostname, .. } = server;
    println!("{}", hostname);

    // println!("{:?}", server); // error: server.hostname has been moved
}''') +
     '<p>To keep the struct usable, destructure by reference: <code>let Server { ref hostname, .. } = server;</code> or borrow the field later with <code>&server.hostname</code>.</p>'),
])

# Section 10: References and the dot operator
sections.append([
    ("dot-operator",
     "The dot operator auto-dereferences",
     '<p>When you call a method with <code>.</code>, Rust automatically dereferences as many times as needed.</p>\n' +
     code("rust", '''fn main() {
    let name = String::from("Billy");
    let double_ref = &&name;

    println!("{}", double_ref.is_empty()); // works!
}''') +
     '<p><code>is_empty</code> expects <code>&String</code>, but <code>double_ref</code> is <code>&&String</code>. The dot operator adds the right number of <code>*</code> for us.</p>'),
    ("dot-vs-eq",
     "The dot operator does not help ==",
     '<p>Comparison operators like <code>==</code> do not auto-dereference. You must still deref explicitly.</p>\n' +
     code("rust", '''fn main() {
    let a = String::from("Billy");
    let b = String::from("Billy");

    // println!("{}", a == &b); // error: cannot compare String with &String
    println!("{}", a == *(&b)); // ok: String == String
}''') +
     '<p>This trips up newcomers. Remember: <code>.</code> handles derefs for method calls, but operators do not.</p>'),
    ("dot-many-derefs",
     "Even many references work",
     '<p>The dot operator will chase through a chain of references.</p>\n' +
     code("rust", '''fn main() {
    let name = String::from("Billy");
    let ref_chain = &&&&&name;

    println!("{}", ref_chain.is_empty()); // still works
}''') +
     '<p>This is why you rarely need to write <code>*</code> when calling methods. Rust keeps the syntax clean.</p>'),
])

# Section 11: Python to Rust notes
sections.append([
    ("py-classes",
     "Classes vs structs and impl blocks",
     '<p>Python puts data and methods together in a class. Rust separates the data definition (struct or enum) from the behavior (impl block).</p>\n' +
     '<p>You can have multiple impl blocks for the same type, and impl blocks can live in different modules. This separation helps large codebases.</p>'),
    ("py-enums",
     "Enums are not just integers",
     '<p>In Python, an enum is usually an integer with names attached. In Rust, enums can carry data and are fully type-checked. A <code>ServerStatus::Maintenance(String)</code> is a different shape from <code>ServerStatus::Online</code>, and the compiler enforces that.</p>'),
    ("py-match",
     "Match is exhaustive",
     '<p>Rust requires every <code>match</code> to cover every possible variant. Python does not have an exact equivalent. This catches bugs where you forget to handle a new status.</p>'),
    ("py-mutability",
     "Mutability is explicit",
     '<p>In Python, any method can mutate an object unless you write defensive code. In Rust, a method must take <code>&mut self</code> to mutate. Callers know from the signature whether the method changes the server.</p>'),
])

# Section 12: Review and finish
sections.append([
    ("review",
     "What we built",
     bullets([
         "Structs group related data: hostname, region, CPU, memory, status.",
         "Enums represent a single choice among variants, with optional data.",
         "impl blocks attach constructors and methods to types.",
         "Self is the type; self is the instance variable.",
         "Destructuring pulls fields out of structs and enums.",
         "The dot operator auto-dereferences for method calls, but operators like == do not.",
     ])),
    ("fin",
     "What comes next",
     '<p class="lede">Next we look at error handling: how to write functions that can fail and how to propagate those failures cleanly.</p>\n<p style="margin-top:1.6rem;color:var(--fg-3);font-family:var(--font-mono);font-size:0.85rem;">Press <code>?</code> for shortcuts, or <a href="../../rust-first-steps/module1/lec05-building-your-own-types/">return to the chapter page</a>.</p>'),
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

body_html = "".join(section_html_parts)
slide_count = slide_idx

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rust: First Steps - Lecture 5: Building Your Own Types · Hassan Aziz</title>

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

    /* -- Copy-to-clipboard button on every <pre> -- */
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
