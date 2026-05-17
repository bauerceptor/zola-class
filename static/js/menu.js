/**
 * menu.js
 * Injects the hamburger overlay menu into every page's <body>.
 * Identical file used in repo1 (main site) and repo2 (class site).
 *
 * Config: edit NAV_LINKS and SOCIAL_LINKS below to match your sites.
 * The "Class ↗" link points to the separate zola-class repo URL.
 * The "Main Site" link (shown only on class site) points back.
 */

(function () {
  "use strict";

  /* ── Site identity ─────────────────────────────────────────────────────
     Change SITE_NAME per repo.
     repo1: "Hassan Aziz"
     repo2: "Class — Hassan Aziz"                                        */
  var SITE_NAME = document.documentElement.dataset.siteName || "Class — Hassan Aziz";

  /* ── Navigation links ──────────────────────────────────────────────────
     Shared across both sites. External links get target="_blank".
     Adjust URLs after deployment.                                        */
  var NAV_LINKS = [
    { label: "Home",       url: "https://bauerceptor.github.io/",              external: false },
    { label: "Posts",      url: "https://bauerceptor.github.io/posts/",        external: false },
    { label: "Notes",      url: "https://bauerceptor.github.io/notes/",        external: false },
    { label: "Research",   url: "https://bauerceptor.github.io/research/",     external: false },
    { label: "Projects",   url: "https://bauerceptor.github.io/projects/",     external: false },
    { label: "Resume",     url: "https://bauerceptor.github.io/resume/",       external: false },
    { label: "Class",      url: "https://bauerceptor.github.io/zola-class/",   external: true  },
  ];

  /* ── Social links ──────────────────────────────────────────────────────
     Shown at the bottom of the overlay.                                  */
  var SOCIAL_LINKS = [
    { label: "GitHub",   url: "https://github.com/PLACEHOLDER" },
    { label: "Email",    url: "mailto:PLACEHOLDER@example.com" },
    { label: "Scholar",  url: "https://scholar.google.com/citations?user=PLACEHOLDER" },
    { label: "Twitter",  url: "https://twitter.com/PLACEHOLDER" },
  ];

  /* ── Build the menu HTML ─────────────────────────────────────────────── */
  function buildMenu() {
    /* Nav links HTML */
    var navHtml = NAV_LINKS.map(function (link) {
      var ext = link.external
        ? ' target="_blank" rel="noopener noreferrer"'
        : "";
      return '<a href="' + link.url + '"' + ext + ">" + link.label + "</a>";
    }).join("\n");

    /* Social links HTML */
    var socialHtml = SOCIAL_LINKS.map(function (s) {
      return (
        '<a href="' +
        s.url +
        '" target="_blank" rel="noopener noreferrer">' +
        s.label +
        "</a>"
      );
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
                  '<span id="theme-icon">☀</span>' +
                  '<span id="theme-label">Light</span>' +
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

  /* ── Inject on DOMContentLoaded ─────────────────────────────────────── */
  function init() {
    var container = document.createElement("div");
    container.innerHTML = buildMenu();
    document.body.insertBefore(container.firstChild, document.body.firstChild);

    /* Close overlay when clicking the backdrop (outside the panel) */
    var overlay = document.querySelector(".menu-overlay");
    var toggler = document.getElementById("menu-toggler");

    if (overlay && toggler) {
      overlay.addEventListener("click", function (e) {
        /* Only close if click is on the backdrop, not the panel */
        if (e.target === overlay) {
          toggler.checked = false;
        }
      });
    }

    /* Close on Escape */
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggler && toggler.checked) {
        toggler.checked = false;
      }
    });

    /* Wire up the theme cycle button (theme-toggle.js sets the logic) */
    var themeBtn = document.getElementById("theme-cycle-btn");
    if (themeBtn) {
      themeBtn.addEventListener("click", function () {
        if (typeof window.cycleTheme === "function") {
          window.cycleTheme();
        }
      });
    }

    /* Wire up copy toggle (copy-code.js reads this state) */
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
