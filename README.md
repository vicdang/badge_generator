# ***Badge Generator***
Badge Generator Tool - Automatically generate ID badges with face detection and QR codes

**Version:** 3.0.0 | **Status:** Production Ready | **Python:** 3.8+ | **License:** See LICENSE file

<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/a909615e-dcb8-4a9d-8220-442fb5e42fee" />

## ***General Information***
### Supporting Features
1. Auto detect faces, resize, rotate, crop and convert images
2. Collage images with templates
3. Place text on manipulated images
4. Generate QR codes based on employee data
5. Support Windows and Unix
6. **GUI tool for easy badge generation** (recommended way to use)
7. **Live preview panel** showing template, source images, and generated output
8. **Auto-refresh preview** on every operation (Generate, Cleanup, Pull Image, Save Config)

### Future Features
1. Integrate with storage tools like Owncloud, Drive, Google Photos, Flickr
2. Auto crawling required images, icons, emoticons

### Prerequisites
- Python >= 3.8
- OpenCV (cv2) 
- NumPy
- PIL/Pillow
- qrcode
- openpyxl (for Excel support)

## ***Folder Structure***

```
badgenerator/                    (Root project folder - git root)
├── run.pyw                         ⭐ START HERE - GUI launcher (Windows)
├── run.py                          Alternative Python launcher
├── run.bat                         Debug launcher (shows console)
├── requirements.txt
├── execute.py                      CLI execution script
├── config.ini                      Configuration file
│
├── src/                            Source code
│   ├── badge_gui.py                ⭐ GUI application
│   ├── config.py                   Centralized configuration
│   ├── badgenerator.py
│   └── core/
│
├── tools/                          Utility modules
│   ├── image_crawler.py
│   ├── image_manager.py
│   └── runner.bat                  Called by GUI
│
├── config/                         Configuration
│   ├── config.ini
│   └── positions.json
│
├── images/                         Image folders
│   ├── source/src_img/             🔒 Original images
│   ├── output/                     Generated badges
│   ├── templates/                  🔒 Templates
│   └── temp/                       Temporary files
│
├── resources/                      Resources
│   ├── fonts/
│   └── haar_cascade/
│
├── docs/                           Documentation
├── tests/                          Tests
└── .git/                           Git root
```

## ***Installation***

```bash
# Clone repository
$ git clone <repo-url>
$ cd badgenerator

# Create virtual environment
$ python -m venv .venv

# Activate virtual environment
# Windows:
$ .venv\Scripts\activate
# macOS/Linux:
$ source .venv/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```

## ***Quick Start (Recommended - GUI)***

### Windows Users (Easiest)
**Option 1 - Double-click:**
> Double-click to execute `run.pyw`

**Option 2 - Command line:**
```bash
python run.pyw
```

### All Users
```bash
# Make sure you're in the badgenerator folder
python run.pyw
```

This launches the **Badge Generator GUI** where you can:
- ✅ **Pull Images** - Crawl missing employee photos from intranet
- ✅ **Save** - Save configuration changes
- ✅ **Cleanup** - Clean up temporary image directories  
- ✅ **Generate** - Generate badges with face detection and QR codes
- 📊 **Monitor** - View progress in built-in terminal

### GUI Features
- **Configuration Editor** (Left Panel)
  - Edit all application settings
  - No need to touch config files

- **Preview Panel** (Right Panel - Middle)
  - Real-time display of template, source, and output images
  - Auto-refreshes on every operation (Generate, Cleanup, Pull Image, Save Config)
  - Thread-safe updates from background processes

- **Terminal Output** (Right Panel - Bottom)
  - Real-time execution logs
  - Shows crawling and generation progress
  - Adjustable height via config

- **Control Buttons** (Right Panel - Very Bottom)
  - Pull Image: Download missing employee photos
  - Save: Save configuration changes
  - Cleanup: Clean temporary files
  - Generate: Start badge generation

---

## ***Command-Line Usage (Advanced)***
- Generate badges
- Monitor progress in the built-in terminal

All configuration can be adjusted directly in the GUI and saved for future runs.

**For Debugging:**
If you need to see error messages and debug output, use `run.bat` instead (Windows) or run with Python directly.

---
## ***Advanced: Command-Line Usage***

### Default Execution
```bash
# Generate badges from images/source/src_img/
python execute.py exec

# With debug and verbose logging
python execute.py -d -v exec

# Convert images to PNG format
python execute.py exec -c
```

### Cleanup Command
```bash
# Clean temporary files (preserves originals and templates)
python execute.py cleanup

# With debug output
python execute.py -d cleanup
```

### Configuration
Edit `config/config.ini` to customize behavior:

```ini
[cleanup]
enabled = true
clean_root = images/
skip_paths = images/source/src_img/,images/templates/
```

## ***Data-Driven Workflow***
The application now supports a data-driven approach:

1. **Load employee data from Excel** (`tools/data.xlsx`)
   - Format: Column 1=ID, Column 2=Name, Column 3=Position
   
2. **Discover available images** in `images/source/src_img/`

3. **Automatically crawl missing images** from configured URL using the ImageCrawler
   - Configured in `config/config.ini` [crawler] section
   - Tries to download images for employees without photos

4. **Process all available images** with employee data

### Workflow Example
```bash
# 1. Prepare data.xlsx with employee information
#    (Place in tools/data.xlsx)

# 2. Run badge generation
python execute.py exec

# The system will:
# - Load employees from tools/data.xlsx
# - Check which images exist in images/source/src_img/
# - Crawl missing images from the configured URL
# - Generate badges for all employees with images
```

---

# ***Support & Contribution***

## Feature Requests & Support
Reach out via GitHub issues or email (check git log).

## Appreciation
If this project helps you:
> Coffee me via PayPal: [@vicdane](https://paypal.me/vicdane)

Contact me via:
>Email: [vudnn.dl@gmail.com](mailto:vudnn.dl@gmail.com)

>Teams: [vudnn.dl@gmail.com]()

