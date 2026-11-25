#!/usr/bin/env python3
"""news-image-20261125 — entry for the make.fun bounty
"Sum up 25 November's world news in one image" (news-image-20261125).

The entry image is the dense front page "THE WORLD TODAY — 25 November
2026" (33 stories: lead on the Hormuz tanker mines, two featured stories,
and 7 region sections), already drawn and stored in this repository as
entry.png (1024x1024, 203,348 bytes). This program copies it to
/output/entry.png.

Standard library only, no network. The grader's pinned Python image
does not ship Pillow, so the entry does not import PIL at all — it
copies the image the repository holds, which is the simplest entry
the bounty rules describe.
"""

import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    src = os.path.join(_HERE, "entry.png")
    if not os.path.isfile(src):
        print(f"entry image missing: {src}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    # Validate the copy: a PNG starts with its 8-byte magic, and the
    # bounty caps the image at 1 MiB and 1024x1024 (this one is 203,348).
    with open(dst, "rb") as fh:
        magic = fh.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("copied file is not a PNG", file=sys.stderr)
        return 1
    if size > 1024 * 1024:
        print(f"image {size} bytes exceeds the 1 MiB cap", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
