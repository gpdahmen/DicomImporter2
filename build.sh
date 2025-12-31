#!/bin/bash
# Build script for DICOM Importer executable
# This script creates a standalone .exe file for Windows distribution

echo "========================================"
echo "   DICOM Importer 2.0 - Build Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q pyinstaller

# Clean previous build
echo "Cleaning previous build..."
rm -rf build dist
echo "✓ Cleaned"

# Build the executable
echo ""
echo "Building executable..."
echo "This may take a few minutes..."
pyinstaller --clean dicom_importer.spec

# Check if build was successful
if [ -f "dist/DicomImporter.exe" ] || [ -f "dist/DicomImporter" ]; then
    echo ""
    echo "========================================"
    echo "   Build Successful!"
    echo "========================================"
    echo ""
    echo "Executable location: dist/DicomImporter.exe"
    echo "File size: $(du -h dist/DicomImporter* | cut -f1)"
    echo ""
    echo "You can now distribute the executable in the 'dist' folder."
    echo "The executable includes all dependencies and can run standalone."
else
    echo ""
    echo "========================================"
    echo "   Build Failed!"
    echo "========================================"
    echo "Check the output above for errors."
    exit 1
fi

# Deactivate virtual environment
deactivate
