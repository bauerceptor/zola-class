/* ────────────────────────────────────────────────────────────────────
 * deck-utils.js — shared slide-deck helpers.
 *
 * Reads the deck's chosen theme (whichever class.css link is in <head>)
 * and lights up the same set of behaviors regardless of which theme is
 * active:
 *
 *   1. Copy-to-clipboard buttons on every <pre>.
 *   2. Mermaid rendering for <pre class="mermaid"> blocks.
 *   3. A custom keyboard-nav indicator (arrow keys) bottom-right.
 *   4. A "?" help overlay listing slide-deck keyboard shortcuts.
 *   5. A slide counter to the left of the keys.
 *
 * Expects Reveal to be present on window.Reveal AND already initialized
 * by the deck's own inline script (the deck owns deck-specific options
 * like hash, transition, plugin choices).
 *
 * Each deck pulls this in once:
 *   <script src="../../../_themes/deck-utils.js" defer></script>
 * Path varies with deck depth.
 * ──────────────────────────────────────────────────────────────────── */

(function () {
  "use strict";

  function init() {
    addCopyButtons();
    setupHelp();
    setupNavKeys();
    setupSlideCounter();
    loadMermaid();
  }

  /* ── Copy-to-clipboard on every <pre> ──────────────────────────── */
  function addCopyButtons() {
    document.querySelectorAll(".reveal pre").forEach(function (pre) {
      /* Skip if the deck already attached its own copy button inline. */
      if (pre.dataset.copyBound || pre.querySelector(".copy-btn")) return;
      pre.dataset.copyBound = "1";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "copy-btn";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy code");
      pre.appendChild(btn);
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var code = pre.querySelector("code");
        var text = code ? code.innerText : pre.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.classList.add("copied");
          btn.textContent = "Copied";
          setTimeout(function () { btn.classList.remove("copied"); btn.textContent = "Copy"; }, 1400);
        }).catch(function () {
          btn.textContent = "Failed";
          setTimeout(function () { btn.textContent = "Copy"; }, 1400);
        });
      });
    });
  }

  /* ── '?' help overlay ──────────────────────────────────────────── */
  function setupHelp() {
    if (document.getElementById("help")) return;
    var help = document.createElement("div");
    help.id = "help";
    help.innerHTML = "<pre>" +
      "  ←/→  prev/next slide        \n" +
      "  ↑/↓  prev/next vertical     \n" +
      "  esc  slide overview         \n" +
      "  f    fullscreen             \n" +
      "  s    speaker notes          \n" +
      "  b    blackout               \n" +
      "  ?    toggle this help       " +
      "</pre>";
    document.body.appendChild(help);
    document.addEventListener("keydown", function (e) {
      if (e.target && e.target.tagName === "INPUT") return;
      if (e.key === "?" || (e.key === "/" && e.shiftKey)) {
        e.preventDefault();
        help.classList.toggle("open");
      } else if (e.key === "Escape" && help.classList.contains("open")) {
        help.classList.remove("open");
      }
    });
    help.addEventListener("click", function () { help.classList.remove("open"); });
  }

  /* ── Bottom-right arrow-key indicator ─────────────────────────── */
  function setupNavKeys() {
    if (!window.Reveal || document.getElementById("nav-keys")) return;
    var box = document.createElement("div");
    box.id = "nav-keys";
    box.innerHTML =
      '<div class="key up"   data-dir="up">↑</div>' +
      '<div class="key left" data-dir="left">←</div>' +
      '<div class="key down" data-dir="down">↓</div>' +
      '<div class="key right" data-dir="right">→</div>';
    document.body.appendChild(box);

    function refresh() {
      var avail = Reveal.availableRoutes ? Reveal.availableRoutes() : {};
      box.querySelectorAll(".key").forEach(function (k) {
        var d = k.dataset.dir;
        k.classList.toggle("active", !!avail[d]);
      });
    }
    box.querySelectorAll(".key").forEach(function (k) {
      k.addEventListener("click", function () {
        if (!k.classList.contains("active")) return;
        var d = k.dataset.dir;
        if (d === "left")  Reveal.left();
        if (d === "right") Reveal.right();
        if (d === "up")    Reveal.up();
        if (d === "down")  Reveal.down();
      });
    });
    Reveal.on("slidechanged", refresh);
    Reveal.on("ready", refresh);
    refresh();
  }

  /* ── Bottom-right slide counter ───────────────────────────────── */
  function setupSlideCounter() {
    if (!window.Reveal || document.getElementById("slide-counter")) return;
    var el = document.createElement("div");
    el.id = "slide-counter";
    document.body.appendChild(el);
    function refresh() {
      var i = Reveal.getIndices();
      var total = Reveal.getTotalSlides();
      el.textContent = (i.h + 1) + " / " + total;
    }
    Reveal.on("slidechanged", refresh);
    Reveal.on("ready", refresh);
    refresh();
  }

  /* ── Mermaid render in slides (fence → SVG) ───────────────────── */
  async function loadMermaid() {
    var blocks = document.querySelectorAll("pre.mermaid, pre > code.language-mermaid, .mermaid");
    if (!blocks.length) return;

    var mod;
    try {
      mod = await import("https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs");
    } catch (err) {
      console.warn("[deck] mermaid load failed:", err);
      return;
    }
    var mermaid = mod.default;

    var dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    mermaid.initialize({
      startOnLoad: false,
      theme: dark ? "dark" : "default",
      securityLevel: "loose",
      themeVariables: { fontFamily: "JetBrains Mono, ui-monospace, monospace" },
    });

    var counter = 0;
    for (var i = 0; i < blocks.length; i++) {
      var node = blocks[i];
      var source;
      var anchor;
      if (node.tagName === "CODE") {
        source = node.textContent.trim();
        anchor = node.parentElement;
      } else {
        source = (node.dataset.source || node.textContent).trim();
        anchor = node;
      }
      if (!source) continue;
      try {
        var id = "deck-mmd-" + (++counter) + "-" + Date.now();
        var rendered = await mermaid.render(id, source);
        var wrap = document.createElement("div");
        wrap.className = "mermaid";
        wrap.dataset.source = source;
        wrap.innerHTML = rendered.svg;
        anchor.replaceWith(wrap);
      } catch (e) {
        console.warn("[deck mermaid]", e && e.message ? e.message : e);
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
