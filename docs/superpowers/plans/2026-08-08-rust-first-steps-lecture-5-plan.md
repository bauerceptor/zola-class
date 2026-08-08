# Rust: First Steps — Lecture 5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the reveal.js slide deck, chapter webpage, and supporting documentation for Rust: First Steps Lecture 5 (Building Your Own Types), and backfill dates for Lectures 1-4.

**Architecture:** Reuse the existing generator pattern from `scripts/build-deck-rfs4.py`. Create `scripts/build-deck-rfs5.py` with the Lecture 5 content, run it to produce `static/slides/rfs-5/index.html`, and write a matching Zola lecture page. Update course overview and date frontmatter in existing lectures.

**Tech stack:** Python 3, reveal.js 5.1.0, Zola 0.19.2, the shared `clean.css` slide theme.

---

## Task 1: Backfill lecture dates

**Files:**
- Modify: `content/rust-first-steps/module1/lec01-the-basics.md`
- Modify: `content/rust-first-steps/module1/lec02-memory-and-ownership.md`
- Modify: `content/rust-first-steps/module1/lec03-the-building-blocks.md`
- Modify: `content/rust-first-steps/module1/lec04-complex-types.md`

- [ ] **Step 1: Change Lecture 1 date to 2026-06-15**
  Replace `date = 2026-06-18` (or current value) with `date = 2026-06-15`.

- [ ] **Step 2: Change Lecture 2 date to 2026-06-17**
  Replace current date with `date = 2026-06-17`.

- [ ] **Step 3: Change Lecture 3 date to 2026-06-19**
  Replace current date with `date = 2026-06-19`.

- [ ] **Step 4: Change Lecture 4 date to 2026-06-21**
  Replace current date with `date = 2026-06-21`.

---

## Task 2: Update course overview

**Files:**
- Modify: `content/rust-first-steps/_index.md`

- [ ] **Step 1: Add Lecture 5 summary paragraph**
  After the Lecture 4 paragraph, add:
  ```markdown
  Chapter 5 - **Building Your Own Types** - uses a DevOps server lifecycle
  tracker to explore structs, enums, `impl` blocks, destructuring, and the
  dot operator.
  ```

---

## Task 3: Create the slide deck generator

**Files:**
- Create: `scripts/build-deck-rfs5.py`

- [ ] **Step 1: Write the generator**
  Copy the structure of `scripts/build-deck-rfs4.py` and adapt the content.
  Key requirements:
  - Set `OUT = "static/slides/rfs-5/index.html"`.
  - Use `../_themes/clean.css` for the theme link.
  - Deck title: "Rust: First Steps - Lecture 5: Building Your Own Types".
  - Final slide links to `../../rust-first-steps/module1/lec05-building-your-own-types/` with text "return to the chapter page".
  - Sections (horizontal) and sub-slides (vertical) follow the approved spec.
  - Include the server lifecycle tracker code incrementally.
  - Include Python-vs-Rust notes and subtleties (Self vs self, derive Debug,
    dot operator auto-deref, exhaustive match, unit structs, etc.).

---

## Task 4: Generate the slide deck

**Files:**
- Create: `static/slides/rfs-5/index.html`

- [ ] **Step 1: Run the generator**
  ```bash
  python3 scripts/build-deck-rfs5.py
  ```
  Expected: `Wrote N slides to static/slides/rfs-5/index.html`.

---

## Task 5: Create the lecture webpage

**Files:**
- Create: `content/rust-first-steps/module1/lec05-building-your-own-types.md`

- [ ] **Step 1: Write frontmatter**
  ```toml
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
  ```

- [ ] **Step 2: Write body**
  Start with `<!-- Chapter codename: rfs-5 -->`.
  Include the slide deck card with the shortcode.
  Summarize structs, enums, impl blocks, destructuring, and the dot operator.
  Include the server lifecycle tracker in incremental steps.
  Add Python-vs-Rust notes and a takeaway list.

---

## Task 6: Update documentation

**Files:**
- Modify: `README.md`
- Modify: `guide-for-ai.md`

- [ ] **Step 1: Document the new generator in README.md**
  Add `build-deck-rfs5.py` to the list of generators and a note about the
  two-day lecture date convention.

- [ ] **Step 2: Document the new generator and date convention in guide-for-ai.md**
  Update the generator list in §3.4 and add a note that lectures are dated
  two days apart, starting from 15 June, rolling into July after June.

---

## Task 7: Build and verify

- [ ] **Step 1: Run Zola build**
  ```bash
  zola build
  ```
  Expected: success, no errors.

- [ ] **Step 2: Sanity-check generated files**
  Confirm `static/slides/rfs-5/index.html` exists and the lecture page is at
  `content/rust-first-steps/module1/lec05-building-your-own-types.md`.

---

## Task 8: Commit and push

- [ ] **Step 1: Stage all changes**
  ```bash
  git add -A
  ```

- [ ] **Step 2: Commit**
  ```bash
  git commit -m "lec: rust-first-steps lecture 5 (building your own types)"
  ```

- [ ] **Step 3: Push**
  ```bash
  git push
  ```
  Expected: pushed to origin/main.
