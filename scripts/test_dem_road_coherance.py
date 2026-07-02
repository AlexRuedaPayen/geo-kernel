import geopandas as gpd
import rasterio

roads = gpd.read_file("data/sample/roads_clean.geojson")

with rasterio.open("data/sample/dem.tif") as src:
    raster_bounds = src.bounds
    raster_crs = src.crs

roads = roads.to_crs(raster_crs)

print(raster_bounds)
print(roads.total_bounds)