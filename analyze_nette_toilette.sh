#!/bin/bash

cat all-toilets.txt | ./overpass_query.py | jq '.elements[].tags' | grep -i nette | sort | uniq -c | sort -nr
