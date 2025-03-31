"""
Service for handling blockchain operations across different cryptocurrency networks.

This service provides unified access to blockchain functionality through specialized providers.
"""

from typing import Optional, Dict, Any, List
from ..core.config import settings
from ..core.logger import logger

# Import providers
from .providers.blockcypher.blockchain import BlockchainService as BCBlockchainService
from .providers.blockcypher.wallets import WalletManager
from .providers.blockcypher.transactions import TransactionManager
from .providers.blockcypher.forwarding import ForwardingManager

class BlockchainService:
    """Service for handling blockchain operations across different networks."""
    
    def __init__(self):
        self.api_token = settings.BLOCKCYPHER_TOKEN
    
    def _get_blockchain_service(self, network: str) -> BCBlockchainService:
        """Get a blockchain service for the specified network."""
        return BCBlockchainService(coin_symbol=network, api_token=self.api_token)
    
    def _get_wallet_manager(self, network: str) -> WalletManager:
        """Get a wallet manager for the specified network."""
        return WalletManager(coin_symbol=network, api_token=self.api_token)
    
    def _get_transaction_manager(self, network: str) -> TransactionManager:
        """Get a transaction manager for the specified network."""
        return TransactionManager(coin_symbol=network, api_token=self.api_token)
    
    def _get_forwarding_manager(self, network: str) -> ForwardingManager:
        """Get a forwarding manager for the specified network."""
        return ForwardingManager(coin_symbol=network, api_token=self.api_token)
    
    def get_supported_networks(self) -> List[str]:
        """Get a list of supported cryptocurrency networks."""
        return [
            "btc", "btc-testnet", "ltc", "doge", "dash", "bcy"
        ]
    
    # Wallet operations
    
    def create_wallet(self, network: str, address: str, wallet_name: Optional[str] = None):
        """Create a new wallet for the specified network."""
        wallet_manager = self._get_wallet_manager(network)
        return wallet_manager.create_wallet(addresses=address, wallet_name=wallet_name)
    
    def get_address_balance(self, network: str, address: str) -> float:
        """Get the balance of an address on the specified network."""
        wallet_manager = self._get_wallet_manager(network)
        return wallet_manager.get_wallet_balance(address)
    
    def get_address_details(self, network: str, address: str):
        """Get detailed information for a specific address on the specified network."""
        wallet_manager = self._get_wallet_manager(network)
        return wallet_manager.get_wallet_details(address)
    
    def get_total_balance(self, network: str, address: str) -> int:
        """Get the current balance for a specific address in the smallest unit."""
        wallet_manager = self._get_wallet_manager(network)
        return wallet_manager.get_raw_balance(address)
    
    # Transaction operations
    
    def create_transaction(
        self,
        network: str,
        from_address: str,
        to_address: str,
        amount: int,  # Amount in satoshis
        private_key: str
    ):
        """Create and send a transaction on the specified network."""
        tx_manager = self._get_transaction_manager(network)
        return tx_manager.create_and_sign_transaction(
            from_address=from_address,
            to_address=to_address,
            amount_satoshis=amount,
            private_key=private_key
        )
    
    def get_transaction_status(self, network: str, tx_hash: str):
        """Get the status of a transaction on the specified network."""
        tx_manager = self._get_transaction_manager(network)
        tx_details = tx_manager.get_transaction(tx_hash)
        confirmations = tx_details.get('confirmations', 0)
        
        if confirmations == 0:
            confidence = tx_manager.get_transaction_confidence(tx_hash)
            return {
                "confirmations": 0,
                "confidence": confidence.get('confidence', 0),
                "double_spend": confidence.get('double_spend', False),
                "status": "unconfirmed"
            }
        elif confirmations < 6:
            return {
                "confirmations": confirmations,
                "status": "confirming"
            }
        else:
            return {
                "confirmations": confirmations,
                "status": "confirmed"
            }
    
    def get_transaction_details(self, network: str, tx_hash: str) -> Dict[str, Any]:
        """Get detailed information for a specific transaction on the specified network."""
        tx_manager = self._get_transaction_manager(network)
        return tx_manager.get_transaction(tx_hash, include_confidence=True)
    
    # Blockchain operations
    
    def get_latest_block_height(self, network: str) -> int:
        """Get the latest block height for the specified network."""
        blockchain_service = self._get_blockchain_service(network)
        return blockchain_service.get_latest_block_height()
    
    def get_block_details(self, network: str, block_height: int):
        """Get details of a specific block on the specified network."""
        blockchain_service = self._get_blockchain_service(network)
        return blockchain_service.get_block_details(block_height)
    
    def get_block_overview(self, network: str, block_height: int) -> Dict[str, Any]:
        """Get overview information for a specific block on the specified network."""
        blockchain_service = self._get_blockchain_service(network)
        return blockchain_service.get_block_overview(block_height)
    
    def get_fee_estimates(self, network: str) -> Dict[str, int]:
        """Get fee estimates for different priority levels on the specified network."""
        blockchain_service = self._get_blockchain_service(network)
        return blockchain_service.get_fee_estimates()
    
    # Forwarding operations
    
    def create_forwarding_address(
        self, 
        network: str,
        destination_address: str,
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a forwarding address that automatically sends funds to a destination address.
        
        Args:
            network: The cryptocurrency network
            destination_address: The address where funds should be forwarded
            callback_url: Optional URL to receive webhook notifications
            
        Returns:
            Dictionary with forwarding information including the input address to share with customers
        """
        forwarding_manager = self._get_forwarding_manager(network)
        return forwarding_manager.create_forwarding_address(
            destination=destination_address,
            callback_url=callback_url
        )
    
    def create_webhook(
        self,
        network: str,
        event: str,
        url: str,
        address: Optional[str] = None,
        transaction_hash: Optional[str] = None,
        confirmations: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a webhook to receive notifications for blockchain events.
        
        Args:
            network: The cryptocurrency network
            event: Event type (unconfirmed-tx, confirmed-tx, tx-confirmation)
            url: Callback URL to receive webhook notifications
            address: Optional address to monitor (for address events)
            transaction_hash: Optional transaction hash to monitor (for tx events)
            confirmations: Optional number of confirmations to require (for tx-confirmation events)
            
        Returns:
            Dictionary with webhook information
        """
        forwarding_manager = self._get_forwarding_manager(network)
        
        if address and event in ["unconfirmed-tx", "confirmed-tx"]:
            return forwarding_manager.create_address_webhook(
                address=address,
                url=url,
                event_type=event
            )
        elif transaction_hash and event == "tx-confirmation":
            return forwarding_manager.create_transaction_webhook(
                transaction_hash=transaction_hash,
                url=url,
                confirmations=confirmations or 6
            )
        else:
            return forwarding_manager.create_webhook(
                url=url,
                event=event,
                address=address,
                hash=transaction_hash,
                confirmations=confirmations
            )

