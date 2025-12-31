# DICOM Importer 2.0 - Quick Reference

## Application Overview

**Lines of Code**: 829 lines  
**Classes**: 4 main classes  
**Methods/Functions**: 33 total

## Quick Start

### Linux/Mac
```bash
./run.sh
```

### Windows
```batch
run.bat
```

### Manual Start
```bash
python3 dicom_importer.py
```

## Main Classes

### 1. DicomConfig
Configuration management with JSON persistence.

**Methods:**
- `load_config()` - Load configuration from config.json
- `save_config()` - Save configuration to config.json

**Default Config:**
```json
{
  "local_ae_title": "DICOM_IMPORTER",
  "local_port": 11112,
  "pacs_servers": [],
  "export_destinations": []
}
```

### 2. DicomImportWorker (QThread)
Background worker for importing DICOM files from external media.

**Signals:**
- `progress(int, str)` - Progress percentage and status message
- `finished(list)` - List of imported file paths
- `error(str)` - Error message if import fails

**Features:**
- 1MB buffer size for fast CD/DVD reading
- Automatic Patient/Study/Series organization
- Non-blocking UI during import

### 3. DicomPACSWorker (QThread)
Background worker for PACS network operations.

**Operations:**
- `C-FIND` - Query PACS for patient studies
- `C-MOVE` - Retrieve studies from PACS
- `C-STORE` - Send files to PACS server

**Signals:**
- `progress(str)` - Status message
- `finished(list)` - Operation results
- `error(str)` - Error message if operation fails

### 4. DicomImporterGUI (QMainWindow)
Main application window with PyQt6.

**Tabs:**
1. **Import from Media** - Import DICOM files from CD/DVD/USB
2. **PACS Operations** - Query and send to PACS servers
3. **Configuration** - Manage AE titles and PACS servers

## Common Workflows

### Import Files from CD/DVD
1. Insert media
2. Open "Import from Media" tab
3. Browse to CD/DVD mount point
4. Select destination folder
5. Click "Start Import"
6. Monitor progress bar

### Query PACS Server
1. Configure PACS server in "Configuration" tab
2. Go to "PACS Operations" tab
3. Select PACS server
4. Enter search criteria (Patient Name, ID, Date)
5. Click "C-FIND (Query)"
6. View results

### Send Files to PACS
1. Import files first (see above)
2. Go to "PACS Operations" tab
3. Select destination PACS server
4. Click "C-STORE (Send)"
5. Monitor progress

## File Organization

Imported files are organized as:
```
destination/
├── PatientID/
│   └── StudyInstanceUID/
│       └── SeriesInstanceUID/
│           ├── file001.dcm
│           ├── file002.dcm
│           └── ...
```

## Configuration

### Add PACS Server
1. Go to "Configuration" tab
2. Fill in PACS server details:
   - Name: Friendly name
   - AE Title: PACS AE title
   - IP Address: PACS server IP
   - Port: PACS server port (typically 11112 or 104)
3. Click "Add PACS Server"
4. Click "Save Configuration"

### Local AE Configuration
- **AE Title**: Your application's AE title (default: DICOM_IMPORTER)
- **Port**: Your application's port (default: 11112)

## Performance Tips

### For CD/DVD Import
- Use the optimized 1MB buffer (automatic)
- Sequential reading is fastest
- Consider copying entire CD to hard drive first for multiple operations

### For USB Import
- Much faster than optical media
- Can handle thousands of files efficiently

### For PACS Operations
- Ensure network connectivity
- Check firewall settings (ports 11112, 104)
- Verify PACS server has your AE title registered

## Troubleshooting

### Import Issues
- **No files found**: Check media is mounted and accessible
- **Permission denied**: Ensure write permissions on destination
- **Non-DICOM files skipped**: This is normal behavior

### PACS Connection Issues
- **Connection refused**: Check IP, port, and AE title
- **Association failed**: Verify PACS has your AE title registered
- **Timeout**: Check network connectivity and firewall

### GUI Issues
- **Window not appearing**: Ensure DISPLAY is set (Linux)
- **Frozen UI**: This shouldn't happen - all operations are threaded

## Dependencies

- **pynetdicom** >= 2.0.2 - DICOM networking
- **pydicom** >= 2.4.0 - DICOM file handling
- **PyQt6** >= 6.6.0 - Modern GUI framework

## Support

- GitHub Issues: Report bugs and request features
- Documentation: See README.md
- Contributing: See CONTRIBUTING.md

## License

MIT License - See LICENSE file for details
