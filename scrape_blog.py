#!/usr/bin/env python3
"""
Scrapes all posts from williamforney.com WordPress blog
and converts them to Jekyll-compatible Markdown files.

Fixes applied vs original:
- Resolves LiteSpeed lazy-load (data-src → src) before conversion
- Extracts real author from post byline
- Strips WordPress/Divi shortcodes [et_pb_*] etc.
- Adds author to front matter when not William Forney
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import html2text

OUTPUT_DIR = "_posts"
SITEMAP_URL = "https://williamforney.com/sitemap-1.xml"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; blog-migrator/1.0)"
}
PRIMARY_AUTHOR = "William Forney"


def fetch_sitemap(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    for url_elem in root.findall("sm:url", ns):
        loc = url_elem.findtext("sm:loc", namespaces=ns)
        if loc:
            urls.append(loc)
    return urls


def is_post_url(url):
    return bool(re.match(r"https://williamforney\.com/\d{4}/\d{2}/\d{2}/", url))


def slug_from_url(url):
    parts = urlparse(url).path.strip("/").split("/")
    return parts[-1] if parts else "unknown"


def date_from_url(url):
    m = re.match(r"https://williamforney\.com/(\d{4})/(\d{2})/(\d{2})/", url)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else "1970-01-01"


def fix_lazy_images(soup):
    """Replace data-src / data-lazy-src with src on all img tags."""
    for img in soup.find_all("img"):
        real_src = img.get("data-src") or img.get("data-lazy-src") or img.get("data-lazy")
        if real_src:
            img["src"] = real_src
        # Remove placeholder data: URIs so html2text doesn't embed them
        if img.get("src", "").startswith("data:"):
            img["src"] = ""
        # Drop srcset / data-srcset to keep markdown clean
        for attr in ("srcset", "data-srcset", "data-src", "data-lazy-src",
                     "data-lazy", "data-sizes", "sizes"):
            if attr in img.attrs:
                del img.attrs[attr]


def strip_wp_shortcodes(text):
    """Remove WordPress / Divi shortcode tags like [et_pb_section ...] [/et_pb_row]."""
    text = re.sub(r"\[/?\w[\w-]*(?:\s[^\]]+)?\]", "", text)
    return text


def extract_author(soup):
    """Return the post author name, or empty string if it's the primary author."""
    # Try standard WordPress author byline
    for sel in ("a[rel='author']", ".author a", ".entry-author a",
                ".byline a", "span.author"):
        el = soup.select_one(sel)
        if el:
            name = el.get_text(strip=True)
            if name and name != PRIMARY_AUTHOR:
                return name
    return ""


