# Creating and Downloading Releases

This document explains how to download pre-built executables and how maintainers can create new releases.

## For Users: Downloading Executables

### Step 1: Go to Releases Page

Visit: https://github.com/gpdahmen/DicomImporter2/releases

### Step 2: Download for Your Platform

Click on the latest release and download:

| Platform | File | Size | Notes |
|----------|------|------|-------|
| Windows | `DicomImporter-windows.exe` | ~120-150 MB | Double-click to run |
| Linux | `DicomImporter-linux` | ~100-130 MB | Run `chmod +x` first |
| macOS | `DicomImporter-macos` | ~110-140 MB | Run `chmod +x` first |

### Step 3: Run the Application

**Windows:**
```batch
# Just double-click DicomImporter-windows.exe
# Or from command line:
DicomImporter-windows.exe
```

**Linux:**
```bash
chmod +x DicomImporter-linux
./DicomImporter-linux
```

**macOS:**
```bash
chmod +x DicomImporter-macos
./DicomImporter-macos
```

### No Installation Needed!

The executable includes everything:
- ✅ Python interpreter
- ✅ PyQt6 GUI framework
- ✅ pynetdicom DICOM networking
- ✅ pydicom DICOM parser
- ✅ All other dependencies

Just download and run - no Python installation required!

## For Maintainers: Creating New Releases

### Automated Build (Recommended)

Releases are automatically built via GitHub Actions when you create a new release tag.

#### Step 1: Create a Release on GitHub

1. Go to: https://github.com/gpdahmen/DicomImporter2/releases
2. Click "Draft a new release"
3. Create a new tag (e.g., `v2.0.0`, `v2.1.0`)
4. Enter release title: "DICOM Importer v2.0.0"
5. Add release notes (see template below)
6. Click "Publish release"

#### Step 2: Wait for Builds

GitHub Actions will automatically:
1. Build executables for Windows, Linux, and macOS
2. Upload them to the release
3. Takes ~10-15 minutes total

You can monitor progress at: https://github.com/gpdahmen/DicomImporter2/actions

#### Step 3: Verify Downloads

Once complete, the release page will show:
- ✅ DicomImporter-windows.exe
- ✅ DicomImporter-linux
- ✅ DicomImporter-macos

### Manual Build (Alternative)

If you prefer to build manually:

#### Windows:
```batch
build.bat
cd dist
ren DicomImporter.exe DicomImporter-windows.exe
```

#### Linux:
```bash
./build.sh
cd dist
mv DicomImporter DicomImporter-linux
chmod +x DicomImporter-linux
```

#### macOS:
```bash
./build.sh
cd dist
mv DicomImporter DicomImporter-macos
chmod +x DicomImporter-macos
```

Then manually upload to GitHub release.

## Release Notes Template

Use this template when creating a new release:

```markdown
## DICOM Importer v2.0.0

### Downloads

Choose your platform:
- **Windows**: [DicomImporter-windows.exe](#)
- **Linux**: [DicomImporter-linux](#)
- **macOS**: [DicomImporter-macos](#)

### What's New

- New feature 1
- New feature 2
- Bug fix 1

### Installation

**No Python required!** Just download and run the executable for your platform.

**Linux/Mac users:** Run `chmod +x DicomImporter-*` first.

### Requirements

None - all dependencies included in the executable.

### Known Issues

- Issue 1 (if any)
- Issue 2 (if any)

### Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete details.
```

## Versioning

Follow [Semantic Versioning](https://semver.org/):

- **Major** (v2.0.0): Breaking changes
- **Minor** (v2.1.0): New features, backwards compatible
- **Patch** (v2.0.1): Bug fixes only

## Testing Releases

Before publishing, test the executables:

1. **Windows**: Test on Windows 10/11
2. **Linux**: Test on Ubuntu 20.04+ or similar
3. **macOS**: Test on macOS 11+ (Big Sur or later)

### Test Checklist:

- [ ] Application launches without errors
- [ ] GUI displays correctly
- [ ] Can browse for files/folders
- [ ] Import functionality works
- [ ] PACS configuration can be saved
- [ ] No antivirus false positives (expected, but verify)

## Troubleshooting Builds

### Build Fails in GitHub Actions

Check the Actions logs:
1. Go to Actions tab
2. Click on the failed workflow
3. Expand the failed step
4. Check error messages

Common issues:
- Missing dependencies in requirements.txt
- PyInstaller spec file errors
- Python version incompatibilities

### Antivirus False Positives

PyInstaller executables may trigger antivirus warnings:
- This is a known issue with all PyInstaller apps
- The executable is safe (built from source)
- Add note in release notes about this
- Users can add to antivirus exceptions

### Large File Sizes

Expected sizes:
- Windows: 120-150 MB (includes PyQt6)
- Linux: 100-130 MB
- macOS: 110-140 MB

This is normal for PyQt6 applications. All dependencies are bundled.

## Distribution Channels

### GitHub Releases (Primary)

- https://github.com/gpdahmen/DicomImporter2/releases
- Direct download links
- Automatic builds via Actions

### Alternative Distribution

For broader distribution, consider:
- PyPI (for Python package)
- Windows Microsoft Store
- Linux Snap Store / AppImage
- macOS Homebrew

## Support

For release issues:
- Create an issue: https://github.com/gpdahmen/DicomImporter2/issues
- Include platform, error messages, and steps to reproduce
