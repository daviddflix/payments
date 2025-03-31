"""
Transaction management for BlockCypher API integration.

This module provides functionality for creating, broadcasting, and monitoring
cryptocurrency transactions.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from requests.exceptions import RequestException
import time

from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.common.types import (
    Address, TransactionHash, TransactionInfo, CoinSymbol
)

class TransactionManager(BlockCypherProvider):
    """
    Manager for handling blockchain transactions through the BlockCypher API.
    
    This class provides methods for creating, sending, and monitoring transactions.
    """
    
    def create_transaction(
        self,
        inputs: List[Dict[str, Any]],
        outputs: List[Dict[str, Any]],
        fees: Optional[int] = None,
        preference: str = 'medium',
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new transaction skeleton.
        
        Args:
            inputs: List of transaction inputs
            outputs: List of transaction outputs
            fees: Optional explicit fee in satoshis
            preference: Fee preference (high, medium, low)
            **kwargs: Additional transaction parameters
            
        Returns:
            Transaction skeleton
        """
        try:
            tx_data = {
                "inputs": inputs,
                "outputs": outputs,
                "preference": preference
            }
            
            # Add optional fees if provided
            if fees is not None:
                tx_data["fees"] = fees
                
            # Add any additional parameters
            tx_data.update(kwargs)
            
            return self.make_request('POST', 'txs/new', data=tx_data)
        except RequestException as e:
            raise Exception(f"Failed to create transaction: {str(e)}")
    
    def sign_transaction(
        self,
        tx_skeleton: Dict[str, Any],
        private_keys: List[str],
        signatures: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Sign a transaction with private keys or signatures.
        
        Args:
            tx_skeleton: Transaction skeleton from create_transaction
            private_keys: List of private keys to sign with
            signatures: Optional list of signatures if not using private keys
            
        Returns:
            Signed transaction
        """
        try:
            tx_data = {
                "tx": tx_skeleton,
                "private_keys": private_keys
            }
            
            if signatures:
                tx_data["signatures"] = signatures
                
            return self.make_request('POST', 'txs/sign', data=tx_data)
        except RequestException as e:
            raise Exception(f"Failed to sign transaction: {str(e)}")
    
    def broadcast_transaction(self, tx_hex: str) -> Dict[str, Any]:
        """
        Broadcast a signed transaction to the network.
        
        Args:
            tx_hex: Hex-encoded signed transaction
            
        Returns:
            Broadcast result
        """
        try:
            tx_data = {
                "tx": tx_hex
            }
            
            return self.make_request('POST', 'txs/push', data=tx_data)
        except RequestException as e:
            raise Exception(f"Failed to broadcast transaction: {str(e)}")
    
    def get_transaction(self, tx_hash: str, include_confidence: bool = False) -> TransactionInfo:
        """
        Get information about a specific transaction.
        
        Args:
            tx_hash: Transaction hash/ID
            include_confidence: Whether to include confidence information for unconfirmed transactions
            
        Returns:
            Transaction information
        """
        try:
            params = {}
            if include_confidence:
                params['includeConfidence'] = 'true'
                
            return self.make_request('GET', f'txs/{tx_hash}', params=params)
        except RequestException as e:
            raise Exception(f"Failed to get transaction {tx_hash}: {str(e)}")
    
    def get_transaction_confidence(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get confidence information for an unconfirmed transaction.
        
        Args:
            tx_hash: Transaction hash/ID
            
        Returns:
            Transaction confidence information
        """
        try:
            return self.make_request('GET', f'txs/{tx_hash}/confidence')
        except RequestException as e:
            raise Exception(f"Failed to get transaction confidence for {tx_hash}: {str(e)}")
    
    def create_and_sign_transaction(
        self,
        from_address: str,
        to_address: str,
        amount_satoshis: int,
        private_key: str,
        fees: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Convenience method to create, sign and broadcast a transaction in one call.
        
        Args:
            from_address: Source address
            to_address: Destination address
            amount_satoshis: Amount to send in satoshis
            private_key: Private key for the source address
            fees: Optional explicit fee in satoshis
            **kwargs: Additional transaction parameters
            
        Returns:
            Broadcast transaction result
        """
        try:
            # Check balance
            balance_info = self.make_request('GET', f'addrs/{from_address}/balance')
            balance = balance_info.get('balance', 0)
            
            if balance < amount_satoshis:
                raise ValueError(f"Insufficient balance. Available: {balance}, Required: {amount_satoshis}")
            
            # Create transaction skeleton
            tx_data = {
                "inputs": [{"addresses": [from_address]}],
                "outputs": [{"addresses": [to_address], "value": amount_satoshis}]
            }
            
            if fees is not None:
                tx_data["fees"] = fees
                
            # Add any additional parameters
            tx_data.update(kwargs)
            
            tx_skeleton = self.make_request('POST', 'txs/new', data=tx_data)
            
            # Sign the transaction
            tx_signed = self.sign_transaction(tx_skeleton, [private_key])
            
            # Broadcast the transaction
            return self.broadcast_transaction(tx_signed.get('tx'))
        except RequestException as e:
            raise Exception(f"Failed to process transaction: {str(e)}")
    
    def get_transaction_confirmations(self, tx_hash: str) -> int:
        """
        Get the number of confirmations for a transaction.
        
        Args:
            tx_hash: Transaction hash/ID
            
        Returns:
            Number of confirmations
        """
        try:
            tx_info = self.get_transaction(tx_hash)
            return tx_info.get('confirmations', 0)
        except RequestException as e:
            raise Exception(f"Failed to get confirmations for {tx_hash}: {str(e)}")
    
    def wait_for_confirmation(
        self,
        tx_hash: str,
        required_confirmations: int = 6,
        timeout_seconds: int = 3600,
        check_interval_seconds: int = 30
    ) -> Dict[str, Any]:
        """
        Wait for a transaction to reach the required number of confirmations.
        
        Args:
            tx_hash: Transaction hash/ID
            required_confirmations: Number of confirmations to wait for
            timeout_seconds: Maximum time to wait in seconds
            check_interval_seconds: How often to check for confirmations
            
        Returns:
            Final transaction information or raises exception on timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            try:
                tx_info = self.get_transaction(tx_hash)
                confirmations = tx_info.get('confirmations', 0)
                
                if confirmations >= required_confirmations:
                    return tx_info
                    
                time.sleep(check_interval_seconds)
            except Exception as e:
                # Log error but continue waiting
                print(f"Error checking transaction status: {str(e)}")
                time.sleep(check_interval_seconds)
                
        raise TimeoutError(f"Transaction {tx_hash} did not reach {required_confirmations} confirmations within {timeout_seconds} seconds")
    
    def decode_raw_transaction(self, tx_hex: str) -> Dict[str, Any]:
        """
        Decode a raw transaction hex string.
        
        Args:
            tx_hex: Hex-encoded transaction
            
        Returns:
            Decoded transaction information
        """
        try:
            data = {
                "tx": tx_hex
            }
            
            return self.make_request('POST', 'txs/decode', data=data)
        except RequestException as e:
            raise Exception(f"Failed to decode transaction: {str(e)}")
    
    def get_address_transactions(self, address: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get transactions for a specific address.
        
        Args:
            address: The address to get transactions for
            limit: Maximum number of transactions to return
            
        Returns:
            List of transactions
        """
        try:
            params = {'limit': limit}
            result = self.make_request('GET', f'addrs/{address}', params=params)
            return result.get('txrefs', [])
        except RequestException as e:
            raise Exception(f"Failed to get transactions for address {address}: {str(e)}")
    
    def get_unconfirmed_transactions(self, address: str) -> List[Dict[str, Any]]:
        """
        Get unconfirmed transactions for a specific address.
        
        Args:
            address: The address to get unconfirmed transactions for
            
        Returns:
            List of unconfirmed transactions
        """
        try:
            result = self.make_request('GET', f'addrs/{address}')
            return result.get('unconfirmed_txrefs', [])
        except RequestException as e:
            raise Exception(f"Failed to get unconfirmed transactions for address {address}: {str(e)}")
            
    def get_transaction_fee_estimate(
        self,
        from_address: str,
        to_address: str,
        amount_satoshis: int
    ) -> int:
        """
        Estimate the fee for a transaction.
        
        Args:
            from_address: Source address
            to_address: Destination address
            amount_satoshis: Amount to send in satoshis
            
        Returns:
            Estimated fee in satoshis
        """
        try:
            # Create a skeleton transaction to get fee estimate
            tx_data = {
                "inputs": [{"addresses": [from_address]}],
                "outputs": [{"addresses": [to_address], "value": amount_satoshis}],
                "estimate_fee": True
            }
            
            result = self.make_request('POST', 'txs/new', data=tx_data)
            return result.get('fees', 0)
        except RequestException as e:
            raise Exception(f"Failed to estimate transaction fee: {str(e)}") 