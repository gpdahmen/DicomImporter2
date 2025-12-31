@echo off
REM DICOM Importer Launcher Script for Windows

echo ========================================
echo    DICOM Importer 2.0
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
python -c "import pynetdicom" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -q -r requirements.txt
    echo Dependencies installed
)

REM Run the application
echo Starting DICOM Importer...
echo.
python dicom_importer.py

REM Deactivate virtual environment
deactivate

pause
