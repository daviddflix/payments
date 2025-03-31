"""
API v1 Package

This package contains all routes and endpoints for version 1 of the API.
"""

from .webhook_routes import router as webhook_router

__all__ = ['webhook_router'] 