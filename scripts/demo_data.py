#!/usr/bin/env python3
"""
PaperForge — demo / smoke-test data.

A small but complete example of the `results` structure produced by the
three-phase pipeline. Consumed by:

    python scripts/demo.py
    python scripts/run_pipeline.py --topic demo --phase paper

The goal is to prove the DOCX + HTML + figures + tables rendering path works
end-to-end on any machine, even without GEE or internet access.
"""

from __future__ import annotations

from typing import Any, Dict

# English labels keep matplotlib CJK-font-free on every platform.
SITES = {"Guishan": [0.144, 0.134, 0.128, 0.121, 0.118, 0.115],
         "Sheshan": [0.214, 0.198, 0.185, 0.172, 0.161, 0.153]}
YEARS = [2020, 2021, 2022, 2023, 2024, 2025]

SECTIONS = [
    {
        "heading": "1. Introduction",
        "level": 2,
        "body": (
            "Urban mountain parks are critical components of urban ecosystems, "
            "regulating microclimate, conserving biodiversity, and buffering the "
            "urban heat island. Satellite-derived vegetation indices such as the "
            "Normalized Difference Vegetation Index (NDVI) and Fractional Vegetation "
            "Cover (FVC) offer a synoptic, repeatable means of monitoring such "
            "change over time. This study quantifies vegetation dynamics of Guishan "
            "and Sheshan, Wuhan, across 2020-2025 using Sentinel-2 imagery."
        ),
    },
    {
        "heading": "2. Study Area & Data",
        "level": 2,
        "body": (
            "Guishan (114.269E, 30.562N) and Sheshan (114.311E, 30.518N) are two "
            "urban mountains in Wuhan, Hubei Province, China. Sentinel-2 "
            "harmonized surface reflectance (COPERNICUS/S2_SR_HARMONIZED) with "
            "cloudy-pixel-percentage < 20% was used. Annual NDVI medians were "
            "computed per calendar year, and FVC was estimated with the dimidiate "
            "pixel model using NDVI_soil = 0.05 and NDVI_veg = 0.85."
        ),
    },
    {
        "heading": "3. Methods",
        "level": 2,
        "body": (
            "NDVI = (NIR - Red) / (NIR + Red). FVC = (NDVI - NDVI_soil) / "
            "(NDVI_veg - NDVI_soil). Temporal trends were quantified with ordinary "
            "least squares regression and tested with the Mann-Kendall statistic. "
            "GEE code: "
            "`img.normalizedDifference(['B8','B4']).rename('NDVI')`."
        ),
    },
    {
        "heading": "4. Results & Analysis",
        "level": 2,
        "body": (
            "Both mountains show declining NDVI from 2020 to 2025. Guishan NDVI "
            "fell from 0.144 to 0.115 (-20.3%); Sheshan fell from 0.214 to 0.153 "
            "(-28.5%). Trends were statistically significant at p < 0.05. Figures "
            "and tables below summarize the temporal and spatial patterns."
        ),
    },
    {
        "heading": "5. Discussion",
        "level": 2,
        "body": (
            "The negative trends are consistent with intensified urban development "
            "pressure and drought episodes reported in the literature. Sentinel-2 "
            "resolution (10 m) is adequate for these ~0.2-0.5 km2 mountain parks, "
            "though residual cloud contamination in humid summers may introduce "
            "uncertainty. Future work should fuse Landsat archives to extend the "
            "record and add high-resolution classification."
        ),
    },
    {
        "heading": "6. Conclusion",
        "level": 2,
        "body": (
            "(1) Guishan NDVI decreased 20.3% (0.144 to 0.115) over 2020-2025; "
            "(2) Sheshan NDVI decreased 28.5% (0.214 to 0.153); (3) low-cover "
            "fraction expanded at both sites; (4) Sentinel-2 monitoring captures "
            "the degradation trajectory and supports urban greening policy."
        ),
    },
]


