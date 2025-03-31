from requests.exceptions import RequestException
from typing import Dict, Any, List, Optional, Union
import requests
import os

class WalletManager:
    """
    Class to handle all BlockCypher wallet operations.
    This manages wallet creation, addresses, and balance queries for the payment gateway.
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
    
    def __init__(self, coin_symbol: str = 'btc-testnet'):
        self.api_token = os.getenv("BLOCKCYPHER_API_TOKEN")
        if not self.api_token:
            raise ValueError("BLOCKCYPHER_API_TOKEN is not set")
        
        if coin_symbol not in self.COIN_SYMBOL_MAPPING:
            raise ValueError(f"Invalid coin symbol: {coin_symbol}")
        
        self.coin_symbol = coin_symbol
        coin, chain = self.COIN_SYMBOL_MAPPING[coin_symbol]
        self.base_url = f"https://api.blockcypher.com/v1/{coin}/{chain}"
        self.satoshi_multiplier = 100000000  # 1 BTC = 100,000,000 satoshis
    
    def create_wallet(self, addresses: Union[str, List[str]], wallet_name: Optional[str] = None) -> Dict[str, Any]:
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
            
            url = f"{self.base_url}/wallets"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=wallet_data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create wallet: {str(e)}")
    
    def list_wallets(self) -> List[Dict[str, Any]]:
        """
        Get a list of all wallets associated with the API token.
        
        Returns:
            List of wallet information
        """
        try:
            url = f"{self.base_url}/wallets"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to list wallets: {str(e)}")
    
    def get_wallet(self, wallet_name: str) -> Dict[str, Any]:
        """
        Get information about a specific wallet.
        
        Args:
            wallet_name: Name of the wallet to retrieve
            
        Returns:
            Dictionary with wallet information
        """
        try:
            url = f"{self.base_url}/wallets/{wallet_name}"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get wallet {wallet_name}: {str(e)}")
    
    def add_addresses_to_wallet(self, wallet_name: str, addresses: List[str]) -> Dict[str, Any]:
        """
        Add addresses to an existing wallet.
        
        Args:
            wallet_name: Name of the wallet to add addresses to
            addresses: List of addresses to add to the wallet
            
        Returns:
            Updated wallet information
        """
        try:
            url = f"{self.base_url}/wallets/{wallet_name}/addresses"
            params = {'token': self.api_token}
            data = {"addresses": addresses}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
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
            url = f"{self.base_url}/wallets/{wallet_name}/addresses"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get addresses for wallet {wallet_name}: {str(e)}")
    
    def remove_addresses_from_wallet(self, wallet_name: str, addresses: List[str]) -> Dict[str, Any]:
        """
        Remove addresses from an existing wallet.
        
        Args:
            wallet_name: Name of the wallet to remove addresses from
            addresses: List of addresses to remove from the wallet
            
        Returns:
            Updated wallet information
        """
        try:
            url = f"{self.base_url}/wallets/{wallet_name}/addresses"
            params = {'token': self.api_token}
            data = {"addresses": addresses}
            response = requests.delete(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
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
            url = f"{self.base_url}/wallets/{wallet_name}/addresses/generate"
            params = {'token': self.api_token}
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            return response.json()
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
            url = f"{self.base_url}/wallets/{wallet_name}"
            params = {'token': self.api_token}
            response = requests.delete(url, params=params)
            response.raise_for_status()
            
            return True
        except RequestException as e:
            raise Exception(f"Failed to delete wallet {wallet_name}: {str(e)}")
    
    def generate_address(self) -> Dict[str, Any]:
        """
        Generate a new address with private and public keys.
        """
        try:
            url = f"{self.base_url}/addrs"
            params = {'token': self.api_token}
            response = requests.post(url, params=params)
            response.raise_for_status()
            result = response.json()
            
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
            
            url = f"{self.base_url}/addrs"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create multisig wallet: {str(e)}")
    
    def get_wallet_balance(self, address: str) -> float:
        """
        Get the balance of a wallet address in the native coin unit (BTC, LTC, etc.)
        """
        try:
            url = f"{self.base_url}/addrs/{address}/balance"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            return float(result.get("balance", 0)) / self.satoshi_multiplier
        except RequestException as e:
            raise Exception(f"Failed to get wallet balance: {str(e)}")
    
    def get_wallet_details(self, address: str) -> Dict[str, Any]:
        """
        Get detailed information about a wallet address including transaction references.
        """
        try:
            url = f"{self.base_url}/addrs/{address}"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
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
        """
        try:
            url = f"{self.base_url}/addrs/{address}/balance"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
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
            url = f"{self.base_url}/addrs/{address}/full"
            params = {
                'token': self.api_token,
                'limit': limit
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
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
            url = f"{self.base_url}/addrs/{address}/full"
            params = {
                'token': self.api_token,
                'limit': limit
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json()
            
            return result.get("txs", [])
        except RequestException as e:
            raise Exception(f"Failed to get wallet transactions: {str(e)}")


if __name__ == "__main__":
    # How to use the WalletManager
    manager = WalletManager(coin_symbol="btc-testnet")
    
    # Example usage
    try:
        # print("\n===== GENERATING ADDRESSES =====")
        # Generate new addresses
        # address1 = manager.generate_address()
        # address2 = manager.generate_address()
        # print(f"Generated address 1: {address1['address']}")
        # print(f"Generated address 2: {address2['address']}")
        
        # Or use existing addresses for testing
        test_address = 'mteBzZDP2LN41SfkJLRfV6JM2s8bPMES93'
        test_address2 = 'mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS'
        pubkey1 = '0384e36c0a1e7eadb322050871e6a47a51fb8e311d875a25f39d9b6c14616ebbe2'
        pubkey2 = '02cf761afc52683abba8622bdf98c431da035e76f989df9797057d38f7343ef76e'

        # print("\n===== WALLET CREATION AND MANAGEMENT =====")
        # Create a wallet with a single address
        wallet_name = "wallet-for-mteBzZDP2L"
        # wallet = manager.create_wallet(test_address)
        # print(f"Created wallet: {wallet}")

        # Create a wallet with multiple addresses
        # multi_wallet_name = "test-multi-wallet"
        # multi_wallet = manager.create_wallet([test_address, test_address2], wallet_name=multi_wallet_name)
        # print(f"Created multi-address wallet: {multi_wallet}")
        
        # List all wallets
        wallets = manager.list_wallets()
        print(f"All wallets: {wallets}")
        
        # Get a specific wallet
        wallet_info = manager.get_wallet(wallet_name)
        print(f"Wallet info for {wallet_name}: {wallet_info}")
        
        # Get addresses in a wallet
        wallet_addresses = manager.get_wallet_addresses(wallet_name)
        print(f"Addresses in wallet {wallet_name}: {wallet_addresses}")
        
        # Add an address to a wallet
        # updated_wallet = manager.add_addresses_to_wallet(wallet_name, [test_address2])
        # print(f"Updated wallet after adding address: {updated_wallet}")
        
        # Generate a new address in a wallet
        # new_address = manager.generate_address_in_wallet(wallet_name)
        # print(f"Generated new address in wallet: {new_address}")
        
        # Remove an address from a wallet
        updated_wallet = manager.remove_addresses_from_wallet(wallet_name, [test_address2])
        print(f"Updated wallet after removing address: {updated_wallet}")

        print("\n===== BALANCE AND TRANSACTION INFORMATION =====")
        # Get wallet balance
        balance = manager.get_wallet_balance(test_address)
        print(f"Wallet balance: {balance} BTC")
        
        # Get raw balance (in satoshis)
        raw_balance = manager.get_raw_balance(test_address)
        print(f"Raw balance (satoshis): {raw_balance}")
        
        # Get wallet details
        wallet_details = manager.get_wallet_details(test_address)
        print(f"Wallet details: {wallet_details}")
        
        # Get comprehensive wallet info with transactions
        full_info = manager.get_wallet_full_info(test_address, limit=10)
        print(f"Full wallet info (truncated): {str(full_info)[:200]}...")
        
        # Get just the transactions
        transactions = manager.get_wallet_transactions(test_address, limit=5)
        print(f"Recent transactions (count): {len(transactions)}")

        print("\n===== MULTISIG WALLET =====")
        # Create a multisig wallet (requires multiple public keys)
        pubkeys = [pubkey1, pubkey2]
        multisig = manager.create_multisig_wallet(pubkeys, script_type='multisig-2-of-2')
        print(f"Created multisig wallet: {multisig}")
        
        print("\n===== WALLET DELETION =====")
        # Delete a wallet (uncomment to actually delete)
        # deleted = manager.delete_wallet(wallet_name)
        # print(f"Deleted wallet {wallet_name}: {deleted}")

    except Exception as e:
        print(f"\nError: {e}")


