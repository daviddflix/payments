"""
Blockchain utility functions for BlockCypher API.

This module provides helper functions for working with blockchain data.
"""

from typing import Dict, Any, Optional, Tuple
import requests
import os

def get_network_parameters(coin_symbol: str) -> Dict[str, Any]:
    """
    Get basic information about a blockchain network.
    
    Args:
        coin_symbol: The cryptocurrency network to query
            Options: btc, btc-testnet, ltc, doge, dash, bcy
            
    Returns:
        Dictionary with network parameters
    """
    # Map coin symbol to API path components
    symbol_map = {
        'btc': ('btc', 'main'),
        'btc-testnet': ('btc', 'test3'),
        'ltc': ('ltc', 'main'),
        'doge': ('doge', 'main'),
        'dash': ('dash', 'main'),
        'bcy': ('bcy', 'test')
    }
    
    if coin_symbol not in symbol_map:
        raise ValueError(f"Invalid coin symbol: {coin_symbol}")
    
    coin, chain = symbol_map[coin_symbol]
    url = f"https://api.blockcypher.com/v1/{coin}/{chain}"
    
    # Get API token from environment variable
    api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
    params = {'token': api_token} if api_token else {}
    
    # Make the request
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()

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
    network_params = get_network_parameters(coin_symbol)
    
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
    symbol_map = {
        'btc': ('btc', 'main'),
        'btc-testnet': ('btc', 'test3'),
        'ltc': ('ltc', 'main'),
        'doge': ('doge', 'main'),
        'dash': ('dash', 'main'),
        'bcy': ('bcy', 'test')
    }
    
    if coin_symbol not in symbol_map:
        raise ValueError(f"Invalid coin symbol: {coin_symbol}")
    
    coin, chain = symbol_map[coin_symbol]
    url = f"https://api.blockcypher.com/v1/{coin}/{chain}/addrs/{address}/balance"
    
    # Get API token from environment variable
    api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
    params = {'token': api_token} if api_token else {}
    
    try:
        response = requests.get(url, params=params)
        # If the response is successful, the address is valid
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

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
    network_params = get_network_parameters(coin_symbol)
    
    # Get average block time in seconds
    avg_block_time_sec = network_params.get('time_between_blocks', 600)  # Default to 10 minutes for Bitcoin
    
    # Calculate estimated confirmation time
    return int((avg_block_time_sec * confirmations) / 60) 