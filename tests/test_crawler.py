#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script for image crawler with trna URL."""

import sys
import logging
import urllib.request
import urllib.error
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_url_connectivity(url: str, timeout: int = 5) -> bool:
    """
    Test if URL is accessible.

    Args:
        url: URL to test.
        timeout: Timeout in seconds.

    Returns:
        True if accessible, False otherwise.
    """
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        response = urllib.request.urlopen(req, timeout=timeout)
        logger.info(f"✅ URL is accessible (HTTP {response.status})")
        logger.info(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        logger.info(f"   Content-Length: {response.headers.get('Content-Length', 'Unknown')} bytes")
        return True
    except urllib.error.HTTPError as e:
        logger.error(f"❌ HTTP Error: {e.code} - {e.reason}")
        return False
    except urllib.error.URLError as e:
        logger.error(f"❌ URL Error: {e.reason}")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return False


def test_crawler():
    """Test image crawler with trna URL."""
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║" + " " * 68 + "║")
    logger.info("║" + "  TESTING IMAGE CRAWLER".center(68) + "║")
    logger.info("║" + "  trna Intranet URL + WebP Format".center(68) + "║")
    logger.info("║" + " " * 68 + "║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")

    # Test parameters
    test_emp_id = "Test_154176_A"
    test_url = "https://intranet.trna.com.vn/images/emp_images/big_new"
    test_output = Path("./images/test/test_download")
    test_output.mkdir(parents=True, exist_ok=True)

    logger.info("📋 TEST PARAMETERS")
    logger.info("━" * 70)
    logger.info(f"Employee ID: {test_emp_id}")
    logger.info(f"Base URL: {test_url}")
    logger.info(f"Output Directory: {test_output}")
    logger.info("")

    # Parse employee ID
    logger.info("🔍 PARSING EMPLOYEE ID")
    logger.info("━" * 70)
    parts = test_emp_id.split("_")
    name, uid, pos = parts[0], parts[1], parts[2]

    prep = ""
    if uid and uid[0] in ("T", "B"):
        prep = uid[0]
        uid = uid[1:]

    uid_int = int(uid)
    download_url = f"{test_url}/{uid_int}.webp"
    output_file = test_output / f"{name}_{prep}{uid_int}_{pos}_1.webp"

    logger.info(f"Name: {name}")
    logger.info(f"UID: {uid} → {uid_int} (prefix: {prep})")
    logger.info(f"Position: {pos}")
    logger.info(f"Constructed URL: {download_url}")
    logger.info(f"Output File: {output_file}")
    logger.info("")

    # Test URL connectivity
    logger.info("🌐 TESTING URL CONNECTIVITY")
    logger.info("━" * 70)
    success = test_url_connectivity(download_url)
    logger.info("")

    if success:
        logger.info("✅ CRAWLER IS READY FOR PRODUCTION")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Prepare employee ID list (Excel or text file)")
        logger.info("  2. Run: python -m tools.image_crawler -f <file> -w 5")
        logger.info("  3. Or use: python execute.py exec --enable-crawler")
    else:
        logger.error("⚠️  URL is not accessible from this network")
        logger.error("Please verify:")
        logger.error("  • Network connectivity")
        logger.error("  • VPN connection (if required)")
        logger.error("  • URL is correct: " + download_url)

    logger.info("")
    logger.info("=" * 70)


if __name__ == "__main__":
    test_crawler()
