#!/bin/bash

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip postgresql redis

# Install Python packages
pip3 install -r requirements.txt

# Set environment variables
export FLASK_APP=server.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://myuser:mypassword@db/mydb
export REDIS_URL=redis://redis:6379/0
