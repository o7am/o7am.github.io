#!/usr/bin/env python3
"""
Compare PL and EN content in data/*.yaml and report sync status.

- Lists keys present in PL but missing in EN (need EN translation).
- Flags EN values that are identical to PL (likely untranslated).
- Supports i18n.yaml (top-level pl/en), blogs.yaml and portfolios.yaml (per-item pl/en fields).

Usage:
  python scripts/sync-en-from-pl.py              # report to stdout
  python scripts/sync-en-from-pl.py --format json
  python scripts/sync-en-from-pl.py --suggest     # print suggested EN snippets (copy from PL) for manual translation

Run from repo root (parent of data/ and scripts/).
"""
from pathlib import Path
import argparse
import json
import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def flatten_keys(d, prefix=""):
    """Flatten nested dict to dotted keys. Values must be scalars (str, int, etc.)."""
    out = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and v and all(not isinstance(x, dict) for x in v.values()):
            for k2, v2 in v.items():
                out[f"{key}.{k2}"] = v2
        elif isinstance(v, dict) and v:
            out.update(flatten_keys(v, key))
        else:
            out[key] = v
    return out


def compare_i18n(pl, en):
    """Compare pl vs en top-level locale dicts. Return missing keys in en, and keys where en == pl."""
    pflat = flatten_keys(pl)
    eflat = flatten_keys(en)
    pl_keys = set(pflat)
    en_keys = set(eflat)
    missing_in_en = sorted(pl_keys - en_keys)
    identical = sorted(k for k in (pl_keys & en_keys) if pflat[k] == eflat[k] and pflat[k] != "")
    return {"missing_in_en": missing_in_en, "identical": identical, "pl_flat": pflat, "en_flat": eflat}


def compare_locale_dict(item, locale_keys=("pl", "en")):
    """For a dict with pl/en subkeys (e.g. title: {pl: ..., en: ...}), return missing en and identical."""
    missing = []
    identical = []
    for key in item:
        val = item[key]
        if not isinstance(val, dict):
            continue
        if "pl" in val and "en" not in val:
            missing.append(f"{key}.en")
        elif "pl" in val and "en" in val:
            if val["pl"] == val["en"] and val["en"] not in ("", None):
                identical.append(key)
    return {"missing_in_en": missing, "identical": identical}


def load_yaml(name):
    path = DATA_DIR / f"{name}.yaml"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_i18n():
    data = load_yaml("i18n")
    if not data or "pl" not in data or "en" not in data:
        return {"file": "i18n.yaml", "error": "Missing pl or en top-level key"}
    out = compare_i18n(data["pl"], data["en"])
    out["file"] = "i18n.yaml"
    return out


def run_blogs():
    data = load_yaml("blogs")
    if not data:
        return {"file": "blogs.yaml", "items": [], "error": "File not found or empty"}
    results = []
    for i, item in enumerate(data):
        slug = item.get("slug", item.get("id", f"item_{i}"))
        cmp = compare_locale_dict(item)
        cmp["slug"] = slug
        results.append(cmp)
    return {"file": "blogs.yaml", "items": results}


def run_portfolios():
    data = load_yaml("portfolios")
    if not data:
        return {"file": "portfolios.yaml", "items": [], "error": "File not found or empty"}
    results = []
    for i, item in enumerate(data):
        slug = item.get("slug", item.get("id", f"item_{i}"))
        cmp = compare_locale_dict(item)
        cmp["slug"] = slug
        results.append(cmp)
    return {"file": "portfolios.yaml", "items": results}


def report_text(report):
    """Human-readable report."""
    lines = []
    # i18n
    if "missing_in_en" in report and report["missing_in_en"]:
        lines.append("i18n.yaml — keys in PL missing in EN:")
        for k in report["missing_in_en"]:
            lines.append(f"  - {k}")
    if "identical" in report and report["identical"]:
        lines.append("i18n.yaml — EN same as PL (likely untranslated):")
        for k in report["identical"]:
            lines.append(f"  - {k}")
    if lines:
        lines.append("")
    return "\n".join(lines)


