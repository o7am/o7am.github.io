# Website Revamp (SEO + i18n) Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the o7.am revamp: validation audit, SEO baseline (unique meta, sitemap, robots, canonical, share image), English translation under `/en/` with hreflang, then targeted performance fixes.

**Architecture:** Static HTML; Polish remains at root (`/`, `/about.html`, …); English mirror under `/en/`. Shared assets; per-page meta and hreflang on every page. No build step; manual or one-off script for sitemap if needed.

**Tech Stack:** HTML, CSS, JS; GitHub Pages; no framework.

**Reference:** Design doc `docs/plans/2025-03-02-website-revamp-seo-i18n-design.md`.

---

## Phase 1: Validation and quick fixes

### Task 1: Create audit report

**Files:**
- Create: `docs/plans/audit-2025-03-02.md`

**Step 1: List all public HTML pages**

From repo root, list:
- `index.html`, `about.html`, `services.html`, `portfolio.html`, `blog.html`, `contact.html`
- `services/3d.html`, `services/de.html`
- `portfolios/3d_prints.html`, `portfolios/emoji.html`
- `blogs/blog1.html`

**Step 2: For each page, record in the audit file**

- Current `<title>` (from `<head>`)
- Current `<meta name="description" content="...">`
- Current `og:url` if present
- Whether og:image / twitter:image are present (currently commented site-wide)

Use this template in `docs/plans/audit-2025-03-02.md`:

```markdown
# Audit 2025-03-02

## Pages inventory
| Page | Title | Meta description | og:url |
|------|-------|------------------|--------|
| index.html | ... | ... | ... |
...
## Sitemap/robots
- sitemap.xml: missing
- robots.txt: missing
## Broken refs
- index.html: style uses assets/pics/logo2.jpg (file missing)
- portfolio.html: src assets/portfolios/entry2.webp (file missing)
## Image sizes (from ls -la or find)
- assets/o7am/logo_wide.jpg: ~1.8MB
...
```

**Step 3: Commit**

```bash
git add docs/plans/audit-2025-03-02.md
git commit -m "docs: add SEO/i18n audit report"
```

---

### Task 2: Fix broken asset reference on index (logo)

**Files:**
- Modify: `o7am.github.io/index.html` (line with `assets/pics/logo2.jpg`)

**Step 1: Locate the broken reference**

In `index.html`, find the CTA block that sets `style="background-image: url(&quot;assets/pics/logo2.jpg&quot;);"`. The `data-bg` correctly points to `assets/o7am/logo_wide.jpg`.

**Step 2: Replace with correct path**

Change the inline `url(...)` to use the same asset as `data-bg` so the visible background matches. Replace:

`url(&quot;assets/pics/logo2.jpg&quot;)` → `url(&quot;assets/o7am/logo_wide.jpg&quot;)`

So the full div looks like:

```html
<div class="cta-block__image lazy-background visible" data-bg="assets/o7am/logo_wide.jpg" style="background-image: url(&quot;assets/o7am/logo_wide.jpg&quot;);">
```

**Step 3: Verify**

Open `index.html` in a browser (or run a local server from repo root). The “Druk 3D na zamówienie” section should show the wide logo image, not a broken image.

**Step 4: Commit**

```bash
git add index.html
git commit -m "fix: use correct logo asset on index CTA"
```

---

### Task 3: Fix or remove broken entry2.webp reference on portfolio

**Files:**
- Modify: `o7am.github.io/portfolio.html` (line referencing `entry2.webp`)

**Step 1: Locate reference**

Grep for `entry2.webp` in `portfolio.html`. The file `assets/portfolios/entry2.webp` does not exist.

**Step 2: Decide fix**

Either (A) remove the portfolio item/card that uses `entry2.webp`, or (B) point it to an existing image (e.g. `assets/portfolios/1/entry1.jpg` or `cover.jpg`) and update alt text to match. Prefer (B) if the card is “Drukowanie prototypów…” or similar; otherwise (A).

