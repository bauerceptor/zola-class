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
    root.querySelectorAll(":scope > ul > li.folder").forEach(function (folder) {
      var leaves = folder.querySelectorAll("li.file > span > a");
      var total = leaves.length;
      if (total === 0) return;
      var done = 0;
      leaves.forEach(function (a) {
        if (a.getAttribute("data-visited") === "true") done += 1;
      });
      var pct = Math.round((done / total) * 100);

      var rail = folder.querySelector(":scope > .nv-progress");
      if (!rail) {
        rail = document.createElement("span");
        rail.className = "nv-progress";
        var title = folder.querySelector(":scope > span");
        if (title && title.nextSibling) {
          folder.insertBefore(rail, title.nextSibling);
        } else {
          folder.appendChild(rail);
        }
      }
      folder.style.setProperty("--nv-progress", pct + "%");
      folder.setAttribute("data-progress", String(pct));
      rail.title = done + " of " + total + " visited (" + pct + "%)";
    });
  }

  function init() {
    var root = document.getElementById("files");
    if (!root) return;
    var set = readSet();
    markCurrent(set);
    paintLeaves(set, root);
    paintCourseProgress(set, root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
