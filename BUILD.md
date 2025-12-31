# Building DICOM Importer Executable

This guide explains how to build a standalone executable (.exe) file for DICOM Importer 2.0 that includes all dependencies and can be distributed without requiring Python installation.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- ~500MB free disk space for build

## Quick Build

### Windows

```batch
build.bat
```

### Linux/Mac

```bash
./build.sh
```

The build script will:
1. Create a virtual environment (if needed)
2. Install all dependencies including PyInstaller
3. Build the standalone executable
4. Place the executable in the `dist/` folder

## Manual Build

If you prefer to build manually:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Build the Executable

```bash
pyinstaller --clean dicom_importer.spec
```

### 3. Find Your Executable

The executable will be in: `dist/DicomImporter.exe` (Windows) or `dist/DicomImporter` (Linux/Mac)

## Build Configuration

The build is configured in `dicom_importer.spec`:

- **Single File**: All dependencies bundled into one .exe
- **No Console**: GUI-only application (no console window)
- **Included Files**: config.example.json, README.md, LICENSE
- **Hidden Imports**: PyQt6, pydicom, pynetdicom modules
- **UPX Compression**: Reduces executable size

## Download Pre-built Executable

### From GitHub Releases

1. Go to the [Releases page](https://github.com/gpdahmen/DicomImporter2/releases)
2. Download the latest release for your platform:
   - **Windows**: `DicomImporter-v2.0.0-windows.exe`
   - **Linux**: `DicomImporter-v2.0.0-linux` (requires `chmod +x`)
   - **Mac**: `DicomImporter-v2.0.0-macos` (requires `chmod +x`)
3. Run the executable directly - no installation needed!

### File Sizes

Expected sizes (may vary by platform):
- Windows: ~120-150 MB
- Linux: ~100-130 MB
- Mac: ~110-140 MB

The executable includes:
- Python interpreter
- PyQt6 GUI framework
- pynetdicom DICOM networking library
- pydicom DICOM file parser
- All other dependencies

## Troubleshooting

### Build Fails with "Module not found"

Add the missing module to `hiddenimports` in `dicom_importer.spec`:

```python
hiddenimports=[
    'pydicom',
    'pynetdicom',
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'your_missing_module',  # Add here
],
```

### Executable is Too Large

The executable size is normal for PyQt6 applications. To reduce size:
1. Remove unused dependencies
2. Use PyInstaller's `--exclude-module` option
3. Consider using a Python installer instead

### Antivirus False Positive

Some antivirus software may flag PyInstaller executables:
- This is a known false positive
- Add the executable to your antivirus exceptions
- Alternatively, users can run from source code

### Linux/Mac Permissions

After downloading or building:
```bash
chmod +x DicomImporter
./DicomImporter
```

## Distribution

### For End Users

Simply distribute the executable from the `dist/` folder. Users can:
1. Download the file
2. Run it directly
3. No Python installation required

### Creating a Portable Package

Include these files in a zip:
```
DicomImporter-v2.0.0/
├── DicomImporter.exe
├── README.md
├── LICENSE
└── config.example.json
```

Users can extract and run immediately.

## GitHub Actions (CI/CD)

To automatically build releases on GitHub:

1. Create `.github/workflows/build.yml`:

```yaml
name: Build Executable

on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt pyinstaller
      - run: pyinstaller --clean dicom_importer.spec
      - uses: actions/upload-release-asset@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ github.event.release.upload_url }}
          asset_path: ./dist/DicomImporter.exe
          asset_name: DicomImporter-${{ github.event.release.tag_name }}-windows.exe
          asset_content_type: application/octet-stream
```

2. Create a new release on GitHub
3. The workflow will automatically build and attach the executable

## Verification

After building, verify the executable:

```bash
# Check file size
ls -lh dist/DicomImporter*

# Test run (should open GUI)
./dist/DicomImporter.exe
```

## Support

For build issues:
- Check the PyInstaller documentation: https://pyinstaller.org/
- Open an issue on GitHub: https://github.com/gpdahmen/DicomImporter2/issues
- Include your platform and error messages
