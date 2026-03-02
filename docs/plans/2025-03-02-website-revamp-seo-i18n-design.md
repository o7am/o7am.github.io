# o7.am Website Revamp: SEO & English Translation

**Date:** 2025-03-02  
**Focus:** Full revamp, mainly SEO; add English translation.  
**Scope:** Validation audit, then phased implementation (SEO + i18n first, then performance and fixes).

---

## 1. Goals, scope, success criteria

**Goals**
- Improve **search visibility** for o7AM (3D print, Data Engineering, ML) in Polish and English.
- Add **full English version** of the site so it can be found and read by international clients.
- Fix **broken assets and meta** so sharing and indexing work correctly.
- Keep the revamp **manageable**: static site, no backend; SEO and content first, then performance.

**Out of scope (for this plan)**
- Full visual/UX redesign (only small fixes if they help SEO or clarity).
- Blog CMS or dynamic content (existing static blog pages stay as-is).

**Success criteria**
- Every page has unique, descriptive `<title>` and `<meta name="description">` in PL and EN.
- English content available at predictable URLs (e.g. `https://o7.am/en/...`).
- Search engines can discover all important pages (sitemap, sensible internal links).
- No broken images or wrong asset paths; one canonical and one share image per page (or section) where it matters.
- Core Web Vitals and image payload improved enough that the site doesn’t suffer from obvious bloat (targets can be set after validation).

---

## 2. Validation phase (audit before implementation)

Run a short audit and record results so the revamp is evidence-based.

**SEO & discoverability**
- [ ] List every public HTML page and its current title, meta description, og:url.
- [ ] Check for sitemap.xml and robots.txt (currently missing).
- [ ] Note canonical and hreflang usage (currently none).
- [ ] Check og:image / twitter:image (currently commented out); decide default and per-page images.

**Content & i18n**
- [ ] Inventory all user-facing text (nav, headings, body, buttons, footer) and mark which are PL-only.
- [ ] Decide default language (recommended: Polish for `/`, English under `/en/`).
- [ ] Identify any content that should differ by locale (e.g. contact details, legal).

**Technical correctness**
- [ ] Confirm broken references: `assets/pics/logo2.jpg` (index), `assets/portfolios/entry2.webp` (portfolio).
- [ ] List all image assets with dimensions and file size; flag those > ~300–500 KB for optimization.

**Performance (light pass)**
- [ ] Measure LCP and main image requests on key pages (e.g. index, one service, one portfolio).
- [ ] Note which images are above-the-fold and repeated across pages (e.g. clancy.jpg, logo_wide.jpg).

Deliverable: a short **audit report** (e.g. `docs/plans/audit-YYYY-MM-DD.md`) with the checklist filled and a prioritized list of fixes.

---

## 3. English translation (i18n approach)

**Recommended approach: language subfolders, static HTML**

- **Polish (default):** current URLs unchanged (`/`, `/about.html`, `/services/3d.html`, etc.).
- **English:** mirror structure under `/en/` (e.g. `/en/index.html`, `/en/about.html`, `/en/services/3d.html`).

**Why this**
- Clear, crawlable URLs; no backend or build-time i18n framework required.
- Easy to add `hreflang` and canonical: each page points to its PL and EN counterparts.
- Simple mental model: duplicate the page tree, swap content and meta into English.

**What to translate**
- All nav, headings, body copy, buttons, footer, and form labels.
- Meta: `<title>`, `<meta name="description">`, and OG/Twitter tags per page in English.
- Image `alt` text in English on EN pages.

**What stays the same**
- Asset paths: EN pages can use `../assets/...` (from `/en/`) so images are shared.
- Structure: same number of pages and same URL shape under `/en/`.

**Optional later**
- Language switcher in header/footer (links to `/en/...` or `/` for current page).
- `Accept-Language` redirect from `/` to `/en/` is optional and can be skipped initially to keep the site static.

---

## 4. SEO implementation (main focus)

