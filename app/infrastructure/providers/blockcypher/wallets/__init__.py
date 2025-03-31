"""
Wallet management module for BlockCypher integration.

This package contains wallet-related functionality such as:
- Wallet creation and management
- Address generation
- Balance queries
- Multi-signature wallets
"""

from app.infrastructure.providers.blockcypher.wallets.manager import WalletManager

__all__ = ['WalletManager'] 