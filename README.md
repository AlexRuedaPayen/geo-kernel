# Geo Kernel 

Geo Kernel is a high-performance geospatial engine that transforms data such as  satellite imagery and terrain geometics into asset intelligence.
Industry specific solutions - including infrastrcture, rail, pipeline, mining and other verticals- are developped as plug-ins sharing a common, scalable processing engine.

As such:

Engine => Platfrom => Plug-ins business cases

## Main business case (not developped here but relevant)

### Infrastructure

Infrastrcture operators manage thousands of kilometers of assets but cannot inspect them continuously.
We can identify road, bridge, tunnels and other infrascture segments where satellite observations and terrain characteristics indicate unusual changes, helping prioritize inspecting and maintenance.

#### Inputs (Assets)

- Roads
- Bridges
- Tunnels
- Highways
- Retaining walls
- Embankments

#### Outputs 

- Risk score
- Terrain anomalies
- Persistent changes
- Inspection priority
- Time-series analysis

### Railway

Railway networks extend over large territories where terrain instability, nearby constrction and environemntal changes can threaten operations. We continuously analyze railway corridors combining Sentinel-1 imagery, DEM-derived terrain infromation and spatial analysis to identify segments requireing closer attention.

#### Inputs (Assets)

- Railway tracks
- Stations
- Embankments
- Cuttings
- Switches
- Rail corridors

#### Outputs

- Corridor risk map
- Earthwork detection
- Slope indicators
- Persistent change analysis
- Maintenance prioritization

### Pipeline & Utility corridor

Linear utility assest such as pipelines and transmission corridors are exposed to terrain evolution and human activities over thousands of kilometers.
We monitor these corridors using Earth Observation and geospatil analysis to detect environemental changes and support proactive inspection planning.

#### Inputs (Assets)

- Oil pipelines
- Gas pipelines
- Hydrogen pipelines
- Power lines
- Fiber corridors
- Utility easements

#### Outputs

- Corridor monitoring
- Terrain evolution
- Earthwork detection
- Risk segmentation
- Inspection recommendations


### Mining & Quarries

Mining operators require continuous visibility over the evolution of extraction sites, sourrounding terrain and operational activities.
We analyze satellite imagery and terrain information to monitor site evolution, detect significant changes and generate operational insight for large mining and quarry assets.

#### Inputs (assets)

- Open-pit mines
- Quarries
- Waste dumps
- Tailing areas
- Haul roads
- Industrial platforms

#### Outputs

- Site evolution
- Expansion detection
- Terrain modification
- Operational activity indictaors
- Time series reports



## Input

All inputs are listed here

``` {YAML}

AOI:
  roads.geoparquet
time:
  start: 2024-01-01
  end: 2025-01-01
Sensor:
  Sentinel-1 ##for now only this one has been implemented
DEM:
  Copernicus 30m
Plugin:
  infrastcture

``` 
#### Assets

Geometry, AOI to study : must contain a geometry type and a CRS (so must be geogrpahy).
Following format are accepted

.geoparquet
.geojson
.shp

#### EO Datasets

We will now only work on Sentinel-1 file
For that we will use a .yaml input that will direct towards the product we must read



### Terrain

For now will only be 
Copernicus DEM



### Business plugin

<To be defined>

## COnfiguration file

It is going to be a .yaml file to control desired resolution on out product

```{YAML}
buffer : 100
window_size : 256
resolution : 10
time_window:
  start: 2025-01-01
  end: 2026-01-01
scheduler:
  tiles: auto
```


## Output

### Feature time-series dataset

a GeoParquet file, with object level features over time
This is the main output of the project


**One row = one asset × one acquisition date**

`asset_features_timeseries.geoparquet`

| asset_id | asset_type | acquisition_date | s1_vv_mean (dB) | s1_vv_std | dem_slope_mean (°) | dem_terrain_roughness | s1_texture_entropy | pixel_count |
|----------|------------|------------------|----------------:|----------:|-------------------:|----------------------:|-------------------:|------------:|
| RD_001 | Road | 2025-01-03 | -11.7 | 2.1 | 12.4 | 0.31 | 4.81 | 148 |
| RD_001 | Road | 2025-01-15 | -11.9 | 2.2 | 12.4 | 0.31 | 4.76 | 148 |
| RD_001 | Road | 2025-01-27 | -10.8 | 3.6 | 12.4 | 0.31 | 5.43 | 148 |
| RD_002 | Road | 2025-01-03 | -13.4 | 1.4 | 2.8 | 0.08 | 3.62 | 201 |
| RD_002 | Road | 2025-01-15 | -13.5 | 1.3 | 2.8 | 0.08 | 3.60 | 201 |
---


### Latest feature snapshot

a GeoParquet file, with one row per asset for most recent acquisition

**One row = one asset using the latest available acquisition**

`asset_features_latest.geoparquet`

