# o7am.github.io – build and preview
# Usage: just build   (with venv activated, or uv will use project env)

default: build

# Build static site into out/ using uv
build:
    uv run python build.py

# Preview built site locally (serve out/ on port 8000)
serve:
    uv run python -m http.server 8000 --directory out
