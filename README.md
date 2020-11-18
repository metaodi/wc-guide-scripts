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
