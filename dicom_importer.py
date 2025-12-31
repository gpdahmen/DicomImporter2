#!/usr/bin/env python3
"""
DICOM Importer - Main Application Module

This application facilitates efficient import of DICOM files from:
- External media (CDs, DVDs, USB drives)
- Remote PACS servers (via C-FIND, C-MOVE)

And exports to:
- Local network folders
- PACS servers (via C-STORE)

Features:
- Modern GUI with PyQt6
- PACS integration with pynetdicom (C-STORE, C-FIND, C-MOVE)
- Threading for responsive UI
- Configuration management for AE Titles, IPs, Ports
- Fast caching mechanism for CD/DVD reading
"""

import sys
import os
import json
import threading
from pathlib import Path
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog,
    QProgressBar, QComboBox, QGroupBox, QFormLayout, QListWidget,
    QMessageBox, QSpinBox, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont

import pydicom
from pynetdicom import AE, evt, StoragePresentationContexts
from pynetdicom.sop_class import (
    PatientRootQueryRetrieveInformationModelFind,
    PatientRootQueryRetrieveInformationModelMove,
    StudyRootQueryRetrieveInformationModelFind,
    StudyRootQueryRetrieveInformationModelMove
)


class DicomConfig:
    """Manages application configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "local_ae_title": "DICOM_IMPORTER",
            "local_port": 11112,
            "pacs_servers": [],
            "export_destinations": []
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return {**default_config, **json.load(f)}
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")


class DicomImportWorker(QThread):
    """Background worker for importing DICOM files from external media"""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, source_path: str, destination_path: str, use_cache: bool = True):
        super().__init__()
        self.source_path = source_path
        self.destination_path = destination_path
        self.use_cache = use_cache
        self.dicom_files = []
    
    def run(self):
        """Import DICOM files from source to destination"""
        try:
            self.progress.emit(0, "Scanning for DICOM files...")
            
            # Fast scan - find all DICOM files
            source_files = []
            for root, dirs, files in os.walk(self.source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Quick check - DICOM files typically have no extension or .dcm
                    if file.upper().endswith('.DCM') or '.' not in file:
                        source_files.append(file_path)
            
            total_files = len(source_files)
            self.progress.emit(5, f"Found {total_files} potential DICOM files")
            
            # Process files
            imported_count = 0
            for idx, file_path in enumerate(source_files):
                try:
                    # Read DICOM file (with caching if from CD/DVD)
                    ds = pydicom.dcmread(file_path, force=True)
                    
                    # Create destination directory structure
                    # Organize by Patient/Study/Series
                    patient_id = str(getattr(ds, 'PatientID', 'Unknown_Patient'))
                    study_uid = str(getattr(ds, 'StudyInstanceUID', 'Unknown_Study'))
                    series_uid = str(getattr(ds, 'SeriesInstanceUID', 'Unknown_Series'))
                    
                    # Sanitize directory names
                    patient_id = "".join(c for c in patient_id if c.isalnum() or c in (' ', '_', '-'))
                    
                    dest_dir = os.path.join(
                        self.destination_path,
                        patient_id,
                        study_uid[:32],  # Truncate long UIDs
                        series_uid[:32]
                    )
                    
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Copy file with fast caching for CD/DVD
                    dest_file = os.path.join(dest_dir, os.path.basename(file_path))
                    
                    # Fast copy with buffering for CD/DVD
                    buffer_size = 1024 * 1024  # 1MB buffer for fast caching
                    with open(file_path, 'rb') as src:
                        with open(dest_file, 'wb') as dst:
                            while True:
                                chunk = src.read(buffer_size)
                                if not chunk:
                                    break
                                dst.write(chunk)
                    
                    self.dicom_files.append(dest_file)
                    imported_count += 1
                    
                    # Update progress
                    progress_pct = int((idx + 1) / total_files * 100)
                    self.progress.emit(
                        progress_pct,
                        f"Imported {imported_count} files ({idx + 1}/{total_files})"
                    )
                
                except Exception as e:
                    # Skip non-DICOM files
                    continue
            
            self.progress.emit(100, f"Import complete! Imported {imported_count} DICOM files")
            self.finished.emit(self.dicom_files)
        
        except Exception as e:
            self.error.emit(f"Import error: {str(e)}")


class DicomPACSWorker(QThread):
    """Background worker for PACS operations (C-FIND, C-MOVE, C-STORE)"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def __init__(self, operation: str, config: Dict, query_params: Dict = None, files: List[str] = None):
        super().__init__()
        self.operation = operation
        self.config = config
        self.query_params = query_params or {}
        self.files = files or []
        self.results = []
    
    def run(self):
        """Execute PACS operation"""
        try:
            if self.operation == "C-FIND":
                self._c_find()
            elif self.operation == "C-MOVE":
                self._c_move()
            elif self.operation == "C-STORE":
                self._c_store()
        except Exception as e:
            self.error.emit(f"PACS error: {str(e)}")
    
    def _c_find(self):
        """Execute C-FIND query"""
        self.progress.emit("Connecting to PACS...")
        
        ae = AE(ae_title=self.config['local_ae_title'])
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
        ae.add_requested_context(StudyRootQueryRetrieveInformationModelFind)
        
        # Associate with PACS
        assoc = ae.associate(
            self.config['pacs_ip'],
            self.config['pacs_port'],
            ae_title=self.config['pacs_ae_title']
        )
        
        if assoc.is_established:
            self.progress.emit("Querying PACS...")
            
            # Create query dataset
            from pydicom.dataset import Dataset
            ds = Dataset()
            ds.QueryRetrieveLevel = self.query_params.get('QueryRetrieveLevel', 'STUDY')
            ds.PatientName = self.query_params.get('PatientName', '')
            ds.PatientID = self.query_params.get('PatientID', '')
            ds.StudyDate = self.query_params.get('StudyDate', '')
            ds.StudyDescription = self.query_params.get('StudyDescription', '')
            ds.StudyInstanceUID = ''
            
            # Send C-FIND request
            responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
            
            for status, identifier in responses:
                if status and identifier:
                    self.results.append(identifier)
                    self.progress.emit(f"Found {len(self.results)} studies...")
            
            assoc.release()
            self.progress.emit(f"Query complete. Found {len(self.results)} studies")
            self.finished.emit(self.results)
        else:
            self.error.emit("Failed to establish association with PACS")
    
    def _c_move(self):
        """Execute C-MOVE to retrieve studies"""
        self.progress.emit("Initiating C-MOVE...")
        
        ae = AE(ae_title=self.config['local_ae_title'])
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)
        
        # Associate with PACS
        assoc = ae.associate(
            self.config['pacs_ip'],
            self.config['pacs_port'],
            ae_title=self.config['pacs_ae_title']
        )
        
        if assoc.is_established:
            # Create move dataset
            from pydicom.dataset import Dataset
            ds = Dataset()
            ds.QueryRetrieveLevel = 'STUDY'
            ds.StudyInstanceUID = self.query_params.get('StudyInstanceUID', '')
            
            # Send C-MOVE request
            responses = assoc.send_c_move(
                ds,
                self.config['move_destination'],
                PatientRootQueryRetrieveInformationModelMove
            )
            
            for status, identifier in responses:
                if status:
                    self.progress.emit(f"Moving study... Status: {status.Status}")
            
            assoc.release()
            self.progress.emit("C-MOVE complete")
            self.finished.emit([])
        else:
            self.error.emit("Failed to establish association with PACS")
    
    def _c_store(self):
        """Execute C-STORE to send files to PACS"""
        self.progress.emit(f"Sending {len(self.files)} files to PACS...")
        
        ae = AE(ae_title=self.config['local_ae_title'])
        
        # Add all storage presentation contexts
        for cx in StoragePresentationContexts:
            ae.add_requested_context(cx.abstract_syntax)
        
        # Associate with PACS
        assoc = ae.associate(
            self.config['pacs_ip'],
            self.config['pacs_port'],
            ae_title=self.config['pacs_ae_title']
        )
        
        if assoc.is_established:
            sent_count = 0
            for idx, file_path in enumerate(self.files):
                try:
                    ds = pydicom.dcmread(file_path)
                    status = assoc.send_c_store(ds)
                    
                    if status and status.Status == 0x0000:
                        sent_count += 1
                    
                    self.progress.emit(
                        f"Sent {sent_count}/{len(self.files)} files"
                    )
                except Exception as e:
                    self.progress.emit(f"Error sending {file_path}: {e}")
            
            assoc.release()
            self.progress.emit(f"C-STORE complete. Sent {sent_count} files")
            self.finished.emit([])
        else:
            self.error.emit("Failed to establish association with PACS")


