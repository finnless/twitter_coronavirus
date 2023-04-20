#!/bin/sh

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
# for file in /data-fast/twitter\ 2020/geoTwitter20-*.zip; do
    echo "START: $file"
    ./src/map.py --input_path="${file}" &
    echo "FINISH: $file"
done

wait
