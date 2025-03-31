"""
Blockchain utility functions for BlockCypher API.

This module provides helper functions for working with blockchain data.
"""

from typing import Dict, Any, Optional, Tuple
import requests
import os

def get_network_parameters(coin_symbol: str = 'btc') -> Dict[str, Any]:
    """
    Get blockchain network parameters from BlockCypher API.
    
    Args:
        coin_symbol: The cryptocurrency network (btc, btc-testnet, bcy, etc.)
        
    Returns:
        Dictionary with network parameters
        
    Note:
        This function is deprecated. Use BlockCypherProvider.get_network_parameters instead.
    """
    import warnings
    warnings.warn(
        "get_network_parameters is deprecated. Use BlockCypherProvider.get_network_parameters instead.",
        DeprecationWarning, 
        stacklevel=2
    )
    
    from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
    provider = BlockCypherProvider(coin_symbol=coin_symbol)
    return provider.get_network_parameters()

def estimate_transaction_fee(coin_symbol: str, tx_size_bytes: int, priority: str = 'medium') -> int:
    """
    Estimate the fee for a transaction based on its size and desired confirmation priority.
    
    Args:
        coin_symbol: The cryptocurrency network (btc, btc-testnet, etc.)
        tx_size_bytes: Size of the transaction in bytes
        priority: Transaction priority (low, medium, high)
        
    Returns:
        Estimated fee in satoshis
    """
    # Get current network parameters including fee estimates
    from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
    
    provider = BlockCypherProvider(coin_symbol=coin_symbol)
    network_params = provider.get_network_parameters()
    
    # Get fee rate based on priority
    if priority == 'high':
        fee_rate = network_params.get('high_fee_per_kb', 50000)  # Default: 50000 satoshis/KB
    elif priority == 'medium':
        fee_rate = network_params.get('medium_fee_per_kb', 25000)  # Default: 25000 satoshis/KB
    else:  # low
        fee_rate = network_params.get('low_fee_per_kb', 10000)  # Default: 10000 satoshis/KB
    
    # Convert fee rate from satoshis/KB to satoshis/byte and calculate total fee
    fee_rate_per_byte = fee_rate / 1000
    estimated_fee = int(tx_size_bytes * fee_rate_per_byte)
    
    # Ensure minimum fee
    min_fee = 1000  # 1000 satoshis as a reasonable minimum
    return max(estimated_fee, min_fee)

def is_valid_address(address: str, coin_symbol: str) -> bool:
    """
    Check if a cryptocurrency address is valid for the given network.
    
    Args:
        address: The address to validate
        coin_symbol: The cryptocurrency network
        
    Returns:
        True if the address is valid, False otherwise
    """
    from app.infrastructure.providers.blockcypher.transactions.validator import TransactionValidator
    
    validator = TransactionValidator(coin_symbol=coin_symbol)
    return validator.is_valid_address(address)

def get_confirmation_time_estimate(coin_symbol: str, confirmations: int = 6) -> int:
    """
    Estimate the time in minutes it will take for a transaction to reach the specified number of confirmations.
    
    Args:
        coin_symbol: The cryptocurrency network
        confirmations: Number of confirmations to estimate time for
        
    Returns:
        Estimated time in minutes
    """
    # Get current network parameters
    from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
    
    provider = BlockCypherProvider(coin_symbol=coin_symbol)
    network_params = provider.get_network_parameters()
    
    # Get average block time in seconds
    avg_block_time_sec = network_params.get('time_between_blocks', 600)  # Default to 10 minutes for Bitcoin
    
    # Calculate estimated confirmation time
    return int((avg_block_time_sec * confirmations) / 60) 