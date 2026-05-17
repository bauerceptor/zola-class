/**
 * theme-toggle.js
 * Cycles through three states: system → light → dark → system …
 *
 * How it works with Serene:
 *   Serene reads the `html` element's class: "light" | "dark" | (none = system).
 *   We add/remove those classes and persist the choice in localStorage.
 *
 * How it works with syntax highlighting:
 *   Zola generates /giallo-light.css and /giallo-dark.css.
 *   The <link> tags for these are in _head_extend.html with id="hl-light" / "hl-dark".
 *   We swap their `media` attributes so only the correct one applies.
 *
 * Exposed globals:
 *   window.cycleTheme()   — called by the menu button in menu.js
 */

(function () {
  "use strict";

  var STORAGE_KEY = "site-theme"; // "light" | "dark" | "system"
  var THEMES = ["system", "light", "dark"];

  var ICONS  = { system: "⬡", light: "☀", dark: "☾" };
  var LABELS = { system: "System", light: "Light", dark: "Dark" };

  /* ── Read persisted preference ─────────────────────────────────────── */
  function getSaved() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      return THEMES.indexOf(v) !== -1 ? v : "system";
    } catch (_) {
      return "system";
    }
  }

  function save(theme) {
    try { localStorage.setItem(STORAGE_KEY, theme); } catch (_) {}
  }

  /* ── Apply a theme to the document ────────────────────────────────── */
  function apply(theme) {
    var html = document.documentElement;

    /* Serene's theme toggle uses `light` / `dark` classes on <html> */
    html.classList.remove("light", "dark");
    if (theme === "light") html.classList.add("light");
    if (theme === "dark")  html.classList.add("dark");

    /* Resolve effective theme for highlight sheet swap */
    var effective = theme;
    if (theme === "system") {
      effective = window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
    }
    swapHighlight(effective);
    updateMenuButton(theme);
  }

  /* ── Swap highlight stylesheets ────────────────────────────────────── */
  function swapHighlight(effective) {
    var light = document.getElementById("hl-light");
    var dark  = document.getElementById("hl-dark");

    if (!light || !dark) return;

    if (effective === "dark") {
      light.media = "not all"; /* disable */
      dark.media  = "all";     /* enable  */
    } else {
      light.media = "all";
      dark.media  = "not all";
    }
  }

  /* ── Update the menu button label/icon ─────────────────────────────── */
  function updateMenuButton(theme) {
    var icon  = document.getElementById("theme-icon");
    var label = document.getElementById("theme-label");
    if (icon)  icon.textContent  = ICONS[theme]  || "⬡";
    if (label) label.textContent = LABELS[theme] || "System";
  }

  /* ── Cycle to next theme ───────────────────────────────────────────── */
  function cycleTheme() {
    var current = getSaved();
    var idx  = THEMES.indexOf(current);
    var next = THEMES[(idx + 1) % THEMES.length];
    save(next);
    apply(next);
  }

  /* Expose globally so menu.js can call it */
  window.cycleTheme = cycleTheme;

  /* ── React to OS preference changes (when in "system" mode) ────────── */
  var mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", function () {
    if (getSaved() === "system") apply("system");
  });

  /* ── Init on load ──────────────────────────────────────────────────── */
  /* Apply immediately (before paint) to avoid flash */
  apply(getSaved());

  /* Re-apply after DOM ready in case menu button nodes weren't available */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      apply(getSaved());
    });
  }
})();
