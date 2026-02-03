# 🚀 Quick Start Guide

## ⚡ 2-Minute GUI Setup (Recommended)

### **Step 1: Navigate to Badge Generator folder**
```bash
# Navigate into the badgenerator directory
cd badgenerator
```

### **Step 2: Launch the GUI**
```bash
# Double-click run.pyw or run from terminal:
python run.pyw
```

The GUI will open with:
- Left side: Configuration editor
- Right side: Terminal and control buttons

### **Step 3: Click Buttons in Order**
1. **Pull Image** - Download any missing employee photos
2. **Save** - Save your configuration
3. **Cleanup** - Clean temporary directories
4. **Generate** - Create badges with face detection & QR codes

### **Step 4: Monitor Progress**
Watch the terminal output to see:
- How many images were downloaded
- Badge generation progress
- Any errors or warnings

✅ **Done!** Generated badges are in `images/output/`

---

## 🔧 Advanced: Command-Line Usage

Edit `config/config.ini` and add this section at the end:

```ini
[crawler]
base_url = https://intranet.company.com/images/emp_images/big_new
workers = 5
timeout = 30
```

**Adjust:**
- `base_url`: Replace with your internal server URL
- `workers`: Number of threads (5 for normal server, 10 for powerful server)
- `timeout`: Timeout per download (30s is default)

### **Step 2: Test Configuration** (1 min)

```bash
# Test if config is valid
python execute.py --help

# View all options
```

### **Step 3: Run với Crawler** (1 min)

```bash
# Run with auto-download
python execute.py --enable-crawler -d -v exec

# Or without crawler (only process existing images)
python execute.py -d -v exec
```

### **Step 4: Monitor Output** (2 min)

View log output:
```
INFO - Image crawler enabled - checking for missing images...
INFO - Found 30 missing images, starting download...
INFO - Successfully downloaded: john_001_SE_1.png
...
INFO - Download Summary:
  Total files: 100
  Missing: 30
  Downloaded: 28
  Failed: 2
  Already available: 70
```

---

## 🔧 Common Commands

### **Run with Crawler**
```bash
python execute.py --enable-crawler -v exec
```

### **Run without Crawler**
```bash
python execute.py -v exec
```

### **Debug Mode**
```bash
python execute.py --enable-crawler -d -v exec
```

### **Loop Mode (Auto-retry)**
```bash
python execute.py --enable-crawler -v -l exec -i 300
# -i 300: Retry every 300 seconds (5 minutes)
```

### **Convert + Process**
```bash
python execute.py --enable-crawler -c -v exec
# -c: Convert images to PNG format first
```

---

## 📊 Configuration Examples

### **Fast Network (Internal Server)**
```ini
[crawler]
base_url = https://intranet.company.com/images/big
workers = 10
timeout = 15
```

### **Slow Network (Firewall/Proxy)**
```ini
[crawler]
base_url = https://company.com/images/big
workers = 2
timeout = 60
```

### **Large Batch (Thousands of Files)**
```ini
[crawler]
base_url = https://intranet.company.com/images/big
workers = 15
timeout = 45
```

---

## 🐛 Troubleshooting

### **Issue: "Connection timeout"**
```
Solution: Increase timeout in config
workers = 3     # Decrease workers
timeout = 60    # Increase timeout
```

### **Issue: "HTTP 404 Not Found"**
```
Solution: Employee ID does not exist
→ Check employee list again
→ Verify base_url is correct
```

### **Issue: "Permission Denied" (HTTP 403)**
```
Solution: No download permission
→ Check authentication
→ Verify user permissions
```

### **Issue: "Module not found"**
```
Solution: Install dependencies
pip install -r requirements.txt
```

---

## 📈 Performance Tuning

### **Slow Performance?**

1. **Increase workers:**
   ```ini
   workers = 10  # Change from 5
   ```

2. **Decrease timeout if network is fast:**
   ```ini
   timeout = 15  # Change from 30
   ```

3. **Check logs to see what's slow:**
   ```bash
   python execute.py --enable-crawler -d -v exec 2>&1 | grep "Thread"
   ```

### **High Resource Usage?**

1. **Decrease workers:**
   ```ini
   workers = 2  # Change from 5
   ```

2. **Run during off-peak hours**

### **Too Many Failures?**

1. **Increase timeout:**
   ```ini
   timeout = 60  # Change from 30
   ```

2. **Check network connectivity:**
   ```bash
   ping intranet.company.com
   ```

---

## 🔍 Monitoring

### **View Real-time Progress**

```bash
# Linux/Mac
tail -f execute.py 2>&1 | grep -E "Downloaded|Failed"

# Windows PowerShell
Get-Content execute.log -Tail 20 -Wait
```

### **Check Download Statistics**

```bash
# After running, check log for:
INFO - Download Summary:
  Total files: 100
  Missing: 30
  Downloaded: 28
  Failed: 2
  Already available: 70
```

### **Debug Failed Downloads**

```bash
# Enable debug mode
python execute.py --enable-crawler -d -v exec 2>&1 | tee full_log.txt

# Grep failed files
grep "Failed\|404\|403" full_log.txt
```

---

## 📋 Checklist

### **Pre-run Checklist**
- [ ] Config.ini updated with [crawler] section
- [ ] base_url is correct and accessible
- [ ] Employee images placed in `img/src_img/`
- [ ] Template image in `img/template/`
- [ ] All required fonts in `fonts/`
- [ ] Output directory `img/des_img/` exists

### **Post-run Checklist**
- [ ] Check download statistics in logs
- [ ] Verify badges generated in `img/des_img/`
- [ ] Review any failed downloads
- [ ] Update config if needed for next run

---

## 🎯 Use Cases

### **Use Case 1: First Run (All images missing)**
```bash
# Config: Adjust workers & timeout for your network
python execute.py --enable-crawler -v exec

# Watch download progress
# All images will be downloaded, then processed
```

### **Use Case 2: Incremental (Some new employees)**
```bash
# Config: Use default (only new missing images downloaded)
python execute.py --enable-crawler -v exec

# Fast because most images already downloaded
```

### **Use Case 3: Testing**
```bash
# Config: Reduce workers to avoid overload
python execute.py --enable-crawler -d -v exec --test

# Process small batch with debug output
```

### **Use Case 4: Production Batch**
```bash
# Config: Optimize for speed
# workers = 10, timeout = 20

python execute.py --enable-crawler -v exec -l exec -i 3600

# Loop every hour, keep running
```

---

## 🔗 More Information

- **Detailed Guide:** `IMAGE_MANAGER_GUIDE.md`
- **Implementation Details:** `IMPLEMENTATION_SUMMARY.md`
- **API Reference:** See `tools/image_manager.py`
- **Test/Demo:** `tools/test_image_manager.py`

---

## 💡 Pro Tips

1. **Always run with `-v` (verbose) first** - helps see what's happening
2. **Check network connectivity** - ping base_url before running
3. **Start with default workers=5** - adjust only if needed
4. **Monitor disk space** - images can take significant space
5. **Use loop mode for production** - `python execute.py --enable-crawler -v exec -l`

---

## ⚡ TL;DR

```bash
# 1. Update config.ini with [crawler] section
# 2. Run:
python execute.py --enable-crawler -v exec

# Done! ✓
```

---
