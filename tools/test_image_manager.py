# -*- coding: utf-8 -*-
"""
Image Manager Demo & Test Script

This script demonstrates how to use ImageManager for automatic image downloading
"""

import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

from tools.image_manager import ImageManager


def demo_basic_usage():
    """Demo 1: Basic usage"""
    print("\n" + "="*60)
    print("DEMO 1: Basic Usage")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    # Get local images
    local_images = img_manager.get_local_images()
    print(f"\n✓ Local images found: {len(local_images)}")
    for img in local_images[:3]:
        print(f"  - {img}")
    if len(local_images) > 3:
        print(f"  ... and {len(local_images) - 3} more")


def demo_filename_parsing():
    """Demo 2: Filename parsing"""
    print("\n" + "="*60)
    print("DEMO 2: Filename Parsing")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    test_filenames = [
        "john_001_SE_1.png",
        "jane_002_TL_1.jpg",
        "bob_T123_PM_2.bmp",
        "alice_B456_D_1.jpeg"
    ]
    
    print("\nParsing filenames:")
    for filename in test_filenames:
        emp_id = img_manager.get_employee_id_from_filename(filename)
        print(f"  {filename:30} → emp_id: {emp_id}")


def demo_check_files():
    """Demo 3: Check file existence"""
    print("\n" + "="*60)
    print("DEMO 3: File Existence Check")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    test_files = [
        "existing_file.png",  # Likely doesn't exist
        "another_file.jpg",   # Likely doesn't exist
    ]
    
    print("\nChecking file existence:")
    for filename in test_files:
        exists = img_manager.file_exists(filename)
        status = "✓ EXISTS" if exists else "✗ MISSING"
        print(f"  {filename:30} → {status}")


def demo_missing_files():
    """Demo 4: Find missing files"""
    print("\n" + "="*60)
    print("DEMO 4: Find Missing Files")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    test_files = [
        "john_001_SE_1.png",
        "jane_002_TL_1.jpg",
        "nonexistent_file_123.png",
        "another_missing_file.jpg"
    ]
    
    missing = img_manager.get_missing_images(test_files)
    
    print(f"\nChecking {len(test_files)} files:")
    print(f"  Available: {len(test_files) - len(missing)}")
    print(f"  Missing: {len(missing)}")
    
    if missing:
        print("\n  Missing files:")
        for filename in missing:
            emp_id = img_manager.get_employee_id_from_filename(filename)
            print(f"    - {filename} (emp_id: {emp_id})")


def demo_url_building():
    """Demo 5: URL building"""
    print("\n" + "="*60)
    print("DEMO 5: URL Building")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    test_emp_ids = ["001", "T123", "B456", "01234", "0001"]
    
    print("\nBuilding download URLs:")
    for emp_id in test_emp_ids:
        url = img_manager.build_download_url(emp_id)
        print(f"  emp_id: {emp_id:10} → {url}")


def demo_format_validation():
    """Demo 6: Image format validation"""
    print("\n" + "="*60)
    print("DEMO 6: Image Format Validation")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new"
    )
    
    test_files = [
        "image.png",
        "image.jpg",
        "image.jpeg",
        "image.bmp",
        "image.gif",     # Not supported
        "image.txt",     # Not supported
        "image.PDF",     # Not supported
    ]
    
    print("\nValidating image formats:")
    for filename in test_files:
        valid = img_manager.validate_image_format(filename)
        status = "✓ VALID" if valid else "✗ INVALID"
        print(f"  {filename:20} → {status}")


def demo_download_simulation():
    """Demo 7: Download simulation (without actual download)"""
    print("\n" + "="*60)
    print("DEMO 7: Download Statistics (Simulation)")
    print("="*60)
    
    img_manager = ImageManager(
        src_path="./img/src_img/",
        base_url="https://intranet.company.com/images/emp_images/big_new",
        workers=5
    )
    
    # Get current local images
    local_images = img_manager.get_local_images()
    
    print(f"\nCurrent local images: {len(local_images)}")
    print(f"Download would use: 5 workers")
    print(f"Timeout per download: 30 seconds")
    
    # Simulate check
    print("\nExample download statistics:")
    stats = {
        'total': 100,
        'missing': 30,
        'downloaded': 0,
        'failed': 0,
        'skipped': 70,
    }
    
    for key, value in stats.items():
        print(f"  {key}: {value}")


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  IMAGE MANAGER DEMO & TEST SCRIPT".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    demos = [
        ("Basic Usage", demo_basic_usage),
        ("Filename Parsing", demo_filename_parsing),
        ("File Existence Check", demo_check_files),
        ("Find Missing Files", demo_missing_files),
        ("URL Building", demo_url_building),
        ("Format Validation", demo_format_validation),
        ("Download Simulation", demo_download_simulation),
    ]
    
    print("\nAvailable demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all demos...\n")
    
    for name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("✓ All demos completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
