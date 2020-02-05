#!/bin/bash
echo "Getting logs..."
sudo ./get_logs.sh

echo "Deploying..."
docker-compose up --build -d

echo "Deployed."
