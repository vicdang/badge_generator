#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create test images with Vietnamese names for Badge Generator testing.

This utility script generates sample badge images with Vietnamese names
to test the badge generation and preview functionality.

Usage:
    python scripts/create_test_images.py
    
    or from project root:
    python -m scripts.create_test_images

Files created:
    - Images are created in: images/source/
    - Each image is 200x200 pixels with name text
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path

# Get project root (parent of this script's directory)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
src_dir = PROJECT_ROOT / 'images' / 'source'

# Create directory if it doesn't exist
src_dir.mkdir(parents=True, exist_ok=True)

filenames = [
    'Hồ Đức Hải_T815714_VP_2.bmp',
    'Lâm Sơn Đình Đại_B672542_SD_2.png',
    'Nguyễn Nhật Quốc_455189_SME_1.jpg',
    'Đặng Tú Yến Mai_B845013_E_2.bmp',
    'Đỗ Hữu Huy_T597678_SE_1.bmp'
]

print(f"Creating test images in: {src_dir}\n")

for filename in filenames:
    try:
        # Create a simple test image (200x200 with a color)
        img = Image.new('RGB', (200, 200), color='white')
        draw = ImageDraw.Draw(img)
        name_part = filename.split('_')[0][:15]
        draw.text((10, 10), name_part, fill='black')
        
        filepath = src_dir / filename
        img.save(filepath)
        print(f"✓ Created: {filename}")
    except Exception as e:
        print(f"✗ Failed to create {filename}: {e}")

print(f"\nAll test images created successfully in {src_dir}")
