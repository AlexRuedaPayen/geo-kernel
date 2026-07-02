from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd
import yaml


def load_config(path:str|Path) -> dict[str, Any]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    if path.suffix not in {".yaml", ".yml"}:
        raise ValueError(f"Expected a YAML file, but got: {path.suffix}")
    

    with path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("Configuration file must contain a YAML mapping/object")
    
    return config


def load_assets(path: str|Path) -> gpd.GeoDataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Assets file not found: {path}")
    
    if path.suffix not in {".geojson", ".shp", ".json", ".parquet",".geopackage"}:
        raise ValueError(f"Unsupported file format: {path.suffix}")
    
    gdf= gpd.read_file(path) if path.suffix != ".geoparquet" else gpd.read_parquet(path)

    if gdf.empty:
        raise ValueError(f"Assets file is empty: {path}")
    
    if gdf.crs is None:
        raise ValueError(f"Assets file has no CRS defined: {path}")
    
    if "geometry" not in gdf.columns:
        raise ValueError(f"Assets file must contain a 'geometry' column: {path}")   
    
    return gdf


def write_geoparquet(gdf: gpd.GeoDataFrame, path: str|Path) -> None:
    path = Path(path)
    if path.suffix != ".geoparquet":
        raise ValueError(f"Output file must have a .geoparquet extension: {path}")
    
    gdf.to_parquet(path, engine="pyarrow", index=False)