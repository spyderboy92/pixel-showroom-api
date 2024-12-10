#!/bin/bash

# Update the package index
sudo yum update -y

# Install necessary packages
sudo yum install -y git python3 python3-pip gcc python3-devel

# Install virtualenv to manage Python dependencies
sudo pip3 install virtualenv

# Clone the Flask app repository
git clone https://github.com/spyderboy92/pixel-showroom-api.git || { echo "Git clone failed"; exit 1; }

# Navigate to the cloned repository
cd pixel-showroom-api || { echo "Repository not found"; exit 1; }

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies from requirements.txt
pip install --upgrade pip
pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

# Navigate to the directory containing app.py
cd app || { echo "App directory not found"; exit 1; }

# Determine the number of CPU cores for optimal worker count
CPU_CORES=$(nproc)
WORKERS=$((CPU_CORES * 2 + 1))

# Run the Flask app using Gunicorn
nohup gunicorn --workers "$WORKERS" --threads 2 --bind 0.0.0.0:80 --timeout 240 --chdir /pixel-showroom-api app.app:app > /tmp/gunicorn.log 2>&1 &
