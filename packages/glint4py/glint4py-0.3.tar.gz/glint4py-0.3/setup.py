from setuptools import setup, find_packages
from pathlib import Path

long_description = Path("README.md").read_text()

setup(
    name="glint4py",
    version="0.3",
    package_dir={'': 'src'},  # Das Hauptpaket befindet sich im 'src'-Verzeichnis
    packages=find_packages(where='src'),  # Findet Pakete im 'src'-Verzeichnis
    install_requires=[],  # Liste deiner Abhängigkeiten, falls vorhanden
    author="acariustv-ufosproject",
    author_email="acariustv@web.de",
    description="Glint is an open-source Python framework used to create lightweight, fast, and efficient server applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/acariustv/Glint",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
