#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed models

# Initialize database
python init_db.py

# Train the model
python train_model.py

echo "Setup completed! You can now run the server with: python run.py" 