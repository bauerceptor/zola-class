/**
 * menu.js — hamburger overlay menu injected into every page.
 *
 * The hamburger lives in the top-right corner. Clicking opens a panel
 * that slides in from the right with nav links, theme switcher, copy
 * toggle, and social links. The panel has an explicit ×-close button
 * in its top-right corner; Escape and backdrop click also close it.
 *
 * Edit NAV_LINKS / SOCIAL_LINKS below to point at your own pages.
 */

(function () {
  "use strict";

  var SITE_NAME = document.documentElement.dataset.siteName || "Class — Hassan Aziz";

  var NAV_LINKS = [
    { label: "Home",     url: "https://bauerceptor.github.io/",            external: false },
    { label: "Research", url: "https://bauerceptor.github.io/research/",   external: false },
    { label: "Projects", url: "https://bauerceptor.github.io/projects/",   external: false },
    { label: "Writing",  url: "https://bauerceptor.github.io/posts/",      external: false },
    { label: "Notes",    url: "https://bauerceptor.github.io/notes/",      external: false },
    { label: "Resume",   url: "https://bauerceptor.github.io/resume/",     external: false },
    { label: "Class",    url: "https://bauerceptor.github.io/zola-class/", external: true  },
  ];

  var SOCIAL_LINKS = [
    { label: "GitHub",   url: "https://github.com/bauerceptor" },
    { label: "Email",    url: "mailto:hassanAZIZ4884@gmail.com" },
    { label: "LinkedIn", url: "https://www.linkedin.com/in/hassan-aziz-382485302" },
  ];

  function buildMenu() {
    var navHtml = NAV_LINKS.map(function (link) {
      var ext = link.external ? ' target="_blank" rel="noopener noreferrer"' : "";
      return '<a href="' + link.url + '"' + ext + ">" + link.label + "</a>";
    }).join("\n");

    var socialHtml = SOCIAL_LINKS.map(function (s) {
      return '<a href="' + s.url + '" target="_blank" rel="noopener noreferrer">' + s.label + "</a>";
    }).join("\n");

    return (
      '<div class="menu-wrap">' +
        '<input type="checkbox" class="toggler" id="menu-toggler" aria-label="Toggle navigation">' +
        '<div class="hamburger" aria-hidden="true"><div></div></div>' +
        '<div class="menu-overlay">' +
          '<div class="menu-overlay__panel">' +
            '<div class="menu-overlay__inner">' +
              '<a href="/" class="menu-overlay__site-name">' + SITE_NAME + "</a>" +
              '<nav class="menu-overlay__nav" aria-label="Main navigation">' +
                navHtml +
              "</nav>" +
              '<div class="menu-overlay__divider"></div>' +
              '<div class="menu-overlay__controls">' +
                '<button class="menu-ctrl-btn" id="theme-cycle-btn" aria-label="Cycle colour theme">' +
                  '<span id="theme-icon">⬢</span>' +
                  '<span id="theme-label">System</span>' +
                "</button>" +
                '<button class="menu-ctrl-btn" id="copy-toggle-btn" aria-pressed="true" aria-label="Toggle copy-to-clipboard">' +
                  "⧉ Copy: <span id='copy-state'>On</span>" +
                "</button>" +
              "</div>" +
              '<div class="menu-overlay__social">' +
                socialHtml +
              "</div>" +
            "</div>" +
          "</div>" +
        "</div>" +
      "</div>"
    );
  }

  function init() {
    var container = document.createElement("div");
    container.innerHTML = buildMenu();
    document.body.insertBefore(container.firstChild, document.body.firstChild);

    var overlay  = document.querySelector(".menu-overlay");
    var toggler  = document.getElementById("menu-toggler");

    function close() { if (toggler) toggler.checked = false; }

    if (overlay && toggler) {
      overlay.addEventListener("click", function (e) {
        if (e.target === overlay) close();
      });
    }

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggler && toggler.checked) close();
    });

    var themeBtn = document.getElementById("theme-cycle-btn");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        if (typeof window.cycleTheme === "function") window.cycleTheme();
      });
    }

    var copyBtn = document.getElementById("copy-toggle-btn");
    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        var enabled = this.getAttribute("aria-pressed") === "true";
        var next = !enabled;
        this.setAttribute("aria-pressed", String(next));
        document.getElementById("copy-state").textContent = next ? "On" : "Off";
        if (typeof window.setCopyEnabled === "function") {
          window.setCopyEnabled(next);
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
