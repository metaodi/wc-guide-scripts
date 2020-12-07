Helper scripts for WC-Guide
===========================

The goal is to migrate all data from WC-Guide to OpenStreetMap.

Part of the data can be migrated using QGIS and a manual workflow (see Stefan Keller).
Another part is suitable for MapRoulette, and I want to provide scripts to do that.

Basic idea:

- [ ] Use the original google speadsheet from WC-Guide as a starting point
- [ ] Convert the spreadsheet to CSV to work with it
- [ ] Install [OSM Conflator](https://wiki.openstreetmap.org/wiki/OSM_Conflator)
    * `pip install osm_conflate` 
    * GitHub: https://github.com/mapsme/osm_conflate
- [ ] Adapt the CSV to work with OSM Conflator
- [ ] Filter all wheelchair toilets from the CSV, those are the ones we want to check against OSM
- [ ] Add them to the resulting GeoJSON for MapRoulette if
    * they are already on OSM
    * they do not yet have the wheelchair tag on OSM
- [ ] Mark all those entries in the google speadsheet, so that others know, that they are being taken care of
- [ ] Upload GeoJSON to MapRoulette
- [ ] Profit!


## Usage

1. Activate the python virtual env and install the dependencies:

```
source env/bin/activate
pip install -r requirements.py
```

2. Download the Google Spreadsheet as CSV

Download the Google Spreadsheet and save the file as `wc-guide-toilets.csv`

3. To generate GeoJSON from the OSM data, we need the npm module `osmtogeojson`:

```
sudo npm install -g osmtogeojson
```

4. To generate a MapRoulette GeoJSON, use the following command

```bash
./wc-guide_wheelchair.py | osmtogeojson | ./convert_to_mr.py > wc-guide-maproulette.geojson
```

This generates a file called `wc-guide-maproulette.geojson`, that can be uploaded as a challange to MapRoulette.

## Explaination of all the parts

* `wc-guide_wheelchair.py` reads the CSV and calls the Overpass API to find matching toilets (in a radius around the lat/lon from the CSV)
* `osmtogeojson` is a node-based tool to convert OSM-Data (e.g. from Overpass) to standard GeoJSON
* `convert_to_mr.py` is a script to flatten the GeoJSON to make it more suitable for MapRoulette