**4.1 Per-page meta (PL and EN)**
- **Title:** Unique per page, descriptive (e.g. “Druk 3D na zamówienie | o7AM” / “Custom 3D Printing | o7AM”). Keep brand at end; length ~50–60 chars.
- **Description:** Unique per page, 1–2 sentences, ~150–160 chars; include main keyword and value proposition.
- **og:url:** Exact canonical URL of that page (e.g. `https://o7.am/services/3d.html`, `https://o7.am/en/services/3d.html`).
- **og:title / og:description / twitter:*:** Match the page’s title and description for that locale.

**4.2 Canonical and hreflang**
- Each page: `<link rel="canonical" href="https://o7.am/...">` (or `https://o7.am/en/...` for EN).
- Each page: two `<link rel="alternate" hreflang="pl" href="...">` and `hreflang="en" href="...">` (and optionally `x-default` to PL or EN).

**4.3 Sitemap and robots**
- **sitemap.xml:** List all important URLs (PL and EN). Use absolute URLs; can be hand-written or generated once; update when adding pages.
- **robots.txt:** Allow crawlers; reference `Sitemap: https://o7.am/sitemap.xml`.

**4.4 Share and default image**
- Choose one default share image (e.g. logo or key visual); fix the typo in favicon comment (`char5et` → `charset`) if you enable it.
- Uncomment and set `og:image` and `twitter:image` to an absolute URL (e.g. `https://o7.am/assets/o7am/logo_wide.jpg` or a dedicated 1200×630 image). Use same or page-specific image per section if needed.

**4.5 Content and structure**
- One clear `<h1>` per page that matches the page purpose.
- Sensible heading hierarchy (h2, h3) and internal links to services/portfolio/contact so crawlers and users see structure.

---

## 5. Performance (targeted fixes)

SEO-first means fixing what directly hurts usability and Core Web Vitals; no big redesign.

**Must-fix**
- Fix broken references: point index CTA to `assets/o7am/logo_wide.jpg` (or remove wrong inline style); fix or remove `entry2.webp` reference on portfolio.
- Ensure above-the-fold images are not unnecessarily huge (e.g. compress or resize slider images, logo, and repeated CTA background).

**Should-do**
- Compress large JPGs/PNG (e.g. logo_wide, logo_tall, clancy, slider, portfolio covers) to modern quality/size; consider WebP versions and `<picture>` or `srcset` for key images if you want smaller payloads without changing design.
- Prefer single shared CSS/JS; avoid duplicate or blocking resources.

**Defer**
- Full image CDN, responsive image matrix, or build-step optimization can be a later phase once SEO and i18n are live.

---

## 6. Phasing and order of work

1. **Validation**  
   Run the audit (Section 2), write the audit report, and fix the two known broken asset references so the site is consistent.

2. **SEO baseline (Polish)**  
   Implement per-page meta, canonical, sitemap, robots.txt, and one default og:image/twitter:image. No new content structure yet.

3. **English translation**  
   Add `/en/` tree with translated content and meta; add hreflang (and optional language switcher). Update sitemap to include EN URLs.

4. **Performance pass**  
   Compress and optionally convert key images; fix any remaining asset paths. Re-check LCP/CLS on a few pages.

5. **Optional**  
   Favicon, language switcher polish, or further image/UX tweaks.

---

## Summary

| Area           | Action                                                                 |
|----------------|------------------------------------------------------------------------|
| **Validation** | Audit SEO, i18n, broken refs, image sizes; produce short report.      |
| **SEO**        | Unique meta per page (PL+EN), canonical, hreflang, sitemap, robots, share image. |
| **i18n**       | English under `/en/` with full translation of content and meta.       |
| **Performance**| Fix broken assets; compress key images; consider WebP for heaviest.    |

Next step: run the validation audit, then implement Phase 1 (fix broken refs) and Phase 2 (SEO baseline for Polish). After that, add the EN tree and hreflang, then do the performance pass.
