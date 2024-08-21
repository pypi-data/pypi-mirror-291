from setuptools import setup, find_packages

setup(
    name="glint4py",
    version="0.2",
    package_dir={'': 'src'},  # Gibt an, dass die Pakete im src-Verzeichnis liegen
    packages=find_packages(where='src'),  # Findet alle Pakete im src-Verzeichnis
    install_requires=[],
    entry_points={
        "console_scripts": [
            "glint=glint:main",  # Falls du eine CLI willst, die `glint` ausführt
        ],
    },
    author="acariustv-ufosproject",
    author_email="acariustv@web.de",
    description="Glint is an open-source Python framework used to create lightweight, fast, and efficient server applications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/acariustv/Glint",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
