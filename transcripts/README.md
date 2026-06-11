# AI Usage Transcript

## Tools Used

* ChatGPT
* GitHub
* Python
* GeoPandas
* Rasterio

## Purpose

I used ChatGPT extensively throughout this assessment to understand the provided starter kit, debug environment issues, understand the geospatial data structures, improve the baseline solution, and prepare the final submission.

## Topics Discussed

### Environment Setup

* Installing Python dependencies
* Installing Pillow, NumPy, GeoPandas, Rasterio, PyProj, Shapely
* Resolving uv installation issues
* Running quickstart.py

### Dataset Understanding

* Understanding input.geojson
* Understanding imagery.tif
* Understanding boundaries.tif
* Understanding example_truths.geojson

### Baseline Analysis

* Understanding the global median shift approach
* Understanding centroid displacement
* Understanding IoU evaluation metrics
* Understanding confidence calibration

### Solution Improvements

* Replaced constant confidence values with area-based confidence calibration
* Added low-confidence plot flagging
* Generated calibrated predictions.geojson

### GitHub Submission

* Repository setup
* Git conflict resolution
* Submission packaging

## Key Results

Public Example Truth Results:

* Median IoU (Official): 0.612
* Median IoU (Prediction): 0.713
* Improvement: +0.112
* Accurate Rate: 100%
* Spearman Confidence Correlation: 0.829

## Reflection

The assessment reinforced the importance of robust geometric reasoning, confidence calibration, reproducible pipelines, and practical debugging under time constraints. Given only six labeled examples, a robust geometric correction approach was selected instead of training a supervised model that could easily overfit.
