#!/usr/bin/env python3
"""
Setup script for Babbitt Quote Generator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

# Read requirements
requirements = []
if (this_directory / "requirements.txt").exists():
    with open(this_directory / "requirements.txt") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="babbitt-quote-generator",
    version="1.0.0",
    author="Babbitt International",
    author_email="support@babbitt.com",
    description="Professional Quote Generator for Babbitt International products",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/babbitt/quote-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "babbitt-quote-generator=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.sql", "*.docx", "*.txt"],
    },
    zip_safe=False,
) 