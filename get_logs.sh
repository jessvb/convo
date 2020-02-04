#!/bin/bash
# Move Docker log files from locations
for file in `find /var/lib/docker/containers -name '*json.log'`; do
    filename=$(basename -- "$file")
    cat $file > "./logs/$filename"
done
