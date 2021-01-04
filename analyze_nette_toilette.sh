#!/bin/bash

cat all-toilets.txt | ./overpass_query.py | jq '.elements[].tags' | sed 's/,$//' | grep -i nette | sort | uniq -c | sort -nr
