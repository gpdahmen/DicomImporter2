# Contributing to DICOM Importer 2.0

Thank you for your interest in contributing to DICOM Importer! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/DicomImporter2.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test your changes thoroughly
4. Commit with clear messages: `git commit -m "Add feature X"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request

## Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and modular
- Comment complex logic

## Testing

Before submitting a PR, ensure:
- Your code compiles without errors: `python3 -m py_compile dicom_importer.py`
- The basic test passes: `python3 test_basic.py`
- You've tested the feature manually in the GUI

## Areas for Contribution

### High Priority
- Additional DICOM modality support
- Enhanced error handling and user feedback
- Performance optimizations for large datasets
- Unit tests and integration tests
- Cross-platform testing (Windows, Linux, Mac)

### Medium Priority
- Additional PACS query filters
- Export to more formats
- Database integration for tracking imports
- Batch processing capabilities
- Command-line interface

### Documentation
- Usage tutorials and videos
- API documentation
- Deployment guides
- Troubleshooting tips

## Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version
- Full error traceback
- Steps to reproduce
- Expected vs actual behavior

## Feature Requests

Feature requests are welcome! Please:
- Check if the feature already exists or is planned
- Describe the use case clearly
- Explain the expected behavior
- Consider if it fits the project scope

## Questions?

- Open a GitHub issue with your question
- Tag it with the "question" label

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

Thank you for contributing! 🎉
