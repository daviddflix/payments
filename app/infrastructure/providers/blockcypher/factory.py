from typing import Dict, Type, Optional
from .base import CryptocurrencyProvider
from .blockchain import BlockCypherProvider

class CryptocurrencyProviderFactory:
    """Factory class for creating cryptocurrency providers."""
    
    # Supported networks and their configurations
    _providers: Dict[str, Type[CryptocurrencyProvider]] = {
        # Bitcoin networks
        "btc": BlockCypherProvider,
        "btc-testnet": BlockCypherProvider,
        
        # Other cryptocurrencies
        "eth": BlockCypherProvider,
        "ltc": BlockCypherProvider,
        "dash": BlockCypherProvider,
        "doge": BlockCypherProvider,
        "bcy": BlockCypherProvider,  # BlockCypher testnet
    }
    
    @classmethod
    def create_provider(
        cls,
        network: str,
        api_token: Optional[str] = None,
        **kwargs
    ) -> CryptocurrencyProvider:
        """
        Create a cryptocurrency provider instance.
        
        Args:
            network: The cryptocurrency network (e.g., 'btc', 'eth', 'ltc')
            api_token: Optional API token for the provider
            **kwargs: Additional arguments for the provider
            
        Returns:
            An instance of the appropriate CryptocurrencyProvider
            
        Raises:
            ValueError: If the network is not supported
        """
        if network not in cls._providers:
            raise ValueError(f"Unsupported network: {network}")
        
        provider_class = cls._providers[network]
        return provider_class(network=network, api_token=api_token, **kwargs)
    
    @classmethod
    def get_supported_networks(cls) -> list:
        """Get a list of supported cryptocurrency networks."""
        return list(cls._providers.keys())
    
    @classmethod
    def is_network_supported(cls, network: str) -> bool:
        """Check if a network is supported."""
        return network in cls._providers 