"use strict";

(function () {
    var STORAGE_KEY = "o7am-theme";
    var UI_STORAGE_KEY = "o7am-theme-ui";
    var DEFAULT_THEME = "dark";
    var DEFAULT_UI = "1";

    function getStoredTheme() {
        try {
            return localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
        } catch (e) {
            return DEFAULT_THEME;
        }
    }

    function setStoredTheme(theme) {
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (e) {}
    }

    function getThemeUIFromUrl() {
        var params = new URLSearchParams(window.location.search);
        var n = params.get("theme-ui");
        if (n === "1" || n === "2" || n === "3" || n === "4") return n;
        return null;
    }

    function getStoredThemeUI() {
        try {
            var n = localStorage.getItem(UI_STORAGE_KEY);
            if (n === "1" || n === "2" || n === "3" || n === "4") return n;
        } catch (e) {}
        return DEFAULT_UI;
    }

    function setStoredThemeUI(n) {
        try {
            localStorage.setItem(UI_STORAGE_KEY, n);
        } catch (e) {}
    }

    function applyTheme(theme) {
        var root = document.documentElement;
        root.setAttribute("data-theme", theme === "light" ? "light" : "dark");
        setStoredTheme(theme);

        // Update meta theme-color for mobile browsers
        var meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            meta.content = theme === "light" ? "#efeae2" : "#008776";
        }

        // Sync segment buttons and select
        document.querySelectorAll(".theme-toggle__seg[data-theme-set]").forEach(function (btn) {
            if (btn.getAttribute("data-theme-set") === theme) {
                btn.setAttribute("data-active", "");
            } else {
                btn.removeAttribute("data-active");
            }
        });
        var sel = document.querySelector(".theme-toggle__select[data-theme-select]");
        if (sel) sel.value = theme;
    }

    function applyThemeUI(n) {
        var toggle = document.querySelector(".theme-toggle");
        if (!toggle) return;
        var num = n === "1" || n === "2" || n === "3" || n === "4" ? n : DEFAULT_UI;
        toggle.setAttribute("data-theme-ui", num);
        setStoredThemeUI(num);
    }

    function toggleTheme() {
        var current = document.documentElement.getAttribute("data-theme");
        var next = current === "light" ? "dark" : "light";
        applyTheme(next);
    }

    function init() {
        var theme = getStoredTheme();
        var uiFromUrl = getThemeUIFromUrl();
        var themeUI = uiFromUrl !== null ? uiFromUrl : getStoredThemeUI();

        applyTheme(theme);
        applyThemeUI(themeUI);

        // Toggle buttons (variant 1 and 3)
        document.querySelectorAll("[data-theme-toggle]").forEach(function (el) {
            el.addEventListener("click", function (e) {
                e.preventDefault();
                toggleTheme();
            });
        });

        // Segment buttons (variant 2)
        document.querySelectorAll(".theme-toggle__seg[data-theme-set]").forEach(function (el) {
            el.addEventListener("click", function (e) {
                e.preventDefault();
                var t = el.getAttribute("data-theme-set");
                if (t) applyTheme(t);
            });
        });

        // Select (variant 4)
        var select = document.querySelector(".theme-toggle__select[data-theme-select]");
        if (select) {
            select.addEventListener("change", function () {
                applyTheme(select.value);
            });
        }

        // Footer: theme UI switcher links
        document.querySelectorAll(".theme-ui-switcher a[data-theme-ui]").forEach(function (a) {
            a.addEventListener("click", function (e) {
                e.preventDefault();
                var n = a.getAttribute("data-theme-ui");
                applyThemeUI(n);
                var url = new URL(window.location.href);
                url.searchParams.set("theme-ui", n);
                window.history.replaceState({}, "", url.toString());
            });
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
