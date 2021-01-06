#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query overpass for WC-Guide entries from a CSV

Usage:
  not-in-osm.py --file <path-to-file> --start <start-row>
  not-in-osm.py (-h | --help)
  not-in-osm.py --version

Options:
  -h, --help                  Show this screen.
  --version                   Show version.
  -f, --file <path-to-file>   Path to the CSV file.
  -s, --start <start-row>     Row number where the CSV should start [default: 0].

"""


import csv
import time
import sys
from docopt import docopt
from pprint import pprint
import common
arguments = docopt(__doc__, version='Query overpass for WC-Guide entries 1.0')


wc_csv = arguments['--file']
toilets = []
count_queries = 0
totalrows = sum(1 for _ in open(wc_csv))
try:
    with open(wc_csv, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        start_row = int(arguments['--start'])
        for i, row in enumerate(reader):
            if i < start_row:
                continue
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
            if row['typ'] == '2':
                continue # handle normal toilets and urinals

            time.sleep(1) # make sure we're not hitting a rate limit
            lat = row['latitude']
            lon = row['longitude']
            # if not lat or not lon:
            #     print(f"Lat or lon missing: {row}. Skipping...", file=sys.stderr)
            #     continue
                
            osm_data = common.find_nearby_toilet(lat, lon)
            count_queries += 1
            # use only result that have no matching toilet on OSM
            if len(osm_data) == 0:
                toilet = common.map_wc_guide(row)
                print(toilet, file=sys.stderr)
                toilets.append(toilet)
                print(f"Found new toilet, that is not on OSM ({len(toilets)}).", file=sys.stderr)

    print(f"Found {len(toilets)} new toilets from WC-Guide, that are not yet on OSM", file=sys.stderr)
except Exception as e:
    print("Error: %s" % e, file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    sys.exit(1)
finally:
    # print what we got so far
    print(common.osm_json(toilets))
