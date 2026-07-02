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



### Input

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
