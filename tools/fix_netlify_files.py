#!/usr/bin/env python3
"""Normalize Netlify `_headers` and `_redirects` files.

Backs up originals to the same folder with `.bak` suffix.
Rules applied:
- Convert HTML comments <!-- --> to `#` comments
- Trim trailing whitespace
- Ensure path lines start at column 0 (no leading spaces)
- Ensure header lines are indented by two spaces and contain a colon
- Remove lines that are clearly invalid
"""

from pathlib import Path
import re
import shutil
import sys


def fix_file(path: Path) -> bool:
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = []
    changed = False

    in_header_block = False

    for i, raw in enumerate(lines):
        line = raw.rstrip()

        # Convert HTML comments to #
        if "<!--" in line or "-->" in line:
            line = re.sub(r"<!--|-->", "", line)
            line = line.strip()
            if line:
                line = "# " + line
            else:
                line = "#"
            changed = True
            out.append(line)
            in_header_block = False
            continue

        # Empty line
        if line.strip() == "":
            out.append("")
            in_header_block = False
            continue

        # Path lines should start with '/'
        if line.lstrip().startswith("/"):
            fixed = line.lstrip()
            if fixed != line:
                changed = True
            out.append(fixed)
            in_header_block = True
            continue

        # Comment lines starting with # - normalize spacing
        if line.lstrip().startswith("#"):
            fixed = line.lstrip()
            if fixed != line:
                changed = True
            out.append(fixed)
            continue

        # Header lines inside a block: should contain ':'
        if in_header_block:
            if ":" in line:
                name, val = line.split(":", 1)
                name = name.strip()
                val = val.strip()
                fixed = f"  {name}: {val}"
                if fixed != line:
                    changed = True
                out.append(fixed)
                continue
            else:
                # invalid header line: convert to comment
                fixed = "# " + line.strip()
                changed = True
                out.append(fixed)
                continue

        # Any other line — keep but normalized
        fixed = line.strip()
        if fixed != line:
            changed = True
        out.append(fixed)

    if changed:
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"Fixed: {path} (backup: {bak})")
    else:
        print(f"No changes needed: {path}")

    return changed


def main():
    repo_root = Path(__file__).resolve().parents[1]
    static = repo_root / "static"
    files = [static / "_headers", static / "_redirects"]

    any_changed = False
    for f in files:
        changed = fix_file(f)
        any_changed = any_changed or changed

    if any_changed:
        print("One or more Netlify files were normalized. Please review and commit the changes.")
        sys.exit(0)
    else:
        print("All Netlify files look good.")
        sys.exit(0)


if __name__ == '__main__':
    main()
