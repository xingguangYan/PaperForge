#!/usr/bin/env python3
"""
PaperForge — GEEPro task recipes.

Reusable, testable Google Earth Engine processing blocks. Every function is
written to run inside `with_cluster()` so that PaperForge's agent can compose
the pieces in-place instead of regenerating boilerplate from scratch.

Importing this module keeps a hard dependency on `ee` optional: the module
imports fine without the Earth Engine SDK installed and only raises a clear,
actionable error the moment GEE execution is actually requested.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

try:  # 'ee' is optional until real GEE execution is needed.
    import ee  # type: ignore
except Exception as _ee_err:  # pragma: no cover - environment dependent
    ee = None
    _EE_IMPORT_ERROR = _ee_err


# --------------------------------------------------------------------------
# Sentinel image ids, in the order PaperForge prefers them (10m → 30m → 250m)
# --------------------------------------------------------------------------
SENTINEL2 = "COPERNICUS/S2_SR_HARMONIZED"
S2_CLOUD_PROB = "COPERNICUS/S2_CLOUD_PROBABILITY"
LANDSAT8 = "LANDSAT/LC08/C02/T1_L2"
LANDSAT9 = "LANDSAT/LC09/C02/T1_L2"
MODIS_NDVI = "MODIS/061/MOD13Q1"

DATASET_FALLBACK = [SENTINEL2, LANDSAT8, MODIS_NDVI]


def require_ee():
    """Raise a friendly error if the Earth Engine SDK is unavailable."""
    if ee is None:
        raise RuntimeError(
            "Google Earth Engine SDK is not installed. "
            "Install it with `pip install earthengine-api`, "
            "authenticate with `earthengine authenticate`, "
            "then re-run PaperForge with --project YOUR_PROJECT_ID."
        )
    return ee


def initialize(project: Optional[str] = None, credentials: Optional[str] = None) -> None:
    """Initialize Earth Engine with an optional project id / service account."""
    e = require_ee()
    try:
        if credentials:
            e.ServiceAccountCredentials(
                "", credentials
            )  # validate early if provided
        e.Initialize(project=project) if project else e.Initialize()
    except Exception as exc:
        raise RuntimeError(
            "GEE initialization failed. Run `earthengine authenticate` or "
            "pass --project / a service-account credentials file, then retry.\n"
            f"Original error: {exc}"
        ) from exc


# --------------------------------------------------------------------------
# Geometry helpers
# --------------------------------------------------------------------------
def point_roi(lon: float, lat: float, buffer_m: float = 500) -> "ee.Geometry":
    """Build a circular ROI around a coordinate pair."""
    e = require_ee()
    return e.Geometry.Point([lon, lat]).buffer(buffer_m)


def to_geometry(region: Any) -> "ee.Geometry":
    """Normalize GeoJSON / dict / list input into an ee.Geometry."""
    e = require_ee()
    if isinstance(region, e.Geometry):
        return region
    if isinstance(region, e.Feature):
        return region.geometry()
    if isinstance(region, e.FeatureCollection):
        return region.geometry()
    if isinstance(region, dict):
        return e.Geometry(region)
    if isinstance(region, str):
        return e.Geometry(json.loads(region))
    if isinstance(region, (list, tuple)) and len(region) >= 2:
        # Coordinate pair [lon, lat] → buffered point.
        try:
            return e.Geometry.Point([float(region[0]), float(region[1])]).buffer(500)
        except (TypeError, ValueError):
            pass
        return e.Geometry(region)
    raise ValueError(f"Cannot convert region of type {type(region).__name__} to ee.Geometry")


# --------------------------------------------------------------------------
# Band math
# --------------------------------------------------------------------------
def add_ndvi(image: "ee.Image") -> "ee.Image":
    """Add an NDVI band: (NIR - Red) / (NIR + Red)."""
    ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
    return image.addBands(ndvi)


def add_fvc(image: "ee.Image", ndvi_soil: float = 0.05, ndvi_veg: float = 0.85) -> "ee.Image":
    """Add FVC via the dimidiate pixel model: (NDVI-NDVIsoil)/(NDVIveg-NDVIsoil)."""
    ndvi = image.select("NDVI")
    fvc = (ndvi.subtract(ndvi_soil)).divide(max(ndvi_veg - ndvi_soil, 1e-6)).clamp(0.0, 1.0)
    return image.addBands(fvc.rename("FVC"))


def add_ndwi(image: "ee.Image") -> "ee.Image":
    """Add NDWI: (Green - NIR) / (Green + NIR)."""
    ndwi = image.normalizedDifference(["B3", "B8"]).rename("NDWI")
    return image.addBands(ndwi)


# --------------------------------------------------------------------------
# Collection builders
# --------------------------------------------------------------------------
def masked_sentinel2(roi: "ee.Geometry", start: str, end: str, max_cloud: float = 20.0) -> "ee.ImageCollection":
    """Cloud-masked, NDVI/FVC-augmented Sentinel-2 collection."""
    e = require_ee()

    def _mask(img: "ee.Image") -> "ee.Image":
        scl = img.select("SCL")
        clear = (
            scl.eq(4)          # vegetation
            .Or(scl.eq(5))     # non-flooded bare soil
            .Or(scl.eq(6))     # water
            .Or(scl.eq(7))     # unclassified
        )
        # Harmonized SR values are already scaled by 10000 except the QA bands.
        return img.updateMask(clear).divide(10000).copyProperties(img, img.propertyNames())

    return (
        e.ImageCollection(SENTINEL2)
        .filterBounds(roi)
        .filterDate(start, end)
        .filter(e.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_cloud))
        .map(_mask)
        .map(add_ndvi)
        .map(add_fvc)
        .map(add_ndwi)
    )


def collection_with_fallback(dataset: str, roi: "ee.Geometry", start: str, end: str) -> "ee.ImageCollection":
    """Return a collection, falling back S2 → L8 → MODIS when empty."""

    e = require_ee()
    for candidate in ([dataset] if dataset else []) + DATASET_FALLBACK:
        try:
            col = e.ImageCollection(candidate).filterBounds(roi).filterDate(start, end)
            if col.size().getInfo() > 0:
                return col
        except Exception:
            continue
    raise RuntimeError(
        f"No imagery found for region between {start} and {end} "
        f"across datasets: {', '.join(DATASET_FALLBACK)}."
    )


def annual_median(image_collection: "ee.ImageCollection", year: int, band: str = "NDVI") -> "ee.Image":
    """Annual median composite of a single band for `year`."""
    return (
        image_collection.filterDate(f"{year}-01-01", f"{year}-12-31")
        .select(band)
        .median()
    )


# --------------------------------------------------------------------------
# Statistics
# --------------------------------------------------------------------------
def roi_stats(image: "ee.Image", roi: "ee.Geometry", scale: int = 10) -> Dict[str, float]:
    """Reduce an image over the ROI to a clean {'property': value} dict."""
    e = require_ee()
    reducers = (
        e.Reducer.mean()
        .combine(e.Reducer.stdDev(), "", True)
        .combine(e.Reducer.min(), "", True)
        .combine(e.Reducer.max(), "", True)
        .combine(e.Reducer.median(), "", True)
        .combine(e.Reducer.count(), "", True)
    )
    reduced = image.reduceRegion(
        reducer=reducers, geometry=roi, scale=scale, bestEffort=True, maxPixels=1e9
    )
    return reduced.getInfo()


def _center_img(t: int) -> "ee.Image":
    """Linear-regression design matrix helper."""
    e = require_ee()
    return e.Image.constant(t).toDouble()


def linear_trend(collection: "ee.ImageCollection", band: str) -> Dict[str, Any]:
    """Per-pixel linear trend via ee.Reducer.linearFit, summarized over the ROI."""
    e = require_ee()
    coll = collection.select(band)
    years = coll.aggregate_array("year").getInfo()

    def _pair(year: int) -> "ee.Image":
        yearly = coll.filter(e.Filter.calendarRange(year, year, "year")).mean()
        t_img = _center_img(year)
        return e.Image.cat(t_img, yearly).rename(["t", "y"]).set("year", year)

    series = e.ImageCollection([_pair(y) for y in sorted(set(years))])
    fit = series.select(["t", "y"]).reduce(e.Reducer.linearFit())
    return {"fit_image": fit, "years": years, "count": len(years)}


# --------------------------------------------------------------------------
# Vegetation classification
# --------------------------------------------------------------------------
def vegetation_grade(ndvi_image: "ee.Image") -> "ee.Image":
    """Classify NDVI into 1=low, 2=medium, 3=high using standard thresholds."""
    ndvi = ndvi_image.select("NDVI")
    grade = ndvi.where(ndvi.lt(0.3), 1).where(ndvi.gte(0.6), 3)
    grade = grade.where(ndvi.gte(0.3).And(ndvi.lt(0.6)), 2)
    return grade.rename("grade").set(
        "class_names", json.dumps({1: "low", 2: "medium", 3: "high"})
    )


def change_detection(first: "ee.Image", last: "ee.Image", band: str = "NDVI") -> "ee.Image":
    """Classify change between two images: -1 degraded, 0 stable, 1 improved."""
    e = require_ee()
    diff = last.select(band).subtract(first.select(band))
    cls = (
        diff.where(diff.lt(-0.05), -1)
        .where(diff.gt(0.05), 1)
        .where(diff.gte(-0.05).And(diff.lte(0.05)), 0)
    )
    return cls.rename("change")


# --------------------------------------------------------------------------
# Export / download
# --------------------------------------------------------------------------
def download_tif(
    image: "ee.Image",
    roi: "ee.Geometry",
    filename: str,
    scale: int = 10,
    crs: str = "EPSG:4326",
    outdir: str = "figures/ndvi_tif",
) -> str:
    """Download an image region as GeoTIFF to `outdir` and return the path."""
    import os
    import time

    import requests

    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, filename if filename.endswith(".tif") else filename + ".tif")

    url = image.getDownloadURL(
        {"name": filename.replace(".tif", ""), "scale": scale, "region": roi, "crs": crs, "format": "GEO_TIFF"}
    )
    backoff = 1.0
    last_err: Optional[Exception] = None
    for _ in range(3):  # exponential backoff retry
        try:
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            with open(out_path, "wb") as fh:
                fh.write(resp.content)
            return out_path
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(backoff)
            backoff *= 2
    raise RuntimeError(f"Failed to download {filename}: {last_err}")


# --------------------------------------------------------------------------
# Task scaffold (mirrors templates/task_template.json)
# --------------------------------------------------------------------------
TASK_TYPES = {
    "classification": {
        "target_variable": "land_cover_type",
        "metrics": ["overall_accuracy", "kappa", "f1_score"],
        "models": ["smileRandomForest", "smileCart", "improved_model"],
    },
    "monitoring": {
        "target_variable": "NDVI_trend_slope",
        "metrics": ["slope", "p_value", "r_squared"],
        "models": ["linearFit", "LandTrendr", "harmonic_regression"],
    },
    "regression": {
        "target_variable": "biophysical_parameter",
        "metrics": ["r_squared", "rmse", "mae", "bias"],
        "models": ["smileRandomForestRegressor", "linear_regression", "improved_rf_regressor"],
    },
    "change_detection": {
        "target_variable": "change_class",
        "metrics": ["area_changed", "change_rate"],
        "models": ["image_difference", "LandTrendr", "improved_model"],
    },
    "time_series": {
        "target_variable": "seasonal_metric",
        "metrics": ["r_squared", "rmse", "trend_significance_p"],
        "models": ["harmonic_regression", "linearFit", "improved_model"],
    },
}


def build_task(task_id: str, task_type: str, region: Any = None, time_range: Optional[List[str]] = None) -> Dict[str, Any]:
    """Create a GEE-ready task scaffold from a type key."""
    spec = TASK_TYPES.get(task_type, TASK_TYPES["monitoring"])
    return {
        "task_id": task_id,
        "type": task_type,
        "target_variable": spec["target_variable"],
        "datasets": [SENTINEL2, LANDSAT8],
        "region": region if isinstance(region, (dict, str)) else None,
        "time_range": time_range or ["2020-01-01", "2025-12-31"],
        "models": spec["models"],
        "metrics": spec["metrics"],
        "expected_output": spec["target_variable"] + "_map",
        "innovation": f"PaperForge improved {task_type} framework",
    }
