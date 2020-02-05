#!/bin/bash
# Move Docker log files from locations
time=$(date +%s)
mkdir -p "./logs/$time"

for file in `find /var/lib/docker/containers -name '*json.log'`; do
    filename=$(basename -- "$file")
    cat $file > "./logs/$time/$filename"
done
