#!/usr/bin/env python3
"""
Static site generator for o7am.github.io.
Reads data from data/*.yaml, renders Jinja templates, writes to out/, copies static assets.
"""
from pathlib import Path
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

SITE_URL = "https://o7.am"
OUT_DIR = Path("out")
DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")
STATIC_FILES = ["style.css", "app.js", "theme.js", "CNAME", "robots.txt", "sitemap.xml", "llms.txt"]
STATIC_DIRS = ["assets"]


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
        pages.append((f"{prefix}services/it.html", "service_it.html", {"title": t["services"]["it_title"], "description": t["services"].get("it_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/it.html"}))
        pages.append((f"{prefix}services/3d.html", "service_3d.html", {"title": t["services"]["3d_title"], "description": t["services"].get("3d_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/3d.html"}))
        pages.append((f"{prefix}services/de.html", "service_de.html", {"title": t["services"]["de_title"], "description": t["services"].get("de_description", t["meta"]["services_description"]), "canonical_path": f"{prefix}services/de.html"}))

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

    for rel_path, template_name, ctx in pages:
        base = locale_base_prefix(rel_path)
        root = root_prefix(rel_path)
        locale = "en" if rel_path.startswith("en/") else "pl"
        pl_path = rel_path[3:] if rel_path.startswith("en/") else rel_path
        en_path = "en/" + rel_path if not rel_path.startswith("en/") else rel_path
        other_lang_href = f"en/{rel_path}" if locale == "pl" else f"../{rel_path[3:]}"
        full_ctx = {
            "base": base,
            "root": root,
            "locale": locale,
            "t": data["i18n"][locale],
            "site_url": SITE_URL,
            "canonical_url": f"{SITE_URL}/{rel_path}",
            "alternate_pl": f"{SITE_URL}/{pl_path}",
            "alternate_en": f"{SITE_URL}/{en_path}",
            "alternate_x": f"{SITE_URL}/{pl_path}",
            "other_lang_href": other_lang_href,
            **ctx,
        }
        template = env.get_template(template_name)
        html = template.render(**full_ctx)
        out_file = out / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(html, encoding="utf-8")

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