def extract_post(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    # --- Title ---
    title = ""
    h1 = soup.find("h1", class_=re.compile(r"entry-title|post-title"))
    if not h1:
        h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
    if not title:
        og = soup.find("meta", property="og:title")
        if og:
            title = og.get("content", "").strip()
            # Strip " - William Forney" suffix added by WordPress SEO
            title = re.sub(r"\s*[–\-]\s*William Forney\s*$", "", title)

    # --- Date ---
    date = date_from_url(url)
    time_elem = soup.find("time", class_=re.compile(r"entry-date|published"))
    if not time_elem:
        time_elem = soup.find("time")
    if time_elem and time_elem.get("datetime"):
        dt = time_elem["datetime"][:10]
        if re.match(r"\d{4}-\d{2}-\d{2}", dt):
            date = dt

    # --- Author ---
    author = extract_author(soup)

    # --- Categories / tags ---
    categories = list(dict.fromkeys(
        a.get_text(strip=True)
        for a in soup.select("a[rel='category tag'], .cat-links a, .entry-categories a")
    ))
    tags = list(dict.fromkeys(
        a.get_text(strip=True)
        for a in soup.select(".tags-links a, .entry-tags a, a[rel='tag']")
    ))

    # --- Content ---
    content_elem = (
        soup.find("div", class_="entry-content")
        or soup.find("div", class_="post-content")
        or soup.find("article")
        or soup.find("main")
    )
    if not content_elem:
        content_elem = soup.find("body")

    if content_elem:
        for junk in content_elem.select(
            "nav, .post-navigation, .navigation, .sharedaddy, "
            ".jp-relatedposts, .wpcnt, #respond, .comments-area, "
            ".widget, aside, footer, .site-footer, .entry-meta, "
            ".post-meta, header.entry-header .entry-meta, "
            ".post-thumbnail, .entry-thumbnail"
        ):
            junk.decompose()
        # Fix lazy-loaded images inside the content
        fix_lazy_images(content_elem)

    # Also fix the featured image (post thumbnail) — grab it before decomposing
    featured_img_md = ""
    thumb = soup.select_one(".post-thumbnail img, .entry-thumbnail img, "
                             "img.wp-post-image, img.attachment-post-thumbnail")
    if thumb:
        real_src = thumb.get("data-src") or thumb.get("data-lazy-src") or thumb.get("src", "")
        if real_src and not real_src.startswith("data:"):
            alt = thumb.get("alt", "")
            featured_img_md = f"![{alt}]({real_src})\n\n"

    content_html = str(content_elem) if content_elem else ""

    # Convert HTML → Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.protect_links = False
    h.wrap_links = False

    markdown = h.handle(content_html).strip()

    # Remove the title if it appears as the first heading
    if title:
        markdown = re.sub(
            rf"^#+ *{re.escape(title)}\s*\n?", "", markdown, flags=re.IGNORECASE
        ).lstrip()

    # Strip empty image placeholders (src="") left by lazy-load removal
    markdown = re.sub(r"!\[([^\]]*)\]\(\s*\)", "", markdown)

    # Strip WordPress / Divi shortcodes
    markdown = strip_wp_shortcodes(markdown)

    # Clean up excessive blank lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()

    return {
        "title": title,
        "date": date,
        "author": author,
        "url": url,
        "categories": categories,
        "tags": tags,
        "featured_img_md": featured_img_md,
        "markdown": markdown,
    }


def yaml_str(s):
    return '"' + s.replace('"', '\\"') + '"'


def yaml_list(items):
    if not items:
        return "[]"
    return "[" + ", ".join(yaml_str(i) for i in items) + "]"


def make_front_matter(post):
    lines = [
        "---",
        f'title: {yaml_str(post["title"])}',
        f'date: {post["date"]}',
    ]
    if post.get("author"):
        lines.append(f'author: {yaml_str(post["author"])}')
    lines += [
        f'categories: {yaml_list(post["categories"])}',
        f'tags: {yaml_list(post["tags"])}',
        f'original_url: {yaml_str(post["url"])}',
        "---",
    ]
    return "\n".join(lines)


def filename_for(post):
    return f"{post['date']}-{slug_from_url(post['url'])}.md"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Fetching sitemap...")
    all_urls = fetch_sitemap(SITEMAP_URL)
    post_urls = [u for u in all_urls if is_post_url(u)]
    print(f"Found {len(post_urls)} post URLs to scrape.\n")

    success = 0
    failed = []

    for i, url in enumerate(post_urls, 1):
        slug = slug_from_url(url)
        print(f"  [{i}/{len(post_urls)}] Fetching: {slug}")
        try:
            post = extract_post(url)
            body = post["featured_img_md"] + post["markdown"] + "\n"
            content = make_front_matter(post) + "\n\n" + body
            out_path = os.path.join(OUTPUT_DIR, filename_for(post))
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            success += 1
        except Exception as e:
            print(f"    ERROR: {e}")
            failed.append((url, str(e)))

        time.sleep(0.5)

    print(f"\nDone! {success} posts saved to '{OUTPUT_DIR}/'")
    if failed:
        print(f"\n{len(failed)} failures:")
        for url, err in failed:
            print(f"  {url}: {err}")


if __name__ == "__main__":
    main()