def report_all_text(i18n_report, blogs_report, portfolios_report):
    parts = ["# PL/EN sync report\n"]
    # i18n
    parts.append("## data/i18n.yaml")
    if "error" in i18n_report:
        parts.append(f"  Error: {i18n_report['error']}\n")
    else:
        if i18n_report.get("missing_in_en"):
            parts.append("  **Keys in PL missing in EN:**")
            for k in i18n_report["missing_in_en"]:
                parts.append(f"  - `{k}`")
            parts.append("")
        if i18n_report.get("identical"):
            parts.append("  **EN identical to PL (review for translation):**")
            for k in i18n_report["identical"]:
                parts.append(f"  - `{k}`")
            parts.append("")
        if not i18n_report.get("missing_in_en") and not i18n_report.get("identical"):
            parts.append("  OK — structure in sync; no identical values flagged.\n")
    # blogs
    parts.append("## data/blogs.yaml")
    if "error" in blogs_report:
        parts.append(f"  {blogs_report['error']}\n")
    else:
        for item in blogs_report.get("items", []):
            m, i = item.get("missing_in_en", []), item.get("identical", [])
            if m or i:
                parts.append(f"  **{item['slug']}:**")
                if m:
                    parts.append("    Missing EN: " + ", ".join(m))
                if i:
                    parts.append("    Same as PL: " + ", ".join(i))
                parts.append("")
        if not any(item.get("missing_in_en") or item.get("identical") for item in blogs_report.get("items", [])):
            parts.append("  OK — all items have EN; no identical values flagged.\n")
    # portfolios
    parts.append("## data/portfolios.yaml")
    if "error" in portfolios_report:
        parts.append(f"  {portfolios_report['error']}\n")
    else:
        for item in portfolios_report.get("items", []):
            m, i = item.get("missing_in_en", []), item.get("identical", [])
            if m or i:
                parts.append(f"  **{item['slug']}:**")
                if m:
                    parts.append("    Missing EN: " + ", ".join(m))
                if i:
                    parts.append("    Same as PL: " + ", ".join(i))
                parts.append("")
        if not any(item.get("missing_in_en") or item.get("identical") for item in portfolios_report.get("items", [])):
            parts.append("  OK — all items have EN; no identical values flagged.\n")
    return "\n".join(parts)


def suggest_i18n(i18n_report):
    """Print suggested EN entries (copy from PL) for missing or identical keys."""
    if "error" in i18n_report or not i18n_report.get("pl_flat"):
        return
    need = set(i18n_report.get("missing_in_en", [])) | set(i18n_report.get("identical", []))
    if not need:
        return
    pl_flat = i18n_report["pl_flat"]
    print("# Suggested EN for i18n.yaml (copy from PL — translate manually)")
    print("# Keys: missing in EN or currently identical to PL\n")
    for k in sorted(need):
        val = pl_flat.get(k, "")
        if isinstance(val, str) and "\n" in val:
            print(f"# {k}:")
            print(f"# (multiline — add to en: section under correct nesting)")
            print()
        else:
            safe = val.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
            print(f"# {k}:")
            print(f'  "{safe}"')
            print()


def main():
    ap = argparse.ArgumentParser(description="Compare PL vs EN content in data/*.yaml")
    ap.add_argument("--format", choices=("text", "json"), default="text", help="Output format")
    ap.add_argument("--suggest", action="store_true", help="Print suggested EN snippets (copy from PL) for i18n")
    args = ap.parse_args()

    i18n_report = run_i18n()
    blogs_report = run_blogs()
    portfolios_report = run_portfolios()

    if args.format == "json":
        out = {"i18n": i18n_report, "blogs": blogs_report, "portfolios": portfolios_report}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print(report_all_text(i18n_report, blogs_report, portfolios_report))
    if args.suggest:
        suggest_i18n(i18n_report)


if __name__ == "__main__":
    main()
