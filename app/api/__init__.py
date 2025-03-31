"""
API Package for Payment Gateway

This package contains API routes and handlers for the payment gateway,
including webhook handlers for BlockCypher cryptocurrency transactions.

The API is versioned with current version v1 available in the v1 subpackage.
"""

from app.api.v1 import webhook_router

__all__ = ['webhook_router'] 