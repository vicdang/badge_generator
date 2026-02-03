#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Badge Generator Environment Verification Script

This script verifies that the Badge Generator environment is properly set up
and all components can communicate correctly.

Usage:
    python tools/verify_environment.py
    
    or from project root:
    python -m tools.verify_environment

Checks performed:
    1. Python environment and version
    2. Virtual environment structure and integrity
    3. Required dependencies (PIL, cv2, openpyxl, etc.)
    4. Image crawler module availability
    5. Configuration files existence
    6. Subprocess Python detection and functionality
"""

import sys
import subprocess
from pathlib import Path
import io

# Set encoding to UTF-8 for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def check_python_env():
    """Check Python environment."""
    print("=" * 60)
    print("1. PYTHON ENVIRONMENT")
    print("=" * 60)
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Virtual Environment: {hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)}")
    return True


def check_venv_structure():
    """Check virtual environment structure."""
    print("\n" + "=" * 60)
    print("2. VIRTUAL ENVIRONMENT STRUCTURE")
    print("=" * 60)
    
    # PROJECT_ROOT is parent of tools directory
    project_root = Path(__file__).parent.parent.resolve()
    
    # Check workspace level venv
    workspace_venv = project_root.parent / '.venv'
    workspace_cfg = workspace_venv / 'pyvenv.cfg'
    workspace_py = workspace_venv / 'Scripts' / 'python.exe'
    
    print(f"Workspace venv exists: {workspace_venv.exists()}")
    print(f"  pyvenv.cfg: {workspace_cfg.exists()}")
    print(f"  python.exe: {workspace_py.exists()}")
    
    # Check project level venv
    project_venv = project_root / '.venv'
    project_cfg = project_venv / 'pyvenv.cfg'
    
    print(f"Project venv exists: {project_venv.exists()}")
    print(f"  pyvenv.cfg: {project_cfg.exists()}")
    
    return workspace_cfg.exists() or project_cfg.exists()


def check_dependencies():
    """Check required dependencies."""
    print("\n" + "=" * 60)
    print("3. REQUIRED DEPENDENCIES")
    print("=" * 60)
    
    dependencies = [
        'PIL',           # Pillow
        'cv2',           # opencv-python
        'openpyxl',      # Excel support
        'qrcode',        # QR code generation
        'requests',      # HTTP requests
        'tkinter',       # GUI
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"[OK] {dep:<20} OK")
        except ImportError:
            print(f"[XX] {dep:<20} MISSING")
            all_ok = False
    
    return all_ok


def check_image_crawler():
    """Check image crawler module."""
    print("\n" + "=" * 60)
    print("4. IMAGE CRAWLER MODULE")
    print("=" * 60)
    
    try:
        # Check if image_crawler.py file exists
        project_root = Path(__file__).parent.parent.resolve()
        crawler_file = project_root / 'tools' / 'image_crawler.py'
        
        if not crawler_file.exists():
            print("✗ Image crawler file not found")
            return False
        
        print("✓ Image crawler module file exists")
        
        # Check data file
        data_file = project_root / 'tools' / 'data.xlsx'
        data_exists = data_file.exists()
        print(f"✓ Data file exists: {data_exists}")
        
        return data_exists
    except Exception as e:
        print(f"✗ Image crawler check failed: {e}")
        return False


def check_config():
    """Check configuration files."""
    print("\n" + "=" * 60)
    print("5. CONFIGURATION FILES")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent.resolve()
    config_file = project_root / 'config' / 'config.ini'
    positions_file = project_root / 'config' / 'positions.json'
    
    print(f"config.ini exists: {config_file.exists()}")
    print(f"positions.json exists: {positions_file.exists()}")
    
    return config_file.exists() and positions_file.exists()


def check_subprocess_python():
    """Check subprocess Python detection."""
    print("\n" + "=" * 60)
    print("6. SUBPROCESS PYTHON DETECTION")
    print("=" * 60)
    
    project_root = Path(__file__).parent.parent.resolve()
    
    # Simulate the detection logic from badge_gui.py
    python_exe = sys.executable
    venv_paths = [
        project_root / '.venv' / 'Scripts' / 'python.exe',         # Project level
        project_root.parent / '.venv' / 'Scripts' / 'python.exe',  # Workspace level
    ]
    
    for venv_path in venv_paths:
        try:
            venv_root = venv_path.parent.parent
            if (venv_root / 'pyvenv.cfg').exists():
                python_exe = str(venv_path.resolve())
                break
        except Exception:
            continue
    
    print(f"Selected Python: {python_exe}")
    
    # Test subprocess
    try:
        result = subprocess.run(
            [python_exe, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"✓ Subprocess Python works: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"✗ Subprocess Python failed: {e}")
        return False


def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("BADGE GENERATOR ENVIRONMENT VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Python Environment", check_python_env),
        ("Virtual Environment Structure", check_venv_structure),
        ("Required Dependencies", check_dependencies),
        ("Image Crawler Module", check_image_crawler),
        ("Configuration Files", check_config),
        ("Subprocess Python Detection", check_subprocess_python),
    ]
    
    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"\n[XX] Error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "[OK]" if result else "[XX]"
        print(f"{status:<10} {name}")
    
    all_pass = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_pass:
        print("[OK] ALL CHECKS PASSED - Environment is ready!")
    else:
        print("[XX] SOME CHECKS FAILED - Please fix issues above")
    print("=" * 60 + "\n")
    
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
