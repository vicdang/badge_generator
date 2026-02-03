# Docker Setup & Usage Guide

## 📦 Overview

This guide covers Docker setup, building, and running Badge Generator in containers.

**Versions:**
- **Base Image:** Python 3.14-slim
- **Docker Compose:** v3.8
- **Supported Platforms:** Linux, macOS, Windows (with Docker Desktop)

---

## 🏗️ Project Structure

```
badgenerator/
├── Dockerfile                  # Production image definition
├── docker-compose.yml          # Base configuration (production)
├── docker-compose.override.yml # Development overrides (auto-loaded)
├── docker-compose.prod.yml     # Production deployment config
├── .dockerignore               # Files to exclude from image
├── requirements.txt            # Python dependencies
├── run.py                       # Application entry point
└── [source code, config, etc]
```

---

## 🚀 Quick Start

### Build the Image

```bash
# Build the Docker image
docker build -t badge-generator:v3.0.0 .

# Or use Docker Compose (builds automatically)
docker-compose build
```

### Run Development Mode

```bash
# Start in development (docker-compose.override.yml auto-applied)
docker-compose up

# Run with logs
docker-compose up -d
docker-compose logs -f

# Stop services
docker-compose down
```

### Run Production Mode

```bash
# Start in production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

---

## 📋 Configuration Files Explained

### docker-compose.yml (Base Configuration)
- **Purpose:** Production-ready configuration
- **Service Name:** badge-generator
- **Volume Mounts:**
  - `./images:/app/images` - Badge output and source images
  - `./config:/app/config` - Configuration files
  - `./logs:/app/logs` - Application logs
  - `./data:/app/data` - Database and mock data
  - `./tools:/app/tools` - Image crawler and utilities
  - `./resources:/app/resources` - Fonts, cascades, templates

- **Network:** badge-network (bridge driver)
- **Health Check:** Validates GUI module import
- **Default Command:** `python run.py` (GUI mode)

### docker-compose.override.yml (Development Configuration)
- **Purpose:** Automatically applied in development
- **Auto-loaded:** Docker Compose loads this automatically when it exists
- **Features:**
  - Debug mode enabled
  - Development environment variables
  - Interactive terminal (tty + stdin)
  - Extended startup timeout (20s)
  - Live code mounting for development

### docker-compose.prod.yml (Production Configuration)
- **Purpose:** Production deployment settings
- **Command:** `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`
- **Features:**
  - Auto-restart policy
  - Resource limits (2 CPU, 2GB memory)
  - Extended health check intervals
  - More retries for reliability

### Dockerfile
- **Base:** `python:3.14-slim`
- **System Dependencies:** OpenCV requirements (libsm6, libxext6, etc.)
- **Directory Structure:** Creates all required folders
- **Startup:** Runs GUI by default (`run.py`)

### .dockerignore
- **Purpose:** Reduce image size by excluding unnecessary files
- **Excludes:** Git files, Python cache, venv, IDE files, test artifacts, documentation

---

## 🔧 Environment Variables

### Development
```bash
BADGE_ENV=development          # Environment mode
DEBUG=true                      # Debug logging
PYTHONUNBUFFERED=1            # Unbuffered output
```

### Production
```bash
BADGE_ENV=production           # Environment mode
DEBUG=false                     # Disable debug
PYTHONUNBUFFERED=1            # Unbuffered output
```

---

## 📁 Volume Mounts Explained

| Host Path | Container Path | Purpose | Persistent |
|-----------|----------------|---------|-----------|
| ./images | /app/images | Badge outputs, source images | ✅ Yes |
| ./config | /app/config | Config files | ✅ Yes |
| ./logs | /app/logs | Application logs | ✅ Yes |
| ./data | /app/data | Database, mock data | ✅ Yes |
| ./tools | /app/tools | Image crawler scripts | ✅ Yes |
| ./resources | /app/resources | Fonts, cascades, templates | ✅ Yes |

---

## 🏥 Health Checks

### Development
- **Interval:** 60s
- **Timeout:** 10s
- **Retries:** 3
- **Start Period:** 10s
- **Test:** Verifies GUI module import

### Production
- **Interval:** 120s (less frequent)
- **Timeout:** 10s
- **Retries:** 5 (more tolerant)
- **Start Period:** 30s (longer startup time)

---

## 🔌 Port Configuration

### Development & Testing
- Ports are commented out by default
- No external ports exposed
- Use `docker exec` to interact

### Production (if needed)
Uncomment in docker-compose.yml:
```yaml
ports:
  - "8000:8000"  # For future REST API
