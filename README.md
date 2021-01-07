Helper scripts for WC-Guide
===========================

The goal is to migrate all data from WC-Guide to OpenStreetMap.

Part of the data can be migrated using QGIS and a manual workflow (see Stefan Keller).
Another part is suitable for MapRoulette, and I want to provide scripts to do that.

Basic idea:

- [x] Use the original google speadsheet from WC-Guide as a starting point
- [x] Convert the spreadsheet to CSV to work with it
- [x] Filter all wheelchair toilets from the CSV, those are the ones we want to check against OSM
- [x] Add them to the resulting GeoJSON for MapRoulette if
    * they are already on OSM (i.e. toilet in 30m radius around the coordinates of WC-Guide)
    * they do not yet have the wheelchair tag on OSM
    * there are currently **over 280 toilets** that match these criteria
- [x] Mark all those entries in the google speadsheet, so that others know, that they are being taken care of
    * they are all marked in the new column _updated_by_ with the value `MapRoulette`
- [x] Upload GeoJSON to MapRoulette -> https://maproulette.org/browse/challenges/13826
- [x] Profit!


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
./wheelchair.py | osmtogeojson > wc-guide-maproulette.geojson
```

This generates a file called `wc-guide-maproulette.geojson`, that can be uploaded as a challange to MapRoulette.

## Scripts

* `wc-guide_wheelchair.py` reads the CSV and calls the Overpass API to find matching toilets (in a radius around the lat/lon from the CSV)
* `osmtogeojson` is a node-based tool to convert OSM-Data (e.g. from Overpass) to standard GeoJSON
* `convert_to_mr.py` is a script to flatten the GeoJSON to make it more suitable for MapRoulette


To convert GeoJSON to OSM, we use the geojson2osm npm package (https://github.com/Rub21/geojson2osm)
