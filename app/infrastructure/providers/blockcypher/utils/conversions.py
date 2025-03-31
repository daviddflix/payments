"""
Currency conversion utilities for BlockCypher API.

This module provides helper functions for converting between different units
of cryptocurrency (e.g., BTC to satoshis).
"""

from typing import Union, Dict, Optional, Any
from decimal import Decimal, getcontext

# Set decimal precision
getcontext().prec = 28

# Conversion constants
SATOSHI_PER_BTC = 100_000_000  # 1 BTC = 100,000,000 satoshis

def satoshi_to_btc(satoshi_amount: Union[int, str]) -> float:
    """
    Convert satoshis to BTC.
    
    Args:
        satoshi_amount: Amount in satoshis
        
    Returns:
        Equivalent amount in BTC
    """
    amount = int(satoshi_amount)
    return float(Decimal(amount) / Decimal(SATOSHI_PER_BTC))

def btc_to_satoshi(btc_amount: Union[float, str]) -> int:
    """
    Convert BTC to satoshis.
    
    Args:
        btc_amount: Amount in BTC
        
    Returns:
        Equivalent amount in satoshis
    """
    amount = Decimal(str(btc_amount))  # Convert to Decimal from either float or string
    return int(amount * Decimal(SATOSHI_PER_BTC))

def format_btc_amount(amount: float, include_symbol: bool = True) -> str:
    """
    Format a BTC amount as a string.
    
    Args:
        amount: Amount in BTC
        include_symbol: Whether to include the BTC symbol
        
    Returns:
        Formatted amount string
    """
    formatted = f"{amount:.8f}".rstrip('0').rstrip('.') if '.' in f"{amount:.8f}" else f"{amount:.8f}"
    return f"{formatted} BTC" if include_symbol else formatted

def format_satoshi_amount(amount: int) -> str:
    """
    Format a satoshi amount as a string with BTC equivalent.
    
    Args:
        amount: Amount in satoshis
        
    Returns:
        Formatted amount string
    """
    btc_equivalent = satoshi_to_btc(amount)
    return f"{amount:,} satoshis ({format_btc_amount(btc_equivalent)})" 