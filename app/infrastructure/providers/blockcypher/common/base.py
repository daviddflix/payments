"""
Base classes for BlockCypher API integration.

This module contains the base provider class that all BlockCypher service classes inherit from.
"""

import os
import requests
from typing import Dict, Any, Tuple, Optional

class BlockCypherProvider:
    """
    Base class for all BlockCypher API providers.
    
    Provides common functionality like API token management, URL construction,
    and network parameter mapping.
    """
    
    # Mapping of coin_symbol to (coin, chain) tuple used in BlockCypher API URL
    COIN_SYMBOL_MAPPING = {
        'btc': ('btc', 'main'),
        'btc-testnet': ('btc', 'test3'),
        'ltc': ('ltc', 'main'),
        'doge': ('doge', 'main'),
        'dash': ('dash', 'main'),
        'bcy': ('bcy', 'test')
    }
    
    def __init__(self, coin_symbol: str = 'btc-testnet', api_token: Optional[str] = None):
        """
        Initialize the BlockCypher provider.
        
        Args:
            coin_symbol: The cryptocurrency to use (default: btc-testnet)
                Options: btc (Bitcoin), btc-testnet, ltc (Litecoin), doge (Dogecoin), etc.
            api_token: Optional API token override. If not provided, will use BLOCKCYPHER_API_TOKEN env var
        """
        self.api_token = api_token or os.getenv("BLOCKCYPHER_API_TOKEN")
        if not self.api_token:
            raise ValueError("BlockCypher API token not provided and BLOCKCYPHER_API_TOKEN is not set")
        
        if coin_symbol not in self.COIN_SYMBOL_MAPPING:
            raise ValueError(f"Invalid coin symbol: {coin_symbol}. Valid options: {list(self.COIN_SYMBOL_MAPPING.keys())}")
        
        self.coin_symbol = coin_symbol
        coin, chain = self.COIN_SYMBOL_MAPPING[coin_symbol]
        self.base_url = f"https://api.blockcypher.com/v1/{coin}/{chain}"
        
        # Set default parameters used in all requests
        self.default_params = {'token': self.api_token}
        
        # Set up the conversion multiplier for satoshis to main units
        self.satoshi_multiplier = 100000000  # 1 BTC = 100,000,000 satoshis
    
    def get_url(self, endpoint: str) -> str:
        """
        Construct a full URL for a given API endpoint.
        
        Args:
            endpoint: The API endpoint path
            
        Returns:
            Full API URL
        """
        # Ensure endpoint does not start with slash to avoid double slashes
        if endpoint.startswith('/'):
            endpoint = endpoint[1:]
        
        return f"{self.base_url}/{endpoint}"
    
    def make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                    data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the BlockCypher API.
        
        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint path
            params: Optional query parameters
            data: Optional request body data
            **kwargs: Additional parameters to pass to the requests library
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = self.get_url(endpoint)
        
        # Merge default params with provided params
        request_params = {**self.default_params}
        if params:
            request_params.update(params)
        
        # Make the request
        response = requests.request(
            method=method,
            url=url,
            params=request_params,
            json=data,
            **kwargs
        )
        
        # Raise an exception for 4XX and 5XX responses
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()
    
    def get_network_parameters(self) -> Dict[str, Any]:
        """
        Get information about the current network/blockchain.
        
        Returns:
            Dictionary with network parameters
        """
        return self.make_request('GET', '') 