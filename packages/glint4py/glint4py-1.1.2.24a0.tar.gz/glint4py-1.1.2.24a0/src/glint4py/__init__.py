"""
glint4py - Package Initialization

This module initializes the glint4py package and sets the version.

The __init__.py file is used to mark a directory as a Python package.
It also allows for package-level variables, imports, or other initialization code.

Attributes:
    __version__ (str): The current version of the glint4py package.
"""

from .glint import Glint
from .error_handler import ErrorHandler
from .middleware import Middleware
from .request import Request
from .response import Response
from .router import Router
from .templates import TemplateRenderer

__version__ = 'v.1.1.0.24-alpha'
