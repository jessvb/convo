#!/bin/bash
# Move Docker log files from locations
time=$(date +%s)
mkdir -p "./logs/$time"

echo "Logging into ./logs/$time"
for file in `sudo find /var/lib/docker/containers -name '*json.log'`; do
    filename=$(basename -- "$file")
    sudo cat $file > "./logs/$time/$filename"
    echo "Logged ./logs/$time/$filename"
done
sudo chown -R kevin "./logs/$time"
