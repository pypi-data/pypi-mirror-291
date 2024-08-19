"""
Gluehome: A Python client for interacting with the Glue Home API.

This package provides tools for authentication and API interactions.
"""

from .auth import GlueAuth
from .client import GlueClient

__all__ = ['GlueAuth', 'GlueClient']
__version__ = "0.1.2"
