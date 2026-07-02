
from pathlib import Path
import json

import geopandas as gpd
from shapely.geometry import LineString


INPUT = Path("data/sample/roads.geojson")
OUTPUT_GEOJSON = Path("data/sample/roads_clean.geojson")
OUTPUT_GEOPARQUET = Path("data/sample/roads_clean.geoparquet")


ALLOWED_HIGHWAYS = {
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "unclassified",
}


def load_roads(path: Path) -> gpd.GeoDataFrame:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Case 1: standard GeoJSON exported by Overpass Turbo
    if data.get("type") == "FeatureCollection":
        return gpd.read_file(path)

    # Case 2: raw Overpass JSON
    rows = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        highway = tags.get("highway")

        if element.get("type") != "way":
            continue

        if highway not in ALLOWED_HIGHWAYS:
            continue

        coords = [
            (point["lon"], point["lat"])
            for point in element.get("geometry", [])
        ]

        if len(coords) < 2:
            continue

        rows.append(
            {
                "osm_id": element["id"],
                "asset_type": "road",
                "highway": highway,
                "name": tags.get("name"),
                "surface": tags.get("surface"),
                "maxspeed": tags.get("maxspeed"),
                "geometry": LineString(coords),
            }
        )

    return gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")


def main() -> None:
    roads = load_roads(INPUT)

    if roads.empty:
        raise ValueError("No valid road geometries found.")

    roads = roads.to_crs("EPSG:4326")

    # Keep only LineStrings
    roads = roads[roads.geometry.type == "LineString"].copy()

    # Keep useful columns only
    keep_cols = [
        col for col in [
            "osm_id",
            "asset_type",
            "highway",
            "name",
            "surface",
            "maxspeed",
            "geometry",
        ]
        if col in roads.columns
    ]
    roads = roads[keep_cols].copy()

    roads.insert(0, "asset_id", [f"RD_{i:03d}" for i in range(1, len(roads) + 1)])

    # Compute metric length in Lambert-93
    roads_metric = roads.to_crs("EPSG:2154")
    roads["length_m"] = roads_metric.length.round(2)

    # Save outputs
    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    roads.to_file(OUTPUT_GEOJSON, driver="GeoJSON")
    roads.to_parquet(OUTPUT_GEOPARQUET, index=False)

    # Print AOI information
    minx, miny, maxx, maxy = roads.total_bounds
    bbox_area_km2 = (
        gpd.GeoSeries.from_bbox((minx, miny, maxx, maxy), crs="EPSG:4326")
        .to_crs("EPSG:2154")
        .area.iloc[0]
        / 1_000_000
    )

    print(f"Roads kept: {len(roads)}")
    print(f"Output GeoJSON: {OUTPUT_GEOJSON}")
    print(f"Output GeoParquet: {OUTPUT_GEOPARQUET}")
    print()
    print("AOI used:")
    print(f"  min_lon: {minx}")
    print(f"  min_lat: {miny}")
    print(f"  max_lon: {maxx}")
    print(f"  max_lat: {maxy}")
    print(f"  bbox_area_km2: {bbox_area_km2:.4f}")


if __name__ == "__main__":
    main()