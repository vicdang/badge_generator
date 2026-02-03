# -*- coding: utf-8 -*-
"""
Tools package entry point - allows running as python -m tools

This module enables running sub-modules via:
  python -m tools.image_crawler [args]
  python -m tools.image_manager [args]
"""

# No explicit implementation needed - Python will automatically route
# python -m tools.image_crawler to image_crawler.py's __main__ block
