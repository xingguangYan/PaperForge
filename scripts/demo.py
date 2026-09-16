#!/usr/bin/env python3
"""
PaperForge — end-to-end smoke demo (no GEE, no internet required).

Generates real publication figures and writes manuscript.md + manuscript.html
+ manuscript.docx into outputs/demo/, proving the full rendering pipeline.

Usage:
    python scripts/demo.py
    python -m scripts.demo
"""

from __future__ import annotations

import json
import os
import sys


def main() -> int:
    # Support both `python scripts/demo.py` and `python -m scripts.demo`.
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)

    from demo_data import build_results
    from paper_writer import count_words, write_outputs

    print("🔨 PaperForge demo run — no GEE, no internet required\n")

    results = build_results()
    out_dir = "outputs/demo"
    paths = write_outputs(results, out_dir)

    print("✅ Outputs written:")
    for key in ("md", "html", "docx", "stats"):
        if key in paths:
            print(f"   {key:6s} → {paths[key]}")

    with open(paths["md"], encoding="utf-8") as fh:
        md = fh.read()
    print(f"\n📊 Estimated word count: {count_words(md)}")
    print(f"📁 Figures: {len(results['figures'])}   Tables: {len(results['tables'])}   "
          f"References: {len(results['references'])}")
    print("\n🎉 Demo complete. Upload outputs/demo/manuscript.html to preview.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
