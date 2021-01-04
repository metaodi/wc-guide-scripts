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
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


def query(q, endpoint='http://overpass.osm.ch/api/interpreter'):
    try:
        r = requests.get(endpoint, params={'data': q})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        print("")
        return []

if __name__ == "__main__":
    try:
        API_ENDPOINT = os.getenv('OVERPASS_API_ENDPOINT', 'http://overpass.osm.ch/api/interpreter')
        query_str = "".join(sys.stdin.readlines())

        r = query(query_str, API_ENDPOINT)
        print(json.dumps(r, sort_keys=True, indent=2))
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
