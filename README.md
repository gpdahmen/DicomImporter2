# DICOM Importer 2.0

A modern, user-friendly application for efficient import of DICOM files from external media (CDs, DVDs, USB drives) or remote PACS servers, with export capabilities to local network folders or PACS servers.

## Features Overview

| Feature | Description | Status |
|---------|-------------|--------|
| 🎨 Modern GUI | PyQt6-based tabbed interface | ✅ Complete |
| 💿 CD/DVD Import | Fast import with 1MB buffer caching | ✅ Complete |
| 🔌 USB Import | High-speed import from USB drives | ✅ Complete |
| 🏥 C-FIND | Query PACS for patient studies | ✅ Complete |
| 📤 C-STORE | Send files to PACS servers | ✅ Complete |
| 📥 C-MOVE | Retrieve studies from PACS | ⚠️ Planned |
| 🧵 Multi-threading | Non-blocking UI operations | ✅ Complete |
| ⚙️ Configuration | Persistent PACS server management | ✅ Complete |
| 📁 Auto-organization | Patient/Study/Series hierarchy | ✅ Complete |

## Features

### 🎨 Modern GUI
- Built with PyQt6 for a clean, intuitive user interface
- Tabbed interface for organized workflow
- Real-time progress indicators and status updates

### 🏥 PACS Integration
- Full support for DICOM networking via `pynetdicom`
- **C-FIND**: Query remote PACS servers for patient studies
- **C-MOVE**: Retrieve studies from PACS
- **C-STORE**: Send DICOM files to PACS servers

### ⚡ Fast Performance
- Multi-threaded architecture keeps UI responsive during long operations
- Optimized file caching with 1MB buffers for fast CD/DVD reading
- Background workers handle all I/O operations

### 🔧 Configuration Management
- Easy setup of Application Entity (AE) titles, IPs, and ports
- Manage multiple PACS server destinations
- Persistent configuration storage

### 📁 Smart Organization
- Automatic file organization by Patient/Study/Series hierarchy
- Creates clean directory structures for imported files
- Handles DICOM metadata extraction and sanitization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start (Recommended)

#### Linux/Mac:
```bash
./run.sh
```

#### Windows:
```batch
run.bat
```

The launcher scripts will automatically:
- Create a virtual environment (if needed)
- Install dependencies
- Start the application

### Manual Installation

Install dependencies manually:

```bash
pip install -r requirements.txt
```

This will install:
- `pynetdicom` - DICOM networking library
- `pydicom` - DICOM file reading/writing
- `PyQt6` - Modern GUI framework

## Usage

### Starting the Application

```bash
python dicom_importer.py
```

### Import from External Media (CD/DVD/USB)

1. Navigate to the **"Import from Media"** tab
2. Click **"Browse..."** next to "Source Path" and select your CD/DVD/USB drive
3. Click **"Browse..."** next to "Destination Path" and select where to save files
4. Click **"Start Import"**
5. Monitor progress in real-time
6. Files will be organized automatically by Patient/Study/Series

### PACS Operations

#### Configure PACS Servers

1. Navigate to the **"Configuration"** tab
2. Under "PACS Servers" section, fill in:
   - Name: A friendly name for your PACS server
   - AE Title: The PACS server's Application Entity title
   - IP Address: The PACS server IP
   - Port: The PACS server port (typically 11112 or 104)
3. Click **"Add PACS Server"**
4. Click **"Save Configuration"**

#### Query PACS (C-FIND)

1. Navigate to the **"PACS Operations"** tab
2. Select a PACS server from the dropdown
3. Enter search criteria:
   - Patient Name (use * as wildcard)
   - Patient ID
   - Study Date (YYYYMMDD format)
4. Click **"C-FIND (Query)"**
5. View results in the results panel

#### Send Files to PACS (C-STORE)

1. First import files using the "Import from Media" tab
2. Navigate to the **"PACS Operations"** tab
3. Select a destination PACS server
4. Click **"C-STORE (Send)"**
5. Monitor the progress as files are transmitted

### Configuration

The application stores configuration in `config.json` which includes:

```json
{
  "local_ae_title": "DICOM_IMPORTER",
  "local_port": 11112,
  "pacs_servers": [
    {
      "name": "Hospital PACS",
      "ae_title": "HOSPITAL_PACS",
      "ip": "192.168.1.100",
      "port": 11112
    }
  ],
  "export_destinations": []
}
```

## Architecture

### Threading Model

The application uses QThread-based workers to keep the UI responsive:

- **DicomImportWorker**: Handles file import operations in the background
- **DicomPACSWorker**: Manages PACS network operations (C-FIND, C-MOVE, C-STORE)

All worker threads communicate with the main UI via Qt signals, ensuring thread-safe updates.

### Fast Caching

For CD/DVD reading, the application uses optimized buffering:
- 1MB read buffers minimize CD/DVD seeks
- Sequential reading pattern maximizes cache efficiency
- Background threading prevents UI freezing during reads

### File Organization

Imported files are automatically organized in a hierarchical structure:
```
destination/
├── PatientID/
│   └── StudyInstanceUID/
│       └── SeriesInstanceUID/
│           ├── file1.dcm
│           ├── file2.dcm
│           └── ...
```

## Troubleshooting

### PACS Connection Issues

- Verify the PACS server IP, port, and AE title are correct
- Ensure your firewall allows DICOM traffic (typically port 11112 or 104)
- Check that the PACS server has your local AE title registered

### Import Issues

- Ensure the source media is mounted and accessible
- Check file permissions on the destination directory
- For non-DICOM files, they will be automatically skipped

### Performance

- For large imports (thousands of files), be patient - the progress bar shows real-time status
- CD/DVD reading is optimized but still limited by optical drive speed
- USB drives will be significantly faster than optical media

## Development

### Project Structure

```
DicomImporter2/
├── dicom_importer.py      # Main application (30KB)
├── requirements.txt       # Python dependencies
├── setup.py              # Package installation config
├── test_basic.py         # Basic functionality tests
├── run.sh                # Linux/Mac launcher
├── run.bat               # Windows launcher
├── config.example.json   # Configuration template
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── CONTRIBUTING.md      # Contribution guidelines
└── README.md            # This file
```

### Key Classes

- **DicomConfig**: Configuration management with JSON persistence
- **DicomImportWorker**: QThread-based worker for file imports from external media
- **DicomPACSWorker**: QThread-based worker for PACS operations (C-FIND, C-MOVE, C-STORE)
- **DicomImporterGUI**: Main Qt6 window with three-tab interface and signal-based updates

## License

This project is open source. Please check the repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or feature requests, please use the GitHub issue tracker.