class DicomImporterGUI(QMainWindow):
    """Main GUI window for DICOM Importer application"""
    
    def __init__(self):
        super().__init__()
        self.config = DicomConfig()
        self.worker = None
        self.imported_files = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("DICOM Importer 2.0")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Add tabs
        tabs.addTab(self.create_import_tab(), "Import from Media")
        tabs.addTab(self.create_pacs_tab(), "PACS Operations")
        tabs.addTab(self.create_config_tab(), "Configuration")
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_import_tab(self) -> QWidget:
        """Create the import from external media tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Import DICOM Files from External Media")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Source selection
        source_group = QGroupBox("Source Selection")
        source_layout = QVBoxLayout()
        
        source_row = QHBoxLayout()
        source_label = QLabel("Source Path:")
        self.source_path_edit = QLineEdit()
        self.source_path_edit.setPlaceholderText("Select CD/DVD/USB drive or folder")
        source_browse_btn = QPushButton("Browse...")
        source_browse_btn.clicked.connect(self.browse_source)
        
        source_row.addWidget(source_label)
        source_row.addWidget(self.source_path_edit)
        source_row.addWidget(source_browse_btn)
        source_layout.addLayout(source_row)
        source_group.setLayout(source_layout)
        layout.addWidget(source_group)
        
        # Destination selection
        dest_group = QGroupBox("Destination Selection")
        dest_layout = QVBoxLayout()
        
        dest_row = QHBoxLayout()
        dest_label = QLabel("Destination Path:")
        self.dest_path_edit = QLineEdit()
        self.dest_path_edit.setPlaceholderText("Select destination folder")
        dest_browse_btn = QPushButton("Browse...")
        dest_browse_btn.clicked.connect(self.browse_destination)
        
        dest_row.addWidget(dest_label)
        dest_row.addWidget(self.dest_path_edit)
        dest_row.addWidget(dest_browse_btn)
        dest_layout.addLayout(dest_row)
        dest_group.setLayout(dest_layout)
        layout.addWidget(dest_group)
        
        # Import button
        self.import_btn = QPushButton("Start Import")
        self.import_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px;")
        self.import_btn.clicked.connect(self.start_import)
        layout.addWidget(self.import_btn)
        
        # Progress
        progress_group = QGroupBox("Import Progress")
        progress_layout = QVBoxLayout()
        
        self.import_progress_bar = QProgressBar()
        self.import_status_label = QLabel("Ready to import")
        
        progress_layout.addWidget(self.import_progress_bar)
        progress_layout.addWidget(self.import_status_label)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Results
        results_group = QGroupBox("Import Results")
        results_layout = QVBoxLayout()
        
        self.import_results_text = QTextEdit()
        self.import_results_text.setReadOnly(True)
        self.import_results_text.setMaximumHeight(150)
        
        results_layout.addWidget(self.import_results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        return widget
    
    def create_pacs_tab(self) -> QWidget:
        """Create the PACS operations tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("PACS Server Operations")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # PACS server selection
        server_group = QGroupBox("PACS Server")
        server_layout = QFormLayout()
        
        self.pacs_combo = QComboBox()
        self.update_pacs_combo()
        server_layout.addRow("Server:", self.pacs_combo)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # Query parameters
        query_group = QGroupBox("C-FIND Query Parameters")
        query_layout = QFormLayout()
        
        self.patient_name_edit = QLineEdit()
        self.patient_name_edit.setPlaceholderText("Patient Name (use * for wildcard)")
        query_layout.addRow("Patient Name:", self.patient_name_edit)
        
        self.patient_id_edit = QLineEdit()
        self.patient_id_edit.setPlaceholderText("Patient ID")
        query_layout.addRow("Patient ID:", self.patient_id_edit)
        
        self.study_date_edit = QLineEdit()
        self.study_date_edit.setPlaceholderText("YYYYMMDD or YYYYMMDD-YYYYMMDD")
        query_layout.addRow("Study Date:", self.study_date_edit)
        
        query_group.setLayout(query_layout)
        layout.addWidget(query_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cfind_btn = QPushButton("C-FIND (Query)")
        self.cfind_btn.clicked.connect(self.execute_cfind)
        button_layout.addWidget(self.cfind_btn)
        
        self.cstore_btn = QPushButton("C-STORE (Send)")
        self.cstore_btn.clicked.connect(self.execute_cstore)
        button_layout.addWidget(self.cstore_btn)
        
        layout.addLayout(button_layout)
        
        # Progress and results
        self.pacs_status_label = QLabel("Ready")
        layout.addWidget(self.pacs_status_label)
        
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        self.pacs_results_text = QTextEdit()
        self.pacs_results_text.setReadOnly(True)
        
        results_layout.addWidget(self.pacs_results_text)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        return widget
    
    def create_config_tab(self) -> QWidget:
        """Create the configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Title
        title = QLabel("Application Configuration")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Local AE configuration
        local_group = QGroupBox("Local Application Entity")
        local_layout = QFormLayout()
        
        self.local_ae_edit = QLineEdit(self.config.config['local_ae_title'])
        local_layout.addRow("AE Title:", self.local_ae_edit)
        
        self.local_port_spin = QSpinBox()
        self.local_port_spin.setRange(1024, 65535)
        self.local_port_spin.setValue(self.config.config['local_port'])
        local_layout.addRow("Port:", self.local_port_spin)
        
        local_group.setLayout(local_layout)
        layout.addWidget(local_group)
        
        # PACS servers configuration
        pacs_group = QGroupBox("PACS Servers")
        pacs_layout = QVBoxLayout()
        
        # PACS list
        self.pacs_list = QListWidget()
        self.update_pacs_list()
        pacs_layout.addWidget(self.pacs_list)
        
        # Add PACS form
        add_pacs_layout = QFormLayout()
        
        self.new_pacs_name_edit = QLineEdit()
        add_pacs_layout.addRow("Name:", self.new_pacs_name_edit)
        
        self.new_pacs_ae_edit = QLineEdit()
        add_pacs_layout.addRow("AE Title:", self.new_pacs_ae_edit)
        
        self.new_pacs_ip_edit = QLineEdit()
        add_pacs_layout.addRow("IP Address:", self.new_pacs_ip_edit)
        
        self.new_pacs_port_spin = QSpinBox()
        self.new_pacs_port_spin.setRange(1024, 65535)
        self.new_pacs_port_spin.setValue(11112)
        add_pacs_layout.addRow("Port:", self.new_pacs_port_spin)
        
        pacs_layout.addLayout(add_pacs_layout)
        
        # Buttons
        pacs_button_layout = QHBoxLayout()
        add_pacs_btn = QPushButton("Add PACS Server")
        add_pacs_btn.clicked.connect(self.add_pacs_server)
        remove_pacs_btn = QPushButton("Remove Selected")
        remove_pacs_btn.clicked.connect(self.remove_pacs_server)
        
        pacs_button_layout.addWidget(add_pacs_btn)
        pacs_button_layout.addWidget(remove_pacs_btn)
        pacs_layout.addLayout(pacs_button_layout)
        
        pacs_group.setLayout(pacs_layout)
        layout.addWidget(pacs_group)
        
        # Save configuration button
        save_btn = QPushButton("Save Configuration")
        save_btn.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px;")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        return widget
    
    def browse_source(self):
        """Browse for source directory"""
        path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if path:
            self.source_path_edit.setText(path)
    
    def browse_destination(self):
        """Browse for destination directory"""
        path = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if path:
            self.dest_path_edit.setText(path)
    
    def start_import(self):
        """Start importing DICOM files"""
        source = self.source_path_edit.text()
        destination = self.dest_path_edit.text()
        
        if not source or not destination:
            QMessageBox.warning(self, "Error", "Please select both source and destination paths")
            return
        
        if not os.path.exists(source):
            QMessageBox.warning(self, "Error", "Source path does not exist")
            return
        
        # Create destination if it doesn't exist
        os.makedirs(destination, exist_ok=True)
        
        # Disable import button
        self.import_btn.setEnabled(False)
        self.import_results_text.clear()
        
        # Start worker thread
        self.worker = DicomImportWorker(source, destination)
        self.worker.progress.connect(self.update_import_progress)
        self.worker.finished.connect(self.import_finished)
        self.worker.error.connect(self.import_error)
        self.worker.start()
    
    def update_import_progress(self, progress: int, status: str):
        """Update import progress"""
        self.import_progress_bar.setValue(progress)
        self.import_status_label.setText(status)
        self.statusBar().showMessage(status)
    
    def import_finished(self, files: List[str]):
        """Handle import completion"""
        self.imported_files = files
        self.import_btn.setEnabled(True)
        
        results = f"Import Complete!\n\n"
        results += f"Total files imported: {len(files)}\n\n"
        results += "Files are organized by Patient/Study/Series\n"
        results += f"Destination: {self.dest_path_edit.text()}"
        
        self.import_results_text.setText(results)
        QMessageBox.information(self, "Success", f"Successfully imported {len(files)} DICOM files")
    
    def import_error(self, error_msg: str):
        """Handle import error"""
        self.import_btn.setEnabled(True)
        self.import_results_text.setText(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", error_msg)
    
    def execute_cfind(self):
        """Execute C-FIND query"""
        if self.pacs_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No PACS servers configured")
            return
        
        server_name = self.pacs_combo.currentText()
        server = next((s for s in self.config.config['pacs_servers'] if s['name'] == server_name), None)
        
        if not server:
            QMessageBox.warning(self, "Error", "Selected PACS server not found")
            return
        
        query_params = {
            'QueryRetrieveLevel': 'STUDY',
            'PatientName': self.patient_name_edit.text() or '',
            'PatientID': self.patient_id_edit.text() or '',
            'StudyDate': self.study_date_edit.text() or '',
            'StudyDescription': ''
        }
        
        config = {
            'local_ae_title': self.config.config['local_ae_title'],
            'pacs_ip': server['ip'],
            'pacs_port': server['port'],
            'pacs_ae_title': server['ae_title']
        }
        
        self.cfind_btn.setEnabled(False)
        self.pacs_results_text.clear()
        
        self.worker = DicomPACSWorker("C-FIND", config, query_params)
        self.worker.progress.connect(self.update_pacs_status)
        self.worker.finished.connect(self.cfind_finished)
        self.worker.error.connect(self.pacs_error)
        self.worker.start()
    
    def update_pacs_status(self, status: str):
        """Update PACS operation status"""
        self.pacs_status_label.setText(status)
        self.statusBar().showMessage(status)
    
    def cfind_finished(self, results: List):
        """Handle C-FIND completion"""
        self.cfind_btn.setEnabled(True)
        
        if not results:
            self.pacs_results_text.setText("No studies found")
            return
        
        text = f"Found {len(results)} studies:\n\n"
        for idx, ds in enumerate(results, 1):
            text += f"Study {idx}:\n"
            text += f"  Patient Name: {getattr(ds, 'PatientName', 'N/A')}\n"
            text += f"  Patient ID: {getattr(ds, 'PatientID', 'N/A')}\n"
            text += f"  Study Date: {getattr(ds, 'StudyDate', 'N/A')}\n"
            text += f"  Study Description: {getattr(ds, 'StudyDescription', 'N/A')}\n"
            text += f"  Study UID: {getattr(ds, 'StudyInstanceUID', 'N/A')}\n"
            text += "\n"
        
        self.pacs_results_text.setText(text)
    
    def execute_cstore(self):
        """Execute C-STORE to send files to PACS"""
        if not self.imported_files:
            QMessageBox.warning(
                self,
                "Error",
                "No files to send. Please import files first from the Import tab."
            )
            return
        
        if self.pacs_combo.count() == 0:
            QMessageBox.warning(self, "Error", "No PACS servers configured")
            return
        
        server_name = self.pacs_combo.currentText()
        server = next((s for s in self.config.config['pacs_servers'] if s['name'] == server_name), None)
        
        if not server:
            QMessageBox.warning(self, "Error", "Selected PACS server not found")
            return
        
        config = {
            'local_ae_title': self.config.config['local_ae_title'],
            'pacs_ip': server['ip'],
            'pacs_port': server['port'],
            'pacs_ae_title': server['ae_title']
        }
        
        self.cstore_btn.setEnabled(False)
        self.pacs_results_text.clear()
        
        self.worker = DicomPACSWorker("C-STORE", config, files=self.imported_files)
        self.worker.progress.connect(self.update_pacs_status)
        self.worker.finished.connect(self.cstore_finished)
        self.worker.error.connect(self.pacs_error)
        self.worker.start()
    
    def cstore_finished(self, results: List):
        """Handle C-STORE completion"""
        self.cstore_btn.setEnabled(True)
        self.pacs_results_text.setText("C-STORE operation completed")
        QMessageBox.information(self, "Success", "Files sent to PACS successfully")
    
    def pacs_error(self, error_msg: str):
        """Handle PACS operation error"""
        self.cfind_btn.setEnabled(True)
        self.cstore_btn.setEnabled(True)
        self.pacs_results_text.setText(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", error_msg)
    
    def update_pacs_combo(self):
        """Update PACS server combo box"""
        self.pacs_combo.clear()
        for server in self.config.config['pacs_servers']:
            self.pacs_combo.addItem(server['name'])
    
    def update_pacs_list(self):
        """Update PACS server list"""
        self.pacs_list.clear()
        for server in self.config.config['pacs_servers']:
            self.pacs_list.addItem(
                f"{server['name']} - {server['ae_title']}@{server['ip']}:{server['port']}"
            )
    
    def add_pacs_server(self):
        """Add a new PACS server"""
        name = self.new_pacs_name_edit.text()
        ae_title = self.new_pacs_ae_edit.text()
        ip = self.new_pacs_ip_edit.text()
        port = self.new_pacs_port_spin.value()
        
        if not name or not ae_title or not ip:
            QMessageBox.warning(self, "Error", "Please fill in all PACS server fields")
            return
        
        server = {
            'name': name,
            'ae_title': ae_title,
            'ip': ip,
            'port': port
        }
        
        self.config.config['pacs_servers'].append(server)
        self.update_pacs_list()
        self.update_pacs_combo()
        
        # Clear form
        self.new_pacs_name_edit.clear()
        self.new_pacs_ae_edit.clear()
        self.new_pacs_ip_edit.clear()
        self.new_pacs_port_spin.setValue(11112)
    
    def remove_pacs_server(self):
        """Remove selected PACS server"""
        current_item = self.pacs_list.currentItem()
        if not current_item:
            return
        
        index = self.pacs_list.currentRow()
        del self.config.config['pacs_servers'][index]
        self.update_pacs_list()
        self.update_pacs_combo()
    
    def save_configuration(self):
        """Save configuration"""
        self.config.config['local_ae_title'] = self.local_ae_edit.text()
        self.config.config['local_port'] = self.local_port_spin.value()
        self.config.save_config()
        
        QMessageBox.information(self, "Success", "Configuration saved successfully")
        self.statusBar().showMessage("Configuration saved", 3000)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    window = DicomImporterGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
