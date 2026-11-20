#!/usr/bin/env python3
"""Copy the bundled front page to the output directory.

Runs on the standard library alone. The PNG itself is produced by
draw.py in this repository; this entry point just places a copy of it
at $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE = ROOT / "entry.png"


def run():
    target = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target / "entry.png")


if __name__ == "__main__":
    run()
