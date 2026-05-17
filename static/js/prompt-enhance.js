/**
 * prompt-enhance.js — turn the theme's `:` prompt into a real command line.
 *
 * Adds three things on top of the vendored commands.js:
 *
 *   1. Fuzzy file search: `:find <q>` (or just `:f <q>`) opens a dropdown
 *      ranking every page in window.SITE_PAGES by match score. Up/Down
 *      moves selection; Enter opens.
 *
 *   2. Direct jump: `:edit <path>` (or `:e <path>`) opens the first page
 *      whose URL contains <path>.
 *
 *   3. History: ↑ / ↓ when the prompt is focused cycle through past
 *      commands (persisted in localStorage under nv-prompt-history).
 *
 * The dropdown UI is injected just above the prompt bar; no DOM changes
 * to the theme templates. Falls back silently if window.SITE_PAGES is
 * missing (e.g. on the 404 page that doesn't include _head_extend.html).
 */

(function () {
  "use strict";

  var HISTORY_KEY = "nv-prompt-history";
  var HISTORY_MAX = 50;

  function loadHistory() {
    try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); }
    catch (_) { return []; }
  }
  function saveHistory(h) {
    try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(-HISTORY_MAX))); }
    catch (_) {}
  }

  /* Tiny fuzzy matcher: returns 0 if no match, otherwise a score where
     higher = better. Consecutive matches and earlier matches score higher;
     matches at word boundaries score even higher. Adapted from common
     fzf-style scoring. */
  function fuzzyScore(text, q) {
    if (!q) return 1;
    var t = text.toLowerCase(), s = q.toLowerCase();
    var ti = 0, si = 0, score = 0, streak = 0;
    while (ti < t.length && si < s.length) {
      if (t.charCodeAt(ti) === s.charCodeAt(si)) {
        streak += 1;
        var base = 1 + streak * 2;
        if (ti === 0 || /[\s\-_/]/.test(t.charAt(ti - 1))) base += 4;
        score += base;
        si += 1;
      } else {
        streak = 0;
      }
      ti += 1;
    }
    return si === s.length ? score : 0;
  }

  function rank(pages, q) {
    var scored = [];
    for (var i = 0; i < pages.length; i++) {
      var p = pages[i];
      var s = fuzzyScore(p.title + " " + p.url, q);
      if (s > 0) scored.push({ page: p, score: s });
    }
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 8).map(function (x) { return x.page; });
  }

  function init() {
    var setter = document.getElementById("setter");
    var writer = document.getElementById("writer");
    if (!setter || !writer) return;

    var pages = Array.isArray(window.SITE_PAGES) ? window.SITE_PAGES : [];
    var history = loadHistory();
    var historyIdx = history.length;

    /* Build the dropdown UI under the prompt label. */
    var prompt = document.getElementById("terminal");
    var dropdown = document.createElement("div");
    dropdown.className = "nv-prompt-dropdown";
    dropdown.setAttribute("role", "listbox");
    dropdown.hidden = true;
    prompt.appendChild(dropdown);

    var selectedIdx = -1;
    var lastMatches = [];

    function render(matches) {
      lastMatches = matches;
      if (!matches.length) { dropdown.hidden = true; return; }
      dropdown.innerHTML = matches.map(function (m, i) {
        var sel = i === selectedIdx ? " nv-prompt-row--sel" : "";
        return '<a class="nv-prompt-row' + sel + '" href="' + m.url + '">' +
                 '<span class="nv-prompt-row__title">' + escapeHtml(m.title) + '</span>' +
                 '<span class="nv-prompt-row__url">' + escapeHtml(m.url.replace(window.location.origin, "")) + '</span>' +
               '</a>';
      }).join("");
      dropdown.hidden = false;
      Array.prototype.forEach.call(dropdown.children, function (row, i) {
        row.addEventListener("mouseenter", function () { selectedIdx = i; refreshSel(); });
        row.addEventListener("click", function (e) {
          e.preventDefault();
          openMatch(lastMatches[i]);
        });
      });
    }

    function refreshSel() {
      Array.prototype.forEach.call(dropdown.children, function (row, i) {
        row.classList.toggle("nv-prompt-row--sel", i === selectedIdx);
      });
    }

    function openMatch(m) {
      if (!m) return;
      pushHistory(setter.value);
      window.location.href = m.url;
    }

    function pushHistory(line) {
      if (!line) return;
      if (history[history.length - 1] === line) return;
      history.push(line);
      saveHistory(history);
      historyIdx = history.length;
    }

    function escapeHtml(s) {
      return String(s)
        .replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    /* Parse the current input. If it starts with `:find ` / `:f ` /
       `:edit ` / `:e `, return { cmd, query }. */
    function parse(value) {
      var m = value.match(/^\s*:?(find|f|edit|e|ls)\b\s*(.*)$/i);
      if (!m) return null;
      var cmd = m[1].toLowerCase();
      if (cmd === "f")  cmd = "find";
      if (cmd === "e")  cmd = "edit";
      return { cmd: cmd, query: (m[2] || "").trim() };
    }

    function update() {
      var raw = setter.value;
      var p = parse(raw);
      if (!p) { dropdown.hidden = true; selectedIdx = -1; return; }
      if (p.cmd === "ls") {
        selectedIdx = 0;
        render(pages.slice(0, 8));
        return;
      }
      var matches = rank(pages, p.query);
      selectedIdx = matches.length ? 0 : -1;
      render(matches);
    }

    setter.addEventListener("input", update);
    setter.addEventListener("focus", update);
    setter.addEventListener("blur", function () {
      /* Delay so mousedown on a row registers first. */
      setTimeout(function () { dropdown.hidden = true; }, 120);
    });

    setter.addEventListener("keydown", function (e) {
      var isOpen = !dropdown.hidden && lastMatches.length;

      if (e.key === "ArrowDown") {
        if (isOpen) {
          e.preventDefault();
          selectedIdx = (selectedIdx + 1) % lastMatches.length;
          refreshSel();
        } else if (historyIdx < history.length) {
          e.preventDefault();
          historyIdx = Math.min(historyIdx + 1, history.length);
          setter.value = history[historyIdx] || "";
          /* Trigger theme's writeit() so #writer updates. */
          setter.dispatchEvent(new Event("input"));
        }
        return;
      }

      if (e.key === "ArrowUp") {
        if (isOpen) {
          e.preventDefault();
          selectedIdx = (selectedIdx - 1 + lastMatches.length) % lastMatches.length;
          refreshSel();
        } else if (history.length) {
          e.preventDefault();
          historyIdx = Math.max(historyIdx - 1, 0);
          setter.value = history[historyIdx] || "";
          setter.dispatchEvent(new Event("input"));
        }
        return;
      }

      if (e.key === "Enter") {
        if (isOpen && lastMatches[selectedIdx]) {
          e.preventDefault();
          openMatch(lastMatches[selectedIdx]);
          return;
        }
        pushHistory(setter.value);
        return;
      }

      if (e.key === "Tab") {
        /* Autocomplete to top match if dropdown is open. */
        if (isOpen && lastMatches[selectedIdx]) {
          e.preventDefault();
          var top = lastMatches[selectedIdx];
          var p = parse(setter.value);
          var prefix = p && p.cmd === "edit" ? ":edit " : ":find ";
          setter.value = prefix + top.title;
          setter.dispatchEvent(new Event("input"));
        }
        return;
      }

      if (e.key === "Escape") {
        dropdown.hidden = true;
        selectedIdx = -1;
      }
    });

    /* Add :find / :edit / :ls cases to the theme's command dispatcher.
       commands.js looks at a global `commands` object before falling
       through to its built-in switch, so register handlers there. */
    window.commands = window.commands || {};
    window.commands.find = function () {
      if (lastMatches[selectedIdx]) openMatch(lastMatches[selectedIdx]);
    };
    window.commands.f = window.commands.find;
    window.commands.edit = function () {
      var p = parse(setter.value);
      if (!p) return;
      var matches = rank(pages, p.query);
      if (matches.length) openMatch(matches[0]);
    };
    window.commands.e = window.commands.edit;
    window.commands.ls = window.commands.find;
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
