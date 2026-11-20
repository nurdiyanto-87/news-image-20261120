#!/usr/bin/env python3
"""Entry program: copy the bundled front-page image to the output dir.

Pure stdlib, deterministic, no network. The image (entry.png) is drawn
by draw.py in this repository; this program only places a copy of it at
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
