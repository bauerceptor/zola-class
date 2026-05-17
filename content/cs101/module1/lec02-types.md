+++
title = "Lecture 2 — Data Types"
date = 2025-01-22
weight = 2
description = "How computers represent integers, floats, strings, and booleans."

[extra]
lang        = "en"
course      = "CS 101"
lecture_num = 2
math        = false
mermaid     = false
copy        = true
+++

## Slides

No slides for this lecture — notes only.

---

## Lecture Notes

### Why types matter

Every value a computer stores has a type. Types tell the machine how
much memory to allocate and how to interpret the raw bits.

### Primitive types in Python

| Type    | Example         | Notes |
|---------|-----------------|-------|
| `int`   | `42`, `-7`      | Arbitrary precision in Python |
| `float` | `3.14`, `1e-5`  | IEEE 754 double precision |
| `str`   | `"hello"`       | Unicode, immutable |
| `bool`  | `True`, `False` | Subclass of `int` |

### Common pitfall: float arithmetic

```python
>>> 0.1 + 0.2
0.30000000000000004
```

This is not a Python bug. It is a consequence of IEEE 754 binary
floating-point representation. For exact decimal arithmetic use the
`decimal` module.

### Type conversion

```python
x = int("42")    # str → int
y = str(3.14)    # float → str
z = float(True)  # bool → float: 1.0
```

---

## Further Reading

- Python docs: [Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- Chapter 2 of the textbook

## Next lecture

[Lecture 3 — Control Flow](../../module2/lec03-control/)
