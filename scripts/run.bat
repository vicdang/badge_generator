@echo off
REM Badge Generator GUI Runner - Windows Batch File
REM This script launches the Badge Generator GUI application from the project root.
REM
REM Usage:
REM   From project root: .\scripts\run.bat
REM   Or double-click this file
REM
REM This file assumes:
REM   - Project root is one level above scripts/
REM   - Python is installed and in PATH (or use venv)
REM   - run.py exists in project root

cd /d "%~dp0.."
python run.py
pause
