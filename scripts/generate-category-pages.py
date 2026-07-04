#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "_posts"
PINS_FILE = ROOT / "_data" / "pins.json"
CATEGORIES_DIR = ROOT / "categories"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def read_post_categories(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return []

    front_matter = text.split("---", 2)
    if len(front_matter) < 3:
        return []

    header = front_matter[1]
    match = re.search(r"^categories:\s*\[(.*?)\]\s*$", header, re.MULTILINE)
    if not match:
        return []

    return re.findall(r'"([^"]+)"', match.group(1))


def main() -> None:
    category_names: set[str] = set()

    for path in POSTS_DIR.glob("*.md"):
        category_names.update(read_post_categories(path))

    with PINS_FILE.open(encoding="utf-8") as f:
        pins = json.load(f)

    for pin in pins:
        for category in pin.get("categories", []) or []:
            category_names.add(category)

    for category in sorted(category_names, key=lambda s: s.lower()):
        slug = slugify(category)
        target_dir = CATEGORIES_DIR / slug
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "index.md"
        target.write_text(
            "---\n"
            "layout: category\n"
            f"title: \"{category}\"\n"
            f"category: \"{category}\"\n"
            f"permalink: /categories/{slug}/\n"
            "---\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