**Step 3: Apply fix**

- If (A): Remove the entire block (e.g. the card/link) that contains `src=assets/portfolios/entry2.webp`.
- If (B): Replace `assets/portfolios/entry2.webp` with e.g. `assets/portfolios/1/entry1.jpg` and set appropriate `alt`.

**Step 4: Verify**

Open `portfolio.html`; no 404 in network tab for the portfolio image.

**Step 5: Commit**

```bash
git add portfolio.html
git commit -m "fix: remove or replace broken entry2.webp reference on portfolio"
```

---

## Phase 2: SEO baseline (Polish)

### Task 4: Add sitemap.xml

**Files:**
- Create: `o7am.github.io/sitemap.xml`

**Step 1: List canonical base URL**

Base: `https://o7.am/` (respect CNAME/www as you use in production).

**Step 2: Create sitemap with all Polish pages**

Create `sitemap.xml` with XML sitemap format. Include at least:

- https://o7.am/
- https://o7.am/about.html
- https://o7.am/services.html
- https://o7.am/services/3d.html
- https://o7.am/services/de.html
- https://o7.am/portfolio.html
- https://o7.am/portfolios/3d_prints.html
- https://o7.am/portfolios/emoji.html
- https://o7.am/blog.html
- https://o7.am/blogs/blog1.html
- https://o7.am/contact.html

Example single entry:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://o7.am/</loc>
    <changefreq>monthly</changefreq>
  </url>
  <!-- ... one <url> per page ... -->
</urlset>
```

**Step 3: Verify**

Open `https://o7.am/sitemap.xml` (or `file://.../sitemap.xml`) and confirm all URLs are valid and absolute.

**Step 4: Commit**

```bash
git add sitemap.xml
git commit -m "feat(seo): add sitemap.xml for Polish pages"
```

---

### Task 5: Add robots.txt

**Files:**
- Create: `o7am.github.io/robots.txt`

**Step 1: Create robots.txt**

Content:

```
User-agent: *
Allow: /

Sitemap: https://o7.am/sitemap.xml
```

**Step 2: Commit**

```bash
git add robots.txt
git commit -m "feat(seo): add robots.txt with sitemap reference"
```

---

### Task 6: Define unique titles and descriptions for each Polish page

**Files:**
- Modify: (none yet – prepare copy in a doc or in head of each file)

**Step 1: Write per-page title and description (PL)**

In a scratch file or the audit doc, define one line each:

- **index:** Title: `o7AM | Innowacje 3D, Data Engineering i ML dla biznesu` (or similar, ~50–60 chars). Description: 1–2 sentences, ~150–160 chars, include 3D, data, ML, Radzyń/Poland if relevant.
- **about:** Unique title (e.g. O nas | o7AM), unique description.
- **services:** Usługi | o7AM + description listing 3D and DE.
- **services/3d.html:** Druk 3D na zamówienie | o7AM + short description.
- **services/de.html:** Data Engineering | o7AM + short description.
- **portfolio:** Portfolio | o7AM + short description.
- **portfolios/3d_prints.html**, **portfolios/emoji.html:** Unique titles/descriptions.
- **blog:** Blog | o7AM + description.
- **blogs/blog1.html:** Title and description for that post.
- **contact:** Kontakt | o7AM + description.

**Step 2: Commit (optional)**

If you wrote these in `docs/plans/audit-2025-03-02.md` or a new `docs/copy-meta-pl.txt`, commit that file so the next tasks can paste from it.

---

### Task 7: Apply unique meta to index.html (Polish)

**Files:**
- Modify: `o7am.github.io/index.html` (head section)

**Step 1: Update title**

Replace current `<title>` with the chosen unique title for the homepage (e.g. `o7AM | Innowacje 3D, Data Engineering i ML dla biznesu`).

**Step 2: Update meta description**

