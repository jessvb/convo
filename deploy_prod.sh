#!/bin/bash
echo "Getting logs..."
sudo ./get_logs.sh

echo "Deploying..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "Deployed."
