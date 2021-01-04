#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query overpass for WC-Guide wheelchair entries from a CSV

Usage:
  wheelchair.py --file <path-to-file> 
  wheelchair.py (-h | --help)
  wheelchair.py --version

Options:
  -h, --help                  Show this screen.
  --version                   Show version.
  -f, --file <path-to-file>   Path to the CSV file.

"""

import csv
import json
import time
import sys
from docopt import docopt
from pprint import pprint
import common
arguments = docopt(__doc__, version='Query overpass for WC-Guide wheelchair entries 1.0')


wc_csv = arguments['--file']
toilets = []
count_queries = 0
totalrows = sum(1 for _ in open(wc_csv))
with open(wc_csv, 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    for i, row in enumerate(reader):
        print(f"{i}/{totalrows} toilets. {count_queries} Overpass requests.", file=sys.stderr)
        """
        typ:
	1 = Normale Toilette
	2 = Normale- und Behinderten-Toilette
	4 = Pissoir

        options:
	1 = Kostenpflichtig
	2 = Wickeltisch
	3 = Treppe
	4 = Handlauf
	5 = Nette Toilette 
        """

        if row['typ'] != '2':
            continue # only handle wheelchair accessible toilets

        time.sleep(1) # make sure we're not hitting a rate limit
        lat = row['latitude']
        lon = row['longitude']
        osm_data = common.find_nearby_toilet(lat, lon)
        count_queries += 1
        if len(osm_data) == 1 and osm_data[0]['tags'].get('wheelchair', '') != 'yes':
            toilet = osm_data[0]
            # remove OSM tags
            toilet['tags'] = {}
            wc_guide_row = common.map_wc_guide(row)
            # update toilet with WC-Guide values
            toilet.update(wc_guide_row)
            print(toilet, file=sys.stderr)
            toilets.append(toilet)
            print(f"Found new wheelchair toilet on OSM ({len(toilets)}).", file=sys.stderr)

print(f"Found {len(toilets)} toilets on OSM, that are tagged as wheelchair on WC-Guide", file=sys.stderr)

print(common.osm_json(toilets))
