#!/usr/bin/env python3
"""
Downloads all images referenced in _posts/*.md and writes them to
assets/img/posts/, then rewrites the markdown files to use local paths.

Usage: python download_images.py
"""

import os
import re
import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

POSTS_DIR   = "_posts"
ASSETS_DIR  = "assets/img/posts"
HEADERS     = {"User-Agent": "Mozilla/5.0 (compatible; blog-migrator/1.0)"}
IMG_PATTERN = re.compile(r'(!\[([^\]]*)\])\((https?://\S+?)\)(?!\()')


def local_filename(url, used: set) -> str:
    """Derive a filename from the URL, avoiding collisions in `used`."""
    path   = urlparse(url).path
    orig   = os.path.basename(path)
    # If the URL path has no useful extension, fall back to an MD5 name
    if not orig or "." not in orig:
        orig = hashlib.md5(url.encode()).hexdigest()[:12] + ".jpg"
    # Strip query strings baked into filenames (rare but possible)
    orig = re.sub(r"[?&=].*$", "", orig)

    stem, suffix = os.path.splitext(orig)
    candidate = orig
    counter = 2
    while candidate in used:
        candidate = f"{stem}_{counter}{suffix}"
        counter += 1
    return candidate


def download_image(url: str, dest: Path) -> bool:
    if dest.exists():
        return True
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as fh:
            for chunk in resp.iter_content(8192):
                fh.write(chunk)
        return True
    except Exception as exc:
        print(f"    FAIL  {url}: {exc}")
        return False


def main():
    posts_dir  = Path(POSTS_DIR)
    assets_dir = Path(ASSETS_DIR)
    assets_dir.mkdir(parents=True, exist_ok=True)

    post_files = sorted(posts_dir.glob("*.md"))
    print(f"Scanning {len(post_files)} post files for images …\n")

    # ── Pass 1: collect every unique image URL and assign a local filename ──
    url_to_local: dict[str, str] = {}
    used_names:   set[str]       = set()

    for post_file in post_files:
        for m in IMG_PATTERN.finditer(post_file.read_text(encoding="utf-8")):
            url = m.group(3)
            if url not in url_to_local:
                fname = local_filename(url, used_names)
                used_names.add(fname)
                url_to_local[url] = fname

    print(f"Found {len(url_to_local)} unique image URLs.\n")

    # ── Pass 2: download ────────────────────────────────────────────────────
    downloaded, failed = 0, []
    total = len(url_to_local)
    for i, (url, fname) in enumerate(url_to_local.items(), 1):
        dest = assets_dir / fname
        status = "skip" if dest.exists() else "down"
        print(f"  [{i:3}/{total}] {status}  {fname}")
        if download_image(url, dest):
            downloaded += 1
        else:
            failed.append(url)
        if status == "down":
            time.sleep(0.25)   # be polite to the origin server

    print(f"\nDownloaded {downloaded}/{total} images "
          f"({len(failed)} failures).")

    # ── Pass 3: rewrite markdown files ─────────────────────────────────────
    print("\nRewriting post markdown files …")
    updated = 0
    for post_file in post_files:
        original = post_file.read_text(encoding="utf-8")
        text = original
        for m in IMG_PATTERN.finditer(original):
            url = m.group(3)
            if url in url_to_local and (assets_dir / url_to_local[url]).exists():
                local_path = f"/assets/img/posts/{url_to_local[url]}"
                old_md = f"{m.group(1)}({url})"
                new_md = f"{m.group(1)}({local_path})"
                text = text.replace(old_md, new_md)
        if text != original:
            post_file.write_text(text, encoding="utf-8")
            updated += 1

    print(f"Updated {updated} post files.")

    if failed:
        print(f"\n── {len(failed)} failed downloads ──")
        for u in failed:
            print(f"  {u}")


if __name__ == "__main__":
    main()
