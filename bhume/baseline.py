"""A deliberately naive baseline — improved confidence calibration."""

from __future__ import annotations

import statistics

import geopandas as gpd
from shapely.affinity import translate


def _utm_for(geom) -> str:
    lon = geom.centroid.x
    return f'EPSG:{32600 + int((lon + 180) // 6) + 1}'


def global_median_shift(village) -> gpd.GeoDataFrame:
    """
    Estimate one village-wide translation using example truths and
    apply it to every plot.
    """

    if village.example_truths is None:
        raise ValueError(
            f'{village.slug} has no example_truths.geojson to estimate a shift from'
        )

    utm = _utm_for(village.example_truths.geometry.iloc[0])

    official_u = village.plots.to_crs(utm)
    truth_u = village.example_truths.to_crs(utm)

    dxs = []
    dys = []

    for pn in village.example_truths.index:
        if pn in official_u.index:
            o = official_u.loc[pn, 'geometry'].centroid
            t = truth_u.loc[pn, 'geometry'].centroid

            dxs.append(t.x - o.x)
            dys.append(t.y - o.y)

    if not dxs:
        raise ValueError(
            'no overlapping plots between example truths and the cadastre'
        )

    mdx = statistics.median(dxs)
    mdy = statistics.median(dys)

    shifted = official_u.copy()
    shifted["geometry"] = shifted.geometry.apply(
        lambda g: translate(g, mdx, mdy)
    )

    preds = shifted.to_crs("EPSG:4326")

    # Confidence based on plot area
    areas = shifted.geometry.area

    min_area = float(areas.min())
    max_area = float(areas.max())

    if max_area > min_area:
        preds["confidence"] = (
        0.3 + 0.6 * ((areas - min_area) / (max_area - min_area))
        )
    else:
        preds["confidence"] = 0.5

    preds["confidence"] = preds["confidence"].clip(0.3, 0.9)

    preds["status"] = "corrected"

    # Flag smallest 5% plots
    threshold = areas.quantile(0.05)

    preds.loc[areas < threshold, "status"] = "flagged"
    preds.loc[areas < threshold, "confidence"] = 0.2

    preds["method_note"] = (
    f"median-shift correction dx={mdx:.1f}m dy={mdy:.1f}m "
    f"with area-based confidence calibration"
    )

    return preds[
        [
            "plot_number",
            "status",
            "confidence",
            "method_note",
            "geometry",
        ]
    ]