import json
from overpass_query import query

def map_wc_guide(row):
    tags = {'amenity': 'toilets'}
    tags['wc_guide_id'] = row['id']
    types = {
        '1': 'normal_toilet',
        '2': 'wheelchair_accessible_toilet',
        '4': 'urinal',
    }
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

def find_nearby_toilet(lat, lon, radius=30.0):
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
    result = query(around_query)
    return result['elements'] if result else []

def osm_json(elements):
    osm_data = {
        'version': 0.6,
        'generator': 'Overpass API 0.7.55.7 8b86ff77',
        'osm3s': {'timestamp_osm_base': '66901', 'copyright': 'The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.'},
        'elements': elements,
    }
    return json.dumps(osm_data, sort_keys=True, indent=2)

def to_float(s):
    try:
        f = float(s)
        return f
    except ValueError:
        return s

def to_geojson(elements):
    features = []
    for e in elements:
        features.append({
            'type': 'Feature',
            'id': e['id'],
            'properties': e['tags'],
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    to_float(e['lon']),
                    to_float(e['lat']),
                ]
            },
        })
    geojson = {
        'type': 'FeatureCollection',
        'features': features,
    }

    return json.dumps(geojson, indent=2)
