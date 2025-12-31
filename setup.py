#!/usr/bin/env python3
"""
Setup script for DICOM Importer 2.0
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dicom-importer",
    version="2.0.0",
    author="DICOM Importer Team",
    description="A modern application for efficient DICOM file import from external media and PACS servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gpdahmen/DicomImporter2",
    py_modules=["dicom_importer"],
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "dicom-importer=dicom_importer:main",
        ],
    },
    keywords="dicom pacs medical-imaging healthcare pynetdicom",
)
