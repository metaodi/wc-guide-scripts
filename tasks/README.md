WC-Guide Tasks for OSM Tasking Manager
======================================

To add all toilets from WC-Guide to OSM, that are not yet there (i.e. there is no matching toilet on OSM), we will use the OSM Tasking Manager.
There is a public instance from the Swiss OSM Assiciation here: https://tasks.osm.ch.

To get a new project, simply sign up on the page and send an email to the contact as described on the website.
Once you have the «Project Manager» role on the tasking manager, you can start by creating a new project.
New projects are private by default, so you can try the different options before making a new project public.

The currently setup project is here: http://tasks.osm.ch/project/22

The project uses a XS grid, so we have to split all the toilets to each of the squares.

## Generate a task file per square in the grid

Steps:

0. Download the grid GeoJSON: http://tasks.osm.ch/project/22/tasks.json
0. Generate a GeoJSON from the WC-Guide CSV using `./not-in-osm.py -f wc-guide.csv > not-in-osm.geojson`
0. Load both in QGIS (see the `wc-guide-tasks.qgz` QGIS project file)
0. Create a new column `xyz` in the grid layer to combine the `x`, `y` and `z` column in one (`CONCAT("x",'_', "y", '_', "zoom")`)
0. Use the QGIS processing tool «Clip points with polygons» to match the toilet points to the grid. Choose the `xyz` field to copy to the points.
![](clip_points_with_polygons.png)
0. Split the new "Clipped Points" layer using the QGIS Tool «Vector» -> «Split vector layer...» and use the `xyz` field as primary key.

As a result you get a directory full of GeoPackage files (one for each square), containing all the toilets of that square.
The it's a matter of converting the GeoPackage to the OSM file format to make it easier to consume the file in JOSM.
JOSM is the prefered tool to solve tasks of the OSM Tasking Manager.

In order to convert the GeoPackages to the OSM file format, we will first create GeoJSON with `ogr2ogr` and finally use `geojson2osm` to convert each GeoJSON to the OSM file format.

These files are then made available via an URL (e.g. here on GitHub) and can then be referenced on the OSM Tasking manager like that:

0. Edit the project
0. Update the instructions per tasks like that:

```
This task involves loading extra data. Click [here](http://localhost:8111/import?new_layer=true&url=https://raw.githubusercontent.com/metaodi/wc-guide-scripts/master/tasks/xyz_{x}_{y}_{z}.osm) to load the data into JOSM.
```