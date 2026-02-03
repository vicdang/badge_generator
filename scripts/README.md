# Scripts Directory

This folder contains launcher scripts and utility runners for Badge Generator.

## 📁 Contents

### `run.bat` - Windows GUI Launcher
**Purpose:** Launch Badge Generator GUI on Windows  
**Usage:** Double-click or run from command prompt: `scripts\run.bat`

**Features:**
- Automatically finds project root
- Launches `run.py` in GUI mode
- Pauses to show any error messages

### `create_test_images.py` - Test Data Generator
**Purpose:** Create sample badge images for testing  
**Usage:** 
```bash
python scripts/create_test_images.py
```

**Features:**
- Creates 5 test images with Vietnamese names
- Generates images in `images/source/` directory
- Images are 200x200 pixels with name text
- Safe to run multiple times

---

## 🚀 Quick Start

### Launch GUI
**Windows:**
```bash
# Double-click scripts/run.bat
# OR from command prompt:
cd /path/to/project
scripts\run.bat
```

**Linux/macOS:**
```bash
python run.py
```

### Generate Test Images
```bash
# From project root
python scripts/create_test_images.py

# Or use module syntax
python -m scripts.create_test_images
```

---

## 📝 Notes

- All scripts expect to be run from the **project root** directory
- Windows batch files require Python in PATH or virtual environment activated
- Test images are created in `images/source/` directory
- Existing images won't be overwritten (file name conflicts)

---

## 🔗 Related

- `run.py` - Main GUI entry point (project root)
- `run.pyw` - Silent GUI launcher (project root)
- `execute.py` - CLI badge generation (project root)
- [DEVELOPER_GUIDE.md](../docs/DEVELOPER_GUIDE.md) - Development setup guide

---

**Status:** ✅ Ready for use
