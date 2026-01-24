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
import subprocess
from pathlib import Path

def main():
    """Launch the Badge Generator GUI."""
    # Get the directory where this script is located (badge_generator folder)
    script_dir = Path(__file__).parent.resolve()
    gui_script = script_dir / 'src' / 'badge_gui.py'
    
    # Verify the GUI script exists
    if not gui_script.exists():
        print(f"Error: Could not find badge_gui.py at {gui_script}")
        print("Please ensure the badge_generator package is properly installed.")
        sys.exit(1)
    
    # Change to the badge_generator directory
    import os
    os.chdir(script_dir)
    
    # Launch the GUI
    try:
        subprocess.run([sys.executable, str(gui_script)], check=False)
    except Exception as e:
        print(f"Error launching GUI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
