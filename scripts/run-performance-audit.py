#!/usr/bin/env python3
"""
Run Lighthouse performance audits against the live o7.am site and write a summary report.

Uses multiple runs and median-run selection so results are stable and programmatically
confirmable (single runs can vary a lot; contact going 100→68 is normal variance).

Requires: Node/npx and Chrome/Chromium (for Lighthouse).
Usage: from repo root, run:  uv run python scripts/run-performance-audit.py
       or:  just perf
       Optional: PERF_RUNS=5 just perf   (default 3)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "docs"
# Use www so Lighthouse doesn't count the o7.am → www redirect (~1s penalty)
LIVE_BASE = "https://www.o7.am"

# Pages to audit: (label, path)
PAGES = [
    ("Homepage", ""),
    ("Contact (with map)", "/contact.html"),
]

# Default number of runs per URL; median run is then selected for reporting
DEFAULT_RUNS = 3


def _get_fcp_ms(lhr: dict) -> float | None:
    a = (lhr.get("audits") or {}).get("first-contentful-paint")
    return a.get("numericValue") if a and "numericValue" in a else None


def _get_interactive_ms(lhr: dict) -> float | None:
    a = (lhr.get("audits") or {}).get("interactive")
    return a.get("numericValue") if a and "numericValue" in a else None


def _pick_median_run(lhrs: list[dict]) -> dict:
    """Pick the run whose (FCP, TTI) is closest to the median (FCP, TTI). Keeps one consistent LHR."""
    if not lhrs:
        raise ValueError("empty lhrs")
    if len(lhrs) == 1:
        return lhrs[0]
    fcps = []
    ttis = []
    for lhr in lhrs:
        f = _get_fcp_ms(lhr)
        i = _get_interactive_ms(lhr)
        if f is not None:
            fcps.append(f)
        if i is not None:
            ttis.append(i)
    median_fcp = _median(fcps) if fcps else None
    median_tti = _median(ttis) if ttis else None
    if median_fcp is None and median_tti is None:
        return lhrs[0]
    best = None
    best_dist = math.inf
    for lhr in lhrs:
        f = _get_fcp_ms(lhr) or median_fcp or 0
        i = _get_interactive_ms(lhr) or median_tti or 0
        m_f = median_fcp if median_fcp is not None else f
        m_i = median_tti if median_tti is not None else i
        # Normalize so FCP and TTI contribute similarly (scale by median to avoid one dominating)
        scale_f = m_f if m_f > 0 else 1
        scale_i = m_i if m_i > 0 else 1
        dist = ((f - m_f) / scale_f) ** 2 + ((i - m_i) / scale_i) ** 2
        if dist < best_dist:
            best_dist = dist
            best = lhr
    return best or lhrs[0]


def _median(vals: list[float]) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def run_lighthouse(url: str, out_path: Path) -> dict | None:
    """Run Lighthouse once against url; save JSON to out_path. Returns parsed JSON or None on failure."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "npx",
        "--yes",
        "lighthouse",
        url,
        "--output=json",
        "--output-path=" + str(out_path),
        "--chrome-flags=--headless=new --no-sandbox",
        "--only-categories=performance",
        "--quiet",
    ]
    try:
        subprocess.run(cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=120)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Lighthouse failed for {url}: {e}", file=sys.stderr)
        return None
    if not out_path.exists():
        return None
    with open(out_path, encoding="utf-8") as f:
        return json.load(f)


def extract_metrics(lhr: dict) -> dict:
    """Extract performance score and core metrics from Lighthouse result."""
    out = {}
    cats = lhr.get("categories") or {}
    perf = cats.get("performance") or {}
    out["score"] = perf.get("score")
    if out["score"] is not None:
        out["score"] = round(out["score"] * 100)

    audits = lhr.get("audits") or {}
    # LCP (ms)
    lcp = audits.get("largest-contentful-paint")
    if lcp and "numericValue" in lcp:
        out["LCP_ms"] = round(lcp["numericValue"])
    # CLS
    cls = audits.get("cumulative-layout-shift")
    if cls and "numericValue" in cls:
        out["CLS"] = round(cls["numericValue"], 3)
    # TBT (ms)
    tbt = audits.get("total-blocking-time")
    if tbt and "numericValue" in tbt:
        out["TBT_ms"] = round(tbt["numericValue"])
    # INP (ms) or FID
    inp = audits.get("interaction-to-next-paint") or audits.get("first-input-delay")
    if inp and "numericValue" in inp:
        out["INP_ms"] = round(inp["numericValue"])
    # FCP (ms)
    fcp = audits.get("first-contentful-paint")
    if fcp and "numericValue" in fcp:
        out["FCP_ms"] = round(fcp["numericValue"])
    return out


