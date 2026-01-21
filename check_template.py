#!/usr/bin/env python3
"""Check template image and find PIL paste issue."""

from PIL import Image
import pathlib

template_path = pathlib.Path('./img/template/template.png')
tpl = Image.open(template_path)
print(f"Template mode: {tpl.mode}, size: {tpl.size}")
print(f"Has alpha: {tpl.mode in ['RGBA', 'LA', 'PA']}")

# Convert template to RGBA if needed
if tpl.mode != 'RGBA':
    print(f"Converting from {tpl.mode} to RGBA...")
    tpl = tpl.convert('RGBA')
    tpl.save(template_path)
    print("Template converted and saved!")
else:
    print("Template is already RGBA")
