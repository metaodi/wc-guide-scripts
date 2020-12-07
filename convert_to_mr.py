#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Query OpenStreetMap data from OverPass API
This script reads a query from stdin and writes the resulting OSM data to stdout

Example:
    cat queries/defis_stadt_zh.txt | python query_overpass.py > data/defis_stadt_zh.geojson
"""

import os
import sys
import traceback
import json


try:
    geojson = json.loads("".join(sys.stdin.readlines()))
    
    features = []
    for feature in geojson['features']:
        props = feature['properties'].copy()
        props.update(props['tags'])
        del props['tags']

        feature['properties'] = {k: v for k,v in props.items() if v}
        features.append(feature)
    geojson['features'] = features

    print(json.dumps(geojson, sort_keys=True, indent=2))
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
