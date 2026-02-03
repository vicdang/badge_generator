# -*- coding: utf-8 -*-
"""
Badge Generator GUI - Graphical interface for badge generation.

Copyright (C) 2021
Authors: Vic Dang
Date: 16-Dec-21
Version: 1.0

Usage example:
  python execute_gui.py
"""

import re
import subprocess
import sys
import os
import threading
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser as tkcolor
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple

# First, write detailed diagnostics to a file
_diagnostics = []
_diagnostics.append(f"Python Executable: {sys.executable}")
_diagnostics.append(f"Python Version: {sys.version}")
_diagnostics.append(f"sys.path[0]: {sys.path[0] if sys.path else 'EMPTY'}")
_diagnostics.append(f"Working Directory: {os.getcwd()}")
_pil_error_details = None

HAS_PIL = False
HAS_PIL_IMAGE = False
HAS_PIL_IMAGETK = False
_pil_msg = "[SYSTEM] PIL Status: UNKNOWN"

try:
    _diagnostics.append("Attempting: from PIL import Image")
    from PIL import Image
    _diagnostics.append("SUCCESS: PIL.Image imported")
    HAS_PIL_IMAGE = True
except ImportError as e:
    _diagnostics.append(f"FAILED: PIL.Image - {e}")
    _pil_error_details = f"PIL.Image: {e}\n"
except Exception as e:
    _diagnostics.append(f"FAILED: PIL.Image (Exception) - {e}")
    _pil_error_details = f"PIL.Image Exception: {e}\n"

try:
    _diagnostics.append("Attempting: from PIL import ImageTk")
    from PIL import ImageTk
    _diagnostics.append("SUCCESS: PIL.ImageTk imported")
    HAS_PIL_IMAGETK = True
except ImportError as e:
    _diagnostics.append(f"FAILED: PIL.ImageTk - {e}")
    if _pil_error_details:
        _pil_error_details += f"PIL.ImageTk: {e}\n"
    else:
        _pil_error_details = f"PIL.ImageTk: {e}\n"
except Exception as e:
    _diagnostics.append(f"FAILED: PIL.ImageTk (Exception) - {e}")
    if _pil_error_details:
        _pil_error_details += f"PIL.ImageTk Exception: {e}\n"
    else:
        _pil_error_details = f"PIL.ImageTk Exception: {e}\n"

# We need BOTH PIL.Image AND PIL.ImageTk for preview functionality
HAS_PIL = HAS_PIL_IMAGE and HAS_PIL_IMAGETK

if HAS_PIL:
    _pil_msg = "[SYSTEM] PIL Status: AVAILABLE"
    _diagnostics.append("PIL import: SUCCESS (both Image and ImageTk available)")
else:
    _pil_msg = f"[SYSTEM] PIL Status: NOT AVAILABLE"
    if HAS_PIL_IMAGE and not HAS_PIL_IMAGETK:
        _diagnostics.append("PIL import: PARTIAL - Image available but ImageTk FAILED")
    elif HAS_PIL_IMAGETK and not HAS_PIL_IMAGE:
        _diagnostics.append("PIL import: PARTIAL - ImageTk available but Image FAILED")
    else:
        _diagnostics.append("PIL import: FAILED - Both Image and ImageTk missing")
    
    # Create dummy classes so code doesn't crash if PIL is missing
    class Image:
        class Resampling:
            LANCZOS = 1
        @staticmethod
        def open(*args, **kwargs):
            raise RuntimeError("PIL not available")
    class ImageTk:
        @staticmethod
        def PhotoImage(*args, **kwargs):
            raise RuntimeError("PIL not available")

# Try to diagnose further if PIL failed
if not HAS_PIL:
    try:
        import importlib.util
        pil_spec = importlib.util.find_spec("PIL")
        if pil_spec:
            _diagnostics.append(f"PIL module found at: {pil_spec.origin}")
        else:
            _diagnostics.append("PIL module NOT found in any sys.path")
            _diagnostics.append(f"sys.path entries: {sys.path[:5]}")
    except Exception as diag_err:
        _diagnostics.append(f"Diagnosis failed: {diag_err}")

# Write diagnostics to file - use project root for visibility
try:
    from pathlib import Path
    diag_file = Path(__file__).parent.parent.parent / "PIL_ERROR_LOG.txt"
    with open(diag_file, "w", encoding="utf-8") as f:
        f.write("\n".join(_diagnostics))
        if _pil_error_details:
            f.write(f"\n\nDETAILED ERROR:\n{_pil_error_details}")
except Exception as write_err:
    pass

# Print status immediately at module load
print(_pil_msg)
print(f"[DEBUG] Python: {sys.executable}")
print(f"[DEBUG] sys.path[0]: {sys.path[0] if sys.path else 'EMPTY'}")
print(f"[DEBUG] Working dir: {os.getcwd()}")
if not HAS_PIL:
    print(f"[DEBUG] **CRITICAL: PIL IMPORT FAILED - Check PIL_ERROR_LOG.txt for details**")

# Try relative import first (when imported as module), fall back to absolute import (when run as script)
try:
    from .config import get_gui_config
except ImportError:
    from config import get_gui_config

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
CONFIG_FILE = str(PROJECT_ROOT / 'config' / 'config.ini')
UI_CONFIG = get_gui_config()

# Window settings from config
WINDOW_TITLE = UI_CONFIG['window_title']
GRID_COLS = UI_CONFIG['grid_cols']
WINDOW_HEIGHT = UI_CONFIG['window_height']
WINDOW_WIDTH = UI_CONFIG['window_width']

