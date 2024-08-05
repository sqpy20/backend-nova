#!/bin/bash

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Check if pip install was successful
if [ $? -eq 0 ]; then
    echo "Requirements installed successfully."
else
    echo "Error: Failed to install requirements."
    exit 1
fi

# Run create_db.py
echo "Creating database..."
python create_db.py

# Check if create_db.py was successful
if [ $? -eq 0 ]; then
    echo "Database created successfully."
else
    echo "Error: Failed to create database."
    exit 1
fi

echo "Setup completed successfully."
