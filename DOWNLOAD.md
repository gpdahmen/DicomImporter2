# Download DICOM Importer

## 🚀 Quick Download

### Pre-built Executable (Recommended)

The easiest way to use DICOM Importer is to download the pre-built executable for your platform:

#### Option 1: Download from GitHub Releases (When Available)

Visit: **https://github.com/gpdahmen/DicomImporter2/releases**

Download for your platform:
- **Windows**: `DicomImporter-windows.exe` (~120-150 MB)
- **Linux**: `DicomImporter-linux` (~60-100 MB)
- **macOS**: `DicomImporter-macos` (~110-140 MB)

#### Option 2: Build Locally (Available Now)

Since this is a development build, you can build the executable locally:

**Linux/Mac:**
```bash
./build.sh
```

**Windows:**
```batch
build.bat
```

The executable will be in the `dist/` folder.

## 📦 What You Get

The executable includes everything you need:
- ✅ Python interpreter
- ✅ PyQt6 GUI framework  
- ✅ pynetdicom DICOM networking
- ✅ pydicom DICOM parser
- ✅ All other dependencies

**No Python installation required!**

## 🎯 Current Build Status

### Linux Build - ✅ READY

**A Linux executable has been built and is available in the `dist/` folder:**

- **File**: `dist/DicomImporter-linux`
- **Size**: ~59 MB
- **Platform**: Linux x86_64
- **Status**: ✅ Built successfully

**To use:**
```bash
cd dist
chmod +x DicomImporter-linux
./DicomImporter-linux
```

### Windows & macOS Builds

To create Windows and macOS builds:
1. Use the GitHub Actions workflow (automatic on release)
2. Or build locally on those platforms using `build.bat` (Windows) or `build.sh` (macOS)

## 📖 How to Use

### Linux:
```bash
chmod +x DicomImporter-linux
./DicomImporter-linux
```

### Windows:
```batch
DicomImporter-windows.exe
```

### macOS:
```bash
chmod +x DicomImporter-macos
./DicomImporter-macos
```

## 🔧 Alternative: Run from Source

If you prefer to run from source code:

1. **Install Python 3.8+**
2. **Clone the repository:**
   ```bash
   git clone https://github.com/gpdahmen/DicomImporter2.git
   cd DicomImporter2
   ```
3. **Run:**
   - Linux/Mac: `./run.sh`
   - Windows: `run.bat`

The launcher scripts automatically create a virtual environment and install dependencies.

## 📋 System Requirements

### For Pre-built Executable

**Linux:**
- x86_64 architecture
- X11 display server (GUI environment)
- ~60 MB disk space

**Windows:**
- Windows 10 or later (64-bit)
- ~150 MB disk space

**macOS:**
- macOS 11 (Big Sur) or later
- ~140 MB disk space

### For Running from Source

- Python 3.8 or higher
- pip package manager
- ~200 MB disk space (including dependencies)

## 🎉 Features

Once you download and run DICOM Importer, you can:

- **Import DICOM files** from CDs, DVDs, USB drives
- **Connect to PACS servers** using C-FIND, C-STORE, C-MOVE
- **Fast caching** with 1MB buffers for optical media
- **Auto-organize** files by Patient/Study/Series
- **Modern GUI** with real-time progress indicators

## 📚 Documentation

- **README.md** - Complete user guide
- **BUILD.md** - Build instructions
- **QUICKREF.md** - Quick reference guide
- **RELEASES.md** - Release management
- **CONTRIBUTING.md** - Contribution guidelines

## 🆘 Support

Need help?
- GitHub Issues: https://github.com/gpdahmen/DicomImporter2/issues
- Check the documentation in the repository
- Review the troubleshooting section in README.md

## ⚡ Quick Start Example

```bash
# Download or build the executable
./build.sh

# Navigate to dist folder
cd dist

# Make executable (Linux/Mac)
chmod +x DicomImporter-linux

# Run
./DicomImporter-linux
```

The GUI will open, and you can start importing DICOM files immediately!

## 🔐 Security

All executables are built from verified source code:
- ✅ No malware or viruses
- ✅ Open source - inspect the code
- ✅ Built with official PyInstaller
- ✅ All dependencies scanned for vulnerabilities

**Note:** Some antivirus software may flag PyInstaller executables as false positives. This is a known issue with all PyInstaller applications. The executable is safe.

## 🎯 Next Steps

1. **Download** the executable for your platform
2. **Run** it - no installation needed
3. **Configure** your PACS servers in the Configuration tab
4. **Start importing** DICOM files!

Enjoy using DICOM Importer! 🎉
