/**
 * tree-visited.js — quietly keep score of what the reader has opened.
 *
 *   1. On every page load, mark the current URL's pathname as visited
 *      in localStorage (key: nv-visited-pages, capped at 500 entries).
 *   2. Walk the sidebar tree and:
 *        - For every lecture leaf (li.file > span > a) whose href is in
 *          the visited set, set data-visited="true" so the CSS shows a
 *          quiet dot at the row end.
 *        - For every top-level course (li.folder), count its descendant
 *          lecture leaves + how many are visited, insert a tiny progress
 *          rail under the course title (.nv-progress span), and set
 *          --nv-progress: <pct>% on the folder.
 *
 * No template change required. Purely additive — disabling JS leaves the
 * sidebar identical to its server-rendered HTML.
 */

(function () {
  "use strict";

  var KEY = "nv-visited-pages";
  var MAX = 500;

  function readSet() {
    try {
      var arr = JSON.parse(localStorage.getItem(KEY) || "[]");
      return new Set(Array.isArray(arr) ? arr : []);
    } catch (_) { return new Set(); }
  }
  function writeSet(set) {
    try {
      var arr = Array.from(set).slice(-MAX);
      localStorage.setItem(KEY, JSON.stringify(arr));
    } catch (_) {}
  }

  function normalize(href) {
    try {
      var u = new URL(href, window.location.origin);
      return u.pathname.replace(/\/+$/, "/");
    } catch (_) { return href; }
  }

  function markCurrent(set) {
    var here = normalize(window.location.pathname);
    if (!here || here === "/") return;       /* don't count the home page itself */
    if (!set.has(here)) {
      set.add(here);
      writeSet(set);
    }
  }

  function paintLeaves(set, root) {
    root.querySelectorAll("li.file > span > a").forEach(function (a) {
      var href = normalize(a.getAttribute("href") || a.href);
      if (set.has(href)) a.setAttribute("data-visited", "true");
      else a.removeAttribute("data-visited");
    });
  }

  function paintCourseProgress(set, root) {
    /* Drop the older free-floating rail if a previous version left one. */
    root.querySelectorAll(".nv-progress").forEach(function (el) { el.remove(); });

    root.querySelectorAll(":scope > ul > li.folder").forEach(function (folder) {
      var leaves = folder.querySelectorAll("li.file > span > a");
      var total = leaves.length;
      var done = 0;
      leaves.forEach(function (a) {
        if (a.getAttribute("data-visited") === "true") done += 1;
      });

      /* Inline compact "n / m" chip next to the course title — no
         risk of horizontal overflow into the viewer pane. */
      var titleSpan = folder.querySelector(":scope > span");
      if (!titleSpan) return;
      var chip = titleSpan.querySelector(":scope > .nv-progress-chip");
      if (total === 0) {
        if (chip) chip.remove();
        return;
      }
      if (!chip) {
        chip = document.createElement("span");
        chip.className = "nv-progress-chip";
        titleSpan.appendChild(chip);
      }
      chip.textContent = done + "/" + total;
      chip.dataset.done = String(done);
      chip.dataset.total = String(total);
      chip.title = done + " of " + total + " visited";
      if (done === total) chip.classList.add("nv-progress-chip--full");
      else                chip.classList.remove("nv-progress-chip--full");
    });
  }

  function markCurrentCourse(root) {
    /* Mark the li.folder that contains the currently-selected lecture so
       CSS can give the active course extra emphasis without confusing it
       with "courses I've visited before". */
    root.querySelectorAll(":scope > ul > li.folder").forEach(function (f) {
      f.removeAttribute("data-current");
    });
    var selected = root.querySelector("a.selected");
    if (!selected) return;
    var folder = selected.closest("li.folder");
    if (folder) folder.setAttribute("data-current", "true");
  }

  function init() {
    var root = document.getElementById("files");
    if (!root) return;
    var set = readSet();
    markCurrent(set);
    paintLeaves(set, root);
    paintCourseProgress(set, root);
    markCurrentCourse(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
