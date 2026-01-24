# Troubleshooting & FAQs

Comprehensive troubleshooting guide and frequently asked questions for Badge Generator.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Image Processing Issues](#image-processing-issues)
4. [Configuration Problems](#configuration-problems)
5. [GUI Issues](#gui-issues)
6. [Performance Issues](#performance-issues)
7. [Frequently Asked Questions](#frequently-asked-questions)
8. [Getting Help](#getting-help)

---

## Installation Issues

### Issue: Python Not Found

**Error Message**:
```
'python' is not recognized as an internal or external command
```

**Solution**:

1. **Check Python Installation**:
   ```bash
   python --version
   ```

2. **Add Python to PATH** (Windows):
   - Go to Settings → Environment Variables
   - Add Python installation directory to PATH
   - Restart terminal
   - Verify: `python --version`

3. **Use Python 3**:
   ```bash
   python3 --version  # macOS/Linux
   py --version       # Windows
   ```

### Issue: pip Not Found

**Error Message**:
```
'pip' is not recognized or No module named pip
```

**Solution**:

```bash
# Use pip module directly
python -m pip --version

# Or upgrade pip
python -m pip install --upgrade pip

# Try pip3
pip3 install -r requirements.txt
```

### Issue: Virtual Environment Not Activating

**Error Message**:
```
Cannot activate virtual environment
```

**Solution**:

```bash
# Windows
cd venv\Scripts
activate

# Or use python
python -m venv venv
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Verify**: Prompt should show `(venv)` prefix

### Issue: Dependencies Won't Install

**Error Message**:
```
ERROR: Failed to build package
```

**Solution**:

```bash
# Update pip first
python -m pip install --upgrade pip

# Try installing with no binary cache
pip install --no-cache-dir -r requirements.txt

# For specific problematic packages
pip install --force-reinstall --no-cache-dir Pillow
pip install --force-reinstall --no-cache-dir opencv-python
```

### Issue: Conflicting Python Versions

**Error Message**:
```
ImportError: cannot import module (wrong architecture)
```

**Solution**:

```bash
# Check Python architecture
python -c "import struct; print(struct.calcsize('P') * 8)"

# For 64-bit Python:
pip install package_name  # Should work

# For issues, specify architecture
pip install -U setuptools
pip install --only-binary :all: package_name
```

---

## Runtime Errors

### Issue: Module Not Found

**Error Message**:
```
ModuleNotFoundError: No module named 'src'
```

**Solution**:

1. **Verify virtual environment active**:
   ```bash
   # Should show (venv) in prompt
   ```

2. **Reinstall package**:
   ```bash
   pip install -e .
   ```

3. **Check Python path**:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

4. **Run from correct directory**:
   ```bash
   cd badge_generator  # Project root
   python src/badge_generator.py
   ```

### Issue: ImportError with PIL

**Error Message**:
```
ImportError: No module named 'PIL'
```

**Solution**:

```bash
# Reinstall Pillow
pip uninstall Pillow
pip install Pillow

# Or specific version
pip install Pillow==9.5.0

# Verify
python -c "from PIL import Image; print('OK')"
```

### Issue: cv2 Not Working

**Error Message**:
```
ImportError: No module named 'cv2'
```

**Solution**:

```bash
# Install opencv-python
pip install opencv-python

# Or headless version for servers
pip install opencv-python-headless

# Verify
python -c "import cv2; print(cv2.__version__)"
```

### Issue: Configuration File Not Found

**Error Message**:
```
FileNotFoundError: config.ini not found
```

**Solution**:

1. **Check file location**:
   ```bash
   # Should be in config/ directory
   ls config/config.ini
   ```

2. **Create from template**:
   ```bash
   cp config/config_base.ini config/config.ini
   ```

3. **Update configuration path** in code if needed

### Issue: File Permission Denied

**Error Message**:
```
PermissionError: [Errno 13] Permission denied: 'file.png'
```

**Solution**:

```bash
# Check file permissions
ls -la file.png

# Fix permissions (Unix/Linux)
chmod 644 file.png
chmod 755 directory_name

# Ensure directory is writable
chmod 755 images/output

# Windows: Use file properties (GUI) or
attrib -R file.png
```

---

## Image Processing Issues

### Issue: Cannot Determine Region Size

**Error Message**:
```
OSError: cannot determine region size; use 4-item box
```

**Solution**:

This is usually fixed in v2.0, but if it occurs:

```bash
# Reinstall Pillow
pip install --force-reinstall --no-cache-dir Pillow

# Update code to use alpha_composite
# See: src/badge_generator.py for correct implementation
```

### Issue: Face Detection Not Working

**Error Message**:
```
Error loading cascade file
```

**Solution**:

1. **Verify cascade file exists**:
   ```bash
   ls resources/haar_cascade/haarcascade_frontalface_default.xml
   ```

2. **Check file path** in config/code

3. **Download if missing**:
   ```python
   # Run this Python script to download
   import cv2
   url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
   # Download and save to resources/haar_cascade/
   ```

### Issue: Images Not Downloading

**Error Message**:
```
ConnectionError: Failed to download image
```

**Solution**:

1. **Check internet connection**:
   ```bash
   ping intranet.tma.com.vn
   ```

2. **Verify base URL** in config:
   ```ini
   [crawler]
   base_url = https://intranet.tma.com.vn/images/emp_images/big_new
   ```

3. **Check timeout** settings:
   ```ini
   [crawler]
   timeout = 30
   ```

4. **Enable proxy if needed**:
   ```python
   import os
   os.environ['http_proxy'] = 'proxy.company.com:8080'
   ```

### Issue: WebP Format Not Supported

**Error Message**:
```
OSError: cannot identify image file (WebP)
```

**Solution**:

```bash
# Reinstall Pillow with WebP support
pip install --force-reinstall --no-cache-dir Pillow[webp]

# Or use libreimages
pip install libwebp

# Or convert to PNG/JPG
# Update config to use PNG instead
```

### Issue: Image Too Large

**Error Message**:
```
MemoryError or Image too large
```

**Solution**:

```python
# Resize image first
from PIL import Image

img = Image.open("large_image.png")
img.thumbnail((800, 800))  # Max size
img.save("resized.png")

# Or configure in code
max_size = (800, 800)
```

### Issue: Corrupted Image File

**Error Message**:
```
OSError: cannot open image (corrupt file)
```

**Solution**:

1. **Verify image**:
   ```bash
   file image.png
   ```

2. **Try opening with image viewer** to test

3. **Re-download** the image

4. **Use different format** (PNG instead of WebP)

---

## Configuration Problems

### Issue: Configuration Not Loading

**Error Message**:
```
ValueError: Configuration section not found
```

**Solution**:

1. **Check config.ini format**:
   ```ini
   [section_name]
   key = value
   ```

2. **Verify all sections exist**:
   ```ini
   [general]
   [generation]
   [crawler]
   [image_processing]
   ```

3. **Check for typos** in section/key names

4. **Validate JSON in positions.json**:
   ```bash
   python -c "import json; json.load(open('config/positions.json'))"
   ```

### Issue: Invalid Configuration Value

**Error Message**:
```
ValueError: Invalid value for setting
```

**Solution**:

1. **Check data types**:
   - String: `"value"` or `value`
   - Number: `123` (no quotes)
   - Boolean: `true` or `false`

2. **Verify paths exist**:
   ```bash
   ls path/to/file.png
   ```

3. **Check for special characters** needing escaping

### Issue: Position Mapping Incorrect

**Error Message**:
```
Text appears in wrong location on badge
```

**Solution**:

1. **Edit positions.json**:
   ```json
   {
     "name": [x, y],
     "id": [x, y],
     "department": [x, y]
   }
   ```

2. **Adjust x,y coordinates** based on template size

3. **Test with known values** first

---

## GUI Issues

### Issue: GUI Won't Start

**Error Message**:
```
ModuleNotFoundError: No module named 'tkinter'
```

**Solution**:

**Windows**:
- Reinstall Python with "tcl/tk and IDLE" checked

**macOS**:
```bash
brew install python-tk@3.11
```

**Ubuntu/Debian**:
```bash
sudo apt-get install python3-tk
```

**Fedora**:
```bash
sudo dnf install python3-tkinter
```

### Issue: GUI Unresponsive

**Error Message**:
```
GUI freezes or becomes unresponsive
```

**Solution**:

1. **Process in background thread**:
   ```python
   import threading
   thread = threading.Thread(target=long_task)
   thread.daemon = True
   thread.start()
   ```

2. **Reduce batch size** if processing many items

3. **Add progress indicator** for long tasks

4. **Update GUI** with `root.update()`

### Issue: GUI Elements Not Displaying

**Error Message**:
```
Buttons/labels not showing in GUI
```

**Solution**:

1. **Check geometry managers**:
   ```python
   widget.pack()  # or
   widget.grid()  # or
   widget.place()
   ```

2. **Ensure widgets have sizes**:
   ```python
   widget.config(width=20, height=5)
   ```

3. **Call update** after creating widgets:
   ```python
   root.update()
   ```

### Issue: File Dialog Not Opening

**Error Message**:
```
File dialog doesn't appear
```

**Solution**:

```python
# Verify tkinter filedialog
from tkinter import filedialog

# Ensure root window exists
import tkinter as tk
root = tk.Tk()

# Open dialog
filename = filedialog.askopenfilename()

# Keep window open
root.mainloop()
```

---

## Performance Issues

### Issue: Slow Batch Processing

**Problem**: Processing 100+ badges takes too long

**Solution**:

1. **Enable multi-threading**:
   ```python
   max_workers = 5  # In config
   ```

2. **Reduce image quality**:
   ```python
   image_format = "JPEG"  # Instead of PNG
   ```

3. **Resize images before processing**:
   ```python
   max_size = (800, 600)  # In config
   ```

4. **Use SSD if available** for faster I/O

### Issue: High Memory Usage

**Problem**: Memory usage keeps growing

**Solution**:

1. **Process in smaller batches**:
   ```python
   batch_size = 10
   for batch in chunks(items, batch_size):
       process(batch)
   ```

2. **Clear cache regularly**:
   ```python
   del image
   gc.collect()
   ```

3. **Use generators** instead of lists

4. **Close file handles**:
   ```python
   with open(file) as f:
       # File closed automatically
   ```

### Issue: Slow Download

**Problem**: Image downloads are taking too long

**Solution**:

1. **Increase worker threads**:
   ```ini
   [crawler]
   workers = 10  # Was 5
   ```

2. **Increase timeout**:
   ```ini
   timeout = 60  # Was 30
   ```

3. **Check network speed**:
   ```bash
   ping intranet.tma.com.vn
   ```

4. **Download during off-peak hours**

### Issue: Slow Face Detection

**Problem**: Face detection is very slow

**Solution**:

1. **Use faster cascade file** (trade accuracy for speed)

2. **Resize images first**:
   ```python
   img.thumbnail((400, 400))  # Faster detection
   ```

3. **Skip face detection** if not critical:
   ```ini
   [image_processing]
   detect_faces = false
   ```

---

## Frequently Asked Questions

### General Questions

#### Q: What is Badge Generator?
**A**: Badge Generator is an automated tool that creates employee ID badges from photos, including face detection, QR codes, and customizable layouts.

#### Q: What platforms are supported?
**A**: Windows (7+), macOS (10.14+), and Linux (Ubuntu 18.04+)

#### Q: What's the minimum Python version?
**A**: Python 3.8 or higher

#### Q: Is there a GUI version?
**A**: Yes! Run with `python src/badge_gui.py`

#### Q: How much disk space is needed?
**A**: ~2GB for all dependencies and typical usage

### Usage Questions

#### Q: How do I generate badges?
**A**: 
```bash
# CLI
python src/badge_generator.py exec

# GUI
python src/badge_gui.py
```

#### Q: Where are the generated badges?
**A**: In `images/output/` directory

#### Q: Can I customize the badge layout?
**A**: Yes! Edit `config/positions.json` to adjust text positions

#### Q: How do I change fonts?
**A**: 
1. Place font file in `resources/fonts/`
2. Update path in `config/config.ini`

#### Q: Can I use my own template?
**A**: Yes! Put template in `resources/templates/` and configure in code

### Download Questions

#### Q: Where does it download images from?
**A**: TMA intranet by default (configurable)

#### Q: Can I download from a different source?
**A**: Yes! Update `base_url` in `config/config.ini`

#### Q: How many images can I download?
**A**: Theoretically unlimited, but batch process for safety

#### Q: What formats are supported?
**A**: PNG, JPG, WebP (configure in `config.ini`)

### Configuration Questions

#### Q: How do I configure the application?
**A**: Edit `config/config.ini` or use GUI

#### Q: Where is the configuration file?
**A**: `config/config.ini` in project root

#### Q: Can I have multiple configurations?
**A**: Yes! Create `config_custom.ini` and load it

#### Q: How do I set up for crawler?
**A**: Set `enable_crawler = true` in `[crawler]` section

### Testing Questions

#### Q: How do I run tests?
**A**: `pytest tests/ -v`

#### Q: How do I run specific tests?
**A**: `pytest tests/test_image_manager.py -v`

#### Q: What's the test coverage?
**A**: 85%+ coverage (see FINAL_TEST_REPORT.md)

#### Q: Can I write my own tests?
**A**: Yes! Add to `tests/` directory and follow conventions

### Troubleshooting Questions

#### Q: The GUI won't start
**A**: Install tkinter (see [GUI Issues](#gui-issues))

#### Q: Badges aren't generating
**A**: Check logs in `logs/` directory

#### Q: Images won't download
**A**: Verify internet and config (see [Image Processing Issues](#image-processing-issues))

#### Q: Getting memory errors
**A**: Process in smaller batches (see [Performance Issues](#performance-issues))

### Integration Questions

#### Q: Can I use this in my script?
**A**: Yes! Import modules:
```python
from src.badge_generator import BadgeGenerator
gen = BadgeGenerator()
result = gen.generate_badge(user_info, output)
```

#### Q: Is there an API?
**A**: REST API planned for v2.3+

#### Q: Can I automate badge generation?
**A**: Yes! Use CLI or programmatic API

#### Q: Can I integrate with my HR system?
**A**: Yes! Write integration code using the Python API

### Support Questions

#### Q: How do I get help?
**A**: See [Getting Help](#getting-help) section

#### Q: Where's the documentation?
**A**: In `docs/` directory (start with README.md)

#### Q: How do I report a bug?
**A**: Create issue on GitHub with details

#### Q: Can I contribute?
**A**: Yes! See CONTRIBUTING.md

---

## Getting Help

### Documentation

1. **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
2. **API Reference**: [API_REFERENCE.md](API_REFERENCE.md)
3. **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Development**: [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md)
5. **Troubleshooting**: This file

### Online Resources

- **Documentation**: See `docs/` directory
- **Issue Tracker**: GitHub Issues
- **Discussions**: GitHub Discussions

### Community

1. **GitHub Issues**: Report bugs and feature requests
2. **GitHub Discussions**: General questions
3. **Contributing**: See CONTRIBUTING.md

### Professional Support

For enterprise support, contact the project maintainers.

---

## Quick Diagnostic Script

```python
#!/usr/bin/env python
"""Quick diagnostic script for troubleshooting."""

import sys
import os

def check_python():
    print(f"Python: {sys.version}")
    return sys.version_info >= (3, 8)

def check_imports():
    required = ['PIL', 'cv2', 'numpy', 'qrcode', 'openpyxl']
    missing = []
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    return missing

def check_files():
    required = [
        'src/badge_generator.py',
        'src/badge_gui.py',
        'config/config.ini',
        'resources/haar_cascade/haarcascade_frontalface_default.xml'
    ]
    missing = []
    for f in required:
        if not os.path.exists(f):
            missing.append(f)
    return missing

def main():
    print("Badge Generator Diagnostic")
    print("=" * 40)
    
    if check_python():
        print("✓ Python version OK")
    else:
        print("✗ Python 3.8+ required")
    
    missing_imports = check_imports()
    if missing_imports:
        print(f"✗ Missing packages: {missing_imports}")
    else:
        print("✓ All packages installed")
    
    missing_files = check_files()
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
    else:
        print("✓ All required files present")
    
    print("=" * 40)
    if not (check_python() and not missing_imports and not missing_files):
        print("Fix issues above before running application")
        return 1
    else:
        print("✓ System ready!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
```

Save as `diagnose.py` and run:
```bash
python diagnose.py
```

---

**Last Updated**: 2024  
**Version**: 2.0  
**Status**: Current

For more help, visit the documentation or create an issue on GitHub.
