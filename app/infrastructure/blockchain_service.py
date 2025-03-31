from typing import Optional, Dict, Any, List
from ..core.config import settings
from .providers.blockcypher.factory import CryptocurrencyProviderFactory
from ..core.logger import logger

class BlockchainService:
    """Service for handling blockchain operations across different networks."""
    
    def __init__(self):
        self.api_token = settings.BLOCKCYPHER_TOKEN
    
    def get_provider(self, network: str, **kwargs) -> Any:
        """Get a cryptocurrency provider for the specified network."""
        return CryptocurrencyProviderFactory.create_provider(
            network=network,
            api_token=self.api_token,
            **kwargs
        )
    
    def get_supported_networks(self) -> List[str]:
        """Get a list of supported cryptocurrency networks."""
        return CryptocurrencyProviderFactory.get_supported_networks()
    
    def create_wallet(self, network: str, address: str):
        """Create a new wallet for the specified network."""
        provider = self.get_provider(network)
        return provider.create_wallet(address)
    
    def get_address_balance(self, network: str, address: str) -> float:
        """Get the balance of an address on the specified network."""
        provider = self.get_provider(network)
        return provider.get_address_balance(address)
    
    def get_address_details(self, network: str, address: str):
        """Get detailed information for a specific address on the specified network."""
        provider = self.get_provider(network)
        return provider.get_address_details(address)
    
    def get_total_balance(self, network: str, address: str) -> int:
        """Get the current balance for a specific address in the smallest unit."""
        provider = self.get_provider(network)
        return provider.get_total_balance(address)
    
    def create_transaction(
        self,
        network: str,
        from_address: str,
        to_address: str,
        amount: float,
        private_key: str
    ):
        """Create and send a transaction on the specified network."""
        provider = self.get_provider(network)
        return provider.create_transaction(
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            private_key=private_key
        )
    
    def get_transaction_status(self, network: str, tx_hash: str):
        """Get the status of a transaction on the specified network."""
        provider = self.get_provider(network)
        return provider.get_transaction_status(tx_hash)
    
    def get_transaction_details(self, network: str, tx_hash: str) -> Dict[str, Any]:
        """Get detailed information for a specific transaction on the specified network."""
        provider = self.get_provider(network)
        return provider.get_transaction_details(tx_hash)
    
    def get_latest_block_height(self, network: str) -> int:
        """Get the latest block height for the specified network."""
        provider = self.get_provider(network)
        return provider.get_latest_block_height()
    
    def get_block_details(self, network: str, block_height: int):
        """Get details of a specific block on the specified network."""
        provider = self.get_provider(network)
        return provider.get_block_details(block_height)
    
    def get_block_overview(self, network: str, block_height: int) -> Dict[str, Any]:
        """Get overview information for a specific block on the specified network."""
        provider = self.get_provider(network)
        return provider.get_block_overview(block_height) 
    
# How to use the BlockchainService

service = BlockchainService()

logger.info(service.get_supported_networks())