# Friendly label mapping for config keys
LABEL_MAPPING = {
    # General section
    'interval': 'Interval (s)',
    'img_prefix': 'Prefix',
    'src_path': 'Source',
    'des_path': 'Output',
    'tmp_path': 'Temp Dir',
    'converted_path': 'Convert Dir',
    'base_font': 'Font',
    'mode': 'Mode',
    'base_text_size': 'Text Size',
    'background_color': 'BG Color',
    
    # Template section
    'width': 'Width',
    'height': 'Height',
    'avata_x': 'Avatar X',
    'avata_y': 'Avatar Y',
    'avata_w': 'Avatar W',
    'avata_h': 'Avatar H',
    'filename': 'Template',
    'padding': 'Padding',
    
    # Avatar section
    'scalefactor': 'Scale',
    
    # Username section
    'toppad': 'Top Pad',
    'font': 'Font',
    'size': 'Size',
    'color': 'Color',
    
    # Position section (uses same keys as username)
    
    # UserID section (uses same keys as username)
    
    # QRCode section
    'version': 'Version',
    'boxsize': 'Box Size',
    'border': 'Border',
    'fit': 'Auto Fit',
    'fillcolor': 'Fill',
    'backcolor': 'Back',
    'qr_x': 'QR X',
    'qr_y': 'QR Y',
    'qr_w': 'QR W',
    'qr_h': 'QR H',
    
    # Crawler section
    'base_url': 'Base URL',
    'workers': 'Workers',
    'timeout': 'Timeout',
    
    # Cleanup section
    'enabled': 'Enabled',
    'clean_root': 'Clean Dir',
    'skip_paths': 'Skip Paths',
    
    # UI Settings section
    'show_success': 'Success Msg',
    'show_error': 'Error Msg',
}


