# DEVELOPER_GUIDE

Hướng dẫn toàn diện dành cho các nhà phát triển Badge Generator.

## Table of Contents
1. [Development Setup](#development-setup)
2. [Code Style Guide](#code-style-guide)
3. [Professional Setup](#professional-setup)
4. [Setup Completion](#setup-completion)

---

## Development Setup

### Prerequisites

- **OS:** Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python:** 3.8 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** 2GB available for dependencies

### Required Software

1. **Python 3.8+**
   - Download: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Git**
   - Download: https://git-scm.com/
   - Verify installation: `git --version`

3. **Visual Studio Code** (recommended)
   - Download: https://code.visualstudio.com/
   - Recommended extensions:
     - Python (Microsoft)
     - Pylance (Microsoft)
     - Black Formatter (Microsoft)
     - Pytest (LittleFoxTeam)

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/vicdang/badge-generator.git
cd badgenerator
```

#### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Upgrade pip

```bash
python -m pip install --upgrade pip setuptools wheel
```

#### 4. Install Dependencies

```bash
# Development installation
pip install -e ".[dev]"

# Or GUI support
pip install -e ".[gui]"
```

#### 5. Verify Installation

```bash
# Check main imports
python -c "import src.badgenerator; print('✓ Main module OK')"
python -c "import src.badge_gui; print('✓ GUI module OK')"
python -c "import tools.image_manager; print('✓ Tools OK')"

# Test pytest
pytest --version
pytest tests/ -v
```

### Development Tools Setup

#### Code Formatting

```bash
# Format code with Black
black src/ tools/ tests/

# Check formatting
black --check src/

# Format specific file
black src/badgenerator.py
```

#### Linting

```bash
# Check code with flake8
flake8 src/ tools/ tests/

# Check with specific rules
flake8 --max-line-length=100 src/

# Generate report
flake8 --output-file=flake8_report.txt src/
```

#### Import Sorting

```bash
# Sort imports with isort
isort src/ tools/ tests/

# Check without modifying
isort --check-only src/
```

#### Type Checking

```bash
# Check types with mypy
mypy src/ tools/

# Generate type report
mypy src/ --html=mypy_report
```

#### Running All Checks

```bash
# Create pre-commit hook or run manually
black src/ tools/ tests/
isort src/ tools/ tests/
flake8 src/ tools/ tests/
mypy src/ tools/
pytest tests/ -v
```

### Running Applications

#### CLI Application

```bash
# Basic badge generation
python -m src.badgenerator exec

# With options
python -m src.badgenerator exec --check-path
python -m src.badgenerator exec --enable-crawler

# Get help
python -m src.badgenerator --help
```

#### GUI Application

```bash
# Launch GUI
python -m src.badge_gui

# Or directly
python src/badge_gui.py
```

#### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_image_manager.py -v

# Run specific test
pytest tests/test_image_manager.py::TestImageManager::test_download -v

# Run with coverage
pytest tests/ --cov=src --cov=tools --cov-report=html

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Troubleshooting

#### Issue: Module Not Found

```bash
# Solution 1: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Solution 2: Reinstall in editable mode
pip install -e ".[dev]"

# Solution 3: Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue: PIL/Pillow Import Error

```bash
# Reinstall Pillow with all features
pip install --force-reinstall --no-cache-dir Pillow

# Or specific version
pip install Pillow==9.5.0
```

#### Issue: OpenCV (cv2) Import Error

```bash
# Reinstall opencv-python
pip install --force-reinstall --no-cache-dir opencv-python

# If that doesn't work, try opencv-python-headless
pip uninstall opencv-python
pip install opencv-python-headless
```

#### Issue: Tests Not Found

```bash
# Ensure __init__.py exists in tests/
touch tests/__init__.py

# Reinstall package
pip install -e ".[dev]"

# Run pytest with verbose output
pytest tests/ -v --tb=short
```

#### Issue: Virtual Environment Issues

```bash
# Recreate virtual environment
deactivate
rm -rf venv  # or rmdir venv on Windows
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -e ".[dev]"
```

---

## Code Style Guide

This guide defines the coding standards and best practices for the Badge Generator project.

### Python Style

#### General Principles

- Follow **PEP 8** (https://www.python.org/dev/peps/pep-0008/)
- Line length: **100 characters maximum**
- Indentation: **4 spaces** (never tabs)
- Use `black` for automatic formatting

#### Imports

**Order:** stdlib → third-party → local

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Third-party
import cv2
import numpy as np
from PIL import Image, ImageDraw

# Local
from src.config import Config
from tools.image_manager import ImageManager
```

**Rules:**
- One import per line (except `from X import A, B`)
- Use absolute imports, not relative
- Avoid wildcard imports (`from module import *`)
- Group imports with blank lines

#### Spacing

```python
# Two blank lines between module-level functions and classes
class ImageProcessor:
    """Image processing utilities."""
    pass


def process_image() -> None:
    """Process an image."""
    pass


# One blank line between methods in a class
class ImageProcessor:
    def load_image(self, path: str) -> Image.Image:
        """Load an image."""
        pass

    def save_image(self, img: Image.Image, path: str) -> None:
        """Save an image."""
        pass
```

#### String Formatting

```python
# Use f-strings (Python 3.6+)
name = "John"
age = 30
message = f"Name: {name}, Age: {age}"

# For multiline strings
text = f"""
    Name: {name}
    Age: {age}
    Status: Active
"""
```

### Naming Conventions

#### Variables and Functions

```python
# Good: snake_case
user_name = "John Doe"
employee_id = 12345
def get_user_by_id(user_id: int) -> Dict:
    pass

# Avoid: camelCase or UPPER_CASE for variables
userId = "bad"
USER_NAME = "bad"
```

#### Classes

```python
# Good: PascalCase
class ImageProcessor:
    pass

class BadgeGenerator:
    pass

# Avoid
class image_processor:
    pass

class badgenerator:
    pass
```

#### Constants

```python
# Good: UPPER_SNAKE_CASE
DEFAULT_IMAGE_SIZE = (100, 100)
MAX_RETRIES = 3
SUPPORTED_FORMATS = (".png", ".jpg", ".webp")

# Module-level constants
_PRIVATE_CONSTANT = "internal"
PUBLIC_CONSTANT = "external"
```

### Type Hints

#### Basic Types

```python
from typing import Dict, List, Optional, Set, Tuple, Union

# Function parameters and return types
def process_users(users: List[Dict[str, str]]) -> Dict[str, int]:
    """Process list of users."""
    pass

def get_user(user_id: int) -> Optional[Dict]:
    """Get user or None if not found."""
    pass

def save_image(img, path: str) -> bool:
    """Save image. Returns success status."""
    pass
```

### Docstrings

#### Function Docstrings

```python
def process_image(
    image_path: str,
    scale: float = 1.0,
    format: str = "PNG"
) -> Optional[Image.Image]:
    """
    Process an image file with optional scaling.
    
    Args:
        image_path: Full path to the image file.
        scale: Scale factor for resizing. Default 1.0 (no resize).
        format: Output image format. Defaults to "PNG".
    
    Returns:
        PIL Image object if successful, None if image cannot be loaded.
        
    Raises:
        FileNotFoundError: If image_path does not exist.
        ValueError: If scale is not positive.
    
    Example:
        >>> img = process_image("photo.png", scale=0.5)
        >>> if img:
        ...     img.save("output.png")
    """
    pass
```

#### Class Docstrings

```python
class ImageManager:
    """
    Manage image lifecycle from download to processing.
    
    Attributes:
        source_url: Base URL for image downloads
        output_dir: Directory for processed images
        max_workers: Maximum concurrent download threads
    
    Example:
        >>> manager = ImageManager(
        ...     source_url="https://example.com/images",
        ...     output_dir="output/"
        ... )
        >>> manager.download_batch(["image1", "image2"])
    """
```

### Error Handling

#### Proper Exception Handling

```python
# Good: Specific exception handling
try:
    image = Image.open(image_path)
except FileNotFoundError:
    logger.error(f"Image not found: {image_path}")
    return None
except IOError as e:
    logger.error(f"Cannot read image {image_path}: {e}")
    raise

# Good: Custom exceptions
class BadgeGenerationError(Exception):
    """Base exception for badge generation."""
    pass

class TemplateNotFoundError(BadgeGenerationError):
    """Raised when badge template cannot be found."""
    pass
```

---

## Professional Setup

Complete summary of all professional setup files and configurations.

### Configuration Files

#### pyproject.toml
Modern Python project configuration with build system, dependencies, and tool settings.

#### setup.py
Package distribution configuration for PyPI deployment.

#### pytest.ini
Test runner configuration with discovery patterns and coverage settings.

### Documentation Files

#### Core Documentation
- README.md - Project overview
- QUICKSTART.md - Quick setup guide
- API_REFERENCE.md - API documentation
- ARCHITECTURE.md - System design

#### Development Documentation
- CONTRIBUTING.md - Contribution guidelines
- CODE_STYLE_GUIDE.md - Coding standards
- DEVELOPMENT_SETUP.md - Development environment

#### Support Documentation
- TROUBLESHOOTING_AND_FAQS.md - Common issues and solutions
- ROADMAP.md - Future development plans
- RELEASE_NOTES.md - Release documentation

### Version Control

✅ **Proper .gitignore** - Excludes cache, venv, IDE settings  
✅ **License file** - MIT license included  
✅ **README in root** - Project overview  
✅ **Contributing guidelines** - Community guidelines  

### Build & Distribution

✅ **pyproject.toml** - Modern Python config  
✅ **setup.py** - Package distribution  
✅ **Entry points** - CLI and GUI scripts  
✅ **Dependency management** - Required + optional  

### Testing

✅ **pytest configuration** - Test discovery and settings  
✅ **Test markers** - Organization of different test types  
✅ **Coverage configuration** - Code coverage tracking  
✅ **Timeout settings** - Prevent hanging tests  

### Code Quality

✅ **Black formatter** - Automatic code formatting  
✅ **isort** - Import sorting  
✅ **mypy** - Type checking  
✅ **flake8** - Linting  
✅ **Pre-commit hooks** - Automated quality checks  

---

## Setup Completion

### Verification Checklist

- [x] Modern Python metadata created
- [x] Comprehensive documentation complete
- [x] Professional code standards implemented
- [x] Development infrastructure ready
- [x] Build system configured
- [x] Testing infrastructure set up
- [x] Code quality tools configured
- [x] All systems verified and operational

### Distribution Ready

- ✅ PyPI-ready package metadata
- ✅ Proper versioning
- ✅ License information
- ✅ Entry points for tools
- ✅ Installation methods documented

### Development Friendly

- ✅ Editable installation support
- ✅ Optional dev dependencies
- ✅ Test framework configured
- ✅ Code quality tools ready
- ✅ Pre-commit hook support

### Documentation Complete

- ✅ 20+ comprehensive guides
- ✅ API reference included
- ✅ Examples throughout
- ✅ Troubleshooting section
- ✅ FAQ coverage

### Next Steps

1. Review [CODE_STYLE_GUIDE.md](#code-style-guide)
2. Set up development environment using these instructions
3. Run full test suite: `pytest tests/ -v`
4. Read CONTRIBUTING.md before contributing
5. Check ROADMAP.md for future plans

---

**Last Updated:** January 2026  
**Version:** 2.0  
**Status:** Production Ready