def write_report(
    results: list[tuple[str, str, dict | None]],
    report_path: Path,
    *,
    num_runs: int,
    method_note: str,
) -> None:
    """Write docs/performance-report.md from list of (label, url, metrics)."""
    lines = [
        "# Performance audit — o7.am",
        "",
        "Generated by `scripts/run-performance-audit.py` (run with `just perf`).",
        "Requires Chrome/Chromium and Node/npx.",
        "",
        "## How results are computed",
        "",
        method_note,
        "",
        "## Live site",
        "",
        f"**Base URL:** {LIVE_BASE}",
        "**Tool:** Lighthouse (CLI), performance category only.",
        "*(Audit uses www so the o7.am→www redirect is not counted.)*",
        "",
        "## Results",
        "",
    ]
    for label, url, metrics in results:
        lines.append(f"### {label}")
        lines.append("")
        lines.append(f"- **URL:** {url}")
        if metrics:
            score = metrics.get("score")
            lines.append(f"- **Performance score:** {score}/100" if score is not None else "- **Performance score:** —")
            if metrics.get("LCP_ms") is not None:
                lines.append(f"- **LCP:** {metrics['LCP_ms']} ms")
            if metrics.get("CLS") is not None:
                lines.append(f"- **CLS:** {metrics['CLS']}")
            if metrics.get("TBT_ms") is not None:
                lines.append(f"- **TBT:** {metrics['TBT_ms']} ms")
            if metrics.get("INP_ms") is not None:
                lines.append(f"- **INP:** {metrics['INP_ms']} ms")
            if metrics.get("FCP_ms") is not None:
                lines.append(f"- **FCP:** {metrics['FCP_ms']} ms")
        else:
            lines.append("- *Audit failed or not run.*")
        lines.append("")
    lines.extend([
        "## Improvement ideas",
        "",
        "1. **LCP:** Preload key hero image or font if they block LCP; ensure images have width/height to avoid CLS.",
        "2. **CLS:** Reserve space for map iframe and any dynamic content; avoid inserting content above existing content.",
        "3. **TBT:** Defer or reduce non-critical JS; keep theme script minimal so it doesn't block main thread.",
        "",
        "## Next quick wins",
        "",
        "See **[performance-correction-plan.md](performance-correction-plan.md)** § 7 and **[performance-report-concise.md](performance-report-concise.md)**.",
        "",
        "---",
        "",
        "*Re-run `just perf` to refresh this report.*",
    ])
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Lighthouse performance audit (median of N runs).")
    parser.add_argument(
        "--runs",
        type=int,
        default=int(os.environ.get("PERF_RUNS", DEFAULT_RUNS)),
        help="Number of Lighthouse runs per URL; median run is used (default: 3, or PERF_RUNS env)",
    )
    parser.add_argument(
        "--single",
        action="store_true",
        help="Single run per URL (no median); faster but higher variance",
    )
    args = parser.parse_args()
    num_runs = 1 if args.single else max(1, args.runs)

    if num_runs == 1:
        method_note = (
            "Single run per URL. For more stable results, run without `--single` (default: median of 3 runs)."
        )
    else:
        method_note = (
            f"**Median run of {num_runs} runs.** For each URL we run Lighthouse {num_runs} times, "
            "then pick the run whose First Contentful Paint and Time to Interactive are closest to "
            "the medians. That run's metrics are reported. This reduces variance (single runs can swing "
            "e.g. contact 100→68); the result is programmatically confirmable."
        )

    results = []
    for label, path in PAGES:
        url = LIVE_BASE.rstrip("/") + ("/" + path.lstrip("/") if path else "/")
        slug = "home" if not path else path.replace("/", "-").strip("-").removesuffix(".html")
        json_path = OUT_DIR / f"lighthouse-{slug}.json"

        if num_runs == 1:
            print(f"Auditing {label} ({url}) ...")
            lhr = run_lighthouse(url, json_path)
            if lhr is not None:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(lhr, f, indent=2, ensure_ascii=False)
            metrics = extract_metrics(lhr) if lhr else None
            results.append((label, url, metrics))
            if metrics:
                print(f"  Score: {metrics.get('score', '—')}/100")
            continue

        # Multiple runs: collect LHRs, pick median run, save it and its metrics
        runs: list[dict] = []
        for r in range(num_runs):
            print(f"Auditing {label} ({url}) run {r + 1}/{num_runs} ...")
            with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
                tmp_path = Path(tmp.name)
            try:
                lhr = run_lighthouse(url, tmp_path)
                if lhr is not None:
                    runs.append(lhr)
            finally:
                tmp_path.unlink(missing_ok=True)
        if not runs:
            results.append((label, url, None))
            print(f"  All {num_runs} runs failed.", file=sys.stderr)
            continue
        median_lhr = _pick_median_run(runs)
        json_path.write_text(json.dumps(median_lhr, indent=2, ensure_ascii=False), encoding="utf-8")
        metrics = extract_metrics(median_lhr)
        results.append((label, url, metrics))
        print(f"  Median run score: {metrics.get('score', '—')}/100 (of {len(runs)} runs)")

    report_path = OUT_DIR / "performance-report.md"
    write_report(results, report_path, num_runs=num_runs, method_note=method_note)
    print(f"Report written to {report_path}")
    return 0 if any(r[2] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
