#!/usr/bin/env python3
"""
PaperForge — publication figure renderer.

Deterministic, matplotlib-based figure generation. All labels are English so
the output never depends on CJK fonts. Each figure is saved as a 300-DPI PNG.

Functions are importable by the agent so it can regenerate figures for real
GEE results rather than handwriting matplotlib boilerplate every run.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence

import os


def _figure_size(n_panels: int = 1) -> tuple:
    """Return a publication-appropriate (inch) size for a given panel count."""
    base_w, base_h = 10.0, 4.5
    return (base_w, base_h * max(1, n_panels))


def _save(fig, path: str, dpi: int = 300) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path


def render_time_series(
    series: Dict[str, Sequence[float]],
    years: Sequence[int],
    out_path: str = "figures/fig2_ndvi_timeseries.png",
    ylabel: str = "Mean NDVI",
) -> str:
    """Line chart of one or more named series across years."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=_figure_size(), dpi=150)
    for name, values in series.items():
        ax.plot(list(years), list(values), marker="o", linewidth=2, label=name)
    ax.set_xlabel("Year")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{ylabel} Time Series")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return _save(fig, out_path)


def render_grouped_bar(
    categories: Sequence[str],
    values: Dict[str, Sequence[float]],
    out_path: str = "figures/fig4_classification.png",
    ylabel: str = "Fraction",
) -> str:
    """Grouped bar chart across categories."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(len(categories))
    width = 0.8 / max(1, len(values))
    fig, ax = plt.subplots(figsize=_figure_size(), dpi=150)
    for i, (name, vals) in enumerate(values.items()):
        ax.bar(x + (i - (len(values) - 1) / 2) * width, list(vals), width, label=name)
    ax.set_xticks(x)
    ax.set_xticklabels(list(categories))
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    return _save(fig, out_path)


def render_demo_figures(
    outdir: str = "outputs/demo/figures",
    sites: Optional[Dict[str, Sequence[float]]] = None,
    years: Optional[Sequence[int]] = None,
) -> List[dict]:
    """Render the standard PaperForge 2-figure demo set and return metadata."""
    sites = sites or {"Guishan": [0.144, 0.134, 0.128, 0.121, 0.118, 0.115],
                      "Sheshan": [0.214, 0.198, 0.185, 0.172, 0.161, 0.153]}
    years = list(years) if years else [2020, 2021, 2022, 2023, 2024, 2025]

    ts_path = render_time_series(sites, years, os.path.join(outdir, "fig2_ndvi_timeseries.png"))

    # Vegetation grade: low / medium / high fraction (illustrative for demo)
    cats = ["Low (<0.3)", "Medium (0.3-0.6)", "High (>0.6)"]
    grade = {
        "Guishan": [0.45, 0.40, 0.15],
        "Sheshan": [0.30, 0.41, 0.29],
    }
    bar_path = render_grouped_bar(cats, grade, os.path.join(outdir, "fig4_vegetation_grade.png"))

    return [
        {"path": ts_path, "caption": "Fig 2. Annual mean NDVI time series (2020-2025)."},
        {"path": bar_path, "caption": "Fig 4. Vegetation grade distribution by site."},
    ]
