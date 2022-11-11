#!/bin/bash

cat all-toilets.overpassql | ./overpass_query.py | jq '.elements[].tags' | sed 's/,$//' | grep -i nette | sort | uniq -c | sort -nr