Replace `<meta name="description" content="o7AM" />` with the chosen 150–160 char description for the homepage.

**Step 3: Update og:url**

Set `<meta property="og:url" content="https://o7.am/" />` (trailing slash or no trailing slash – match your canonical choice and keep consistent).

**Step 4: Update og:title and og:description**

Set `og:title` and `og:description` to the same values as `<title>` and `<meta name="description">`.

**Step 5: Update twitter:title and twitter:description**

Match the same title and description.

**Step 6: Commit**

```bash
git add index.html
git commit -m "feat(seo): unique title and meta description for index"
```

---

### Task 8: Apply unique meta to remaining Polish pages

**Files:**
- Modify: `about.html`, `services.html`, `services/3d.html`, `services/de.html`, `portfolio.html`, `portfolios/3d_prints.html`, `portfolios/emoji.html`, `blog.html`, `blogs/blog1.html`, `contact.html`

**Step 1: For each file**

In each file’s `<head>`:
- Set `<title>` to the chosen unique title for that page.
- Set `<meta name="description" content="...">` to the chosen unique description.
- Set `<meta property="og:url" content="https://o7.am/...">` to the exact URL of that page (e.g. `https://o7.am/about.html`, `https://o7.am/services/3d.html`).
- Set `og:title`, `og:description`, `twitter:title`, `twitter:description` to match.

Use relative path from root for subpages: e.g. for `services/3d.html`, og:url is `https://o7.am/services/3d.html`.

**Step 2: Verify**

Spot-check 2–3 pages: view source and confirm title and description differ per page.

**Step 3: Commit**

One commit per page or one batch commit, e.g.:

```bash
git add about.html services.html services/3d.html services/de.html portfolio.html portfolios/3d_prints.html portfolios/emoji.html blog.html blogs/blog1.html contact.html
git commit -m "feat(seo): unique title and meta for all Polish pages"
```

---

### Task 9: Enable default og:image and twitter:image

**Files:**
- Modify: All HTML files that currently have og:image/twitter:image commented out.

**Step 1: Choose default image**

Use one existing asset as default share image, e.g. `https://o7.am/assets/o7am/logo_wide.jpg`. Ensure it exists and is reasonable for social preview (e.g. 1200×630 or similar aspect).

**Step 2: Uncomment and set in one template file first**

In `index.html`, uncomment the two lines and set absolute URLs:

```html
<meta property="og:image" content="https://o7.am/assets/o7am/logo_wide.jpg" />
<meta name="twitter:image" content="https://o7.am/assets/o7am/logo_wide.jpg" />
```

**Step 3: Replicate to all other Polish pages**

