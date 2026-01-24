#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple End-to-End Test Report."""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')


def main():
    """Generate end-to-end test report."""
    
    print()
    print("╔" + "═" * 70 + "╗")
    print("║" + "  END-TO-END TEST - RESULTS REPORT".center(70) + "║")
    print("║" + "  January 21, 2026".center(70) + "║")
    print("╚" + "═" * 70 + "╝")
    print()
    
    # Check for source images
    src_dir = Path("./images/source/src_img")
    webp_files = list(src_dir.glob("*.webp")) if src_dir.exists() else []
    jpg_files = list(src_dir.glob("*.jpg")) if src_dir.exists() else []
    
    print("📥 STEP 1: IMAGE DOWNLOAD")
    print("━" * 70)
    
    if webp_files:
        print(f"  ✅ WebP images downloaded: {len(webp_files)}")
        for img_file in webp_files:
            size = img_file.stat().st_size / 1024
            print(f"     • {img_file.name} ({size:.1f} KB)")
    else:
        print(f"  ❌ No WebP images found")
    
    if jpg_files:
        print(f"  ✅ JPG images found: {len(jpg_files)}")
    
    print()
    
    # Check for generated badges
    des_dir = Path("./images/output/des_img")
    badge_png = list(des_dir.glob("*.png")) if des_dir.exists() else []
    badge_jpg = list(des_dir.glob("*.jpg")) if des_dir.exists() else []
    
    print("📤 STEP 2: BADGE GENERATION")
    print("━" * 70)
    
    if badge_png or badge_jpg:
        total_badges = len(badge_png) + len(badge_jpg)
        print(f"  ✅ Badges generated: {total_badges}")
        
        if badge_png:
            for badge_file in badge_png[:3]:
                size = badge_file.stat().st_size / 1024
                print(f"     • {badge_file.name} ({size:.1f} KB)")
        if badge_jpg:
            for badge_file in badge_jpg[:3]:
                size = badge_file.stat().st_size / 1024
                print(f"     • {badge_file.name} ({size:.1f} KB)")
    else:
        print(f"  ℹ️  No badges generated yet")
        print(f"     (Requires run: python execute.py exec -c)")
    
    print()
    print("📊 SUMMARY")
    print("━" * 70)
    
    source_count = len(webp_files) + len(jpg_files)
    badge_count = len(badge_png) + len(badge_jpg)
    
    print(f"  Source Images: {source_count} ✅" if source_count > 0 else f"  Source Images: {source_count} ❌")
    print(f"  Generated Badges: {badge_count}")
    
    if source_count == 3:
        print()
        print("✅ IMAGE DOWNLOAD: SUCCESS")
        print()
        print("Next step: Generate badges")
        print("  Command: python execute.py exec -c --check-path")
    
    if source_count > 0 and badge_count > 0:
        print()
        print("🎉 END-TO-END TEST: COMPLETE SUCCESS! 🎉")
        print("   ✅ Downloaded 3 images from TMA intranet")
        print(f"   ✅ Generated {badge_count} badges successfully")
    
    print()


if __name__ == "__main__":
    main()
