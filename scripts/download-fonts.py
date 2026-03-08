#!/usr/bin/env python3
"""
Download Fira Sans and Oswald woff2 fonts into assets/fonts/ so the site can serve
them from its own domain (no Cyberfolks or Mozilla CDN).

Sources:
- Fira Sans: Mozilla Fira repo (https://github.com/mozilla/Fira)
- Oswald: Google Fonts (we fetch the CSS and extract woff2 URLs)

Run from repo root:  uv run python scripts/download-fonts.py
"""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_DIR = REPO_ROOT / "assets" / "fonts"
MOZILLA_RAW = "https://raw.githubusercontent.com/mozilla/Fira/master/woff2"

# style.css uses these Fira Sans names; Mozilla uses Heavy for 900 and Hair for 100
FIRA_FILES = [
    ("FiraSans-Black.woff2", "FiraSans-Heavy.woff2"),      # 900
    ("FiraSans-BlackItalic.woff2", "FiraSans-HeavyItalic.woff2"),
    ("FiraSans-Bold.woff2", "FiraSans-Bold.woff2"),
    ("FiraSans-BoldItalic.woff2", "FiraSans-BoldItalic.woff2"),
    ("FiraSans-ExtraBold.woff2", "FiraSans-ExtraBold.woff2"),
    ("FiraSans-ExtraBoldItalic.woff2", "FiraSans-ExtraBoldItalic.woff2"),
    ("FiraSans-ExtraLight.woff2", "FiraSans-ExtraLight.woff2"),
    ("FiraSans-ExtraLightItalic.woff2", "FiraSans-ExtraLightItalic.woff2"),
    ("FiraSans-Italic.woff2", "FiraSans-Italic.woff2"),
    ("FiraSans-Light.woff2", "FiraSans-Light.woff2"),
    ("FiraSans-LightItalic.woff2", "FiraSans-LightItalic.woff2"),
    ("FiraSans-Medium.woff2", "FiraSans-Medium.woff2"),
    ("FiraSans-MediumItalic.woff2", "FiraSans-MediumItalic.woff2"),
    ("FiraSans-Regular.woff2", "FiraSans-Regular.woff2"),
    ("FiraSans-SemiBold.woff2", "FiraSans-SemiBold.woff2"),
    ("FiraSans-SemiBoldItalic.woff2", "FiraSans-SemiBoldItalic.woff2"),
    ("FiraSans-Thin.woff2", "FiraSans-Hair.woff2"),        # 100
    ("FiraSans-ThinItalic.woff2", "FiraSans-HairItalic.woff2"),
]

OSWALD_WEIGHT_TO_FILE = {
    200: "Oswald-ExtraLight.woff2",
    300: "Oswald-Light.woff2",
    400: "Oswald-Regular.woff2",
    500: "Oswald-Medium.woff2",
    600: "Oswald-SemiBold.woff2",
    700: "Oswald-Bold.woff2",
}


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; o7am-font-fetch)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        dest.write_bytes(resp.read())


def main() -> int:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading Fira Sans from Mozilla Fira repo...")
    for local_name, remote_name in FIRA_FILES:
        url = f"{MOZILLA_RAW}/{remote_name}"
        dest = FONTS_DIR / local_name
        try:
            download(url, dest)
            print(f"  {local_name}")
        except Exception as e:
            print(f"  FAILED {local_name}: {e}")
            return 1

    print("Downloading Oswald from Google Fonts...")
    # Request CSS with User-Agent that gets woff2
    css_url = "https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap"
    req = urllib.request.Request(
        css_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        css = resp.read().decode()
    # Parse each @font-face block for font-weight and url
    for block in re.finditer(r"@font-face\s*\{([^}]+)\}", css):
        inner = block.group(1)
        w_match = re.search(r"font-weight:\s*(\d+)", inner)
        u_match = re.search(r"url\((https://[^)]+\.woff2)\)", inner)
        if w_match and u_match:
            weight, url = int(w_match.group(1)), u_match.group(1)
            if weight in OSWALD_WEIGHT_TO_FILE:
                dest = FONTS_DIR / OSWALD_WEIGHT_TO_FILE[weight]
                try:
                    download(url, dest)
                    print(f"  {dest.name}")
                except Exception as e:
                    print(f"  FAILED {dest.name}: {e}")

    print(f"Done. Fonts in {FONTS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