Add the same two lines (with the same default image) to every other HTML file. For subpages, use the same absolute URL (https://o7.am/...), not relative.

**Step 4: Commit**

```bash
git add *.html services/*.html portfolios/*.html blogs/*.html
git commit -m "feat(seo): add default og:image and twitter:image site-wide"
```

---

### Task 10: Add canonical link to each Polish page

**Files:**
- Modify: All HTML files (same list as Task 8).

**Step 1: Add canonical in head**

In each page’s `<head>`, add:

```html
<link rel="canonical" href="https://o7.am/PAGE_PATH" />
```

Replace `PAGE_PATH` with the path for that page (e.g. empty for index, `about.html`, `services/3d.html`, etc.). Use the same URL style as og:url (with or without trailing slash consistently).

**Step 2: Commit**

```bash
git add *.html services/*.html portfolios/*.html blogs/*.html
git commit -m "feat(seo): add canonical URL to all Polish pages"
```

---

## Phase 3: English translation and hreflang

### Task 11: Create /en/ directory and copy Polish structure

**Files:**
- Create: `o7am.github.io/en/index.html` (copy from `index.html`), and equivalent for every other page under `en/` mirroring the path (e.g. `en/about.html`, `en/services/3d.html`, …).

**Step 1: Create directory**

```bash
mkdir -p o7am.github.io/en/services o7am.github.io/en/portfolios o7am.github.io/en/blogs
```

**Step 2: Copy each HTML file**

Copy each Polish HTML into `en/` with the same relative path:
- `index.html` → `en/index.html`
- `about.html` → `en/about.html`
- `services.html` → `en/services.html`
- `services/3d.html` → `en/services/3d.html`
- `services/de.html` → `en/services/de.html`
- `portfolio.html` → `en/portfolio.html`
- `portfolios/3d_prints.html` → `en/portfolios/3d_prints.html`
- `portfolios/emoji.html` → `en/portfolios/emoji.html`
- `blog.html` → `en/blog.html`
- `blogs/blog1.html` → `en/blogs/blog1.html`
- `contact.html` → `en/contact.html`

**Step 3: Fix asset and link paths in EN files**

In each file under `en/`:
- CSS: change `href="style.css"` to `href="../style.css"` (or `../` as needed by depth). Subpages: `../style.css` for `en/*.html`, `../../style.css` for `en/services/*.html`, etc.
- JS: change `src="app.js"` to `src="../app.js"` (or appropriate `../` count).
- Images and data-bg: add `../` prefix so they point to repo root assets (e.g. `../assets/o7am/alice.png` from `en/index.html`, `../../assets/...` from `en/services/3d.html`).
- Internal links: point to EN versions under `/en/` (e.g. `href="about.html"` from `en/index.html`, `href="../about.html"` from `en/services/3d.html`; or use paths like `index.html`, `../index.html` so they stay inside `/en/`).

**Step 4: Commit**

```bash
git add en/
git commit -m "feat(i18n): add /en/ mirror structure with corrected asset paths"
```

---

### Task 12: Translate content and meta in en/index.html

**Files:**
- Modify: `o7am.github.io/en/index.html`

**Step 1: Update head (EN)**

- `<title>`: e.g. `o7AM | 3D, Data Engineering & ML for Your Business`
- `<meta name="description" content="...">`: English, 150–160 chars.
- `og:url`: `https://o7.am/en/`
- `og:title`, `og:description`, `twitter:*`: same as title/description.
- `og:image`, `twitter:image`: same default image URL (absolute).
- `<link rel="canonical" href="https://o7.am/en/">`

**Step 2: Translate body copy**

Replace Polish text with English: nav labels (e.g. “O nas” → “About”, “Usługi” → “Services”, “Portfolio”, “Blog”, “Contact”), headings, paragraphs, buttons, footer. Keep structure and links; only change visible text.

**Step 3: Translate alt text**

Replace `alt="Logo o7AM"` with `alt="o7AM logo"` (and any other img alt on the page).

**Step 4: Commit**

```bash
git add en/index.html
git commit -m "feat(i18n): translate index page to English"
```

---

### Task 13: Translate content and meta in remaining EN pages

**Files:**
- Modify: `en/about.html`, `en/services.html`, `en/services/3d.html`, `en/services/de.html`, `en/portfolio.html`, `en/portfolios/3d_prints.html`, `en/portfolios/emoji.html`, `en/blog.html`, `en/blogs/blog1.html`, `en/contact.html`

**Step 1: For each EN page**

- Set EN `<title>`, `<meta name="description">`, `og:url` (https://o7.am/en/...), `og:title`, `og:description`, `twitter:*`, canonical to `https://o7.am/en/...`.
- Translate all user-visible text (nav, headings, body, buttons, footer, form labels).
- Translate image `alt` attributes.

**Step 2: Commit in batches**

e.g.:

```bash
git add en/about.html en/contact.html en/services.html en/services/3d.html en/services/de.html
git commit -m "feat(i18n): translate about, contact, services to English"
git add en/portfolio.html en/portfolios/3d_prints.html en/portfolios/emoji.html en/blog.html en/blogs/blog1.html
git commit -m "feat(i18n): translate portfolio and blog pages to English"
```

---

### Task 14: Add hreflang to all Polish pages

**Files:**
- Modify: All Polish HTML files (root, services/, portfolios/, blogs/).

**Step 1: Add hreflang links in head**

In each Polish page, add (adjust path for subpages):

```html
<link rel="alternate" hreflang="pl" href="https://o7.am/CURRENT_PAGE_PATH" />
<link rel="alternate" hreflang="en" href="https://o7.am/en/CURRENT_PAGE_PATH" />
<link rel="alternate" hreflang="x-default" href="https://o7.am/CURRENT_PAGE_PATH" />
```

For index, `CURRENT_PAGE_PATH` is `` or `index.html` (match your canonical). For `about.html` it’s `about.html`; for `services/3d.html` it’s `services/3d.html`, etc. Use the same URL style as canonical.

**Step 2: Commit**

```bash
git add index.html about.html services.html contact.html portfolio.html blog.html services/*.html portfolios/*.html blogs/*.html
git commit -m "feat(seo): add hreflang (pl, en, x-default) to Polish pages"
```

---

### Task 15: Add hreflang to all English pages

**Files:**
- Modify: All EN HTML files under `en/`.

**Step 1: Add hreflang links in head**

Same as Task 14, but in each EN file the `pl` URL points to the root path and `en` points to the `/en/` path. Example for `en/about.html`:

```html
<link rel="alternate" hreflang="pl" href="https://o7.am/about.html" />
<link rel="alternate" hreflang="en" href="https://o7.am/en/about.html" />
<link rel="alternate" hreflang="x-default" href="https://o7.am/about.html" />
```

**Step 2: Commit**

```bash
git add en/*.html en/services/*.html en/portfolios/*.html en/blogs/*.html
git commit -m "feat(seo): add hreflang to English pages"
```

---

### Task 16: Update sitemap with English URLs

**Files:**
- Modify: `o7am.github.io/sitemap.xml`

**Step 1: Add EN URLs**

Append a `<url>` block for each English page (same paths as Polish but with `https://o7.am/en/...`).

**Step 2: Commit**

```bash
git add sitemap.xml
git commit -m "feat(seo): add English URLs to sitemap"
```

---

## Phase 4: Performance (targeted)

### Task 17: Compress or resize heaviest images

**Files:**
- Modify/replace: `assets/o7am/logo_wide.jpg`, `logo_tall.jpg`, `clancy.jpg`, `assets/index/slider/3d.jpg`, `assets/index/slider/de.jpg`, `assets/portfolios/1/cover.jpg`, `assets/portfolios/1/entry1.jpg`, `assets/services/3d/cover.jpg` (and optionally `alice.png`).

**Step 1: Resize/compress**

Use a tool of choice (e.g. ImageOptim, squoosh, `cwebp`, or script) to:
- Resize to max width/height actually used (e.g. 1200px or 1600px for hero images).
- Save JPG at 80–85 quality; optionally export WebP and keep JPG as fallback for now.

**Step 2: Replace originals or add WebP**

Either replace the existing files with smaller versions or add WebP versions and switch to `<picture>` in a follow-up task. At minimum, replace with compressed versions so file sizes drop (e.g. aim for &lt; 300–500 KB per hero image where possible).

**Step 3: Verify**

Reload key pages; confirm images still render and no broken refs.

**Step 4: Commit**

```bash
git add assets/
git commit -m "perf: compress and resize heavy images"
```

---

## Verification (after implementation)

- [ ] Every PL and EN page has unique title and description.
- [ ] `sitemap.xml` contains all PL and EN URLs; `robots.txt` references it.
- [ ] No broken image or asset links (index logo, portfolio entry2).
- [ ] Each page has canonical and hreflang; default og:image/twitter:image set.
- [ ] English content readable at `https://o7.am/en/...` (or your live base URL).
- [ ] Key images compressed; LCP improved on homepage and one service page (optional: measure with Lighthouse).
