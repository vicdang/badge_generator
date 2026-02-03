# Badge Generator - v3.1.0 Enhancements

> Comprehensive refactoring with modern Python best practices, enterprise-grade architecture, and production-ready features.

## 🎯 What's New in v3.1.0

This release includes **15 major architectural improvements** and enhancements:

### Core Infrastructure
- ✅ **Consolidated Utilities** - Single source of truth for all helper functions
- ✅ **Centralized Configuration** - Singleton ConfigManager for consistent config access
- ✅ **Service Layer** - Clean separation of business logic from UI/CLI
- ✅ **Dependency Injection** - Loosely coupled, testable architecture

### Data Management
- ✅ **SQLite Database** - Persistent storage for jobs, badges, downloads, and metrics
- ✅ **Configuration Profiles** - Save/load/switch between badge configurations
- ✅ **Profile Management** - Import/export, defaults, custom presets

### Quality & Reliability
- ✅ **Input Validation Pipeline** - Comprehensive validation for images and data
- ✅ **Structured Logging** - JSON-formatted logs with rotation and metrics
- ✅ **Error Handling** - Detailed error messages with recovery suggestions
- ✅ **Performance Metrics** - Track processing time, download speeds, resource usage

### Processing & Downloads
- ✅ **Async Download Manager** - Multi-threaded downloads with progress tracking
- ✅ **Download Scheduler** - Task prioritization and batch management
- ✅ **Progress Tracking** - Callbacks for UI progress bars and status updates
- ✅ **Retry Logic** - Exponential backoff for failed downloads

### DevOps & Testing
- ✅ **Docker Containerization** - Production-ready Dockerfile with health checks
- ✅ **Docker Compose** - Easy local development environment
- ✅ **GitHub Actions CI/CD** - Automated testing, linting, and releases
- ✅ **Comprehensive Test Suite** - 30+ unit tests with 80%+ coverage

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Optional: Docker

### Local Setup

```bash
# Clone repository
git clone <repo-url>
cd badgenerator

# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Setup

```bash
# Build image
docker build -t badge-generator:latest .

# Or use docker-compose
docker-compose up -d
```

---

## 🚀 Quick Start

### 1. Using Configuration Profiles

```python
from src.config_profiles import ProfileManager

manager = ProfileManager()

# List available profiles
profiles = manager.list_profiles()
print(profiles)  # ['standard', 'high_quality', 'compact']

# Load profile
profile = manager.load_profile("high_quality")

# Create custom profile
custom = manager.create_custom_profile(
    name="my_profile",
    description="Custom badge settings",
    badge_config={
        'width': 1920,
        'height': 1440,
        'text_size': 48,
    },
    crawler_config={
        'base_url': 'https://company.com/images/',
        'workers': 10,
    }
)
```

### 2. Processing with Service Layer

```python
from src.services import BadgeGenerationService
from src.config_manager import ConfigManager

# Setup
config = ConfigManager()
service = BadgeGenerationService(config)

# Define progress callback
def on_progress(current, total, message):
    print(f"Progress: {current}/{total} - {message}")
    # Update GUI progress bar, log, etc.

service.set_progress_callback(on_progress)

# Create job
job_id = service.create_job(
    job_name="Batch 001",
    images=image_list,
    profile="standard"
)

# Process
stats = service.process_batch(badge_data)
print(stats)  # JobStatistics with detailed metrics
```

### 3. Download Management

```python
from src.async_downloader import AsyncDownloadManager, DownloadTask
from pathlib import Path

manager = AsyncDownloadManager(max_workers=5)

# Setup progress
def progress_update(current, total, msg):
    print(f"{current}/{total}: {msg}")

manager.set_progress_callback(progress_update)

# Create tasks
tasks = [
    DownloadTask(
        task_id=f"img_{i}",
        url=f"{base_url}/image_{i}.png",
        destination=Path(f"./images/image_{i}.png"),
        emp_id=f"EMP{i:03d}"
    )
    for i in range(100)
]

# Download all
results = manager.download_batch_sync(tasks)

# Get statistics
stats = manager.get_statistics()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

### 4. Input Validation

