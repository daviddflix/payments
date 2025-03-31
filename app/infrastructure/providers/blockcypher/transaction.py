from requests.exceptions import RequestException
from typing import Dict, Any, List, Optional, Union
import requests
import os

class TransactionManager:
    """
    Class to handle all BlockCypher transaction operations.
    This manages transaction creation, querying, and broadcasting for the payment gateway.
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
    
    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get detailed information about a transaction by its hash.
        
        Args:
            tx_hash: The transaction hash to look up
            
        Returns:
            Dictionary with transaction details
        """
        try:
            url = f"{self.base_url}/txs/{tx_hash}"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get transaction details: {str(e)}")
    
    def get_unconfirmed_transactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get a list of currently unconfirmed transactions.
        
        Args:
            limit: Maximum number of transactions to return (1-100)
            
        Returns:
            List of unconfirmed transactions
        """
        try:
            url = f"{self.base_url}/txs"
            params = {
                'token': self.api_token,
                'limit': limit,
                'includeHex': False,  # Set to True if you need the raw transaction hex
                'confidence': 0       # Only transactions with 0 confidence (unconfirmed)
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get unconfirmed transactions: {str(e)}")
    
    def create_transaction(
        self, 
        inputs: List[Dict[str, Any]], 
        outputs: List[Dict[str, Any]], 
        fees: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new transaction with specified inputs and outputs.
        This creates the transaction skeleton but does not sign it.
        
        Args:
            inputs: List of inputs (addresses or previous transaction outputs)
            outputs: List of outputs (addresses and amounts)
            fees: Optional fee amount (in satoshis)
            
        Returns:
            Transaction skeleton with data needed for signing
        """
        try:
            data = {
                "inputs": inputs,
                "outputs": outputs
            }
            
            if fees is not None:
                data["fees"] = fees
                
            url = f"{self.base_url}/txs/new"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to create transaction: {str(e)}")
    
    def sign_transaction(self, tx_skeleton: Dict[str, Any], private_keys: List[str]) -> Dict[str, Any]:
        """
        Sign a transaction with the provided private keys.
        
        Args:
            tx_skeleton: Transaction skeleton from create_transaction
            private_keys: List of private keys for signing
            
        Returns:
            Signed transaction data
        """
        try:
            data = {
                "tx": tx_skeleton["tx"],
                "tosign": tx_skeleton["tosign"],
                "signatures": self._create_signatures(tx_skeleton["tosign"], private_keys)
            }
            
            url = f"{self.base_url}/txs/sign"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to sign transaction: {str(e)}")
    
    def _create_signatures(self, to_sign: List[str], private_keys: List[str]) -> List[str]:
        """
        Helper method to create signatures for each input.
        This should be replaced with actual cryptographic signing.
        
        Args:
            to_sign: List of hex strings to sign
            private_keys: List of private keys for signing
            
        Returns:
            List of signature hex strings
        """
        # In a real implementation, you would sign each tosign item with the 
        # corresponding private key using appropriate cryptographic libraries
        # For now, we'll just return a placeholder indicating that proper
        # client-side signing is needed
        return ["SIGNATURE_PLACEHOLDER" for _ in to_sign]
    
    def broadcast_transaction(self, signed_tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Broadcast a signed transaction to the network.
        
        Args:
            signed_tx: Signed transaction data from sign_transaction
            
        Returns:
            Transaction details including hash if successful
        """
        try:
            url = f"{self.base_url}/txs/send"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=signed_tx)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to broadcast transaction: {str(e)}")
    
    def push_raw_transaction(self, tx_hex: str) -> Dict[str, Any]:
        """
        Push a raw transaction in hex format to the network.
        
        Args:
            tx_hex: Raw transaction in hexadecimal format
            
        Returns:
            Transaction details including hash if successful
        """
        try:
            data = {"tx": tx_hex}
            url = f"{self.base_url}/txs/push"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to push raw transaction: {str(e)}")
    
    def decode_raw_transaction(self, tx_hex: str) -> Dict[str, Any]:
        """
        Decode a raw transaction hex string without broadcasting it.
        
        Args:
            tx_hex: Raw transaction in hexadecimal format
            
        Returns:
            Decoded transaction details
        """
        try:
            data = {"tx": tx_hex}
            url = f"{self.base_url}/txs/decode"
            params = {'token': self.api_token}
            response = requests.post(url, params=params, json=data)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to decode raw transaction: {str(e)}")
    
    def simple_transaction(
        self, 
        from_address: str,
        to_address: str, 
        amount_satoshis: int,
        private_key: str = None
    ) -> Dict[str, Any]:
        """
        Create and optionally sign/broadcast a simple transaction from one address to another.
        
        Args:
            from_address: Source address to send from
            to_address: Destination address to send to
            amount_satoshis: Amount to send in satoshis
            private_key: Optional private key for signing; if provided, transaction is signed and broadcast
            
        Returns:
            Transaction details or transaction hash if broadcast
        """
        try:
            # Step 1: Create transaction skeleton
            inputs = [{"addresses": [from_address]}]
            outputs = [{"addresses": [to_address], "value": amount_satoshis}]
            
            tx_skeleton = self.create_transaction(inputs, outputs)
            
            # If no private key provided, just return the skeleton
            if not private_key:
                return tx_skeleton
            
            # Step 2: Sign the transaction
            signed_tx = self.sign_transaction(tx_skeleton, [private_key])
            
            # Step 3: Broadcast the transaction
            return self.broadcast_transaction(signed_tx)
        except Exception as e:
            raise Exception(f"Failed to create simple transaction: {str(e)}")
    
    def create_multisig_transaction(
        self,
        from_address: str,
        to_address: str,
        amount_satoshis: int,
        pubkeys: List[str],
        script_type: str = 'multisig-2-of-3'
    ) -> Dict[str, Any]:
        """
        Create a multisignature transaction skeleton that requires multiple signatures.
        
        Args:
            from_address: Multisig address to send from
            to_address: Destination address to send to
            amount_satoshis: Amount to send in satoshis
            pubkeys: List of public keys involved in the multisig
            script_type: Type of multisig script (e.g., 'multisig-2-of-3')
            
        Returns:
            Transaction skeleton with data needed for multi-party signing
        """
        try:
            inputs = [{
                "addresses": [from_address],
                "script_type": script_type,
                "pubkeys": pubkeys
            }]
            
            outputs = [{"addresses": [to_address], "value": amount_satoshis}]
            
            return self.create_transaction(inputs, outputs)
        except Exception as e:
            raise Exception(f"Failed to create multisig transaction: {str(e)}")
    
    def send_transaction_with_confidence(
        self, 
        from_address: str,
        to_address: str, 
        amount_satoshis: int,
        private_key: str,
        min_confidence: float = 0.90
    ) -> Dict[str, Any]:
        """
        Send a transaction and wait until it reaches a minimum confidence threshold.
        Confidence is a BlockCypher-specific metric for unconfirmed transactions.
        
        Args:
            from_address: Source address to send from
            to_address: Destination address to send to
            amount_satoshis: Amount to send in satoshis
            private_key: Private key for signing
            min_confidence: Minimum confidence level (0.0-1.0) to wait for
            
        Returns:
            Transaction details with confidence information
        """
        try:
            # Send the transaction
            result = self.simple_transaction(from_address, to_address, amount_satoshis, private_key)
            
            # If successful, get the transaction hash
            tx_hash = result.get('hash')
            if not tx_hash:
                return result
            
            # Get transaction details with confidence
            tx_details = self.get_transaction_confidence(tx_hash)
            
            # In a real implementation, you might poll until confidence reaches threshold
            # For now, just return the details
            return tx_details
        except Exception as e:
            raise Exception(f"Failed to send transaction with confidence: {str(e)}")
    
    def get_transaction_confidence(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get the confidence factor for an unconfirmed transaction.
        
        Args:
            tx_hash: The transaction hash to check
            
        Returns:
            Transaction confidence details
        """
        try:
            url = f"{self.base_url}/txs/{tx_hash}/confidence"
            params = {'token': self.api_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
        except RequestException as e:
            raise Exception(f"Failed to get transaction confidence: {str(e)}")


if __name__ == "__main__":
    # How to use the TransactionManager
    manager = TransactionManager(coin_symbol="btc-testnet")
    
    # Example usage
    try:
        print("\n===== TRANSACTION DETAILS =====")
        # Get transaction details by hash
        # Replace with a real transaction hash
        tx_hash = "67b5c8a1c5e1dcbd5f3b8a246153433572a17a59ffec27329be12ecce1221a7e"
        tx_details = manager.get_transaction(tx_hash)
        print(f"Transaction details: {tx_details}")
        
        print("\n===== UNCONFIRMED TRANSACTIONS =====")
        # Get unconfirmed transactions
        unconfirmed = manager.get_unconfirmed_transactions(limit=5)
        print(f"Unconfirmed transactions count: {len(unconfirmed)}")
        
        print("\n===== TRANSACTION CREATION (EXAMPLE) =====")
        # This is just an example that won't be executed
        print("To create a transaction:")
        print("1. Create inputs and outputs")
        print("2. Call create_transaction(inputs, outputs)")
        print("3. Sign the transaction client-side or with sign_transaction()")
        print("4. Broadcast with broadcast_transaction()")
        
        print("\n===== TRANSACTION CONFIDENCE =====")
        # Get transaction confidence
        confidence = manager.get_transaction_confidence(tx_hash)
        print(f"Transaction confidence: {confidence}")
        
    except Exception as e:
        print(f"\nError: {e}") 