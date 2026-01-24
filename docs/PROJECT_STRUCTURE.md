# PROJECT_STRUCTURE

Hướng dẫn toàn diện về cấu trúc dự án Badge Generator.

## Table of Contents
1. [File Manifest](#file-manifest)
2. [Project Organization](#project-organization)
3. [Documentation Index](#documentation-index)
4. [Directory Descriptions](#directory-descriptions)

---

## File Manifest

### Root Directory Files

```
badge_generator/
├── .gitignore                  # Git ignore file for version control
├── LICENSE                     # MIT License
├── README.md                   # Project README
├── config.ini                  # Default configuration file
├── pictool.conf               # Picture tool configuration
├── pyproject.toml             # Python project metadata (build config)
├── pytest.ini                 # Pytest test configuration
├── requirements.txt           # Python package dependencies
└── setup.py                   # Package setup script for distribution
```

**Total Root Files**: 8

---

## Project Organization

### Source Code Directory (src/)

**Purpose**: Main application source code

```
src/
├── __init__.py                # Python package marker
├── badge_generator.py         # Main CLI application (700+ lines)
│   ├── BadgeGenerator class
│   ├── Command-line interface
│   ├── Image downloading
│   └── Badge generation pipeline
│
├── badge_gui.py               # GUI application (393 lines)
│   ├── ConfigEditor class
│   ├── Tkinter UI elements
│   ├── Configuration editor UI
│   └── Badge generation UI
│
├── config.py                  # Configuration management
│   ├── Config class
│   ├── Position mappings
│   └── File extension definitions
│
└── core/
    └── __init__.py            # Core module package marker
```

**Total Source Files**: 5  
**Lines of Code**: 1,500+

### Tools Directory (tools/)

**Purpose**: Utility modules for image processing and management

```
tools/
├── __init__.py                # Package marker
├── image_manager.py           # Image lifecycle management (450+ lines)
│   ├── ImageManager class
│   ├── Image downloading
│   ├── Image processing
│   ├── Face detection
│   └── Image validation
│
├── image_crawler.py           # Multi-threaded image downloader (400+ lines)
│   ├── ImageCrawler class
│   ├── URL building
│   ├── Multi-threaded downloads
│   └── Timeout handling
│
├── name_verifier.py           # Employee name verification
│   ├── Verification logic
│   ├── Database queries
│   └── Name validation
│
├── mock_data_generator.py     # Test data generation
│   ├── Employee list generation
│   ├── Image mock creation
│   └── Test data utilities
│
├── owncloud_connector.py      # Cloud storage integration
│   ├── OwnCloud connection
│   ├── File upload/download
│   └── Cloud operations
│
├── test_image_manager.py      # ImageManager unit tests
│   ├── Test cases
│   ├── Fixtures
│   └── Assertions
│
└── util.py                    # General utilities
    ├── Logging functions
    ├── File operations
    ├── Validation helpers
    └── Retry mechanisms
```

**Total Tool Files**: 8  
**Lines of Code**: 2,500+

### Tests Directory (tests/)

**Purpose**: Test suite for the project

```
tests/
├── __init__.py                # Package marker
├── check_template.py          # Badge template validation tests
│   ├── Template verification
│   └── Position validation
│
├── comprehensive_test.py      # Comprehensive test suite
│   ├── Multiple test groups
│   ├── Integration tests
│   └── End-to-end scenarios
│
├── end_to_end_test.py         # Complete workflow tests
│   ├── Download → Process → Generate
│   ├── Real-world scenarios
│   └── Success/failure cases
│
├── test_crawler.py            # Image crawler tests
│   ├── URL construction
│   ├── Download verification
│   └── Error handling
│
└── test_results.py            # Test result reporting
    ├── Result analysis
    ├── Performance metrics
    └── Coverage reporting
```

**Total Test Files**: 5  
**Test Cases**: 50+

### Configuration Directory (config/)

**Purpose**: Application configuration files

```
config/
├── __init__.py                # Python package marker
├── config.ini                 # Main configuration (INI format)
│   ├── [general] section
│   ├── [generation] section
│   ├── [crawler] section
│   └── [image_processing] section
│
├── config_base.ini           # Base configuration template
│   └── Default values
│
├── config_with_crawler.ini   # Configuration with crawler enabled
│   └── Crawler settings
│
├── config.ini.bak            # Configuration backup
└── positions.json            # Text position mappings (JSON)
    ├── Name position
    ├── ID position
    ├── Department position
    └── Other text positions
```

**Total Config Files**: 5

### Data Directory (data/)

**Purpose**: Data files and mock data

```
data/
├── __init__.py                # Python package marker
├── employee_list.xlsx         # Employee data spreadsheet
│   ├── Columns: Name, ID, Department
│   └── Sample data for testing
│
└── mock_images/               # Mock/test images
    ├── image1.webp
    ├── image2.webp
    └── image3.jpg
```

**Total Data Files**: 1 Excel + multiple images

### Resources Directory (resources/)

**Purpose**: Static resources (fonts, templates, cascade files)

```
resources/
├── fonts/                     # Font files
│   ├── Arial.ttf
│   ├── Arial Bold.ttf
│   └── (additional fonts)
│
├── haar_cascade/              # OpenCV cascade files
│   └── haarcascade_frontalface_default.xml
│       └── Face detection cascade file (700KB)
│
└── templates/                 # Badge templates
    └── template/
        ├── badge_template.png
        ├── badge_template.jpg
        └── (other templates)
```

**Total Resource Files**: 10+

### Images Directory (images/)

**Purpose**: Image processing directories (organized by function)

```
images/
├── source/                    # Input images (employee photos)
│   ├── README.md
│   └── (employee images)
│
├── output/                    # Generated badges
│   ├── README.md
│   └── (badge files: 001.png, 002.png, etc.)
│
├── temp/                      # Temporary processing files
│   ├── README.md
│   └── .gitkeep
│
├── test/                      # Test images
│   ├── test_download/
│   └── (test files)
│
└── cv/                        # Computer vision processing
    ├── cv_img/
    └── (CV intermediate files)
```

**Total Image Dirs**: 5

### Scripts Directory (scripts/)

**Purpose**: Utility scripts called by the application

```
scripts/
└── runner.bat                 # Execution script called by GUI
    └── Runs: python ../execute.py exec
```

**Note**: After cleanup, only `runner.bat` remains (internal use by GUI).
Entry points are in the root folder instead.

### Root Entry Points (Top Level)

**Purpose**: User entry points for running the application

```
badge_generator/ (root)
├── run.pyw                    # 🎯 Recommended: GUI launcher (no console)
├── run.py                     # Python GUI launcher (alternative)
└── run.bat                    # Debug launcher (console visible)
```

**Main Entry Point**: Use `run.pyw` (double-click to launch)

### Logs Directory (logs/)

**Purpose**: Application log files

```
logs/
├── .gitkeep                   # Placeholder file (empty)
├── generation.log             # Badge generation log
├── test.log                   # Test execution log
└── (other logs as generated)
```

---

## Documentation Index

### Complete Documentation Structure

```
docs/
├── 00_START_HERE.md                     ⭐ Start here!
├── QUICKSTART.md                        📍 5-min setup
├── SOLUTION_SUMMARY.md                  📊 Features overview
├── README.md                            📄 Project overview
├── ARCHITECTURE.md                      🏗️ System design
├── IMAGE_MANAGER_GUIDE.md               📘 API reference
├── IMPLEMENTATION_SUMMARY.md            📝 Implementation details
├── CODE_STYLE_GUIDE.md                  📖 Coding standards
├── DEVELOPMENT_SETUP.md                 🛠️ Dev environment
├── CONTRIBUTING.md                      🤝 Contribution guidelines
├── PYTHON_STANDARDS_GUIDE.md            🐍 Python best practices
├── ROADMAP.md                           🚀 Future plans
├── TROUBLESHOOTING_AND_FAQS.md          ❓ FAQ & troubleshooting
├── RELEASE_NOTES.md                     📢 Release information
├── FINAL_CHECKLIST.md                   ✅ Deployment checklist
├── PROJECT_COMPLETION_SUMMARY.md        📋 Project status
├── FINAL_TEST_REPORT.md                 🧪 Test results
├── FINAL_VERIFICATION_REPORT.md         ✔️ QA verification
├── REFACTORING_REPORT.md                🔄 Refactoring details
├── REFACTORING_SUMMARY.md               📊 Refactoring summary
└── FILE_MANIFEST.md                     📁 File listing
```

**Total Documentation Files**: 20+  
**Total Documentation Lines**: 5,500+  
**Language**: 100% English

---

## Directory Descriptions

### Complete Directory Tree

```
badge_generator/
│
├── 📄 Root Configuration Files
│   ├── .gitignore                      # Version control
│   ├── LICENSE                         # MIT License
│   ├── README.md                       # Project overview
│   ├── config.ini                      # Main config
│   ├── pictool.conf                    # Picture tool config
│   ├── pyproject.toml                  # Project metadata
│   ├── pytest.ini                      # Test config
│   ├── requirements.txt                # Dependencies
│   └── setup.py                        # Package setup
│
├── 🐍 src/ - Source Code
│   ├── __init__.py
│   ├── badge_generator.py              # Main CLI app
│   ├── badge_gui.py                    # GUI application
│   ├── config.py                       # Configuration
│   └── core/
│       └── __init__.py
│
├── 🔧 tools/ - Utilities
│   ├── __init__.py
│   ├── util.py                         # General utilities
│   ├── image_manager.py                # Image management
│   ├── image_crawler.py                # Image downloading
│   ├── name_verifier.py                # Name validation
│   ├── mock_data_generator.py          # Test data
│   ├── owncloud_connector.py           # Cloud integration
│   └── test_image_manager.py           # Tests & demos
│
├── 🧪 tests/ - Test Suite
│   ├── __init__.py
│   ├── check_template.py
│   ├── comprehensive_test.py
│   ├── end_to_end_test.py
│   ├── test_crawler.py
│   └── test_results.py
│
├── ⚙️ config/ - Configuration
│   ├── __init__.py
│   ├── config.ini
│   ├── config_base.ini
│   ├── config_with_crawler.ini
│   ├── config.ini.bak
│   └── positions.json
│
├── 📊 data/ - Data Files
│   ├── __init__.py
│   ├── employee_list.xlsx
│   └── mock_images/
│
├── 📚 resources/ - Static Assets
│   ├── fonts/                          # Font files
│   ├── haar_cascade/                   # Face detection
│   └── templates/                      # Badge templates
│
├── 🖼️ images/ - Image Processing
│   ├── source/                         # Input images
│   ├── output/                         # Generated badges
│   ├── temp/                           # Temp files
│   ├── test/                           # Test images
│   └── cv/                             # CV processing
│
├── 🚀 scripts/ - Executables
│   ├── run.bat                         # CLI launcher
│   ├── runner.bat                      # Additional runner
│   └── run.pyw                         # GUI launcher
│
├── 📝 docs/ - Documentation (20+ files)
│   └── [See documentation structure above]
│
└── 📋 logs/ - Log Files
    └── [Generated at runtime]
```

---

## Summary Statistics

### By Type

| Type | Count | Description |
|------|-------|-------------|
| Python files | 20+ | Source code and tests |
| Markdown docs | 20+ | Documentation files |
| Configuration | 5 | Config files (.ini, .json) |
| Scripts | 3 | Batch/shell scripts |
| Images | 50+ | Photos, templates, cascade |
| Resources | 10+ | Fonts, templates |
| Other | 10+ | License, requirements, etc. |

### By Directory

| Directory | Files | Purpose |
|-----------|-------|---------|
| src/ | 5 | Main source code |
| tools/ | 8 | Utility modules |
| tests/ | 5 | Test suite |
| config/ | 5 | Configuration |
| docs/ | 20+ | Documentation |
| resources/ | 10+ | Static assets |
| images/ | 50+ | Working images |
| scripts/ | 3 | Executables |

### Total Project Size

- **Total Files**: 150+
- **Total Directories**: 30+
- **Total Python Code**: 3,500+ lines
- **Total Documentation**: 5,500+ lines
- **Total Size**: ~100+ MB (with images)

---

## Key Files Reference

### Critical Files (Must Have)

| File | Purpose | Location | Status |
|------|---------|----------|--------|
| badge_generator.py | Main application | src/ | ✅ Required |
| config.py | Configuration | src/ | ✅ Required |
| image_manager.py | Image management | tools/ | ✅ Required |
| config.ini | Configuration data | config/ | ✅ Required |
| requirements.txt | Dependencies | root | ✅ Required |
| pyproject.toml | Project metadata | root | ✅ Required |

### Important Files (Should Have)

| File | Purpose | Location | Status |
|------|---------|----------|--------|
| tests/ | Test suite | root | ✅ Important |
| docs/ | Documentation | root | ✅ Important |
| badge_gui.py | GUI application | src/ | ✅ Important |
| scripts/ | Entry scripts | root | ✅ Important |

### Optional Files (Nice to Have)

| File | Purpose | Location | Status |
|------|---------|----------|--------|
| .gitignore | Version control | root | ✅ Recommended |
| LICENSE | Legal | root | ✅ Recommended |
| resources/ | Static assets | root | ✅ Optional |
| data/mock_images/ | Test data | data/ | ✅ Optional |

---

## File Organization Principles

### 1. Separation of Concerns

- **src/**: Application code (main features)
- **tools/**: Utilities and helpers
- **tests/**: Testing code
- **docs/**: Documentation
- **config/**: Configuration
- **resources/**: Static files
- **data/**: Data files
- **images/**: Working images
- **logs/**: Log output

### 2. Module Organization

Each Python module focuses on specific functionality:
- `badge_generator.py` - Badge generation
- `badge_gui.py` - User interface
- `config.py` - Configuration
- `image_manager.py` - Image operations
- `image_crawler.py` - Downloading
- `util.py` - General utilities

### 3. Configuration Strategy

- `config.ini` - Main configuration
- `positions.json` - Data mappings
- Backup files for recovery
- Version control for changes

### 4. Documentation Strategy

- Quick start guides
- API documentation
- Architecture documentation
- Contributing guides
- Troubleshooting guides

---

## Configuration Files Reference

### config.ini Sections

```ini
[general]          # General settings
[generation]       # Badge generation settings
[crawler]          # Image crawler settings
[image_processing] # Image processing settings
```

### positions.json Structure

```json
{
  "name": [x, y],           # Name text position
  "id": [x, y],             # ID text position
  "department": [x, y],     # Department text position
  "qr_code": [x, y, w, h]   # QR code position and size
}
```

---

## Adding New Files

### When Adding Source Code

1. Put in appropriate directory (`src/` or `tools/`)
2. Add `__init__.py` to package directory if needed
3. Follow code style guide
4. Add docstrings and type hints
5. Add tests in `tests/`
6. Update documentation

### When Adding Documentation

1. Put in `docs/` directory
2. Use markdown format
3. Update documentation index
4. Follow documentation style
5. Add to table of contents

### When Adding Configuration

1. Put in `config/` directory
2. Document in API reference
3. Add to config template
4. Update documentation

### When Adding Tests

1. Put in `tests/` directory
2. Name as `test_*.py` or `*_test.py`
3. Follow naming conventions
4. Add pytest marks
5. Update test documentation

---

## Maintenance Guidelines

### File Size Monitoring

- Source code: < 5MB (Python)
- Documentation: < 2MB (Markdown)
- Resources: < 100MB (images, fonts)
- Total: Keep under 500MB for distribution

### Cleanup Guidelines

- Remove unused files regularly
- Archive old versions
- Clean temporary files
- Update obsolete documentation
- Verify all links work

### Backup Strategy

- Config backups: `*.bak` files
- Version control: Git repository
- Distribution: GitHub releases
- Archive: Periodic full backups

---

## Quick Navigation

### Finding Files

**Configuration**:
```
config/config.ini
config/positions.json
```

**Source Code**:
```
src/badge_generator.py
src/badge_gui.py
tools/image_manager.py
```

**Documentation**:
```
docs/QUICKSTART.md
docs/API_REFERENCE.md
docs/ARCHITECTURE.md
```

**Tests**:
```
tests/test_*.py
```

### Common Operations

**List all Python files**:
```bash
find . -name "*.py" | grep -v __pycache__
```

**List all documentation**:
```bash
ls docs/*.md
```

**List project structure**:
```bash
tree -L 2 -I '__pycache__|*.pyc'
```

---

## Related Documentation

- **Detailed File Information**: See [FILE_MANIFEST.md](FILE_MANIFEST.md)
- **Documentation Navigation**: See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
- **Setup Instructions**: See [QUICKSTART.md](QUICKSTART.md)
- **Architecture Overview**: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Last Updated**: January 2026  
**Version**: 2.0  
**Total Files**: 150+  
**Total Directories**: 30+
