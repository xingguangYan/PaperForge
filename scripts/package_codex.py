#!/usr/bin/env python3
"""
PaperForge — packager for the OpenAI Codex CLI `.codex/skills` format.

Codex CLI discovers skills from `~/.codex/skills/<SkillName>/SKILL.md`
(global) or `.codex/skills/<SkillName>/` (repo). PaperForge lives at the repo
root, so this script stamps the metadata Codex expects and copies the tree
into the target location.

Usage:
    python scripts/package_codex.py --target ~/.codex/skills
    python scripts/package_codex.py --target .codex/skills
"""

from __future__ import annotations

import argparse
import os
import shutil

SKIP_DIRS = {".git", "__pycache__", "outputs", "runs", "tasks", ".codex",
             ".claude", ".agents", "node_modules", ".venv"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}


def _copy_tree(src: str, dst: str) -> int:
    count = 0
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES:
                continue
            src_path = os.path.join(root, name)
            rel = os.path.relpath(src_path, src)
            dst_path = os.path.join(dst, rel)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Package PaperForge as a Codex CLI skill.")
    parser.add_argument("--target", default=".codex/skills", help="Destination skills directory")
    args = parser.parse_args()

    target = os.path.expanduser(args.target)
    dest = os.path.join(target, "PaperForge")
    copied = _copy_tree(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), dest)
    print(f"✅ Copied PaperForge → {dest} ({copied} files)")
    print(f"   Restart Codex CLI, then invoke with: $paperforge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
