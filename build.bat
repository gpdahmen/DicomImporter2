@echo off
REM Build script for DICOM Importer executable (Windows)
REM This script creates a standalone .exe file for Windows distribution

echo ========================================
echo    DICOM Importer 2.0 - Build Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed
    pause
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Clean previous build
echo Cleaning previous build...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
echo Cleaned

REM Build the executable
echo.
echo Building executable...
echo This may take a few minutes...
pyinstaller --clean dicom_importer.spec

REM Check if build was successful
if exist "dist\DicomImporter.exe" (
    echo.
    echo ========================================
    echo    Build Successful!
    echo ========================================
    echo.
    echo Executable location: dist\DicomImporter.exe
    for %%I in (dist\DicomImporter.exe) do echo File size: %%~zI bytes
    echo.
    echo You can now distribute the executable in the 'dist' folder.
    echo The executable includes all dependencies and can run standalone.
) else (
    echo.
    echo ========================================
    echo    Build Failed!
    echo ========================================
    echo Check the output above for errors.
    pause
    exit /b 1
)

REM Deactivate virtual environment
deactivate

pause
