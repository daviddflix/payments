"""
Blockchain service for interacting with blockchain data through BlockCypher API.

This module provides access to blockchain-specific features like blocks and network information.
Use specialized manager classes for transactions, wallets, and other features.
"""

from typing import Dict, Any, Optional, List
import blockcypher
import os
import warnings

from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.common.types import CoinSymbol
from app.infrastructure.providers.blockcypher.wallets.manager import WalletManager

class BlockchainService(BlockCypherProvider):
    """
    High-level service for interacting with blockchain data through BlockCypher API.
    
    This class provides access to blockchain data like blocks and network information.
    
    Note:
        - For transaction operations, use TransactionManager instead.
        - For wallet operations, use WalletManager instead.
        - For forwarding and webhook operations, use ForwardingManager instead.
    """
    
    def __init__(self, coin_symbol: CoinSymbol = 'btc-testnet', api_token: Optional[str] = None):
        """
        Initialize the blockchain service.
        
        Args:
            coin_symbol: Cryptocurrency network symbol (default: btc-testnet)
            api_token: BlockCypher API token (default: None, reads from environment)
        """
        super().__init__(coin_symbol=coin_symbol, api_token=api_token)
        self._wallet_manager = None
    
    @property
    def wallet_manager(self):
        """
        Get or create a wallet manager instance.
        
        Returns:
            WalletManager instance
        """
        if self._wallet_manager is None:
            self._wallet_manager = WalletManager(
                coin_symbol=self.coin_symbol,
                api_token=self.api_token
            )
        return self._wallet_manager
    
    def get_latest_block_height(self) -> int:
        """
        Get the latest block height for this blockchain.
        
        Returns:
            Block height as an integer
        """
        try:
            return blockcypher.get_latest_block_height(coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get latest block height: {str(e)}")
    
    def get_block_details(self, block_height: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific block.
        
        Args:
            block_height: The height of the block to retrieve
            
        Returns:
            Dictionary with block details
        """
        try:
            details = blockcypher.get_block_details(block_height, coin_symbol=self.coin_symbol)
            return {
                "hash": details.get("hash"),
                "height": details.get("height"),
                "time": details.get("time"),
                "n_tx": details.get("n_tx"),
                "total": details.get("total"),
                "fees": details.get("fees"),
                "size": details.get("size"),
                "ver": details.get("ver"),
                "prev_block": details.get("prev_block"),
                "mrkl_root": details.get("mrkl_root"),
                "txids": details.get("txids", [])
            }
        except Exception as e:
            raise Exception(f"Failed to get block details: {str(e)}")
    
    def get_block_overview(self, block_height: int) -> Dict[str, Any]:
        """
        Get a summarized overview of a specific block.
        
        Args:
            block_height: The height of the block to retrieve
            
        Returns:
            Dictionary with block overview
        """
        try:
            return blockcypher.get_block_overview(block_height, coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get block overview: {str(e)}")
    
    def get_network_info(self) -> Dict[str, Any]:
        """
        Get information about the current network.
        
        Returns:
            Dictionary with network information
        """
        try:
            return blockcypher.get_blockchain_overview(coin_symbol=self.coin_symbol)
        except Exception as e:
            raise Exception(f"Failed to get network information: {str(e)}")

    def get_fee_estimates(self) -> Dict[str, int]:
        """
        Get fee estimates for different priority levels.
        
        Returns:
            Dictionary with fee estimates in satoshis per kilobyte
        """
        try:
            info = blockcypher.get_blockchain_overview(coin_symbol=self.coin_symbol)
            return {
                "high_fee_per_kb": info.get("high_fee_per_kb", 0),
                "medium_fee_per_kb": info.get("medium_fee_per_kb", 0),
                "low_fee_per_kb": info.get("low_fee_per_kb", 0)
            }
        except Exception as e:
            raise Exception(f"Failed to get fee estimates: {str(e)}")
    
    def get_address_balance(self, address: str) -> float:
        """
        Get the balance of an address.
        
        Deprecated:
            Use WalletManager.get_wallet_balance() instead.
            
        Args:
            address: The address to check
            
        Returns:
            Balance in the native coin unit
        """
        warnings.warn(
            "get_address_balance() is deprecated. Use WalletManager.get_wallet_balance() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.wallet_manager.get_wallet_balance(address)
    
    def get_address_details(self, address: str) -> Dict[str, Any]:
        """
        Get details about an address.
        
        Deprecated:
            Use WalletManager.get_wallet_details() instead.
            
        Args:
            address: The address to get details for
            
        Returns:
            Dictionary with address details
        """
        warnings.warn(
            "get_address_details() is deprecated. Use WalletManager.get_wallet_details() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.wallet_manager.get_wallet_details(address)


