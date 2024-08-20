# cdrc

`cdrc` is a Python wrapper client library designed to connect to the CriticalMAAS Data Repository (CDR) and programmatically pull data. It can build GeoJSON files and GeoPackages for features extracted from COGs (Cloud Optimized GeoTIFF files of maps).

All georeferenced data returned will be in ESPG:4326 projection. Projected maps used to georeference features will be returned as the original projection they were projected with. 

CDR github:
https://github.com/DARPA-CRITICALMAAS/cdr

## Features

- Connect to the CDR with a token
- Pull data programmatically from COGs
- Build GeoJSON files
- Build GeoPackages
- Download COG images in pixel space and projected COGs if features are projected

## Installation

To install the `cdrc` library, use pip:

```
pip install cdrc
```

## Running cdrc

To import the library and set up the client: 
```
import cdrc

client = cdrc.CDRClient(token="your bearer token")
```
If you want to view data for a specific cog you can use the client.build_cog_geopackages function. It will download data from the cdr and convert it to a ready to use geopackage or geojson files you can load directly into QGIS.

This query can return a lot of data and take a long time to complete so if you only care about certain feature types or data from specific system/versions those should be set. 

Parameters:

**cog_id**: Cog id.

**feature_types**: An array of the features you want. Options are: line, point, polygon.

**system_versions**: An array of tuples with system and system_version. An empty array will return results from all systems.

**validated**: Return validated features or not validated. None will return both validated and not validated features/legend_items.

```
cog_id = "specify what cog you want"
system =  "system_name"
system_version = "0.0.1"

client.build_cog_geopackages(
    cog_id=cog_id,
    feature_types=['polygon', 'point', 'line'],
    system_versions=[(system, system_version)],
    validated=None
)
```


If you want to view data for a specific CMA area you can use the client.build_cma_geopackages function. It will download data from the cdr and convert it to a ready to use geopackage or geojson files you can load directly into QGIS.

This query can return a lot of data and take a long time to complete so if you only care about certain feature types or data from specific system/versions those should be set. 

Parameters:

**cog_ids**: List of cog ids that you want results for.

**feature_type**: Provide an the type of feature you want. Options are line, point, polygon.

**system_versions**: An array of tuples with system and system_version. An empty array will return results from all systems

**validated**: Return validated features or not validated. None will return both validated and not validated features.

**search_text**: String to be searched over the Legend description/label/abbreviation fields.

**intersect_polygon**: Geojson polygon to intersect over the features. EPSG:4326

**cma_name**: Name of the output folder for this search. 

```
cog_ids = ["specify list of cogs you want","..."]

client.build_cma_geopackages(
    cog_ids=cog_ids,
    feature_type='line',
    system_versions=[(system, system_version)],
    validated=None,
    search_text="",
    intersect_polygon= { 
        "type": "Polygon", 
        "coordinates": [
            [
                [-94.23558192118045, 48.0],
                [-94.24500827925175, 48.0],
                [-94.24500827925175, 49.0], 
                [-95.24500827925175, 49.0], 
                [-95.24500827925175, 48.0], 
                [-94.23558192118045, 48.0] 
            ]
        ] 
        },
    cma_name="cma_test"
)
```

