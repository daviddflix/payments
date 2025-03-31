"""
Testing utilities for BlockCypher API integration.

This module provides helpers for testing with the BlockCypher Test Chain (BCY),
including functions to fund test addresses using the BCY faucet.
"""

import os
import time
from typing import Dict, Any, Optional
import warnings
import random
import string
import blockcypher

def get_test_api_token() -> str:
    """
    Get the BlockCypher API token for testing.
    
    Returns:
        API token from environment variable
    
    Raises:
        ValueError: If the token is not set
    """
    token = os.getenv("BLOCKCYPHER_API_TOKEN")
    if not token:
        raise ValueError(
            "BLOCKCYPHER_API_TOKEN environment variable must be set for tests. "
            "Get a token at https://accounts.blockcypher.com/"
        )
    return token

def generate_test_address(coin_symbol: str = 'bcy') -> Dict[str, Any]:
    """
    Generate a new test address.
    
    Args:
        coin_symbol: Coin symbol (default: 'bcy' for BlockCypher Test Chain)
        
    Returns:
        Dictionary with address, private key, and public key
    """
    try:
        return blockcypher.generate_new_address(coin_symbol=coin_symbol, api_key=get_test_api_token())
    except Exception as e:
        raise Exception(f"Failed to generate test address: {str(e)}")

def fund_test_address(address: str, amount_satoshis: int = 100000, coin_symbol: str = 'bcy') -> Dict[str, Any]:
    """
    Fund a test address using the BlockCypher faucet.
    
    Args:
        address: The address to fund
        amount_satoshis: Amount to fund in satoshis (default: 100,000)
        coin_symbol: Coin symbol (default: 'bcy' for BlockCypher Test Chain)
        
    Returns:
        Dictionary with transaction reference
        
    Notes:
        - For BCY (BlockCypher Test Chain): max 100M satoshis per request, 500B satoshis total
        - For BTC-TESTNET: max 500,000 satoshis per request, 10M satoshis total
    """
    if coin_symbol not in ['bcy', 'btc-testnet']:
        warnings.warn(
            f"Faucet only works with 'bcy' or 'btc-testnet', not '{coin_symbol}'. "
            f"Switching to 'bcy' for faucet request."
        )
        coin_symbol = 'bcy'
    
    # Validate amount limits based on network
    if coin_symbol == 'bcy' and amount_satoshis > 100000000:
        warnings.warn(
            f"Requested {amount_satoshis} satoshis exceeds BCY faucet limit of 100M. "
            f"Reducing to 100M satoshis."
        )
        amount_satoshis = 100000000
    elif coin_symbol == 'btc-testnet' and amount_satoshis > 500000:
        warnings.warn(
            f"Requested {amount_satoshis} satoshis exceeds BTC-TESTNET faucet limit of 500K. "
            f"Reducing to 500K satoshis."
        )
        amount_satoshis = 500000
    
    try:
        return blockcypher.send_faucet_coins(
            address_to_fund=address,
            satoshis=amount_satoshis,
            api_key=get_test_api_token(),
            coin_symbol=coin_symbol
        )
    except Exception as e:
        raise Exception(f"Failed to fund test address: {str(e)}")

def generate_random_wallet_name() -> str:
    """
    Generate a random wallet name for testing.
    
    Returns:
        Random string of 10 characters prefixed with 'test-'
    """
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test-{random_suffix}"

def wait_for_confirmation(tx_hash: str, coin_symbol: str = 'bcy', 
                         target_confirmations: int = 1, 
                         timeout_seconds: int = 60,
                         check_interval: float = 2.0) -> bool:
    """
    Wait for a transaction to get a certain number of confirmations.
    
    Args:
        tx_hash: Transaction hash to monitor
        coin_symbol: Coin symbol (default: 'bcy' for BlockCypher Test Chain)
        target_confirmations: Number of confirmations to wait for (default: 1)
        timeout_seconds: Maximum time to wait in seconds (default: 60)
        check_interval: Time between checks in seconds (default: 2.0)
        
    Returns:
        True if transaction reached target confirmations within timeout, False otherwise
    """
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        try:
            tx_details = blockcypher.get_transaction_details(
                tx_hash=tx_hash,
                coin_symbol=coin_symbol,
                api_key=get_test_api_token()
            )
            confirmations = tx_details.get('confirmations', 0)
            
            if confirmations >= target_confirmations:
                return True
                
            # Wait before checking again
            time.sleep(check_interval)
            
        except Exception as e:
            print(f"Error checking transaction confirmation: {str(e)}")
            time.sleep(check_interval)
    
    return False

def setup_funded_test_address(amount_satoshis: int = 100000, coin_symbol: str = 'bcy') -> Dict[str, Any]:
    """
    Generate a new address and fund it in one step.
    
    Args:
        amount_satoshis: Amount to fund in satoshis (default: 100,000)
        coin_symbol: Coin symbol (default: 'bcy' for BlockCypher Test Chain)
        
    Returns:
        Dictionary with address information and funding transaction
    """
    # Generate new address
    address_info = generate_test_address(coin_symbol=coin_symbol)
    
    # Fund the address
    funding_tx = fund_test_address(
        address=address_info['address'],
        amount_satoshis=amount_satoshis,
        coin_symbol=coin_symbol
    )
    
    # Wait for at least 1 confirmation if using BCY
    if coin_symbol == 'bcy':
        tx_hash = funding_tx.get('tx_ref')
        if tx_hash:
            wait_for_confirmation(tx_hash, coin_symbol=coin_symbol)
    
    return {
        "address_info": address_info,
        "funding_tx": funding_tx
    } 