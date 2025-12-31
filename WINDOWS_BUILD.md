# Building Windows Executable

## Important Note About Cross-Platform Builds

**PyInstaller cannot cross-compile.** This means:
- Windows .exe files must be built on Windows
- Linux executables must be built on Linux  
- macOS executables must be built on macOS

## How to Get a Windows .exe

### Option 1: Automatic Build via GitHub Actions (Recommended) 🤖

The repository is already configured to automatically build Windows, Linux, and macOS executables.

**Steps:**
1. Go to: https://github.com/gpdahmen/DicomImporter2/releases
2. Click **"Draft a new release"**
3. Create a tag (e.g., `v2.0.0`)
4. Add a title: "DICOM Importer v2.0.0"
5. Click **"Publish release"**

**GitHub Actions will automatically:**
- ✅ Build `DicomImporter-windows.exe` on Windows runner
- ✅ Build `DicomImporter-linux` on Linux runner
- ✅ Build `DicomImporter-macos` on macOS runner
- ✅ Upload all executables to the release (~10-15 minutes)

**Download from:** https://github.com/gpdahmen/DicomImporter2/releases/latest

### Option 2: Build Locally on Windows 💻

If you have access to a Windows machine:

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/gpdahmen/DicomImporter2.git
   cd DicomImporter2
   ```

2. **Run the build script:**
   ```cmd
   build.bat
   ```

3. **Find your executable:**
   ```
   dist\DicomImporter.exe
   ```

The script will:
- Create a virtual environment
- Install all dependencies
- Run PyInstaller
- Create a standalone .exe (~120-150 MB)

### Option 3: Manual Build on Windows ⚙️

If you prefer manual steps:

```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Build executable
pyinstaller --clean dicom_importer.spec

# Executable will be in: dist\DicomImporter.exe
```

## Current Build Status

| Platform | Status | Location | Size |
|----------|--------|----------|------|
| **Linux** | ✅ Built | `dist/DicomImporter-linux` | 59 MB |
| **Windows** | ⏳ Pending | Build on Windows or via GitHub Actions | ~120-150 MB |
| **macOS** | ⏳ Pending | Build on macOS or via GitHub Actions | ~110-140 MB |

## Why Can't We Build Windows .exe on Linux?

PyInstaller works by:
1. Bundling the Python interpreter from the current system
2. Packaging system-specific libraries
3. Creating an executable for the current OS

**Technical limitations:**
- Windows .exe requires Windows system libraries
- Windows uses different executable formats (PE) than Linux (ELF)
- DLL dependencies are Windows-specific
- No reliable cross-compilation toolchain exists for Python+PyQt6

## Recommended Approach

**Use GitHub Actions (Option 1)** - This is the easiest and most reliable method:

1. It builds on actual Windows, Linux, and macOS machines
2. No local setup needed
3. Automatic and repeatable
4. All platforms built simultaneously
5. Executables automatically attached to release

**Just create a GitHub Release, and you'll have all three executables in ~15 minutes!**

## Alternative: Virtual Machine or Container

If you need to build locally without Windows:
- Use a Windows VM (VirtualBox, VMware)
- Use a cloud Windows instance (Azure, AWS)
- Use GitHub Codespaces with Windows container (if available)

However, **GitHub Actions is much simpler** than any of these alternatives.

## Support

For questions about building:
- See: [BUILD.md](BUILD.md) for detailed instructions
- See: [RELEASES.md](RELEASES.md) for GitHub Release instructions
- Open an issue if you need help