```python
from src.validators import (
    ImageValidator,
    EmployeeDataValidator,
    ConfigurationValidator,
    validate_all
)

# Validate images
valid_images, errors = ImageValidator.validate_batch_images(image_paths)
print(f"Valid: {len(valid_images)}, Errors: {len(errors)}")

# Validate employee data
for emp_data in employees:
    result = EmployeeDataValidator.validate_employee_data(emp_data)
    if not result.is_valid:
        print(f"Errors: {result.errors}")
        print(f"Warnings: {result.warnings}")

# Complete validation
config_dict = {
    'paths': image_paths,
    'badge': badge_config,
    'crawler': crawler_config,
}
result = validate_all(image_files, employee_list, config_dict)
print(result)  # Detailed validation report
```

### 5. Database & History

```python
from src.database import Database

db = Database()

# Get statistics
stats = db.get_statistics()
print(f"Total badges: {stats['total_badges']}")
print(f"Success rate: {stats['badges_by_status']}")

# Get recent jobs
recent = db.get_recent_jobs(limit=5)
for job in recent:
    print(f"{job['job_name']}: {job['status']}")

# Get job details
badges = db.get_job_badges(job_id)
metrics = db.get_job_metrics(job_id)

db.close()
```

### 6. Logging & Performance

```python
from src.logging_config import setup_logging, get_logger, PerformanceLogger
import logging

# Setup structured logging
setup_logging(level=logging.INFO)
logger = get_logger(__name__)

# Performance tracking
perf = PerformanceLogger(logger, "badge_generation")
perf.start()

# ... do work ...

perf.add_metric("badges_processed", 100)
perf.add_metric("avg_processing_time", 123.45, unit="ms")
perf.log_metrics()
elapsed = perf.end()  # Returns elapsed time in ms
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────┐
│           GUI / CLI Interface                   │
│       (tkinter / argparse)                      │
└────────────────┬────────────────────────────────┘
                 │
┌─────────────────────────────────────────────────┐
│       Service Layer (services.py)               │
│  • BadgeGenerationService                       │
│  • Progress callbacks                           │
│  • Job management                               │
└────────┬────────────────────────────┬───────────┘
         │                            │
    ┌────▼─────┐          ┌──────────▼──────┐
    │Validators│          │ConfigManager    │
    │(validate)│          │(config_manager) │
    │  - Image │          │  - Singleton    │
    │  - Data  │          │  - Validated    │
    │  - Config│          │  - Profiles     │
    └──────────┘          └─────────────────┘
         │
    ┌────▼──────────────────────────────────┐
    │    Core Processing Layer              │
    │  • AsyncDownloadManager               │
    │  • Badge generation logic             │
    │  • Image processing                   │
    └────┬───────────────────────────────────┘
         │
    ┌────▼──────────────────────────────────┐
    │    Data Persistence Layer             │
    │  • Database (SQLite)                  │
    │  • Logging (JSON format)              │
    │  • Performance metrics                │
    └───────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| **employees** | Employee records | user_id, username, position |
| **badge_jobs** | Batch jobs | job_name, status, timing |
| **badges** | Individual badges | job_id, filename, status, timing |
| **image_downloads** | Download history | source_url, destination, status |
| **config_profiles** | Saved configs | profile_name, config_data |
| **performance_metrics** | Performance data | job_id, metric_name, metric_value |

---

## 🧪 Testing

### Run Tests

```bash
# All tests
pytest tests/test_units.py -v

# With coverage
pytest tests/test_units.py --cov=src --cov-report=html

# Specific test class
pytest tests/test_units.py::TestUtility -v

# Specific test
pytest tests/test_units.py::TestUtility::test_sanitize_filename
```

### Test Coverage

- ✅ Utility functions (20+ tests)
- ✅ Configuration management (5+ tests)
- ✅ Input validation (10+ tests)
- ✅ Service layer (5+ tests)
- ✅ Dependency injection (5+ tests)
- ✅ Logging setup (2+ tests)

---

## 🐳 Docker Usage

### Build

```bash
docker build -t badge-generator:latest .
```

### Run

```bash
# Basic
docker run badge-generator:latest