class ConfigEditor(tk.Frame):
    """GUI for editing configuration and running badge generation."""

    def __init__(self, master: tk.Tk, config: Any) -> None:
        """
        Initialize ConfigEditor.

        Args:
            master: Root Tkinter window.
            config: ConfigParser object with settings.
        """
        super().__init__(master)
        self.master = master
        self.config = config
        self.dict_val: Dict[str, Any] = {}
        self.stop_threads = False
        self.processes: list = []
        
        # UI setup - Create fonts for different elements
        self.section_title_font = (UI_CONFIG['font_name'], UI_CONFIG['section_title_font_size'])
        self.button_font = (UI_CONFIG['font_name'], UI_CONFIG['button_font_size'])
        self.textbox_font = (UI_CONFIG['font_name'], UI_CONFIG['textbox_font_size'])
        # Keep self.font for backward compatibility
        self.font = self.section_title_font
        self.pb = None  # Will be created in _create_widgets
        
        self._init_window()
        self._create_widgets()

    def _init_window(self) -> None:
        """Initialize window properties."""
        self.master.title(WINDOW_TITLE)
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.pack(fill=tk.BOTH, expand=True)

    def _create_widgets(self) -> None:
        """Create GUI widgets from configuration."""
        # Create main container with left and right sections
        main_container = tk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=UI_CONFIG['padding'], pady=UI_CONFIG['padding'])
        
        # Left section for config
        left_frame = tk.Frame(main_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=UI_CONFIG['frame_padx'])
        
        # Create sections from config
        for section in self.config.sections():
            frame = tk.LabelFrame(
                left_frame,
                text=section.upper(),
                width=30,
                font=self.font
            )
            expand_setting = "yes" if UI_CONFIG['section_expand'] else "no"
            frame.pack(fill="both", expand=expand_setting, padx=UI_CONFIG['section_padx'], pady=UI_CONFIG['section_pady'], 
                      ipadx=UI_CONFIG['section_ipadx'], ipady=UI_CONFIG['section_ipady'])
            self._create_section_fields(section, frame)

        # Right section for output and execution controls
        right_frame = tk.Frame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=UI_CONFIG['frame_padx'])

        # Terminal section (fixed height based on textbox_height)
        terminal_frame = tk.LabelFrame(right_frame, text="TERMINAL", font=self.font)
        terminal_frame.pack(fill="x", expand=False, padx=UI_CONFIG['frame_padx'], pady=UI_CONFIG['frame_pady'])

        # Text output with scrollbar
        self.textbox = tk.Text(
            terminal_frame,
            fg=UI_CONFIG['textbox_fg'],
            bg=UI_CONFIG['textbox_bg'],
            height=UI_CONFIG['textbox_height'],
            width=UI_CONFIG['textbox_width'],
            wrap="word",
            font=self.textbox_font
        )
        
        vsb = tk.Scrollbar(terminal_frame, orient="vertical", command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.textbox.pack(fill="x", expand=False, side="left", 
                         padx=UI_CONFIG['textbox_padx'], pady=UI_CONFIG['textbox_pady'], 
                         ipadx=UI_CONFIG['textbox_ipadx'], ipady=UI_CONFIG['textbox_ipady'])

        # Execute section (buttons)
        execute_frame = tk.LabelFrame(right_frame, text="ACTION", font=self.font)
        execute_frame.pack(fill="x", padx=UI_CONFIG['frame_padx'], pady=UI_CONFIG['frame_pady'])

        # Button container
        btn_frame = tk.Frame(execute_frame)
        btn_frame.pack(fill="both", expand=True, padx=UI_CONFIG['frame_padx'], pady=UI_CONFIG['frame_pady'])

        tk.Button(
            btn_frame,
            text="Pull Image",
            command=self._crawl_images,
            fg=UI_CONFIG['execute_fg'],
            bg=UI_CONFIG['execute_bg'],
            height=UI_CONFIG['button_height'],
            width=UI_CONFIG['button_width'],
            font=self.button_font
        ).pack(fill="both", expand="yes", padx=UI_CONFIG['button_padx'], pady=UI_CONFIG['button_pady'], 
               ipadx=UI_CONFIG['button_ipadx'], ipady=UI_CONFIG['button_ipady'], side="left")

        tk.Button(
            btn_frame,
            text="Save Config",
            command=self._save_config,
            fg=UI_CONFIG['save_fg'],
            bg=UI_CONFIG['save_bg'],
            height=UI_CONFIG['button_height'],
            width=UI_CONFIG['button_width'],
            font=self.button_font
        ).pack(fill="both", expand="yes", padx=UI_CONFIG['button_padx'], pady=UI_CONFIG['button_pady'], 
               ipadx=UI_CONFIG['button_ipadx'], ipady=UI_CONFIG['button_ipady'], side="left")

        tk.Button(
            btn_frame,
            text="Cleanup",
            command=self._cleanup,
            fg=UI_CONFIG['execute_fg'],
            bg=UI_CONFIG['execute_bg'],
            height=UI_CONFIG['button_height'],
            width=UI_CONFIG['button_width'],
            font=self.button_font
        ).pack(fill="both", expand="yes", padx=UI_CONFIG['button_padx'], pady=UI_CONFIG['button_pady'], 
               ipadx=UI_CONFIG['button_ipadx'], ipady=UI_CONFIG['button_ipady'], side="left")

        tk.Button(
            btn_frame,
            text="Generate",
            command=self._execute,
            fg=UI_CONFIG['generate_fg'],
            bg=UI_CONFIG['generate_bg'],
            height=UI_CONFIG['button_height'],
            width=UI_CONFIG['button_width'],
            font=self.button_font
        ).pack(fill="both", expand="yes", padx=UI_CONFIG['button_padx'], pady=UI_CONFIG['button_pady'], 
               ipadx=UI_CONFIG['button_ipadx'], ipady=UI_CONFIG['button_ipady'], side="left")

        # Progress bar in execute section
        self.pb = ttk.Progressbar(
            execute_frame,
            orient='horizontal',
            mode='indeterminate',
            length=UI_CONFIG['progressbar_length']
        )
        self.pb.pack(fill="x", expand=False, padx=UI_CONFIG['progressbar_padx'], pady=UI_CONFIG['progressbar_pady'], 
                    ipadx=UI_CONFIG['progressbar_ipadx'], ipady=UI_CONFIG['progressbar_ipady'])

        # Preview section
        preview_frame = tk.LabelFrame(right_frame, text="PREVIEW", font=self.font)
        preview_frame.pack(fill="both", expand=True, padx=UI_CONFIG['frame_padx'], pady=UI_CONFIG['frame_pady'])

        # Create 3 preview image containers (label + image)
        preview_container = tk.Frame(preview_frame)
        preview_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Labels for each preview
        preview_labels = ["Template", "Source", "Output"]
        self.preview_images = {}
        
        for idx, label_text in enumerate(preview_labels):
            # Label
            lbl = tk.Label(preview_container, text=label_text, font=("Arial", 8, "bold"), fg="#666666")
            lbl.grid(row=0, column=idx, padx=2, pady=2)
            
            # Image placeholder - no fixed size to allow dynamic scaling
            img_label = tk.Label(
                preview_container,
                text="No Image",
                bg="#e0e0e0",
                fg="#999999",
                font=("Arial", 9)
            )
            img_label.grid(row=1, column=idx, padx=2, pady=2, sticky="nsew")
            self.preview_images[label_text.lower()] = img_label
        
        # Configure grid weights for equal column and row sizes
        for i in range(3):
            preview_container.grid_columnconfigure(i, weight=1)
        preview_container.grid_rowconfigure(1, weight=1)  # Make image row expandable
        
        # Load initial preview images
        self._load_preview_images()

    def _refresh_preview(self) -> None:
        """Schedule preview refresh on main GUI thread (thread-safe)."""
        try:
            # Log the refresh attempt
            self._append_output("[Preview] Scheduling refresh...\n")
            # Schedule on main thread with slight delay for file system catch-up
            self.master.after(500, self._load_preview_images)
        except Exception as e:
            self._append_output(f"[Preview] Refresh error: {e}\n")

    def _load_preview_images(self) -> None:
        """Load and display preview images from configured paths."""
        # DEBUGGING: Write current state to file
        try:
            diag_file = Path(__file__).parent.parent.parent / "PIL_ERROR_LOG.txt"
            with open(diag_file, "a", encoding="utf-8") as f:
                f.write(f"\n\n[PREVIEW_LOAD_CALLED] HAS_PIL={HAS_PIL}, time={__import__('datetime').datetime.now()}\n")
        except:
            pass
        
        if not HAS_PIL:
            msg = "[Preview] PIL not available - preview images cannot be displayed"
            self._append_output(f"{msg}\n")
            print(msg)
            return  # PIL not available, skip preview loading
        
        try:
            self._append_output("[Preview] Loading images...\n")
            config = self.config
            self._append_output(f"[Preview] Config object type: {type(config)}\n")
            
            # Log current config values
            try:
                src_path_cfg = config.get("general", "src_path")
                des_path_cfg = config.get("general", "des_path")
                template_cfg = config.get("template", "filename")
                self._append_output(f"[Preview] Config values: src={src_path_cfg}, des={des_path_cfg}, template={template_cfg}\n")
            except:
                pass
            
            # Clear all preview images first to remove old cached images
            self._clear_preview_images()
            
            # Helper function to find an existing path (try multiple locations)
            def find_path(config_path_str):
                """Try to find path in multiple locations."""
                # Try 1: Absolute path (if config has absolute path)
                p = Path(config_path_str)
                if p.is_absolute() and p.exists():
                    return p
                
                # Try 2: Relative to PROJECT_ROOT
                p = PROJECT_ROOT / config_path_str
                if p.exists():
                    return p
                
                # Try 3: Relative to parent directory of PROJECT_ROOT (workspace root)
                p = PROJECT_ROOT.parent / config_path_str
                if p.exists():
                    return p
                
                # Try 4: Check parent directory - sometimes subdirs don't have images but parent does
                parent_path = PROJECT_ROOT / Path(config_path_str).parent
                if parent_path.exists():
                    return parent_path
                
                return None
            
            # Load template image
            template_path_str = config.get("template", "filename")
            self._append_output(f"[Preview] Template config: {template_path_str}\n")
            template_path = find_path(template_path_str)
            if template_path:
                self._append_output(f"[Preview] Template found: {template_path}\n")
                self._display_image("template", str(template_path))
            else:
                self._append_output(f"[Preview] Template not found: {template_path_str}\n")
            
            # Load first image from source directory
            src_path_str = config.get("general", "src_path")
            self._append_output(f"[Preview] Source config: {src_path_str}\n")
            src_path = find_path(src_path_str)
            if src_path:
                # Search recursively for images (including subdirectories like src_img/)
                image_files = sorted([f for f in src_path.rglob("*") if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
                self._append_output(f"[Preview] Source path: {src_path}, files found: {len(image_files)}\n")
                
                # If no images in source, check temp folder as fallback
                if not image_files:
                    temp_path = PROJECT_ROOT / "images/temp"
                    if temp_path.exists():
                        image_files = sorted([f for f in temp_path.rglob("*") if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
                        self._append_output(f"[Preview] Source empty, checking temp: {len(image_files)} files\n")
                        if image_files:
                            self._append_output(f"[Preview] Using temp folder for source preview\n")
                            src_path = temp_path
                
                if image_files:
                    try:
                        self._append_output(f"[Preview] Displaying source: {image_files[0].name}\n")
                    except UnicodeEncodeError:
                        self._append_output(f"[Preview] Displaying source image\n")
                    self._display_image("source", str(image_files[0]))
                else:
                    self._append_output(f"[Preview] No images found in source or temp\n")
            else:
                self._append_output(f"[Preview] Source path not found: {src_path_str}\n")
            
            # Load first image from output directory
            output_path_str = config.get("general", "des_path")
            self._append_output(f"[Preview] Output config: {output_path_str}\n")
            output_path = find_path(output_path_str)
            if output_path:
                # Search recursively for images (including subdirectories)
                image_files = sorted([f for f in output_path.rglob("*") if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
                self._append_output(f"[Preview] Output path: {output_path}, files found: {len(image_files)}\n")
                if image_files:
                    try:
                        self._append_output(f"[Preview] Displaying output: {image_files[0].name}\n")
                    except UnicodeEncodeError:
                        self._append_output(f"[Preview] Displaying output image\n")
                    self._display_image("output", str(image_files[0]))
                else:
                    # Fallback: if no output images, use source image as placeholder
                    if src_path:
                        src_files = sorted([f for f in src_path.rglob("*") if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']])
                        if src_files:
                            self._display_image("output", str(src_files[0]))
                            self._append_output(f"[Preview] Output empty, showing source as placeholder\n")
                        else:
                            self._append_output(f"[Preview] No images in output: {output_path}\n")
                    else:
                        self._append_output(f"[Preview] No images in output: {output_path}\n")
            else:
                self._append_output(f"[Preview] Output path not found: {output_path_str}\n")
            self._append_output("[Preview] Images loaded successfully\n")
        except Exception as e:
            # Log the error
            import traceback
            self._append_output(f"[Preview] Error loading images: {e}\n")
            self._append_output(f"[Preview] Traceback: {traceback.format_exc()}\n")

    def _clear_preview_images(self) -> None:
        """Clear all preview images and reset to placeholders."""
        try:
            for preview_type in ['template', 'source', 'output']:
                if preview_type in self.preview_images:
                    label = self.preview_images[preview_type]
                    # Clear the image reference to allow garbage collection
                    label.image = None
                    # Reset label to show placeholder
                    label.config(image='', text='No Image')
        except Exception:
            pass  # Silently fail if there's any issue

    def _display_image(self, preview_type: str, image_path: str, max_width: int = 200, max_height: int = 300) -> None:
        """Display image in preview label.
        
        Args:
            preview_type: 'template', 'source', or 'output'
            image_path: Path to image file
            max_width: Maximum width for display
            max_height: Maximum height for display
        """
        try:
            if preview_type not in self.preview_images:
                self._append_output(f"[Preview] WARNING: preview_type '{preview_type}' not in {list(self.preview_images.keys())}\n")
                return
            
            self._append_output(f"[Preview] Opening image: {image_path}\n")
            # Load and resize image
            img = Image.open(image_path)
            self._append_output(f"[Preview] Image loaded: {img.size}, mode: {img.mode}\n")
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            self._append_output(f"[Preview] PhotoImage created: {photo.width()}x{photo.height()}\n")
            
            # Update label
            label = self.preview_images[preview_type]
            label.config(image=photo, text="")
            label.image = photo  # Keep reference to prevent garbage collection
            self._append_output(f"[Preview] Label updated: {preview_type}\n")
        except Exception as e:
            # Log the error
            import traceback
            try:
                error_msg = f"[Preview] Error displaying image: {e}\n"
                self._append_output(error_msg)
                tb_msg = f"[Preview] Traceback: {traceback.format_exc()}\n"
                self._append_output(tb_msg)
            except UnicodeEncodeError:
                # If Unicode encoding fails (Vietnamese filenames), just log generic message
                self._append_output(f"[Preview] Error displaying image (Unicode filename issue)\n")

    def _get_friendly_label(self, key: str, section: str = '') -> str:
        """
        Get user-friendly label for a config key.
        
        Args:
            key: Config key name.
            section: Optional section name for context.
        
        Returns:
            Friendly label or original key if not in mapping.
        """
        # First try exact key match
        if key in LABEL_MAPPING:
            return LABEL_MAPPING[key]
        
        # If not found, convert to title case with spaces
        # e.g., "show_success" -> "Show Success"
        friendly = ' '.join(word.capitalize() for word in key.split('_'))
        return friendly

    def _create_section_fields(self, section: str, master: tk.Widget) -> None:
        """
        Create input fields for a configuration section.

        Args:
            section: Config section name.
            master: Parent widget.
        """
        items = dict(self.config.items(section))
        num_items = len(items)
        cols_per_section = (num_items + GRID_COLS - 1) // GRID_COLS
        
        # Get label configuration from UI_CONFIG
        label_text_align = UI_CONFIG['label_text_align']
        label_width = UI_CONFIG['label_width']
        label_color = UI_CONFIG['label_color']
        label_bg = UI_CONFIG['label_bg']
        label_font_family = UI_CONFIG['label_font_family']
        label_font_size = UI_CONFIG['label_font_size']
        label_font_bold = UI_CONFIG['label_font_bold']
        label_font_italic = UI_CONFIG['label_font_italic']
        label_font_underline = UI_CONFIG['label_font_underline']
        
        # Build font tuple with styles
        font_style = ''
        if label_font_bold:
            font_style += 'bold '
        if label_font_italic:
            font_style += 'italic '
        if label_font_underline:
            font_style += 'underline'
        font_style = font_style.strip()
        
        label_font = (label_font_family, label_font_size, font_style) if font_style else (label_font_family, label_font_size)
        
        # Map text alignment to anchor value (for proper text positioning within label)
        anchor_map = {
            'left': 'w',      # West (left)
            'right': 'e',     # East (right)
            'center': 'center'
        }
        label_anchor = anchor_map.get(label_text_align.lower(), 'w')
        
        row = 1
        col = 1
        
        for key, value in items.items():
            # Label with config settings - use friendly label
            friendly_label = self._get_friendly_label(key, section)
            label_kwargs = {
                'text': friendly_label,
                'padx': UI_CONFIG['label_padx'],
                'font': label_font,
                'width': label_width,
                'fg': label_color,
                'anchor': label_anchor,
                'justify': tk.LEFT  # Keep for multi-line text
            }
            # Only set bg if it's not empty (empty = transparent)
            if label_bg and label_bg.strip():
                label_kwargs['bg'] = label_bg
            
            label = tk.Label(master, **label_kwargs)
            label.grid(row=row, column=col, ipadx=UI_CONFIG['label_ipadx'], sticky=tk.EW)

            # Input field based on value type
            self._create_field_widget(master, section, key, value, row, col + 1)

            row += 1
            if row > cols_per_section:
                col += 2
                row = 1

    def _create_field_widget(
        self,
        master: tk.Widget,
        section: str,
        key: str,
        value: str,
        row: int,
        col: int
    ) -> None:
        """
        Create appropriate input widget based on value type.

        Args:
            master: Parent widget.
            section: Config section.
            key: Config key.
            value: Config value.
            row: Grid row.
            col: Grid column.
        """
        field_key = f"{section}_{key}"
        widget = None

        # Boolean field
        if re.match(r'^([Tt][Rr][Uu][Ee]|[Ff][Aa][Ll][Ss][Ee])$', value):
            var = tk.BooleanVar(value=value.lower() == 'true')
            widget = tk.Checkbutton(
                master,
                # text=key,
                height=2,
                variable=var
            )
            widget.grid(row=row, column=col, 
                       padx=UI_CONFIG['input_grid_padx'], pady=UI_CONFIG['input_grid_pady'],
                       ipadx=UI_CONFIG['input_grid_ipadx'], sticky=UI_CONFIG['input_sticky'])
            # Store the variable, not the value - so we can get current value when saving
            self.dict_val[field_key] = [widget, var]
            
            # Add callback to auto-save when checkbox is toggled (for ui settings section)
            if section == 'ui settings':
                var.trace_add('write', lambda *args, fk=field_key: self._on_config_change(fk))

        # Color field
        elif re.match(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
            widget = tk.Button(
                master,
                text=value,
                width=UI_CONFIG['input_width_button'],
                command=lambda k=field_key: self._select_color(k)
            )
            widget.grid(row=row, column=col, 
                       padx=UI_CONFIG['input_grid_padx'], pady=UI_CONFIG['input_grid_pady'],
                       ipadx=UI_CONFIG['input_grid_ipadx'], sticky=UI_CONFIG['input_sticky'])
            self.dict_val[field_key] = [widget, value]

        # Folder field
        elif re.match(r'^(.+)\/([^\/]+)\/$', value):
            widget = tk.Button(
                master,
                text=value,
                width=UI_CONFIG['input_width_button'],
                command=lambda k=field_key: self._select_folder(k)
            )
            widget.grid(row=row, column=col, 
                       padx=UI_CONFIG['input_grid_padx'], pady=UI_CONFIG['input_grid_pady'],
                       ipadx=UI_CONFIG['input_grid_ipadx'], sticky=UI_CONFIG['input_sticky'])
            self.dict_val[field_key] = [widget, value]

        # File field
        elif re.match(r'^(.+)\/([^\/]+)$', value):
            widget = tk.Button(
                master,
                text=value, 
                width=UI_CONFIG['input_width_file'],
                command=lambda k=field_key: self._select_file(k)
            )
            widget.grid(row=row, column=col, 
                       padx=UI_CONFIG['input_grid_padx'], pady=UI_CONFIG['input_grid_pady'],
                       ipadx=UI_CONFIG['input_grid_ipadx'], sticky=UI_CONFIG['input_sticky'])
            self.dict_val[field_key] = [widget, value]

        # Text field (default)
        else:
            widget = tk.Entry(master, justify=tk.LEFT, font=self.font, width=UI_CONFIG['input_width'])
            widget.delete(0, tk.END)
            widget.insert(0, str(value))
            widget.grid(row=row, column=col, 
                       padx=UI_CONFIG['input_grid_padx'], pady=UI_CONFIG['input_grid_pady'],
                       ipadx=UI_CONFIG['input_grid_ipadx'], sticky=UI_CONFIG['input_sticky'])
            widget.bind("<KeyRelease>", lambda e, k=field_key: self._on_text_changed(e, k))
            self.dict_val[field_key] = [widget, value]

    def _on_text_changed(self, event: tk.Event, key: str) -> None:
        """Handle text field changes."""
        text = event.widget.get()
        self.dict_val[key][1] = text

    def _select_folder(self, key: str) -> None:
        """Open folder selection dialog."""
        path = fd.askdirectory(title="Select a Folder")
        if path:
            self.dict_val[key][0].config(text=path)
            self.dict_val[key][1] = path
            
            # Save the new config value to file so _load_preview_images can read it
            self._save_config(show_message=False)

    def _select_file(self, key: str) -> None:
        """Open file selection dialog."""
        path = fd.askopenfilename(
            title="Select a File",
            filetypes=[
                ('all files', '.*'),
                ('text files', '.txt'),
                ('image files', ('.png', '.jpg'))
            ]
        )
        if path:
            self.dict_val[key][0].config(text=path)
            self.dict_val[key][1] = path
            
            # Save the new config value to file so _load_preview_images can read it
            self._save_config(show_message=False)

    def _on_config_change(self, field_key: str) -> None:
        """Handle config changes from widgets (e.g., checkbox toggle).
        
        Args:
            field_key: The field key that changed (e.g., 'ui settings_show_success').
        """
        if field_key not in self.dict_val:
            return
        
        # Extract section and config key
        if field_key.startswith('ui settings'):
            section = 'ui settings'
            config_key = field_key.replace('ui settings_', '', 1)
        else:
            parts = field_key.split('_', 1)
            section = parts[0]
            config_key = parts[1] if len(parts) > 1 else ''
        
        # Get current value from widget
        value_obj = self.dict_val[field_key][1]
        if isinstance(value_obj, tk.BooleanVar):
            actual_value = str(value_obj.get())
        elif isinstance(value_obj, tk.StringVar):
            actual_value = value_obj.get()
        else:
            actual_value = str(value_obj)
        
        # Update in-memory config
        self.config.set(section, config_key, actual_value)
        
        # Save to file immediately
        config_path = Path(CONFIG_FILE)
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as err:
            self._append_output(f"Warning: Could not save config: {err}\n")

    def _select_color(self, key: str) -> None:
        """Open color selection dialog."""
        color_tuple = tkcolor.askcolor()
        if color_tuple[1]:
            hex_color = color_tuple[1]
            self.dict_val[key][0].config(text=hex_color)
            self.dict_val[key][1] = hex_color
            
            # Save the new config value to file
            self._save_config(show_message=False)

    def _save_config(self, show_message: bool = True) -> None:
        """Save configuration to file.
        
        Args:
            show_message: If True, show messagebox. If False, log to terminal output.
        """
        for key, value in self.dict_val.items():
            # Get the actual value - if it's a BooleanVar, call .get()
            value_obj = self.dict_val[key][1]
            if isinstance(value_obj, tk.BooleanVar):
                actual_value = str(value_obj.get())
            elif isinstance(value_obj, tk.StringVar):
                actual_value = value_obj.get()
            else:
                actual_value = str(value_obj)
            
            # Handle section names with spaces - split only on first underscore
            # "ui settings_show_success" -> "ui settings", "show_success"
            if key.startswith('ui settings'):
                section = 'ui settings'
                config_key = key.replace('ui settings_', '', 1)
            else:
                parts = key.split('_', 1)
                section = parts[0]
                config_key = parts[1] if len(parts) > 1 else ''
            
            self.config.set(section, config_key, actual_value)

        config_path = Path(CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)
        
        # Reload config from file to ensure in-memory config is up-to-date
        import time
        time.sleep(0.1)  # Small delay to ensure file is flushed
        self.config.read(CONFIG_FILE)

        if show_message and self._get_show_success():
            messagebox.showinfo(
                title="Success",
                message="Configuration saved successfully!",
                parent=self.master
            )
            # Refresh preview images after config save (thread-safe)
            self._refresh_preview()
        elif show_message:
            # Log to terminal if messagebox disabled
            self._append_output("Configuration saved successfully!\n")
            # Refresh preview images after config save (thread-safe)
            self._refresh_preview()
        else:
            # Log to terminal instead of showing messagebox
            self._append_output("Configuration saved successfully!\n")
            # Refresh preview images after config save (thread-safe)
            self._refresh_preview()
            # Refresh preview images after config save (thread-safe)
            self._refresh_preview()

    def _execute(self) -> None:
        """Execute badge generation in background thread."""
        t1 = threading.Thread(target=lambda: self.pb.start(UI_CONFIG['progressbar_pulse_interval']), daemon=True)
        t1.name = 'Progress Bar'
        t1.start()

        t2 = threading.Thread(target=self._run_generation, daemon=True)
        t2.name = "Image processing"
        t2.start()

        self.processes.extend([t1, t2])

    def _run_generation(self) -> None:
        """Run the badge generation process."""
        try:
            # Save config first (log to terminal, not messagebox)
            self._save_config(show_message=False)

            self._append_output("Processing...\n")

            # Get absolute path to execute.py (preferred over runner.bat)
            project_root = Path(__file__).parent.parent
            execute_py = project_root / 'execute.py'

            if not execute_py.exists():
                raise FileNotFoundError(f"execute.py not found at {execute_py}")

            # Use current Python interpreter (already in the correct environment)
            # This is more reliable than trying to find venv paths
            python_exe = sys.executable
            
            # Try to find venv Python as fallback for better isolation
            # Check both project level and workspace level
            venv_paths = [
                project_root / '.venv' / 'Scripts' / 'python.exe',         # Project level venv
                project_root.parent / '.venv' / 'Scripts' / 'python.exe',  # Workspace level venv
                project_root.parent / 'venv' / 'Scripts' / 'python.exe',   # Alt Windows venv
            ]
            
            for venv_path in venv_paths:
                try:
                    # Verify venv is valid by checking pyvenv.cfg exists
                    venv_root = venv_path.parent.parent
                    if (venv_root / 'pyvenv.cfg').exists():
                        python_exe = str(venv_path.resolve())
                        break
                except Exception:
                    continue

            # Run badge generation with Python
            # Windows: suppress console window with CREATE_NO_WINDOW flag
            kwargs = {'cwd': project_root}
            if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            process = subprocess.Popen(
                [python_exe, str(execute_py), 'exec'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False,
                **kwargs
            )
            output, _ = process.communicate()

            self._append_output(output.decode('utf-8', errors='replace'))

            if process.returncode == 0:
                if self._get_show_success():
                    messagebox.showinfo(
                        title="Completed",
                        message="Badge generation completed successfully!",
                        parent=self.master
                    )
                else:
                    self._append_output("Badge generation completed successfully!\n")
            else:
                if self._get_show_error():
                    messagebox.showerror(
                        title="Error",
                        message=f"Process failed with code {process.returncode}",
                        parent=self.master
                    )
                else:
                    self._append_output(f"ERROR: Process failed with code {process.returncode}\n")

        except Exception as err:
            self._append_output(f"Error: {err}\n")
            if self._get_show_error():
                messagebox.showerror(
                    title="Error",
                    message=f"Failed to execute: {err}",
                    parent=self.master
                )
        finally:
            self._append_output("Completed.\n")
            self.pb.stop()
            # Refresh preview images (thread-safe)
            self._refresh_preview()

    def _cleanup(self) -> None:
        """Execute cleanup in background thread."""
        t1 = threading.Thread(target=lambda: self.pb.start(UI_CONFIG['progressbar_pulse_interval']), daemon=True)
        t1.name = 'Progress Bar'
        t1.start()

        t2 = threading.Thread(target=self._run_cleanup, daemon=True)
        t2.name = "Cleanup"
        t2.start()

        self.processes.extend([t1, t2])

    def _run_cleanup(self) -> None:
        """Run the cleanup process."""
        try:
            self._append_output("Starting cleanup...\n")

            # Get absolute path to execute.py
            project_root = Path(__file__).parent.parent
            execute_py = project_root / 'execute.py'

            if not execute_py.exists():
                raise FileNotFoundError(f"execute.py not found at {execute_py}")

            # Use current Python interpreter (already in the correct environment)
            # This is more reliable than trying to find venv paths
            python_exe = sys.executable
            
            # Try to find venv Python as fallback for better isolation
            # Check both project level and workspace level
            venv_paths = [
                project_root / '.venv' / 'Scripts' / 'python.exe',         # Project level venv
                project_root.parent / '.venv' / 'Scripts' / 'python.exe',  # Workspace level venv
                project_root.parent / 'venv' / 'Scripts' / 'python.exe',   # Alt Windows venv
            ]
            
            for venv_path in venv_paths:
                try:
                    # Verify venv is valid by checking pyvenv.cfg exists
                    venv_root = venv_path.parent.parent
                    if (venv_root / 'pyvenv.cfg').exists():
                        python_exe = str(venv_path.resolve())
                        break
                except Exception:
                    continue

            # Run cleanup subcommand with Python
            # Windows: suppress console window with CREATE_NO_WINDOW flag
            kwargs = {'cwd': project_root}
            if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            process = subprocess.Popen(
                [python_exe, str(execute_py), 'cleanup'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False,
                **kwargs
            )
            output, _ = process.communicate()

            self._append_output(output.decode('utf-8', errors='replace'))

            if process.returncode == 0:
                if self._get_show_success():
                    messagebox.showinfo(
                        title="Cleanup Completed",
                        message="Cleanup completed successfully!",
                        parent=self.master
                    )
                else:
                    self._append_output("Cleanup completed successfully!\n")
            else:
                if self._get_show_error():
                    messagebox.showerror(
                        title="Error",
                        message=f"Cleanup failed with code {process.returncode}",
                        parent=self.master
                    )
                else:
                    self._append_output(f"ERROR: Cleanup failed with code {process.returncode}\n")

        except Exception as err:
            self._append_output(f"Error: {err}\n")
            if self._get_show_error():
                messagebox.showerror(
                    title="Error",
                    message=f"Failed to cleanup: {err}",
                    parent=self.master
                )
        finally:
            self._append_output("Cleanup finished.\n")
            self.pb.stop()
            # Refresh preview images (thread-safe)
            self._refresh_preview()
            self.pb.stop()
            # Refresh preview images (thread-safe)
            self._refresh_preview()

    def _crawl_images(self) -> None:
        """Execute image crawling in background thread."""
        t1 = threading.Thread(target=lambda: self.pb.start(UI_CONFIG['progressbar_pulse_interval']), daemon=True)
        t1.name = 'Progress Bar'
        t1.start()

        t2 = threading.Thread(target=self._run_crawl, daemon=True)
        t2.name = "Image Crawling"
        t2.start()

        self.processes.extend([t1, t2])

    def _run_crawl(self) -> None:
        """Run the image crawling process."""
        try:
            self._append_output("Starting image crawl...\n")

            # Get absolute path to project root
            project_root = Path(__file__).parent.parent

            # Get data file path from config
            data_file = project_root / 'data' / 'employee_list.xlsx'
            
            if not data_file.exists():
                raise FileNotFoundError(f"employee data file not found at {data_file}")

            # Use the project-level venv (has packages)
            python_exe = None
            
            # Use current Python interpreter (already in the correct environment)
            # This is more reliable than trying to find venv paths
            python_exe = sys.executable
            
            # Try to find venv Python as fallback for better isolation
            # Check both project level and workspace level
            venv_paths = [
                project_root / '.venv' / 'Scripts' / 'python.exe',         # Project level venv
                project_root.parent / '.venv' / 'Scripts' / 'python.exe',  # Workspace level venv
                project_root.parent / 'venv' / 'Scripts' / 'python.exe',   # Alt Windows venv
            ]
            
            for venv_path in venv_paths:
                try:
                    # Verify venv is valid by checking pyvenv.cfg exists
                    venv_root = venv_path.parent.parent
                    if (venv_root / 'pyvenv.cfg').exists():
                        python_exe = str(venv_path.resolve())
                        break
                except Exception:
                    continue
            
            # Run image crawler as a module (allows relative imports to work)
            # Use the Python interpreter to ensure all packages are available
            # Windows: suppress console window with CREATE_NO_WINDOW flag
            kwargs = {'cwd': project_root}
            if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            
            process = subprocess.Popen(
                [python_exe, '-m', 'tools.image_crawler', '--file-path', str(data_file), '--workers', '10'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=False,
                **kwargs
            )
            output, _ = process.communicate()

            self._append_output(output.decode('utf-8', errors='replace'))

            if process.returncode == 0:
                if self._get_show_success():
                    messagebox.showinfo(
                        title="Crawl Completed",
                        message="Image crawling completed successfully!",
                        parent=self.master
                    )
                else:
                    self._append_output("Image crawling completed successfully!\n")
            else:
                if self._get_show_error():
                    messagebox.showerror(
                        title="Error",
                        message=f"Image crawl failed with code {process.returncode}",
                        parent=self.master
                    )
                else:
                    self._append_output(f"ERROR: Image crawl failed with code {process.returncode}\n")

        except Exception as err:
            self._append_output(f"Error: {err}\n")
            if self._get_show_error():
                messagebox.showerror(
                    title="Error",
                    message=f"Failed to crawl images: {err}",
                    parent=self.master
                )
        finally:
            self._append_output("Image crawl finished.\n")
            self.pb.stop()
            # Refresh preview images (thread-safe)
            self._refresh_preview()

    def _append_output(self, text: str) -> None:
        """
        Append text to output display.

        Args:
            text: Text to append.
        """
        # Guard check - textbox may not exist during initialization
        if not hasattr(self, 'textbox'):
            return
        self.textbox.insert(tk.END, text)
        self.textbox.see("end")
        self.master.update()

    def _get_show_success(self) -> bool:
        """Get show_success from config."""
        return self.config.getboolean('ui settings', 'show_success', fallback=True)

    def _get_show_error(self) -> bool:
        """Get show_error from config."""
        return self.config.getboolean('ui settings', 'show_error', fallback=True)


def get_config() -> Any:
    """
    Load configuration from file.

    Returns:
        ConfigParser object.
    """
    try:
        from configparser import ConfigParser
    except ImportError:
        from ConfigParser import ConfigParser  # Python 2

    config = ConfigParser()
    config.read(CONFIG_FILE)
    return config


def main() -> None:
    """Main entry point for GUI application."""
    root = tk.Tk()
    root.resizable(True, True)
    
    try:
        config = get_config()
        app = ConfigEditor(root, config)
        root.mainloop()
    except Exception as err:
        messagebox.showerror(
            title="Error",
            message=f"Failed to start application: {err}"
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
