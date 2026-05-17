/**
 * theme-toggle.js — three-way theme switcher: system → light → dark → …
 *
 * The class on <html> (`light`, `dark`, or absent for system) drives every
 * theme-aware CSS rule in class.css (the OKLCH palette tokens) and the
 * WebGL aurora reads the same CSS variables so it follows along.
 *
 * Loaded SYNCHRONOUSLY (not deferred) so the initial paint already has
 * the correct theme applied — prevents a flash of the wrong palette.
 *
 * Exposed globals:
 *   window.cycleTheme()       cycle to next mode (called by the menu button)
 *   window.currentTheme()     "system" | "light" | "dark"
 *   window.effectiveTheme()   resolves "system" to the actual OS preference
 */

(function () {
  "use strict";

  var STORAGE_KEY = "site-theme";
  var THEMES = ["system", "light", "dark"];
  var ICONS  = { system: "⬢", light: "☼", dark: "☽" };
  var LABELS = { system: "System",  light: "Light", dark: "Dark" };

  function getSaved() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      return THEMES.indexOf(v) !== -1 ? v : "system";
    } catch (_) { return "system"; }
  }

  function save(theme) {
    try { localStorage.setItem(STORAGE_KEY, theme); } catch (_) {}
  }

  function resolveEffective(theme) {
    if (theme === "system") {
      return window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark" : "light";
    }
    return theme;
  }

  function swapSyntax(effective) {
    var light = document.getElementById("hl-light");
    var dark  = document.getElementById("hl-dark");
    if (!light || !dark) return;
    if (effective === "dark") { light.media = "not all"; dark.media = "all"; }
    else                      { light.media = "all";     dark.media = "not all"; }
  }

  function apply(theme) {
    var html = document.documentElement;
    html.classList.remove("light", "dark");
    var effective = resolveEffective(theme);
    html.classList.add(effective);
    html.dataset.themeMode = theme;
    html.dataset.themeEffective = effective;
    swapSyntax(effective);
    updateMenuButton(theme);
    window.dispatchEvent(new CustomEvent("themechange", {
      detail: { mode: theme, effective: effective }
    }));
  }

  function updateMenuButton(theme) {
    var icon  = document.getElementById("theme-icon");
    var label = document.getElementById("theme-label");
    if (icon)  icon.textContent  = ICONS[theme]  || ICONS.system;
    if (label) label.textContent = LABELS[theme] || LABELS.system;
  }

  function cycleTheme() {
    var current = getSaved();
    var next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length];
    save(next);
    apply(next);
  }

  window.cycleTheme = cycleTheme;
  window.currentTheme = getSaved;
  window.effectiveTheme = function () { return resolveEffective(getSaved()); };

  var media = window.matchMedia("(prefers-color-scheme: dark)");
  media.addEventListener("change", function () {
    if (getSaved() === "system") apply("system");
  });

  apply(getSaved());

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      apply(getSaved());
    });
  }
})();
