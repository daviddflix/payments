"""
Factory for creating BlockCypher API providers.

This module provides a simple factory for creating provider instances.
"""

from typing import Optional, Dict, Any, Type
from app.infrastructure.providers.blockcypher.common.types import CoinSymbol
from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.wallets.manager import WalletManager
from app.infrastructure.providers.blockcypher.transactions.manager import TransactionManager
from app.infrastructure.providers.blockcypher.forwarding import ForwardingManager

class BlockCypherFactory:
    """
    Factory for creating BlockCypher service instances.
    
    This factory simplifies the creation of various BlockCypher 
    provider instances with consistent configuration.
    """
    
    def __init__(self, api_token: Optional[str] = None, coin_symbol: CoinSymbol = 'btc-testnet'):
        """
        Initialize the factory with default configuration.
        
        Args:
            api_token: The BlockCypher API token (defaults to BLOCKCYPHER_API_TOKEN env var)
            coin_symbol: The cryptocurrency to use (default: btc-testnet)
        """
        self.api_token = api_token
        self.coin_symbol = coin_symbol
    
    def create_wallet_manager(self) -> WalletManager:
        """
        Create a WalletManager instance with the factory's configuration.
        
        Returns:
            Configured WalletManager instance
        """
        return WalletManager(coin_symbol=self.coin_symbol, api_token=self.api_token)
    
    def create_transaction_manager(self) -> TransactionManager:
        """
        Create a TransactionManager instance with the factory's configuration.
        
        Returns:
            Configured TransactionManager instance
        """
        return TransactionManager(coin_symbol=self.coin_symbol, api_token=self.api_token)
    
    def create_forwarding_manager(self) -> ForwardingManager:
        """
        Create a ForwardingManager instance with the factory's configuration.
        
        Returns:
            Configured ForwardingManager instance
        """
        return ForwardingManager(coin_symbol=self.coin_symbol, api_token=self.api_token) 