```

---

## 📊 Common Commands

### View Running Containers
```bash
docker-compose ps
```

### Access Container Shell
```bash
# Development
docker-compose exec badge-generator bash

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml exec badge-generator bash
```

### View Application Logs
```bash
# Last 100 lines
docker-compose logs badge-generator -n 100

# Follow logs in real-time
docker-compose logs -f
```

### Rebuild Image
```bash
# Force rebuild (ignore cache)
docker-compose build --no-cache
```

### Clean Up
```bash
# Remove stopped containers
docker-compose down

# Remove images too
docker-compose down --rmi all

# Remove volumes (careful - deletes data!)
docker-compose down -v
```

---

## 🚨 Troubleshooting

### Issue: "Image not found"
```bash
# Rebuild the image
docker-compose build

# Or pull if using registry
docker pull badge-generator:v3.0.0
```

### Issue: "Permission denied" on volumes
```bash
# On Linux, may need to adjust permissions
sudo chown -R $(id -u):$(id -g) ./images ./logs ./data
```

### Issue: "Port already in use"
```bash
# Find what's using the port
lsof -i :8000

# Or change port in docker-compose.yml
# ports:
#   - "8001:8000"
```

### Issue: "Out of memory"
```bash
# Increase Docker memory in settings, or
# Use resource limits in docker-compose.prod.yml
```

### Issue: Container exits immediately
```bash
# Check logs
docker-compose logs badge-generator

# Get more detail
docker logs [container-id] --details
```

---

## 🔐 Security Considerations

### Current Setup
- ✅ Non-root user recommended
- ✅ Read-only file system possible
- ✅ Resource limits supported
- ✅ Health checks active

### Recommendations
1. **Production**: Create non-root user in Dockerfile
2. **Secrets**: Use Docker secrets for sensitive data
3. **Scanning**: Run `docker scan badge-generator:v3.0.0`
4. **Updates**: Regularly update base image
5. **Registry**: Use private registry for production

---

## 📈 Performance Tips

### Optimize Build Time
```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build -t badge-generator:v3.0.0 .

# Or use compose
DOCKER_BUILDKIT=1 docker-compose build
```

### Optimize Image Size
- Base image uses `-slim` variant (saves ~200MB)
- .dockerignore excludes unnecessary files
- Consider multi-stage builds if needed

### Runtime Performance
- Resource limits prevent runaway processes
- Health checks ensure stability
- Volume mounts should be on fast storage

---

## 📚 Related Documentation

- [ARCHITECTURE.md](../ARCHITECTURE.md) - Application architecture
- [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - File organization
- [DEVELOPER_GUIDE.md](../DEVELOPER_GUIDE.md) - Development setup
- [TROUBLESHOOTING_AND_FAQS.md](../TROUBLESHOOTING_AND_FAQS.md) - General troubleshooting

---

## ✅ Checklist for Docker Deployment

- [ ] Dockerfile uses Python 3.14
- [ ] All required directories created
- [ ] Volume mounts configured
- [ ] Health checks passing
- [ ] .dockerignore optimized
- [ ] Environment variables set
- [ ] docker-compose.yml validated
- [ ] docker-compose.prod.yml configured
- [ ] Resource limits set (production)
- [ ] Tested with `docker-compose up`
- [ ] Tested with production config
- [ ] Documentation updated
- [ ] Images tagged properly
- [ ] Registry configured (if needed)

---

**Last Updated:** January 27, 2026  
**Version:** 3.0.0  
**Status:** ✅ Production Ready
