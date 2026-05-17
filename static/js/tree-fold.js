/**
 * tree-fold.js — collapsible folder tree in the left sidebar.
 *
 * The vendored neovim-theme renders the file tree fully expanded with no
 * fold affordance. This walks the rendered tree, inserts a chevron
 * disclosure before each folder, hides the children of collapsed folders,
 * and persists the open/closed state per-folder in localStorage. The path
 * to the currently-viewed page is auto-expanded on first visit so the
 * active lecture is always visible.
 *
 * Keys for keyboard navigation:
 *   Enter / Space on a folder chevron → toggle.
 *   Clicking the folder *name* still navigates (preserves theme behavior).
 *
 * Storage key: nv-tree-folds → { "/cs101/": "open", "/speeches/": "closed" }
 */

(function () {
  "use strict";

  var STORAGE_KEY = "nv-tree-folds";

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}"); }
    catch (_) { return {}; }
  }
  function saveState(state) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch (_) {}
  }

  function init() {
    var root = document.getElementById("files");
    if (!root) return;

    var state = loadState();

    /* Walk every folder li (theme uses .folder and .subfolder). Each
       folder is structured: <li class="folder"><span>...<a>name</a></span><ul>…</ul></li>
       We treat any li that contains a direct <ul> as a folder. */
    var folderItems = root.querySelectorAll("li");
    folderItems.forEach(function (li) {
      var inner = li.querySelector(":scope > ul");
      if (!inner) return;

      var span = li.querySelector(":scope > span");
      if (!span) return;

      var anchor = span.querySelector("a");
      if (!anchor) return;

      var key = anchor.getAttribute("href") || anchor.textContent.trim();

      var chevron = document.createElement("button");
      chevron.type = "button";
      chevron.className = "nv-fold-toggle";
      chevron.setAttribute("aria-label", "Toggle folder");
      chevron.setAttribute("aria-expanded", "true");
      chevron.innerHTML = "<span aria-hidden='true'>▾</span>";

      span.insertBefore(chevron, span.firstChild);

      function setOpen(open) {
        li.classList.toggle("nv-fold-closed", !open);
        chevron.setAttribute("aria-expanded", String(open));
        chevron.firstElementChild.textContent = open ? "▾" : "▸";
      }

      chevron.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var nowClosed = li.classList.toggle("nv-fold-closed");
        chevron.setAttribute("aria-expanded", String(!nowClosed));
        chevron.firstElementChild.textContent = nowClosed ? "▸" : "▾";
        state[key] = nowClosed ? "closed" : "open";
        saveState(state);
      });

      var saved = state[key];
      if (saved === "closed") setOpen(false);
      else if (saved === "open") setOpen(true);
      else setOpen(false);  /* default: all closed */
    });

    /* Auto-expand the path to the currently-selected page (or to the page
       whose URL matches the current location). */
    var current = root.querySelector("a.selected")
              || Array.prototype.find.call(
                  root.querySelectorAll("a"),
                  function (a) { return a.href === window.location.href; }
                );
    if (current) {
      var node = current.closest("li");
      while (node && node !== root) {
        if (node.classList.contains("nv-fold-closed")) {
          node.classList.remove("nv-fold-closed");
          var c = node.querySelector(":scope > span > .nv-fold-toggle");
          if (c) {
            c.setAttribute("aria-expanded", "true");
            c.firstElementChild.textContent = "▾";
          }
        }
        node = node.parentElement && node.parentElement.closest("li");
      }
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
