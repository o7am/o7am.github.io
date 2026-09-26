#!/usr/bin/env python3
"""
Static site generator for o7am.github.io.
Reads data from data/*.yaml, renders Jinja templates, writes to out/, copies static assets.
"""
from pathlib import Path
from datetime import date
from functools import lru_cache
import shutil
import subprocess
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

SITE_URL = "https://o7.am"
SITE_NAME = "o7AM"
BUSINESS_ID = f"{SITE_URL}/#business"
OUT_DIR = Path("out")
DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")
STATIC_FILES = ["style.css", "app.js", "theme.js", "CNAME", "robots.txt", "llms.txt"]
STATIC_DIRS = ["assets"]

# Extra content sources (beyond the page's own template) that affect a page's lastmod.
TEMPLATE_EXTRA_SOURCES = {
    "blog.html": [DATA_DIR / "blogs.yaml"],
    "blog_post.html": [DATA_DIR / "blogs.yaml"],
    "portfolio.html": [DATA_DIR / "portfolios.yaml"],
    "portfolio_item.html": [DATA_DIR / "portfolios.yaml"],
    "portfolio_emoji.html": [DATA_DIR / "portfolios.yaml"],
}

LOCAL_BUSINESS_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": BUSINESS_ID,
    "name": SITE_NAME,
    "url": f"{SITE_URL}/",
    "image": f"{SITE_URL}/assets/o7am/logo_wide.jpg",
    "telephone": "+48579057915",
    "email": "contact@o7.am",
    "vatID": "PL7822478211",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Dojazdowa",
        "addressLocality": "Radzyny",
        "postalCode": "64-530",
        "addressCountry": "PL",
    },
    "sameAs": [
        "https://www.instagram.com/__o7am__",
        "https://www.linkedin.com/company/o7-am",
        "https://ko-fi.com/o7am_",
    ],
}


@lru_cache(maxsize=None)
def git_last_modified(paths):
    """Last-modified date (YYYY-MM-DD) of the given source file(s), from git history.
    Falls back to today if git is unavailable or the files are untracked."""
    existing = [str(p) for p in paths if Path(p).exists()]
    if not existing:
        return date.today().isoformat()
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", *existing],
            capture_output=True, text=True, check=True, cwd=Path(__file__).resolve().parent,
        )
        return result.stdout.strip() or date.today().isoformat()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return date.today().isoformat()


