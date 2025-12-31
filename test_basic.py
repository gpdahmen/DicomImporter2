#!/usr/bin/env python3
"""
Simple test script to verify DICOM Importer functionality
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Test imports
print("Testing imports...")
try:
    import pydicom
    print("✓ pydicom imported successfully")
except ImportError as e:
    print(f"✗ pydicom import failed: {e}")
    sys.exit(1)

try:
    from pynetdicom import AE
    print("✓ pynetdicom imported successfully")
except ImportError as e:
    print(f"✗ pynetdicom import failed: {e}")
    sys.exit(1)

try:
    from PyQt6.QtWidgets import QApplication
    print("✓ PyQt6 imported successfully")
except ImportError as e:
    print(f"✗ PyQt6 import failed: {e}")
    sys.exit(1)

# Test DicomConfig
print("\nTesting DicomConfig...")
from dicom_importer import DicomConfig

config = DicomConfig("test_config.json")
print(f"✓ DicomConfig created with AE title: {config.config['local_ae_title']}")

# Test adding PACS server
config.config['pacs_servers'].append({
    'name': 'Test PACS',
    'ae_title': 'TEST_PACS',
    'ip': '127.0.0.1',
    'port': 11112
})
config.save_config()
print("✓ Configuration saved successfully")

# Reload config
config2 = DicomConfig("test_config.json")
assert len(config2.config['pacs_servers']) == 1
assert config2.config['pacs_servers'][0]['name'] == 'Test PACS'
print("✓ Configuration loaded and verified")

# Clean up
os.remove("test_config.json")

# Test creating a simple DICOM file
print("\nTesting DICOM file creation...")
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid
import datetime

# Create a simple test DICOM file
file_meta = Dataset()
file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1'
file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
file_meta.MediaStorageSOPInstanceUID = generate_uid()

ds = FileDataset("test.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)
ds.PatientName = "Test^Patient"
ds.PatientID = "12345"
ds.StudyInstanceUID = generate_uid()
ds.SeriesInstanceUID = generate_uid()
ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
ds.SOPClassUID = file_meta.MediaStorageSOPClassUID
ds.StudyDate = datetime.datetime.now().strftime('%Y%m%d')
ds.Modality = "CT"

# Save test DICOM file
with tempfile.TemporaryDirectory() as tmpdir:
    test_file = os.path.join(tmpdir, "test.dcm")
    ds.save_as(test_file, write_like_original=False)
    print(f"✓ Test DICOM file created: {test_file}")
    
    # Verify it can be read
    ds_read = pydicom.dcmread(test_file)
    assert ds_read.PatientName == "Test^Patient"
    assert ds_read.PatientID == "12345"
    print("✓ Test DICOM file verified")

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
print("\nThe application is ready to use.")
print("Run: python dicom_importer.py")
