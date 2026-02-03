#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test preview paths.

This utility script helps debug and verify that preview image paths are correctly
resolved from the configuration file.

Usage:
    python tools/test_preview_paths.py
    
    or from project root:
    python -m tools.test_preview_paths

Purpose:
    - Verifies config.ini paths are correctly set
    - Tests path resolution logic (absolute, relative, parent-relative)
    - Shows actual image files in source/output directories
    - Helps troubleshoot preview image loading issues
"""

from pathlib import Path
import sys
import io

# Set encoding to UTF-8 for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Set up path - PROJECT_ROOT is parent of this script's directory
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from src.config_manager import ConfigManager

print(f"PROJECT_ROOT: {PROJECT_ROOT}")

config = ConfigManager()
print(f"\nTemplate path (config): {config.get('template', 'filename')}")
print(f"Src path (config): {config.get('general', 'src_path')}")
print(f"Des path (config): {config.get('general', 'des_path')}")


# Test path resolution
def find_path(config_path_str):
    """Try to find path in multiple locations."""
    # Try 1: Absolute path
    p = Path(config_path_str)
    if p.is_absolute() and p.exists():
        print(f"  [+] Found absolute: {p}")
        return p
    
    # Try 2: Relative to PROJECT_ROOT
    p = PROJECT_ROOT / config_path_str
    if p.exists():
        print(f"  [+] Found relative to PROJECT_ROOT: {p}")
        return p
    
    # Try 3: Relative to parent directory (workspace level)
    p = PROJECT_ROOT.parent / config_path_str
    if p.exists():
        print(f"  [+] Found relative to parent: {p}")
        return p
    
    # Try 4: Check parent directory structure
    parent_path = PROJECT_ROOT / Path(config_path_str).parent
    if parent_path.exists():
        print(f"  [+] Found parent dir: {parent_path}")
        return parent_path
    
    print(f"  [-] Not found!")
    return None


print("\nResolving template path:")
template_path = find_path(config.get("template", "filename"))

print("\nResolving source path:")
src_path = find_path(config.get("general", "src_path"))

print("\nResolving output path:")
des_path = find_path(config.get("general", "des_path"))

print("\nActual files in source:")
if src_path:
    image_files = sorted([f for f in src_path.glob("*") if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
    if image_files:
        for f in image_files:
            try:
                print(f"  {f.name}")
            except UnicodeEncodeError:
                print(f"  {f.name.encode('utf-8', errors='replace').decode('utf-8', errors='replace')}")
    else:
        print("  (no images found)")
else:
    print("  (source path not found)")

print("\nActual files in output:")
if des_path:
    image_files = sorted([f for f in des_path.glob("*") if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
    if image_files:
        for f in image_files:
            try:
                print(f"  {f.name}")
            except UnicodeEncodeError:
                print(f"  {f.name.encode('utf-8', errors='replace').decode('utf-8', errors='replace')}")
    else:
        print("  (empty)")
else:
    print("  (output path not found)")
