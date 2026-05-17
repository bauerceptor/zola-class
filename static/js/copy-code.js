/**
 * copy-code.js
 * Adds a "Copy" button to every <pre><code> block.
 * The feature can be toggled on/off via the menu button (menu.js calls
 * window.setCopyEnabled). State persists in localStorage.
 *
 * Works with Serene's rendered code blocks (Zola wraps highlighted code
 * in <pre class="..."><code>...</code></pre>).
 */

(function () {
  "use strict";

  var STORAGE_KEY = "site-copy-enabled";

  function isEnabled() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      /* Default on if not set */
      return v === null ? true : v === "true";
    } catch (_) {
      return true;
    }
  }

  function setEnabled(val) {
    try { localStorage.setItem(STORAGE_KEY, String(val)); } catch (_) {}
    if (val) {
      addButtons();
    } else {
      removeButtons();
    }
    /* Keep the menu button in sync if it was rendered before this ran */
    syncMenuButton(val);
  }

  /* Expose so menu.js can call it */
  window.setCopyEnabled = setEnabled;

  function syncMenuButton(enabled) {
    var btn   = document.getElementById("copy-toggle-btn");
    var state = document.getElementById("copy-state");
    if (btn)   btn.setAttribute("aria-pressed", String(enabled));
    if (state) state.textContent = enabled ? "On" : "Off";
  }

  /* ── Build a single copy button ────────────────────────────────────── */
  function makeButton(pre) {
    var btn = document.createElement("button");
    btn.className   = "copy-btn";
    btn.textContent = "Copy";
    btn.setAttribute("aria-label", "Copy code to clipboard");

    btn.addEventListener("click", function () {
      var code = pre.querySelector("code");
      var text = code ? code.innerText : pre.innerText;

      navigator.clipboard.writeText(text).then(function () {
        btn.textContent = "Copied!";
        btn.classList.add("copy-btn--ok");
        setTimeout(function () {
          btn.textContent = "Copy";
          btn.classList.remove("copy-btn--ok");
        }, 1800);
      }).catch(function () {
        /* Fallback for browsers without clipboard API */
        var ta = document.createElement("textarea");
        ta.value = text;
        ta.style.cssText = "position:fixed;opacity:0;pointer-events:none";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
        btn.textContent = "Copied!";
        setTimeout(function () { btn.textContent = "Copy"; }, 1800);
      });
    });

    return btn;
  }

  /* ── Add buttons to all pre blocks ────────────────────────────────── */
  function addButtons() {
    document.querySelectorAll("pre").forEach(function (pre) {
      /* Skip if already has a button */
      if (pre.querySelector(".copy-btn")) return;
      /* Skip inline code / very short snippets (< 20 chars) */
      var code = pre.querySelector("code");
      if (code && code.innerText.trim().length < 20) return;

      /* Make pre position:relative so the button can be absolute inside */
      if (getComputedStyle(pre).position === "static") {
        pre.style.position = "relative";
      }

      pre.appendChild(makeButton(pre));
    });
  }

  /* ── Remove all buttons ────────────────────────────────────────────── */
  function removeButtons() {
    document.querySelectorAll(".copy-btn").forEach(function (btn) {
      btn.remove();
    });
  }

  /* ── Init ──────────────────────────────────────────────────────────── */
  function init() {
    var enabled = isEnabled();
    syncMenuButton(enabled);
    if (enabled) addButtons();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
