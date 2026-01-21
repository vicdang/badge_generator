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
import threading
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser as tkcolor
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple

CONFIG_FILE = './config/config.ini'
WINDOW_TITLE = "Image Producer"
GRID_COLS = 3
WINDOW_HEIGHT = 1300
WINDOW_WIDTH = 1000


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
        
        # UI setup
        self.font = ('Lucida Grande', 12)
        self.pb = ttk.Progressbar(
            master,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        
        self._init_window()
        self._create_widgets()

    def _init_window(self) -> None:
        """Initialize window properties."""
        self.master.title(WINDOW_TITLE)
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.pack(fill=tk.BOTH, expand=True)

    def _create_widgets(self) -> None:
        """Create GUI widgets from configuration."""
        # Create sections from config
        for section in self.config.sections():
            frame = tk.LabelFrame(
                self,
                text=section.upper(),
                width=50,
                font=self.font
            )
            frame.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)
            self._create_section_fields(section, frame)

        # Create control panel
        control_frame = tk.LabelFrame(self, text="", width=50, font=self.font)
        control_frame.pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

        # Text output
        self.textbox = tk.Text(
            control_frame,
            fg="White",
            bg="Black",
            height=10,
            width=100,
            wrap="word"
        )
        
        vsb = tk.Scrollbar(control_frame, orient="vertical", command=self.textbox.yview)
        self.textbox.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.textbox.pack(fill="both", expand="yes", side="left", padx=10, pady=10, ipadx=5, ipady=5)

        # Progress bar
        self.pb.pack(fill="both", expand="yes", side="right", padx=10, pady=10, ipadx=5, ipady=5)

        # Buttons
        btn_frame = tk.Frame(control_frame)
        btn_frame.pack(side="right", padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="Execute",
            command=self._execute,
            fg="Black",
            bg="Green",
            height=2,
            width=10
        ).pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

        tk.Button(
            btn_frame,
            text="Save",
            command=self._save_config,
            fg="Black",
            bg="Light green",
            height=2,
            width=10
        ).pack(fill="both", expand="yes", padx=5, pady=5, ipadx=5, ipady=5)

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
        
        row = 1
        col = 1
        
        for key, value in items.items():
            # Label
            label = tk.Label(
                master,
                text=key,
                justify=tk.LEFT,
                padx=5,
                font=self.font,
                width=10
            )
            label.grid(row=row, column=col, ipadx=10, sticky=tk.EW)

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
                text=key,
                height=2,
                variable=var
            )
            widget.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
            self.dict_val[field_key] = [widget, var.get()]

        # Color field
        elif re.match(r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$', value):
            widget = tk.Button(
                master,
                text=value,
                width=20,
                command=lambda k=field_key: self._select_color(k)
            )
            widget.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
            self.dict_val[field_key] = [widget, value]

        # Folder field
        elif re.match(r'^(.+)\/([^\/]+)\/$', value):
            widget = tk.Button(
                master,
                text=value,
                width=20,
                command=lambda k=field_key: self._select_folder(k)
            )
            widget.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
            self.dict_val[field_key] = [widget, value]

        # File field
        elif re.match(r'^(.+)\/([^\/]+)$', value):
            widget = tk.Button(
                master,
                text=value,
                width=20,
                command=lambda k=field_key: self._select_file(k)
            )
            widget.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
            self.dict_val[field_key] = [widget, value]

        # Text field (default)
        else:
            widget = tk.Entry(master, justify=tk.LEFT, font=self.font, width=20)
            widget.delete(0, tk.END)
            widget.insert(0, str(value))
            widget.grid(row=row, column=col, ipadx=5, sticky=tk.EW)
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

    def _select_color(self, key: str) -> None:
        """Open color selection dialog."""
        color_tuple = tkcolor.askcolor()
        if color_tuple[1]:
            hex_color = color_tuple[1]
            self.dict_val[key][0].config(text=hex_color)
            self.dict_val[key][1] = hex_color

    def _save_config(self) -> None:
        """Save configuration to file."""
        for key, value in self.dict_val.items():
            section, config_key = key.split('_', 1)
            self.config.set(section, config_key, str(self.dict_val[key][1]))

        config_path = Path(CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            self.config.write(f)

        messagebox.showinfo(
            title="Success",
            message="Configuration saved successfully!",
            parent=self.master
        )

    def _execute(self) -> None:
        """Execute badge generation in background thread."""
        t1 = threading.Thread(target=self.pb.start, daemon=True)
        t1.name = 'Progress Bar'
        t1.start()

        t2 = threading.Thread(target=self._run_generation, daemon=True)
        t2.name = "Image processing"
        t2.start()

        self.processes.extend([t1, t2])

    def _run_generation(self) -> None:
        """Run the badge generation process."""
        try:
            # Save config first
            self._save_config()

            self._append_output("Processing...\n")

            # Run the generator script
            process = subprocess.Popen(
                'runner.bat',
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True
            )
            output, _ = process.communicate()

            self._append_output(output.decode('utf-8', errors='replace'))

            if process.returncode == 0:
                messagebox.showinfo(
                    title="Completed",
                    message="Badge generation completed successfully!",
                    parent=self.master
                )
            else:
                messagebox.showerror(
                    title="Error",
                    message=f"Process failed with code {process.returncode}",
                    parent=self.master
                )

        except Exception as err:
            self._append_output(f"Error: {err}\n")
            messagebox.showerror(
                title="Error",
                message=f"Failed to execute: {err}",
                parent=self.master
            )
        finally:
            self._append_output("Completed.\n")
            self.pb.stop()

    def _append_output(self, text: str) -> None:
        """
        Append text to output display.

        Args:
            text: Text to append.
        """
        self.textbox.insert(tk.END, text)
        self.textbox.see("end")
        self.master.update()


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
