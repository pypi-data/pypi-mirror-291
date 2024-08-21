from setuptools import setup

setup(
    name="glint4py",
    version="0.1",
    py_modules=["glint"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "glint=glint:App",  # Falls du eine CLI willst, die `glint` ausführt
        ],
    },
    author="acariustv-ufosproject",
    author_email="acariustv@web.de",
    description="Glint is a open-source python framework, used to create lightweight, fast and efficient server applications.",
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
