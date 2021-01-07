#!/bin/bash
for f in *.geojson; do geojson2osm ${f} > ${f%.*}.osm ; done
