#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Badge Generator GUI Runner (Windows GUI Mode - No Console)

This script launches the Badge Generator GUI without showing console window.
Directly imports and runs the GUI instead of using subprocess for better reliability.

For debugging with console visible, use run.bat instead.

Usage:
    Double-click run.pyw (or: python run.pyw)
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Launch the Badge Generator GUI without console."""
    try:
        # Get the directory where this script is located
        script_dir = Path(__file__).parent.resolve()
        
        # Verify the GUI script exists
        gui_script = script_dir / 'src' / 'badge_gui.py'
        if not gui_script.exists():
            raise FileNotFoundError(f"Could not find badge_gui.py at {gui_script}")
        
        # CRITICAL: Ensure we're using the correct Python with PIL installed
        # Check which Python has PIL available
        print(f"[DEBUG] Current Python: {sys.executable}")
        print(f"[DEBUG] Python Version: {sys.version}")
        
        # Check if PIL is available in current Python
        try:
            import PIL
            print(f"[DEBUG] PIL found in current Python: {PIL.__file__}")
        except ImportError:
            # Try to find Python with PIL installed
            possible_pythons = [
                "D:\\Program Files\\Python\\Python314\\python.exe",
                "D:\\Program Files\\Python\\Python311\\python.exe",
                "C:\\Python314\\python.exe",
                "C:\\Python311\\python.exe",
            ]
            
            pil_python = None
            for py_path in possible_pythons:
                if Path(py_path).exists():
                    try:
                        result = subprocess.run(
                            [py_path, "-c", "import PIL; print('OK')"],
                            capture_output=True,
                            timeout=2
                        )
                        if result.returncode == 0:
                            pil_python = py_path
                            print(f"[DEBUG] Found PIL in: {py_path}")
                            break
                    except:
                        pass
            
            if pil_python:
                print(f"[DEBUG] Switching to Python with PIL: {pil_python}")
                # Re-launch using the correct Python
                script_path = Path(__file__).resolve()
                os.execv(pil_python, [pil_python, str(script_path)])
        
        # Change to the badgenerator directory
        os.chdir(script_dir)
        
        # Add src to path so we can import badge_gui
        sys.path.insert(0, str(script_dir))
        
        # Import and run the GUI directly (more reliable than subprocess)
        from src.badge_gui import main as gui_main
        gui_main()
        
    except Exception as e:
        # Show error using messagebox
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Badge Generator Error",
                f"Failed to launch Badge Generator GUI:\n\n{str(e)}\n\n"
                "Please check:\n"
                "1. Python is installed\n"
                "2. All required packages are installed (pip install -r requirements.txt)\n"
                "3. The src folder exists"
            )
        except:
            # If tkinter fails, print to stderr
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()


