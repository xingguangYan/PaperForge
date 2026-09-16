#!/usr/bin/env python3
"""
PaperForge — offline test suite (no GEE, no internet required).

Usage:
    python scripts/test_pipeline.py
"""

from __future__ import annotations

import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def test_word_count():
    from paper_writer import count_words

    assert count_words("") == 0
    n = count_words("Hello world 2025")
    assert n == 3, n
    zh = count_words("遥感监测")
    assert zh == 4, zh  # CJK chars counted individually


def test_md_table():
    from paper_writer import render_md_table

    out = render_md_table(["A", "B"], [[1, 2], [3, 4]])
    assert "| A | B |" in out
    assert "| 1 | 2 |" in out
    assert "---" in out


def test_format_reference():
    from literature import format_reference

    p = {"author": "Tucker C J", "year": "1979", "title": "Red and photographic infrared", "journal": "RSE"}
    gb = format_reference(p, "gb")
    assert "[J]" in gb and "1979" in gb
    apa = format_reference(p, "apa")
    assert "(1979)" in apa


def test_validate_literature():
    from literature import validate_corpus

    ok = {"title": "t", "year": "2020", "journal": "j", "algorithm": "RF", "innovation": "x"}
    papers = [ok] * 15
    report = validate_corpus(papers)
    assert report["pass"] is False  # < 3 distinct methods
    assert report["meets_minimum"] is True


def test_parse_time_range():
    from literature import parse_time_range

    assert parse_time_range("2018-2023") == ("2018", "2023")
    assert parse_time_range(None) == ("2020", "2025")


def test_build_task():
    from gee_tasks import build_task

    t = build_task("Task-1", "monitoring")
    assert t["task_id"] == "Task-1"
    assert t["type"] == "monitoring"


def test_geography_error_is_friendly():
    from gee_tasks import require_ee, ee

    if ee is None:
        try:
            require_ee()
            assert False, "should have raised"
        except RuntimeError as exc:
            assert "pip install earthengine-api" in str(exc)


def test_render_manifest(tmp_path):
    from paper_writer import render_manifest

    results = {"title": "T", "abstract": "A", "keywords": ["k"], "sections": [], "figures": [], "tables": [], "references": []}
    md = render_manifest(results)
    assert "# T" in md and "Abstract" in md


def test_end_to_end_exports(tmp_path):
    """Full md/html/docx export path runs on demo data."""
    from demo_data import build_results
    from paper_writer import write_outputs

    results = build_results()
    paths = write_outputs(results, str(tmp_path))
    assert os.path.exists(paths["md"])
    assert os.path.exists(paths["html"])
    html = open(paths["html"], encoding="utf-8").read()
    assert "<!DOCTYPE html>" in html or "html" in html.lower()
    # docx optional; md+html are the guaranteed artifacts


def _run():
    import traceback

    tests = [
        (name, fn)
        for name, fn in sorted(globals().items())
        if name.startswith("test_") and callable(fn)
    ]
    passed = failed = 0
    for name, fn in tests:
        try:
            if name in ("test_end_to_end_exports", "test_render_manifest"):
                with tempfile.TemporaryDirectory() as td:
                    fn(td)
            else:
                fn()
            print(f"  ✅ {name}")
            passed += 1
        except AssertionError as exc:
            print(f"  ❌ {name}: {exc}")
            failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ❌ {name}: {exc.__class__.__name__}: {exc}")
            traceback.print_exc()
            failed += 1
    print(f"\n{'='*50}")
    print(f"  {passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_run())
