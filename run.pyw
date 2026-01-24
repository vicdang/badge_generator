#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Badge Generator GUI Runner (Windows GUI Mode - No Console)

This script launches the Badge Generator GUI without showing console window.
Uses subprocess.CREATE_NO_WINDOW to suppress console on Windows.

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
        gui_script = script_dir / 'src' / 'badge_gui.py'
        
        # Verify the GUI script exists
        if not gui_script.exists():
            raise FileNotFoundError(f"Could not find badge_gui.py at {gui_script}")
        
        # Change to the badge_generator directory
        os.chdir(script_dir)
        
        # Find the correct Python executable (prefer venv)
        python_exe = sys.executable
        
        # Check for venv Python first - PROJECT level is preferred (has the packages)
        venv_paths = [
            script_dir / '.venv' / 'Scripts' / 'python.exe',        # Project level venv (PREFERRED - has packages)
            script_dir.parent / '.venv' / 'Scripts' / 'python.exe', # Workspace level venv
            script_dir.parent / 'venv' / 'Scripts' / 'python.exe',  # Alt venv location
        ]
        
        for venv_python in venv_paths:
            if venv_python.exists():
                python_exe = str(venv_python.resolve())  # Use absolute resolved path
                break
        
        # Try to get pythonw.exe from the same directory as python.exe
        python_dir = Path(python_exe).parent
        pythonw_exe = python_dir / 'pythonw.exe'
        
        if pythonw_exe.exists():
            python_exe = str(pythonw_exe.resolve())  # Use absolute resolved path
        # Otherwise use python_exe as-is (it will work, just may show console)
        
        # Windows: CREATE_NO_WINDOW flag to suppress console
        kwargs = {}
        if hasattr(subprocess, 'CREATE_NO_WINDOW'):
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        
        # Launch the GUI without console
        subprocess.Popen([python_exe, str(gui_script)], **kwargs)
        
    except Exception as e:
        # Show error using messagebox
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
        sys.exit(1)

if __name__ == '__main__':
    main()