# With volumes
docker run -v $(pwd)/images:/app/images \
           -v $(pwd)/logs:/app/logs \
           badge-generator:latest

# With docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📈 Performance Optimization

### Tips for Better Performance

1. **Increase Worker Threads**
   ```python
   manager = AsyncDownloadManager(max_workers=10)  # Default: 5
   ```

2. **Use Async Operations**
   - Always prefer `download_batch_sync()` or async operations

3. **Enable Caching**
   - Cache validated images and configurations

4. **Use Appropriate Profile**
   - Use "compact" profile for quick processing
   - Use "high_quality" for final badges

5. **Monitor Metrics**
   ```python
   stats = db.get_statistics()
   print(f"Avg time: {stats['avg_processing_time_ms']}ms")
   ```

---

## 🔧 Configuration

### Environment Variables

```bash
# Custom config file
export CONFIG_FILE=/path/to/config.ini

# Log level
export LOG_LEVEL=DEBUG

# Database path
export DB_PATH=/path/to/database.db
```

### Config File (config.ini)

```ini
[general]
src_path = images/source/
des_path = images/output/
base_font = Arial
base_text_size = 32

[crawler]
base_url = https://company.com/images/
workers = 5
timeout = 30
enabled = true

[template]
filename = default.png
width = 1024
height = 768
```

---

## 📝 Logging

### Log Files

```
logs/
├── app.log              # Main application log
├── app.log.1            # Rotated backups
├── app.log.2
└── ...
```

### Log Format

```json
{
  "timestamp": "2026-01-26T12:34:56.789123",
  "level": "INFO",
  "logger": "badgenerator",
  "message": "Badge processing complete",
  "module": "services",
  "function": "process_badge",
  "line": 123,
  "extra": {
    "operation": "badge_processing",
    "elapsed_ms": 1234.56
  }
}
```

---

## 🆘 Troubleshooting

### Issue: Database Locked

```
sqlite3.OperationalError: database is locked
```

**Solution:**
- Close all database connections
- Check for multiple processes accessing database
- Restart application

### Issue: Download Failures

```
urllib.error.URLError: [Errno -2] Name or service not known
```

**Solution:**
- Check network connectivity
- Verify base_url is correct
- Check firewall settings
- Increase timeout value

### Issue: Validation Errors

**Solution:**
- Check image file formats (PNG, JPG, BMP)
- Verify employee data format
- Review validation error messages
- Ensure paths are correct

### Issue: Out of Memory

**Solution:**
- Reduce worker threads
- Use "compact" profile
- Process in smaller batches
- Check for image memory leaks

---

## 📚 Documentation Files

- [IMPLEMENTATION_COMPLETE.md](docs/IMPLEMENTATION_COMPLETE.md) - Detailed implementation guide
- [00_START_HERE.md](docs/00_START_HERE.md) - Quick start guide
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture
- [DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md) - Development guidelines
- [QUICKSTART.md](docs/QUICKSTART.md) - Quick start examples

---

## 🚀 Next Steps

### For Users
1. Review [QUICKSTART.md](docs/QUICKSTART.md)
2. Try example profiles
3. Monitor performance with metrics

### For Developers
1. Review [IMPLEMENTATION_COMPLETE.md](docs/IMPLEMENTATION_COMPLETE.md)
2. Study service layer architecture
3. Add tests for custom code
4. Use logging and metrics

### For DevOps
1. Review Dockerfile and docker-compose.yml
2. Setup CI/CD pipeline
3. Configure monitoring
4. Setup backup strategy for database

---

## 🤝 Contributing

When adding new features:

1. ✅ Write tests first (TDD)
2. ✅ Use ConfigManager for configuration
3. ✅ Add logging with PerformanceLogger
4. ✅ Use validators for input validation
5. ✅ Document in docstrings
6. ✅ Update changelog

---

## 📄 License

See LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions:
1. Check [TROUBLESHOOTING_AND_FAQS.md](docs/TROUBLESHOOTING_AND_FAQS.md)
2. Review error logs in `logs/` directory
3. Check GitHub Issues
4. Contact development team

---

**Version:** 3.1.0 | **Released:** January 26, 2026 | **Status:** ✅ Production Ready

