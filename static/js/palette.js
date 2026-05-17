/**
 * palette.js — fuzzel-style command palette + Ctrl+/ keyboard guide.
 *
 *   `:`         opens the palette (anywhere on the page that isn't an input)
 *   Ctrl + /    opens the keyboard guide modal
 *   Esc         closes whichever is open
 *
 * The palette merges two source lists:
 *
 *   - Built-in commands  (help, q, find, edit, ls, set mouse=true/false,
 *                         theme system/light/dark)
 *   - Site pages         (window.SITE_PAGES, injected by _head_extend.html)
 *
 * Typing filters both with the same fzf-style scoring used by the bottom
 * prompt. ↑/↓ navigate, ⏎ executes/opens, ⇥ autocompletes to the top match.
 * History (last 50 inputs) persists in localStorage as nv-palette-history.
 *
 * The keyboard guide is a modal listing every key the site listens for —
 * theme keys, palette keys, prompt commands, sidebar/tab keys, custom kbds.
 */

(function () {
  "use strict";

  var HISTORY_KEY = "nv-palette-history";
  var HISTORY_MAX = 50;

  function loadHist() { try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]"); } catch (_) { return []; } }
  function saveHist(h) { try { localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(-HISTORY_MAX))); } catch (_) {} }
  function escHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  /* fzf-style scoring: streak + word-boundary bonus. */
  function fuzzyScore(text, q) {
    if (!q) return 0.001;
    var t = text.toLowerCase(), s = q.toLowerCase();
    var ti = 0, si = 0, score = 0, streak = 0;
    while (ti < t.length && si < s.length) {
      if (t.charCodeAt(ti) === s.charCodeAt(si)) {
        streak += 1;
        var base = 1 + streak * 2;
        if (ti === 0 || /[\s\-_/:]/.test(t.charAt(ti - 1))) base += 4;
        score += base;
        si += 1;
      } else { streak = 0; }
      ti += 1;
    }
    return si === s.length ? score : 0;
  }

  /* ── Built-in commands (always available, ranked first when matched) ── */
  function builtinCommands() {
    return [
      { kind: "cmd", title: "find <query>",   hint: "Fuzzy-search every page",            run: function () { /* handled inline via :find query input */ } },
      { kind: "cmd", title: "edit <query>",   hint: "Open the top fuzzy match directly",  run: function () {} },
      { kind: "cmd", title: "ls",             hint: "List all pages",                     run: function () { fillResults("", true); } },
      { kind: "cmd", title: "help",           hint: "Open the home/help page",            run: function () { location.href = (window.HELP_URL || "/"); } },
      { kind: "cmd", title: "q",              hint: "Exit the site",                      run: function () { location.href = "about:blank"; } },
      { kind: "cmd", title: "set mouse=true", hint: "Show the cursor",                    run: function () { applyMouse(true); } },
      { kind: "cmd", title: "set mouse=false",hint: "Hide the cursor (presentation)",     run: function () { applyMouse(false); } },
      { kind: "cmd", title: "theme system",   hint: "Follow OS color scheme",             run: function () { setTheme("system"); } },
      { kind: "cmd", title: "theme light",    hint: "Force light palette",                run: function () { setTheme("light"); } },
      { kind: "cmd", title: "theme dark",     hint: "Force dark palette",                 run: function () { setTheme("dark"); } },
    ];
  }

  function applyMouse(visible) {
    document.body.style.cursor = visible ? "" : "none";
    try {
      var cfg = JSON.parse(window.Cookies ? Cookies.get("config") || "{}" : "{}");
      cfg.mouse = visible;
      if (window.Cookies) Cookies.set("config", JSON.stringify(cfg));
    } catch (_) {}
  }

  function setTheme(mode) {
    /* theme-toggle.js doesn't expose a setter directly; cycle until match. */
    if (typeof window.cycleTheme !== "function") return;
    var guard = 0;
    while (window.currentTheme && window.currentTheme() !== mode && guard < 5) {
      window.cycleTheme(); guard += 1;
    }
  }

  /* ── DOM scaffolding ─────────────────────────────────────────────────── */
  function buildPalette() {
    if (document.getElementById("nv-palette")) return document.getElementById("nv-palette");

    var root = document.createElement("div");
    root.id = "nv-palette";
    root.hidden = true;
    root.innerHTML =
      '<div class="nv-palette__backdrop" data-close></div>' +
      '<div class="nv-palette__panel" role="dialog" aria-modal="true" aria-label="Command palette">' +
        '<div class="nv-palette__inputrow">' +
          '<span class="nv-palette__sigil">:</span>' +
          '<input class="nv-palette__input" type="text" autocomplete="off" spellcheck="false" placeholder="type a command, or a page name" aria-label="Command or query">' +
        '</div>' +
        '<ul class="nv-palette__list" role="listbox"></ul>' +
        '<div class="nv-palette__footer">' +
          '<span><kbd>↑</kbd><kbd>↓</kbd> navigate</span>' +
          '<span><kbd>⏎</kbd> open</span>' +
          '<span><kbd>⇥</kbd> complete</span>' +
          '<span><kbd>esc</kbd> close</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(root);

    root.querySelector("[data-close]").addEventListener("click", close);

    var input = root.querySelector(".nv-palette__input");
    input.addEventListener("input", function () { update(input.value); });
    input.addEventListener("keydown", onKey);
    return root;
  }

  function buildGuide() {
    if (document.getElementById("nv-guide")) return document.getElementById("nv-guide");

    var rows = [
      ["Sidebar / content focus", [
        ["shift+h",        "Move focus to the file tree"],
        ["shift+l",        "Move focus to the content"],
        ["j / k",          "Scroll content, or move tree selection"],
        ["enter",          "Open the highlighted file"],
      ]],
      ["Tabs", [
        ["shift+t · enter","Open in a new tab"],
        ["tab",            "Cycle through tabs"],
        ["shift+q",        "Close the current tab"],
      ]],
      ["Palette and help", [
        [":",              "Open the command palette (this kind of menu)"],
        ["ctrl + /",       "Show this keyboard guide"],
        ["esc",            "Close any open overlay"],
      ]],
      ["Sidebar tree", [
        ["click ▾ / ▸",    "Fold / unfold a directory"],
      ]],
      ["Inside the palette", [
        ["↑ / ↓",          "Move selection (or cycle history if empty)"],
        ["⏎",              "Run command / open page"],
        ["⇥",              "Autocomplete to top match"],
      ]],
    ];

    var html = '<div class="nv-guide__backdrop" data-close></div>' +
               '<div class="nv-guide__panel" role="dialog" aria-modal="true" aria-label="Keyboard guide">' +
                 '<header class="nv-guide__header">' +
                   '<h2>Keyboard guide</h2>' +
                   '<span class="nv-guide__close-hint">esc to close</span>' +
                 '</header>' +
                 '<div class="nv-guide__cols">';
    rows.forEach(function (group) {
      html += '<section class="nv-guide__group"><h3>' + escHtml(group[0]) + '</h3><dl>';
      group[1].forEach(function (kv) {
        html += '<div class="nv-guide__row"><dt>' +
                kv[0].split(/\s*([+·])\s*|\s+/).filter(Boolean).map(function (t) {
                  return /^[+·]$/.test(t) || t === "/" ? '<span class="nv-guide__sep">' + t + '</span>'
                                                       : '<kbd>' + escHtml(t) + '</kbd>';
                }).join(" ") +
                '</dt><dd>' + escHtml(kv[1]) + '</dd></div>';
      });
      html += '</dl></section>';
    });
    html += '</div></div>';

    var root = document.createElement("div");
    root.id = "nv-guide";
    root.hidden = true;
    root.innerHTML = html;
    document.body.appendChild(root);

    root.querySelector("[data-close]").addEventListener("click", closeGuide);
    return root;
  }

  /* ── Palette filtering / render ──────────────────────────────────────── */
  var palette, input, listEl, selectedIdx, current, history, historyIdx;

  function open(prefill) {
    palette = buildPalette();
    input   = palette.querySelector(".nv-palette__input");
    listEl  = palette.querySelector(".nv-palette__list");
    palette.hidden = false;
    requestAnimationFrame(function () { palette.classList.add("nv-palette--open"); });
    input.value = prefill || "";
    history = loadHist();
    historyIdx = history.length;
    update(input.value);
    setTimeout(function () { input.focus(); input.select(); }, 0);
    document.documentElement.style.overflow = "hidden";
  }
  function close() {
    if (!palette || palette.hidden) return;
    palette.classList.remove("nv-palette--open");
    palette.hidden = true;
    document.documentElement.style.overflow = "";
  }

  function openGuide() {
    var g = buildGuide();
    g.hidden = false;
    requestAnimationFrame(function () { g.classList.add("nv-guide--open"); });
    document.documentElement.style.overflow = "hidden";
  }
  function closeGuide() {
    var g = document.getElementById("nv-guide");
    if (!g || g.hidden) return;
    g.classList.remove("nv-guide--open");
    g.hidden = true;
    document.documentElement.style.overflow = "";
  }

  function pages() { return Array.isArray(window.SITE_PAGES) ? window.SITE_PAGES : []; }

  function combinedSource(query) {
    var q = (query || "").trim();
    var items = [];
    var pagesList = pages();

    /* Parse :find / :edit / :ls / :set / :theme — strip the leading verb from
       the fuzzy query so page matches don't have to include "find" etc. */
    var verbMatch = q.match(/^(?::\s*)?(find|f|edit|e|ls|help|q|set|theme)\b\s*(.*)$/i);
    var verb = null, rest = q;
    if (verbMatch) {
      verb = verbMatch[1].toLowerCase();
      if (verb === "f") verb = "find";
      if (verb === "e") verb = "edit";
      rest = verbMatch[2] || "";
    }

    if (!verb || verb === "find" || verb === "edit") {
      var qForPages = (verb ? rest : q).trim();
      for (var i = 0; i < pagesList.length; i++) {
        var p = pagesList[i];
        var s = qForPages ? fuzzyScore(p.title + " " + p.url, qForPages) : (pagesList.length - i);
        if (s > 0 || !qForPages) {
          items.push({ kind: "page", title: p.title, hint: shortUrl(p.url), score: s, run: function (page) { return function () { location.href = page.url; }; }(p) });
        }
      }
    }

    builtinCommands().forEach(function (c) {
      var hay = c.title + " " + c.hint;
      var s = q ? fuzzyScore(hay, q) : 50;
      if (s > 0) {
        items.push({ kind: "cmd", title: c.title, hint: c.hint, score: s + 8, run: c.run });
      }
    });

    items.sort(function (a, b) { return (b.score || 0) - (a.score || 0); });
    return items.slice(0, 12);
  }

  function shortUrl(u) {
    try { var url = new URL(u); return url.pathname; } catch (_) { return u; }
  }

  function fillResults(prefill, force) {
    if (input && (force || input.value !== prefill)) input.value = prefill || "";
    update(input ? input.value : "");
  }

  function update(value) {
    current = combinedSource(value);
    selectedIdx = current.length ? 0 : -1;
    listEl.innerHTML = current.map(function (item, i) {
      var sel = i === selectedIdx ? " nv-palette__row--sel" : "";
      var tag = item.kind === "cmd" ? "cmd" : "page";
      return '<li class="nv-palette__row nv-palette__row--' + tag + sel + '" role="option">' +
               '<span class="nv-palette__tag">' + tag + '</span>' +
               '<span class="nv-palette__title">' + escHtml(item.title) + '</span>' +
               '<span class="nv-palette__hint">' + escHtml(item.hint || "") + '</span>' +
             '</li>';
    }).join("");
    Array.prototype.forEach.call(listEl.children, function (row, i) {
      row.addEventListener("mouseenter", function () { selectedIdx = i; refreshSel(); });
      row.addEventListener("click", function () { execIdx(i); });
    });
  }

  function refreshSel() {
    Array.prototype.forEach.call(listEl.children, function (row, i) {
      row.classList.toggle("nv-palette__row--sel", i === selectedIdx);
    });
    var sel = listEl.children[selectedIdx];
    if (sel && sel.scrollIntoView) sel.scrollIntoView({ block: "nearest" });
  }

  function execIdx(i) {
    var item = current[i];
    if (!item) return;
    if (input.value.trim()) {
      history.push(input.value);
      saveHist(history);
      historyIdx = history.length;
    }
    close();
    setTimeout(function () { item.run(); }, 30);
  }

  function onKey(e) {
    if (e.key === "Escape") { e.preventDefault(); close(); return; }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (current.length) { selectedIdx = (selectedIdx + 1) % current.length; refreshSel(); }
      else if (historyIdx < history.length) {
        historyIdx = Math.min(historyIdx + 1, history.length);
        input.value = history[historyIdx] || "";
        update(input.value);
      }
      return;
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (current.length) { selectedIdx = (selectedIdx - 1 + current.length) % current.length; refreshSel(); }
      else if (history.length) {
        historyIdx = Math.max(historyIdx - 1, 0);
        input.value = history[historyIdx] || "";
        update(input.value);
      }
      return;
    }
    if (e.key === "Enter") {
      e.preventDefault();
      if (selectedIdx >= 0) execIdx(selectedIdx);
      return;
    }
    if (e.key === "Tab") {
      e.preventDefault();
      var top = current[selectedIdx];
      if (top) {
        input.value = top.kind === "cmd" ? top.title : top.title;
        update(input.value);
      }
    }
  }

  /* ── Global key bindings ─────────────────────────────────────────────── */
  function isTyping(el) {
    if (!el) return false;
    if (el.id === "setter") return true;          /* theme's hidden prompt */
    var t = el.tagName;
    return t === "INPUT" || t === "TEXTAREA" || t === "SELECT" || el.isContentEditable;
  }

  document.addEventListener("keydown", function (e) {
    /* `:` opens the palette unless the user is typing in another input. */
    if (e.key === ":" && !e.metaKey && !e.ctrlKey && !e.altKey) {
      if (isTyping(e.target)) return;
      e.preventDefault();
      e.stopPropagation();
      open();
      return;
    }
    /* Ctrl/Cmd + / opens the keyboard guide. */
    if ((e.key === "/" || e.key === "?") && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      e.stopPropagation();
      openGuide();
      return;
    }
    if (e.key === "Escape") {
      closeGuide();
      /* palette handles its own Esc via input handler */
    }
  }, true);   /* capture-phase: beats the theme's body-level handler */

  /* Backdrop close for guide. */
  document.addEventListener("click", function (e) {
    if (e.target && e.target.matches && e.target.matches("#nv-guide [data-close]")) closeGuide();
  });
})();
