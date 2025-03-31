"""
BlockCypher API integration for cryptocurrency operations.

This package provides a comprehensive integration with the BlockCypher API,
allowing for wallet management, transaction processing, and blockchain data access.

The module is structured into separate components:
- wallets: Wallet creation and management
- transactions: Transaction creation, signing, and broadcasting
- forwarding: Address forwarding and webhook management
- common: Shared utilities and base classes
- utils: Helper functions for various operations
- webhooks: Handlers for webhook callbacks
"""

# Import main components for easy access
from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.wallets import WalletManager
from app.infrastructure.providers.blockcypher.transactions import TransactionManager, TransactionValidator
from app.infrastructure.providers.blockcypher.forwarding import ForwardingManager
from app.infrastructure.providers.blockcypher.common.factory import BlockCypherFactory
from app.infrastructure.providers.blockcypher.blockchain import BlockchainService
from app.infrastructure.providers.blockcypher.webhooks import BlockcypherWebhookHandler, simulate_webhook

__all__ = [
    'BlockCypherProvider',
    'WalletManager',
    'TransactionManager',
    'TransactionValidator',
    'ForwardingManager',
    'BlockCypherFactory',
    'BlockchainService',
    'BlockcypherWebhookHandler',
    'simulate_webhook',
]
