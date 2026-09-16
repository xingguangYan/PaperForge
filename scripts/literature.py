#!/usr/bin/env python3
"""
PaperForge — ResearchX literature helpers.

Data structures and validators used during the literature-mining phase.
The agent performs the actual multi-round web searches; these helpers keep
the extracted metadata consistent so Phase 2/3 can consume it reliably.
"""

from __future__ import annotations

from typing import Any, Dict, List

REFERENCE_STYLES = ("gb", "apa", "mla")
MIN_PAPERS = 15
TARGET_REFERENCES = (25, 30)

REQUIRED_PAPER_FIELDS = ("title", "year", "journal", "algorithm", "innovation")


def validate_paper(paper: Dict[str, Any]) -> List[str]:
    """Return a list of missing required fields for one extracted paper."""
    missing = [f for f in REQUIRED_PAPER_FIELDS if not paper.get(f)]
    return missing


def validate_corpus(papers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate an extracted literature corpus against PaperForge quality gates."""
    missing_fields: Dict[str, List[str]] = {}
    for i, paper in enumerate(papers):
        m = validate_paper(paper)
        if m:
            missing_fields[f"paper_{i}"] = m

    has_accuracies = sum(
        1 for p in papers if p.get("accuracy") and isinstance(p["accuracy"], dict)
    )
    methods = {p.get("algorithm") for p in papers if p.get("algorithm")}
    return {
        "count": len(papers),
        "meets_minimum": len(papers) >= MIN_PAPERS,
        "missing_fields": missing_fields,
        "papers_with_accuracy": has_accuracies,
        "distinct_methods": len(methods),
        "methods_covered": sorted(methods),
        "pass": len(papers) >= MIN_PAPERS and not missing_fields and len(methods) >= 3,
    }


def format_reference(paper: Dict[str, Any], style: str = "gb") -> str:
    """Format one reference entry in the requested citation style."""
    author = paper.get("author", paper.get("authors", "Anonymous"))
    year = paper.get("year", "n.d.")
    title = paper.get("title", "Untitled")
    journal = paper.get("journal", "")

    if style == "apa":
        return f"{author} ({year}). {title}. *{journal}*."
    if style == "mla":
        return f'{author}. "{title}." *{journal}*, {year}.'
    # GB/T 7714-2015
    return f"{author}. {title}[J]. {journal}, {year}."


def parse_time_range(value: str | None, default: tuple = ("2020", "2025")) -> tuple:
    """Parse a CLI time range like '2020-2025' or '2018-2023' into (start, end)."""
    if not value:
        return default
    parts = [p.strip() for p in value.replace("—", "-").replace("~", "-").split("-") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[-1]
    return parts[0], default[1]
