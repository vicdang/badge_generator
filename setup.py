#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup configuration for Badge Generator project.

This script configures the Badge Generator package for distribution and installation.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "docs" / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = [
    line.strip()
    for line in requirements_file.read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
] if requirements_file.exists() else []

setup(
    name="badge-generator",
    version="2.0.0",
    description="Automatic badge generation tool with image downloading and face detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Badge Generator Team",
    author_email="",
    url="https://github.com/vicdang/badge-generator",
    license="MIT",
    
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_dir={"": "."},
    
    include_package_data=True,
    
    python_requires=">=3.8",
    install_requires=requirements,
    
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.990",
        ],
        "gui": [
            "tkinter",  # Usually comes with Python
        ],
    },
    
    entry_points={
        "console_scripts": [
            "badge-generator=src.badgenerator:main",
            "badge-gui=src.badge_gui:main",
        ],
    },
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    
    keywords=[
        "badge",
        "generation",
        "image",
        "face-detection",
        "qr-code",
        "employee",
    ],
    
    project_urls={
        "Documentation": "https://github.com/vicdang/badge-generator/docs",
        "Source": "https://github.com/vicdang/badge-generator",
        "Tracker": "https://github.com/vicdang/badge-generator/issues",
    },
    
    zip_safe=False,
)
