#!/bin/bash

# Update the package index
sudo yum update -y

# Install necessary packages
sudo yum install -y git python3 python3-pip

# Install virtualenv to manage Python dependencies
sudo pip3 install virtualenv

# Clone the Flask app repository
git clone https://github.com/spyderboy92/pixel-showroom-api.git || { echo "Git clone failed"; exit 1; }

# Navigate to the cloned repository
cd pixel-showroom-api || { echo "Repository not found"; exit 1; }

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies while resolving conflicts
pip install --upgrade pip
pip install -r requirements.txt || { echo "Failed to install requirements"; exit 1; }

# Navigate to the directory containing app.py
cd app || { echo "API directory not found"; exit 1; }

# Export Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Run the Flask app
nohup flask run --host=0.0.0.0 --port=80 > /tmp/flask.log 2>&1 &