| asset_id | asset_type | latest_date | s1_vv_mean (dB) | s1_vv_std | dem_slope_mean (°) | dem_terrain_roughness | s1_texture_entropy |
|----------|------------|-------------|----------------:|----------:|-------------------:|----------------------:|-------------------:|
| RD_001 | Road | 2025-01-27 | -10.8 | 3.6 | 12.4 | 0.31 | 5.43 |
| RD_002 | Road | 2025-01-15 | -13.5 | 1.3 | 2.8 | 0.08 | 3.60 |
| RW_015 | Railway | 2025-01-27 | -8.7 | 2.9 | 17.6 | 0.54 | 6.12 |
| PL_103 | Pipeline | 2025-01-27 | -12.2 | 1.8 | 6.4 | 0.12 | 4.07 |

---

### Summary Features

a GeoParquet file, with for every asset : trends, min/max, variance, persistent change etc.

**One row = one asset summarizing its complete observation history**

`asset_features_summary.geoparquet`

| asset_id | observations | first_date | last_date | s1_vv_mean (dB) | s1_vv_trend (dB/year) | s1_vv_variance | dem_max_slope (°) | change_flag | anomaly_count |
|----------|-------------:|------------|-----------|----------------:|----------------------:|---------------:|------------------:|-------------|--------------:|
| RD_001 | 18 | 2024-06-02 | 2025-01-27 | -11.6 | +0.92 | 1.84 | 18.3 | Persistent | 3 |
| RD_002 | 18 | 2024-06-02 | 2025-01-15 | -13.5 | -0.08 | 0.19 | 4.2 | Stable | 0 |
| RW_015 | 21 | 2024-05-18 | 2025-01-27 | -8.9 | +1.44 | 3.27 | 22.1 | Persistent | 5 |
| PL_103 | 20 | 2024-05-30 | 2025-01-27 | -12.3 | +0.17 | 0.41 | 9.6 | Watch | 1 |

### Derived raster layers

a COG/GeoTIFF, with pixel-level feature maps




### Derived geometries

a GeoParquet, with buffers segments, sampling footprints

**Spatial objects generated by GeoKernel during preprocessing and analysis**

`derived_geometries.geoparquet`

| geometry_id | asset_id | geometry_type | description | area (m²) | length (m) |
|-------------|----------|---------------|-------------|----------:|-----------:|
| BUF_001 | RD_001 | Buffer (50 m) | Road analysis buffer | 184,562 | - |
| SEG_001 | RD_001 | Segment | Road segment (100 m) | - | 100 |
| SEG_002 | RD_001 | Segment | Road segment (100 m) | - | 100 |
| AOI_001 | RD_001 | Sampling Footprint | Sentinel-1 raster footprint used for analysis | 248,731 | - |
| TILE_014 | RD_001 | Processing Tile | Raster window processed by GeoKernel | 65,536 | - |

---

### Plugin outputs

a GeoParquet, with risk/activity/priority scores

**Domain-specific products generated from the Feature Dataset**

`infrastructure_plugin_output.geoparquet`

| asset_id | acquisition_date | priority | risk_score | confidence | dominant_factor |
|----------|------------------|----------|-----------:|-----------:|-----------------|
| RD_001 | 2025-01-27 | High | 0.91 | 0.96 | Persistent SAR change on steep terrain |
| RD_002 | 2025-01-15 | Low | 0.12 | 0.98 | Stable terrain and backscatter |
| RW_015 | 2025-01-27 | Medium | 0.63 | 0.87 | Increased texture variability |
| PL_103 | 2025-01-27 | Medium | 0.58 | 0.82 | Local terrain instability |

---

### Run metdata

a JSON, summarizing parametrs, versions, CRS and data sources

**Complete provenance describing how the dataset was produced**

`run_metadata.json`

```json
{
  "run_id": "2026-07-02T14:35:11Z",
  "geokernel_version": "0.1.0",
  "plugin": "Infrastructure",
  "crs": "EPSG:32631",
  "sensor": "Sentinel-1 IW GRD",
  "dem": "Copernicus GLO-30",
  "feature_resolution": 10,
  "buffer_distance_m": 50,
  "time_range": {
    "start": "2024-06-01",
    "end": "2025-01-31"
  },
  "assets_processed": 4231,
  "output_format": "GeoParquet"
}
```

---


### Benchmarks

a JSON with runtime, memory, throughput, tile count etc.

**Performance report generated after every execution**

`benchmark.json`

```json
{
  "execution_time_s": 221.4,
  "cpu_threads": 16,
  "peak_memory_mb": 2843,
  "pixels_processed": 2834190842,
  "assets_processed": 4231,
  "tiles_processed": 356,
  "throughput_pixels_per_second": 12792271,
  "average_tile_time_ms": 618,
  "output_size_mb": 248.7,
  "cache_hit_rate": 0.94
}
```

### Previws

GeoJSON/PNG files with human-readable demo artifacts



