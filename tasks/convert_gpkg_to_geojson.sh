#!/bin/bash
for f in *.gpkg; do ogr2ogr -f "GeoJSON" ${f%.*}.geojson ${f} ; done
