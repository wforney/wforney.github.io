#!/usr/bin/env python3
"""
Post-processes scraped Jekyll markdown files:
1. Deduplicates categories and tags in front matter
2. Converts indented code blocks to fenced ``` code blocks
"""

import os
import re
import glob

POSTS_DIR = "_posts"


def fix_yaml_list(value: str) -> str:
    """Deduplicate a YAML inline list like ["a", "b", "a"]."""
    if not value.startswith("["):
        return value
    items = re.findall(r'"([^"]*)"', value)
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    if not seen:
        return "[]"
    return "[" + ", ".join(f'"{i}"' for i in seen) + "]"


def fix_front_matter(content: str) -> str:
    """Fix duplicate categories and tags in YAML front matter."""
    def replace_list(m):
        key = m.group(1)
        val = m.group(2)
        return f"{key}: {fix_yaml_list(val)}"

    return re.sub(r"^(categories|tags): (\[.*\])$", replace_list, content, flags=re.MULTILINE)


def convert_indented_code_blocks(content: str) -> str:
    """
    Convert 4-space-indented code blocks to fenced ``` blocks.
    Handles both single and multi-line indented blocks.
    """
    # Split on front matter boundary
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            front_matter = "---" + parts[1] + "---"
            body = parts[2]
        else:
            return content
    else:
        front_matter = ""
        body = content

    lines = body.split("\n")
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect start of an indented block (4 spaces or 1 tab)
        if re.match(r"^(    |\t)", line) and line.strip():
            # Collect all consecutive indented lines
            block_lines = []
            while i < len(lines) and (re.match(r"^(    |\t)", lines[i]) or lines[i].strip() == ""):
                if lines[i].strip() == "" and block_lines and not block_lines[-1].strip():
                    # Stop at double blank line inside block
                    break
                block_lines.append(lines[i])
                i += 1
            # Strip trailing blank lines from the block
            while block_lines and not block_lines[-1].strip():
                block_lines.pop()
            # De-indent: remove leading 4 spaces or 1 tab
            dedented = [re.sub(r"^(    |\t)", "", l) for l in block_lines]
            result.append("```")
            result.extend(dedented)
            result.append("```")
        else:
            result.append(line)
            i += 1

    new_body = "\n".join(result)
    return front_matter + new_body


def process_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        original = f.read()

    fixed = fix_front_matter(original)
    fixed = convert_indented_code_blocks(fixed)

    if fixed != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(fixed)
        return True
    return False


def main():
    files = glob.glob(os.path.join(POSTS_DIR, "*.md"))
    changed = 0
    for path in sorted(files):
        if process_file(path):
            changed += 1
    print(f"Processed {len(files)} files, updated {changed}.")


if __name__ == "__main__":
    main()
