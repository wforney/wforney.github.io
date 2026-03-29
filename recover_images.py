#!/usr/bin/env python3
"""
Copy recovered blog images from OneDrive to assets/img/posts/ and
re-insert them into the matching posts.
"""

import re
import shutil
from pathlib import Path

ONEDRIVE = Path(r"C:\Users\wforn\OneDrive\Blog Images")
ASSETS   = Path("assets/img/posts")
POSTS    = Path("_posts")

# ── filename → (dest_name, post_slug_suffix_or_None, alt_text) ───────────
MAPPING = [
    # Camera-phone photos from the Bellingham LAN (Aug 4, 2007)
    # → appended to the "continued" post (post date 2007-08-15)
    ("0804071922.jpg",  "bellingham-lan-phone-1.jpg", "bellingham-lan-continued", "Bellingham LAN"),
    ("0804071923.jpg",  "bellingham-lan-phone-2.jpg", "bellingham-lan-continued", "Bellingham LAN"),
    ("0804071923a.jpg", "bellingham-lan-phone-3.jpg", "bellingham-lan-continued", "Bellingham LAN"),
    ("0804071923b.jpg", "bellingham-lan-phone-4.jpg", "bellingham-lan-continued", "Bellingham LAN"),

    # Nate's birthday party (Aug 6)
    ("8.6.2007.3.25.40 PM.861_007.jpg", "2007-08-06-nates-party.jpg",
     "nates-birthday-party", "Nate's birthday party"),

    # SYP Good Company Good Eats dinner (Aug 22)
    ("8.22.2007.9.27.53 PM.947.jpg", "2007-08-22-syp-dinner.jpg",
     "skagit-young-professionals-blog-archive-good-company-good-eats",
     "SYP Good Company Good Eats dinner"),

    # SYP website launch party (Sep 7)
    ("9.7.2007.3.48.39 AM.293_138.jpg", "2007-09-07-syp-launch-party.jpg",
     "skagit-young-professionals-blog-archive-todays-the-day-website-release-party-day",
     "SYP website launch party"),

    # Sunny Sunday Hike – Cascade Pass (Sep 10)
    ("9.10.2007.6.08.43 AM.389.jpg",      "2007-09-10-hike-1.jpg",
     "skagit-young-professionals-blog-archive-sunny-sunday-hike", "Cascade Pass hike"),
    ("9.10.2007.12.47.22 PM.511_146.jpg", "2007-09-10-hike-2.jpg",
     "skagit-young-professionals-blog-archive-sunny-sunday-hike", "Cascade Pass hike"),

    # Halo Nights (Sep 19)
    ("9.19.2007.11.50.14 AM.411.jpg", "2007-09-19-halo-nights.jpg",
     "halo-nights", "Halo Nights"),
]

# Images to copy but NOT auto-insert (context unclear)
COPY_ONLY = [
    ("8.9.2007.7.17.30 PM.112_461.jpg",  "2007-08-09-photo.jpg"),
    ("8.20.2007.5.42.09 PM.339.jpg",     "2007-08-20-photo.jpg"),
    ("8.21.2007.7.54.35 PM.576.jpg",     "2007-08-21-photo.jpg"),
    ("8.27.2007.9.10.08 AM.225.jpg",     "2007-08-27-photo.jpg"),
    ("9.5.2007.7.07.24 AM.999_149.jpg",  "2007-09-05-photo-1.jpg"),
    ("9.5.2007.8.10.23 AM.638_594.jpg",  "2007-09-05-photo-2.jpg"),
    ("9.5.2007.8.18.44 AM.980_213.jpg",  "2007-09-05-photo-3.jpg"),
    ("9.6.2007.11.15.37 PM.180.jpg",     "2007-09-06-photo.jpg"),
    ("9.17.2007.6.16.06 AM.454.jpg",     "2007-09-17-photo.jpg"),
]

# All 73 Bellingham LAN gallery photos – copy only
for f in sorted(ONEDRIVE.glob("2007-08-04 Bellingham LAN*.jpg")):
    dest = "bellingham-lan-" + re.sub(r"[^\w.-]", "-", f.name).lower()
    dest = re.sub(r"-+", "-", dest)
    COPY_ONLY.append((f.name, dest))


def find_post(slug_suffix):
    matches = list(POSTS.glob(f"*-{slug_suffix}.md"))
    return matches[0] if matches else None


def append_images_to_post(post_path, images):
    """Append image markdown lines at the end of the post."""
    text = post_path.read_text(encoding="utf-8").rstrip("\n")
    added = []
    for local_path, alt in images:
        if local_path not in text:
            text += f"\n\n![{alt}]({local_path})"
            added.append(local_path)
    if added:
        post_path.write_text(text + "\n", encoding="utf-8")
    return added


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)

    # ── Copy all images ───────────────────────────────────────────────────
    print("Copying images …")
    all_entries = [(s, d) for s, d, *_ in MAPPING] + COPY_ONLY
    copied = skipped = missing = 0
    for src_name, dest_name in all_entries:
        src  = ONEDRIVE / src_name
        dest = ASSETS / dest_name
        if not src.exists():
            print(f"  MISSING  {src_name}")
            missing += 1
            continue
        if dest.exists():
            skipped += 1
            continue
        shutil.copy2(src, dest)
        copied += 1
        print(f"  COPY     {src_name} → {dest_name}")

    print(f"\n  copied={copied}  skipped={skipped}  missing={missing}\n")

    # ── Group inserts by post ────────────────────────────────────────────
    by_post: dict[str, list[tuple[str, str]]] = {}
    for src_name, dest_name, slug, alt in MAPPING:
        dest = ASSETS / dest_name
        if not dest.exists():
            continue
        by_post.setdefault(slug, []).append((f"/assets/img/posts/{dest_name}", alt))

    print("Inserting images into posts …")
    for slug, images in by_post.items():
        post = find_post(slug)
        if post is None:
            print(f"  POST NOT FOUND: {slug}")
            continue
        added = append_images_to_post(post, images)
        if added:
            print(f"  {post.name}  (+{len(added)} image(s))")
        else:
            print(f"  {post.name}  (already present, skipped)")

    print("\nDone.")
    print(f"\nNote: {len(COPY_ONLY)} images were copied but NOT auto-inserted because")
    print("their context is ambiguous. They live in assets/img/posts/ for manual use.")


if __name__ == "__main__":
    main()
