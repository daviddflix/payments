"""
Wallet management for BlockCypher API integration.

This module provides functionality for managing cryptocurrency wallets,
including creating wallets, generating addresses, and querying balances.
"""

from typing import Dict, Any, List, Optional, Union
from requests.exceptions import RequestException

from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.common.types import (
    Address, WalletInfo, AddressInfo, CoinSymbol
)
from app.infrastructure.providers.blockcypher.utils.conversions import satoshi_to_btc

class WalletManager(BlockCypherProvider):
    """
    Class to handle all BlockCypher wallet operations.
    
    This manages wallet creation, addresses, and balance queries for the payment gateway.
    """
    
    def create_wallet(self, addresses: Union[str, List[str]], wallet_name: Optional[str] = None) -> WalletInfo:
        """
        Create a wallet from existing address(es).
        
        Args:
            addresses: Single address or list of addresses to include in the wallet
            wallet_name: Optional custom name for the wallet
            
        Returns:
            Dictionary with wallet information
        """
        try:
            # Convert single address to list if necessary
            if isinstance(addresses, str):
                addresses = [addresses]
                
            if not wallet_name:
                wallet_name = f"wallet-for-{addresses[0][:10]}"
            
            # Wallet name must be 1-25 chars and can't start with chars that begin an address
            if len(wallet_name) < 1 or len(wallet_name) > 25:
                raise ValueError("Wallet name must be between 1-25 characters")
                
            wallet_data = {
                "name": wallet_name,
                "addresses": addresses
            }
            
            return self.make_request('POST', 'wallets', data=wallet_data)
        except RequestException as e:
            raise Exception(f"Failed to create wallet: {str(e)}")
    
    def list_wallets(self) -> List[Dict[str, Any]]:
        """
        Get a list of all wallets associated with the API token.
        
        Returns:
            List of wallet information
        """
        try:
            return self.make_request('GET', 'wallets')
        except RequestException as e:
            raise Exception(f"Failed to list wallets: {str(e)}")
    
    def get_wallet(self, wallet_name: str) -> WalletInfo:
        """
        Get information about a specific wallet.
        
        Args:
            wallet_name: Name of the wallet to retrieve
            
        Returns:
            Dictionary with wallet information
        """
        try:
            return self.make_request('GET', f'wallets/{wallet_name}')
        except RequestException as e:
            raise Exception(f"Failed to get wallet {wallet_name}: {str(e)}")
    
    def add_addresses_to_wallet(self, wallet_name: str, addresses: List[str]) -> WalletInfo:
        """
        Add addresses to an existing wallet.
        
        Args:
            wallet_name: Name of the wallet to add addresses to
            addresses: List of addresses to add to the wallet
            
        Returns:
            Updated wallet information
        """
        try:
            data = {"addresses": addresses}
            return self.make_request('POST', f'wallets/{wallet_name}/addresses', data=data)
        except RequestException as e:
            raise Exception(f"Failed to add addresses to wallet {wallet_name}: {str(e)}")
    
    def get_wallet_addresses(self, wallet_name: str) -> Dict[str, Any]:
        """
        Get all addresses associated with a wallet.
        
        Args:
            wallet_name: Name of the wallet to get addresses for
            
        Returns:
            Dictionary with wallet addresses
        """
        try:
            return self.make_request('GET', f'wallets/{wallet_name}/addresses')
        except RequestException as e:
            raise Exception(f"Failed to get addresses for wallet {wallet_name}: {str(e)}")
    
    def remove_addresses_from_wallet(self, wallet_name: str, addresses: List[str]) -> WalletInfo:
        """
        Remove addresses from an existing wallet.
        
        Args:
            wallet_name: Name of the wallet to remove addresses from
            addresses: List of addresses to remove from the wallet
            
        Returns:
            Updated wallet information
        """
        try:
            data = {"addresses": addresses}
            return self.make_request('DELETE', f'wallets/{wallet_name}/addresses', data=data)
        except RequestException as e:
            raise Exception(f"Failed to remove addresses from wallet {wallet_name}: {str(e)}")
    
    def generate_address_in_wallet(self, wallet_name: str) -> Dict[str, Any]:
        """
        Generate a new address and add it to a wallet.
        
        Args:
            wallet_name: Name of the wallet to add the new address to
            
        Returns:
            Dictionary with the new address information
        """
        try:
            return self.make_request('POST', f'wallets/{wallet_name}/addresses/generate')
        except RequestException as e:
            raise Exception(f"Failed to generate address in wallet {wallet_name}: {str(e)}")
    
    def delete_wallet(self, wallet_name: str) -> bool:
        """
        Delete a wallet.
        
        Args:
            wallet_name: Name of the wallet to delete
            
        Returns:
            True if successful
        """
        try:
            self.make_request('DELETE', f'wallets/{wallet_name}')
            return True
        except RequestException as e:
            raise Exception(f"Failed to delete wallet {wallet_name}: {str(e)}")
    
    def generate_address(self) -> Dict[str, Any]:
        """
        Generate a new address with private and public keys.
        
        Returns:
            Dictionary with address details including private and public keys
        """
        try:
            result = self.make_request('POST', 'addrs')
            
            return {
                "address": result.get("address"),
                "private_key": result.get("private"),
                "public_key": result.get("public"),
                "wif": result.get("wif")
            }
        except RequestException as e:
            raise Exception(f"Failed to generate new address: {str(e)}")
    
    def create_multisig_wallet(
        self, 
        pubkeys: List[str], 
        script_type: str = 'multisig-2-of-3'
    ) -> Dict[str, Any]:
        """
        Create a multi-signature wallet.
        
        Args:
            pubkeys: List of public keys to use in the multisig wallet
            script_type: Type of multisig script (e.g., 'multisig-2-of-3')
            
        Returns:
            Dictionary with wallet details
        """
        try:
            data = {
                "pubkeys": pubkeys,
                "script_type": script_type
            }
            
            return self.make_request('POST', 'addrs', data=data)
        except RequestException as e:
            raise Exception(f"Failed to create multisig wallet: {str(e)}")
    
    def get_wallet_balance(self, address: str) -> float:
        """
        Get the balance of a wallet address in the native coin unit (BTC, LTC, etc.)
        
        Args:
            address: The address to check
            
        Returns:
            Balance in the native coin unit
        """
        try:
            result = self.make_request('GET', f'addrs/{address}/balance')
            return satoshi_to_btc(result.get("balance", 0))
        except RequestException as e:
            raise Exception(f"Failed to get wallet balance: {str(e)}")
    
    def get_wallet_details(self, address: str) -> AddressInfo:
        """
        Get detailed information about a wallet address including transaction references.
        
        Args:
            address: The address to get details for
            
        Returns:
            Address information details
        """
        try:
            result = self.make_request('GET', f'addrs/{address}')
            
            return {
                "address": address,
                "balance": result.get("balance", 0),
                "total_received": result.get("total_received", 0),
                "total_sent": result.get("total_sent", 0),
                "n_tx": result.get("n_tx", 0),
                "unconfirmed_balance": result.get("unconfirmed_balance", 0),
                "final_balance": result.get("final_balance", 0)
            }
        except RequestException as e:
            raise Exception(f"Failed to get wallet details: {str(e)}")
    
    def get_raw_balance(self, address: str) -> int:
        """
        Get the total balance of a wallet address in satoshis (or equivalent smallest unit).
        
        Args:
            address: The address to check
            
        Returns:
            Balance in satoshis
        """
        try:
            result = self.make_request('GET', f'addrs/{address}/balance')
            return result.get("balance", 0)
        except RequestException as e:
            raise Exception(f"Failed to get raw balance: {str(e)}")
    
    def get_wallet_full_info(self, address: str, limit: int = 50) -> Dict[str, Any]:
        """
        Get comprehensive information about a wallet address including full transaction details.
        
        Args:
            address: The address to get details for
            limit: Maximum number of transactions to return
            
        Returns:
            Complete wallet information with full transaction details
        """
        try:
            params = {'limit': limit}
            return self.make_request('GET', f'addrs/{address}/full', params=params)
        except RequestException as e:
            raise Exception(f"Failed to get full wallet details: {str(e)}")
    
    def get_wallet_transactions(self, address: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get transactions for a specific wallet address.
        
        Args:
            address: The wallet address to get transactions for
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions for the wallet
        """
        try:
            params = {'limit': limit}
            result = self.make_request('GET', f'addrs/{address}/full', params=params)
            return result.get("txs", [])
        except RequestException as e:
            raise Exception(f"Failed to get wallet transactions: {str(e)}") 