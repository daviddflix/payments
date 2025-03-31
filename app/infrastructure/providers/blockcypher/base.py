from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from .blockcypher_types import (
    WalletInfo,
    TransactionInfo,
    TransactionStatus,
    BlockInfo,
    AddressInfo,
    TokenInfo
)

class CryptocurrencyProvider(ABC):
    """Base class for cryptocurrency providers."""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token
    
    @abstractmethod
    def get_network_name(self) -> str:
        """Get the name of the cryptocurrency network."""
        pass
    
    @abstractmethod
    def get_network_symbol(self) -> str:
        """Get the symbol of the cryptocurrency network."""
        pass
    
    @abstractmethod
    def get_satoshi_multiplier(self) -> int:
        """Get the multiplier to convert from satoshis to the main unit."""
        pass
    
    @abstractmethod
    def create_wallet(self, address: str) -> WalletInfo:
        """Create a new wallet for the specific cryptocurrency."""
        pass
    
    @abstractmethod
    def get_address_balance(self, address: str) -> float:
        """Get the balance of an address."""
        pass
    
    @abstractmethod
    def get_address_details(self, address: str) -> AddressInfo:
        """Get detailed information for a specific address."""
        pass
    
    @abstractmethod
    def get_total_balance(self, address: str) -> int:
        """Get the current balance for a specific address in the smallest unit (e.g., satoshis)."""
        pass
    
    @abstractmethod
    def create_transaction(
        self,
        from_address: str,
        to_address: str,
        amount: float,
        private_key: str
    ) -> TransactionInfo:
        """Create and send a transaction."""
        pass
    
    @abstractmethod
    def get_transaction_status(self, tx_hash: str) -> TransactionStatus:
        """Get the status of a transaction."""
        pass
    
    @abstractmethod
    def get_transaction_details(self, tx_hash: str) -> Dict[str, Any]:
        """Get detailed information for a specific transaction."""
        pass
    
    @abstractmethod
    def get_latest_block_height(self) -> int:
        """Get the latest block height."""
        pass
    
    @abstractmethod
    def get_block_details(self, block_height: int) -> BlockInfo:
        """Get details of a specific block."""
        pass
    
    @abstractmethod
    def get_block_overview(self, block_height: int) -> Dict[str, Any]:
        """Get overview information for a specific block."""
        pass

    # Token-related methods
    @abstractmethod
    def get_token_balance(self, address: str, token_address: str) -> float:
        """Get the balance of a specific token for an address."""
        pass
    
    @abstractmethod
    def get_token_details(self, token_address: str) -> TokenInfo:
        """Get details of a specific token."""
        pass
    
    @abstractmethod
    def create_token_transaction(
        self,
        from_address: str,
        to_address: str,
        token_address: str,
        amount: float,
        private_key: str
    ) -> TransactionInfo:
        """Create and send a token transaction."""
        pass
    
    @abstractmethod
    def get_token_transactions(
        self,
        address: str,
        token_address: str,
        limit: int = 50
    ) -> List[TransactionInfo]:
        """Get token transactions for an address."""
        pass 