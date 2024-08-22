"""
Setup script for the glint4py package.

This script uses setuptools to package and distribute the glint4py framework,
an open-source Python framework for creating lightweight, fast, and efficient
server applications.
"""

from pathlib import Path
from setuptools import setup, find_packages

# Load the long description from the README.md file
long_description = Path("README.md").read_text(encoding="utf-8")

setup(
    name="glint4py",
    version="1.1.2.24-alpha",
    package_dir={'': 'src'},  # The main package is located in the 'src' directory
    packages=find_packages(where='src'),  # Finds packages within the 'src' directory
    install_requires=[],  # List your dependencies here if applicable
    tests_require=[
        'pytest',  # Example test requirement; update as needed
    ],
    author="acariustv-ufosproject",
    author_email="acariustv@web.de",
    description=(
        "Glint is an open-source Python framework used to create lightweight, "
        "fast, and efficient server applications."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acariustv/Glint",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  # Example development status; update as needed
    ],
    python_requires='>=3.6',
    project_urls={
        "Documentation": "https://github.com/acariustv/Glint/wiki",
        "Source": "https://github.com/acariustv/Glint",
        "Tracker": "https://github.com/acariustv/Glint/issues",
    },
    license="MIT",  # Specify the license
    include_package_data=True,  # Include additional files specified in MANIFEST.in, if any
)
