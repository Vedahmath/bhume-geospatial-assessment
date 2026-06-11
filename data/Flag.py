import json

with open("data/34855_vadnerbhairav_chandavad_nashik/predictions.geojson") as f:
    data = json.load(f)

flagged = sum(
    1 for feat in data["features"]
    if feat["properties"]["status"] == "flagged"
)

print("Flagged:", flagged)