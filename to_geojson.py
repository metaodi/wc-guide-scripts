#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copy the id field from tags to the parent level

Example:
    cat not-in-osm.josn | python copy-id.py > not-in-osm-with-id.json
"""

import sys
import traceback
import json
import common
from pprint import pprint


if __name__ == "__main__":
    try:
        json_str = "".join(sys.stdin.readlines())
        d = json.loads(json_str)
        print(common.to_geojson(d))
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
