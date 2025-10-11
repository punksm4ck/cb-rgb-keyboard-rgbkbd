"""
Main GUI package for the RGB Controller application.
This file makes 'gui' a Python package and can optionally expose
key classes or functions from its submodules for easier access.
"""
from .core.constants import APP_NAME, VERSION
from .core.exceptions import RGBControllerBaseException
__all__ = ['APP_NAME', 'VERSION', 'RGBControllerBaseException']