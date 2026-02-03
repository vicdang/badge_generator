#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Badge Generator GUI Runner

This script launches the Badge Generator GUI application.
It provides an easy way to run the badge generation tool.

Usage:
    python run.py
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the Badge Generator GUI."""
    # Get the directory where this script is located (badgenerator folder)
    script_dir = Path(__file__).parent.resolve()
    
    # Change to the badgenerator directory
    os.chdir(script_dir)
    
    # Add the script directory to Python path to ensure proper imports
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))
    
    # Import and launch the GUI directly (same Python process, same environment)
    try:
        from src.badge_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error importing GUI module: {e}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
