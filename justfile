# o7am.github.io – build and preview
# Usage: just build   (with venv activated, or uv will use project env)

default: build

# Build static site into out/ using uv
build:
    uv run python build.py

# Preview built site locally (serve out/ on port 8000)
serve:
    uv run python -m http.server 8000 --directory out

# Compare PL vs EN content in data/*.yaml (missing EN keys, EN identical to PL)
sync-en:
    uv run python scripts/sync-en-from-pl.py

# Run Lighthouse performance audit against live https://o7.am (requires Chrome and Node/npx)
perf:
    uv run python scripts/run-performance-audit.py
