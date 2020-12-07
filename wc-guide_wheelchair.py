#!/usr/bin/env python3

import csv
import json
import time
import sys
from pprint import pprint
from overpass_query import query


def map_wc_guide(row):
    tags = {}
    tags['wc_guide_id'] = row['id']
    types = {
        '1': 'normal_toilet',
        '2': 'wheelchair_accessible_toilet',
        '4': 'urinal',
    }
    tags['wheelchair'] = types[row['typ']]
    tags['wheelchair'] = 'yes' if row['typ'] == '2' else '' 
    
    position = []
    if row['typ'] in ['1', '2']:
        position.append('seated')
    if row['typ'] == '4':
        position.append('urinal')
    tags['toilets:position'] = ";".join(position)

    options = row['options'].replace('{', '').replace('}', '').split(',')
    tags['fee'] = 'yes' if 1 in options else ''
    tags['changing_table'] = 'yes' if 2 in options else ''
    tags['stairs'] = 'yes' if 3 in options else ''
    tags['hand_rail'] = 'yes' if 4 in options else ''
    tags['network'] = 'nette_toilette' if 5 in options else ''
    tags['municipality'] = row['ort']
    tags['name'] = row['name']
    tags['website'] = row['website']
    tags['description'] = row['description']

    new_row = {}
    new_row['lat'] = row['latitude']
    new_row['lon'] = row['longitude']
    new_row['tags'] = tags

    return new_row

def update_if_not_empty(original, key, value):
    original_copy = original.copy()

    if k not in original:
        original_copy[k] = v

    if k in original and v:
        original_copy[k] = v

    return original_copy


wc_csv = 'wc-guide-toilets.csv'
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

        #row['options'] = json.loads(row['options'])
        if row['typ'] != '2':
            continue # only handle wheelchair accessible toilets

        # around query with radius and latitude,longitude
        lat = row['latitude']
        lon = row['longitude']
        radius = 30.0
        around_query = f"""
        [out:json][timeout:25];
        // gather results
        (
          node["amenity"="toilets"](around:{radius},{lat},{lon});
          );
        // print results
        out body;
        >;
        out skel qt;
        """
        time.sleep(1) # make sure we're not hitting a rate limit
        # limit: 10'0000 requests per day
        result = query(around_query)
        count_queries += 1
        osm_data = result['elements']
        if len(osm_data) == 1 and osm_data[0]['tags'].get('wheelchair', '') != 'yes':
            print(result, file=sys.stderr)
            toilet = osm_data[0]

            wc_guide_row = map_wc_guide(row)
            # update toilet with WC-Guide values
            for k, v in wc_guide_row.items():
                if k == 'tags':
                    for ik, iv in v.items():
                        toilet['tags'] = update_if_not_empty(toilet['tags'], ik, iv)
                    continue
                toilet = update_if_not_empty(toilet, k, v)

            print(toilet, file=sys.stderr)
            toilets.append(toilet)
            print(f"Found new wheelchair toilet on OSM ({len(toilets)}).", file=sys.stderr)
            # if len(toilets) > 1:
            #     break

print(f"Found {len(toilets)} toilets on OSM, that are tagged as wheelchair on WC-Guide", file=sys.stderr)


# stitch all osm data together
# TODO: copy website, opening hours and other useful info from wc_guide to osm
osm_data = {
    'version': 0.6,
    'generator': 'Overpass API 0.7.55.7 8b86ff77',
    'osm3s': {'timestamp_osm_base': '66901', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'},
    'elements': toilets,
}
print(json.dumps(osm_data, sort_keys=True, indent=2))