def build_sitemap(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def load_yaml(name):
    path = DATA_DIR / f"{name}.yaml"
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def locale_base_prefix(rel_path):
    """Path from output file's directory to locale root (for same-locale page links)."""
    path = Path(rel_path)
    parent_parts = path.parent.parts
    if rel_path.startswith("en/"):
        depth = len(parent_parts) - 1
        return "../" * depth if depth > 0 else ""
    depth = len(parent_parts)
    return "../" * depth if depth else ""


def root_prefix(rel_path):
    """Path to site root for static assets (CSS, JS, assets/). Use root-relative so EN and all subpaths load the same assets."""
    return "/"


def main():
    out = OUT_DIR
    out.mkdir(exist_ok=True)

    data = {
        "i18n": load_yaml("i18n"),
        "blogs": load_yaml("blogs"),
        "portfolios": load_yaml("portfolios"),
    }

    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "xml"]),
    )

    locales = ["pl", "en"]
    # Output paths relative to out/ (without leading slash)
    pages = []

    for loc in locales:
        prefix = "" if loc == "pl" else "en/"
        t = data["i18n"][loc]

        # Index (preload LCP image for performance)
        pages.append((f"{prefix}index.html", "index.html", {"title": t["meta"]["home_title"], "description": t["meta"]["home_description"], "canonical_path": f"{prefix.rstrip('/') or ''}", "body_class": "front-page", "preload_lcp": True}))
        # Blog list
        pages.append((f"{prefix}blog.html", "blog.html", {"title": t["meta"]["blog_title"], "description": t["meta"]["blog_description"], "canonical_path": f"{prefix}blog.html", "blogs": data["blogs"]}))
        # Portfolio list
        pages.append((f"{prefix}portfolio.html", "portfolio.html", {"title": t["meta"]["portfolio_title"], "description": t["meta"]["portfolio_description"], "canonical_path": f"{prefix}portfolio.html", "portfolios": data["portfolios"]}))
        # Services
        pages.append((f"{prefix}services.html", "services.html", {"title": t["meta"]["services_title"], "description": t["meta"]["services_description"], "canonical_path": f"{prefix}services.html"}))
        # Contact
        pages.append((f"{prefix}contact.html", "contact.html", {"title": t["meta"]["contact_title"], "description": t["meta"]["contact_description"], "canonical_path": f"{prefix}contact.html"}))

        # Service subpages
        pages.append((f"{prefix}services/it.html", "service_it.html", {"title": t["services"]["it_title"], "description": t["services"].get("it_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/it.html", "service_key": "it"}))
        pages.append((f"{prefix}services/3d.html", "service_3d.html", {"title": t["services"]["3d_title"], "description": t["services"].get("3d_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/3d.html", "service_key": "3d"}))
        pages.append((f"{prefix}services/de.html", "service_de.html", {"title": t["services"]["de_title"], "description": t["services"].get("de_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/de.html", "service_key": "de"}))

        # Blog posts
        for b in data["blogs"]:
            slug = b["slug"]
            title = b["title"][loc]
            desc = b.get("description", {}).get(loc, data["i18n"][loc]["meta"]["blog_description"])
            pages.append((f"{prefix}blogs/{slug}.html", "blog_post.html", {"blog": b, "title": title, "description": desc, "canonical_path": f"{prefix}blogs/{slug}.html"}))

        # Portfolio items
        for p in data["portfolios"]:
            slug = p["slug"]
            title = p["title"][loc]
            desc = p.get("description", {}).get(loc, data["i18n"][loc]["meta"]["portfolio_description"])
            template_name = "portfolio_emoji.html" if slug == "emoji" else "portfolio_item.html"
            pages.append((f"{prefix}portfolios/{slug}.html", template_name, {"item": p, "title": title, "description": desc, "canonical_path": f"{prefix}portfolios/{slug}.html"}))

    sitemap_entries = []

    for rel_path, template_name, ctx in pages:
        base = locale_base_prefix(rel_path)
        root = root_prefix(rel_path)
        locale = "en" if rel_path.startswith("en/") else "pl"
        pl_path = rel_path[3:] if rel_path.startswith("en/") else rel_path
        en_path = "en/" + rel_path if not rel_path.startswith("en/") else rel_path
        other_lang_href = f"en/{rel_path}" if locale == "pl" else f"../{rel_path[3:]}"
        canonical_url = f"{SITE_URL}/{rel_path}"
        t = data["i18n"][locale]
        full_ctx = {
            "base": base,
            "root": root,
            "locale": locale,
            "t": t,
            "site_url": SITE_URL,
            "canonical_url": canonical_url,
            "alternate_pl": f"{SITE_URL}/{pl_path}",
            "alternate_en": f"{SITE_URL}/{en_path}",
            "alternate_x": f"{SITE_URL}/{pl_path}",
            "other_lang_href": other_lang_href,
            "local_business_schema": LOCAL_BUSINESS_SCHEMA,
            **ctx,
        }

        if "service_key" in ctx:
            key = ctx["service_key"]
            full_ctx["service_schema"] = {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": t["services"][f"{key}_short"],
                "serviceType": t["services"][f"{key}_short"],
                "description": t["services"].get(f"{key}_body", t["services"][f"{key}_cta"]),
                "provider": {"@id": BUSINESS_ID},
                "areaServed": "PL",
                "url": canonical_url,
                "inLanguage": locale,
            }

        if "blog" in ctx:
            b = ctx["blog"]
            full_ctx["blogposting_schema"] = {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": b["title"][locale],
                "description": ctx["description"],
                "image": f"{SITE_URL}/{b['image']}",
                "url": canonical_url,
                "mainEntityOfPage": canonical_url,
                "inLanguage": locale,
                **({"datePublished": b["date_iso"]} if b.get("date_iso") else {}),
                "author": {"@type": "Organization", "@id": BUSINESS_ID, "name": SITE_NAME},
                "publisher": {
                    "@type": "Organization",
                    "@id": BUSINESS_ID,
                    "name": SITE_NAME,
                    "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/o7am/logo_wide.jpg"},
                },
                "dateModified": git_last_modified(tuple(TEMPLATE_EXTRA_SOURCES["blog_post.html"])),
            }

        template = env.get_template(template_name)
        html = template.render(**full_ctx)
        out_file = out / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")

        sources = (TEMPLATES_DIR / template_name, *TEMPLATE_EXTRA_SOURCES.get(template_name, []))
        sitemap_entries.append((canonical_url, git_last_modified(sources)))

    (out / "sitemap.xml").write_text(build_sitemap(sitemap_entries), encoding="utf-8")

    # Copy static files and dirs from repo root into out
    root = Path(".")
    for name in STATIC_FILES:
        src = root / name
        if src.exists():
            shutil.copy2(src, out / name)
    for name in STATIC_DIRS:
        src = root / name
        if src.is_dir():
            dest = out / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)

    # Redirect /en.html to EN homepage (GitHub Pages doesn't serve /en as directory index)
    (out / "en.html").write_text(
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<meta http-equiv="refresh" content="0;url=en/index.html">'
        '<script>location.href="en/index.html";</script>'
        '<title>Redirect to English</title></head>'
        '<body><p><a href="en/index.html">English version</a></p></body></html>',
        encoding="utf-8",
    )

    print(f"Built {len(pages)} pages into {OUT_DIR}/")


if __name__ == "__main__":
    main()
