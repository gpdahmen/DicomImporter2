#!/bin/bash
# DICOM Importer Launcher Script

echo "========================================"
echo "   DICOM Importer 2.0"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python3 -c "import pynetdicom" &> /dev/null; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Run the application
echo "Starting DICOM Importer..."
echo ""
python3 dicom_importer.py

# Deactivate virtual environment
deactivate