def build_results() -> Dict[str, Any]:
    """Assemble the full demo results dict (and create figures/tables)."""
    import os

    figures = []
    try:
        import matplotlib  # noqa: F401

        try:
            from .render_figures import render_demo_figures
        except ImportError:
            from render_figures import render_demo_figures

        figures = render_demo_figures(
            outdir="outputs/demo/figures", sites=SITES, years=YEARS
        )
    except Exception as exc:  # matplotlib unavailable → no figures, pipeline still runs
        print(f"  ⚠️  Figures skipped ({exc.__class__.__name__}: {exc})")

    tables = [
        {
            "caption": "Table 1. Annual mean NDVI (2020-2025)",
            "headers": ["Year"] + list(SITES.keys()),
            "rows": [[y] + [SITES[s][i] for s in SITES] for i, y in enumerate(YEARS)],
        },
        {
            "caption": "Table 2. FVC change and trend statistics",
            "headers": ["Site", "FVC 2020", "FVC 2025", "Change", "Slope"],
            "rows": [
                ["Guishan", "0.118", "0.081", "-31.1%", "-0.0073/yr"],
                ["Sheshan", "0.204", "0.129", "-37.0%", "-0.0152/yr"],
            ],
        },
    ]

    references = [
        "Tucker C J. Red and photographic infrared linear combinations for monitoring vegetation[J]. Remote Sensing of Environment, 1979.",
        "Huete A, et al. Overview of the radiometric and biophysical performance of the MODIS vegetation indices[J]. Remote Sensing of Environment, 2002.",
        "Gutman G, Ignatov A. The derivation of the green vegetation fraction from NOAA/AVHRR data for use in numerical weather prediction models[J]. International Journal of Remote Sensing, 1998.",
        "Gorelick N, et al. Google Earth Engine: Planetary-scale geospatial analysis for everyone[J]. Remote Sensing of Environment, 2017.",
        "Drusch M, et al. Sentinel-2: ESA's optical high-resolution mission for GMES operational services[J]. Remote Sensing of Environment, 2012.",
        "Kennedy R E, Yang Z, Cohen W B. Detecting trends in forest disturbance and recovery using yearly Landsat time series[J]. Remote Sensing of Environment, 2010.",
    ]

    return {
        "title": "Sentinel-2 based Monitoring of Vegetation Change in Guishan and Sheshan, Wuhan (2020-2025)",
        "abstract": (
            "Background: Urban mountain parks provide irreplaceable ecosystem "
            "services yet are increasingly stressed by urban expansion. Objective: "
            "This study quantifies vegetation change in Guishan and Sheshan, Wuhan, "
            "from 2020 to 2025. Methods: Annual Sentinel-2 NDVI medians were derived "
            "in Google Earth Engine; FVC was estimated with the dimidiate pixel model "
            "and trends tested with the Mann-Kendall test. Results: Guishan NDVI "
            "declined from 0.144 to 0.115 (-20.3%) and Sheshan from 0.214 to 0.153 "
            "(-28.5%), with low-cover fraction expanding at both sites. Conclusion: "
            "Both urban mountains experienced significant vegetation degradation, "
            "warranting targeted greening intervention."
        ),
        "keywords": ["Sentinel-2", "NDVI", "FVC", "urban mountain", "vegetation change", "Google Earth Engine"],
        "sections": SECTIONS,
        "figures": figures,
        "tables": tables,
        "references": references,
        "author": "PaperForge",
    }


def _ensure_sample_dir() -> str:
    import os

    out = "outputs/demo"
    os.makedirs(out, exist_ok=True)
    return out


if __name__ == "__main__":
    import json

    from paper_writer import write_outputs

    results = build_results()
    out_dir = _ensure_sample_dir()
    paths = write_outputs(results, out_dir)
    print("Demo outputs written:")
    for key, path in sorted(paths.items()):
        print(f"  {key:6s} → {path}")

    stats_path = paths.get("stats")
    if stats_path:
        with open(stats_path, encoding="utf-8") as fh:
            print("  stats:", json.load(fh))
