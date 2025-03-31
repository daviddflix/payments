"""
Transaction validation for BlockCypher API integration.

This module provides functionality for validating cryptocurrency transactions.
"""

from typing import Dict, Any, List, Optional, Tuple, Set
from requests.exceptions import RequestException

from app.infrastructure.providers.blockcypher.common.base import BlockCypherProvider
from app.infrastructure.providers.blockcypher.common.types import (
    TransactionHash, Address
)

class TransactionValidator(BlockCypherProvider):
    """
    Validator for blockchain transactions through the BlockCypher API.
    
    This class provides methods for validating transaction data and status.
    """
    
    def is_valid_transaction_hash(self, tx_hash: str) -> bool:
        """
        Check if a transaction hash is valid for the current blockchain.
        
        Args:
            tx_hash: Transaction hash to validate
            
        Returns:
            True if the transaction exists, False otherwise
        """
        try:
            self.make_request('GET', f'txs/{tx_hash}')
            return True
        except Exception:
            return False
    
    def is_valid_address(self, address: str) -> bool:
        """
        Check if an address is valid for the current blockchain.
        
        Args:
            address: Address to validate
            
        Returns:
            True if the address is valid, False otherwise
        """
        try:
            validation_info = self.make_request('GET', f'addrs/{address}/validate')
            return validation_info.get('valid', False)
        except Exception:
            return False
    
    def is_confirmed_transaction(self, tx_hash: str, min_confirmations: int = 6) -> bool:
        """
        Check if a transaction has the required number of confirmations.
        
        Args:
            tx_hash: Transaction hash to check
            min_confirmations: Minimum number of confirmations required
            
        Returns:
            True if the transaction has required confirmations, False otherwise
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            return tx_info.get('confirmations', 0) >= min_confirmations
        except Exception:
            return False
    
    def is_double_spend(self, tx_hash: str) -> bool:
        """
        Check if a transaction is a double spend.
        
        Args:
            tx_hash: Transaction hash to check
            
        Returns:
            True if the transaction is a double spend, False otherwise
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            return tx_info.get('double_spend', False)
        except Exception:
            return False
    
    def get_transaction_status(self, tx_hash: str) -> Dict[str, Any]:
        """
        Get comprehensive status information about a transaction.
        
        Args:
            tx_hash: Transaction hash to check
            
        Returns:
            Dictionary with status information
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            confirmations = tx_info.get('confirmations', 0)
            
            status = {
                'exists': True,
                'confirmed': confirmations > 0,
                'confirmations': confirmations,
                'double_spend': tx_info.get('double_spend', False),
                'receive_count': tx_info.get('receive_count', 0),
                'block_height': tx_info.get('block_height', None),
                'confidence': tx_info.get('confidence', None),
                'status': 'confirmed' if confirmations > 0 else 'unconfirmed'
            }
            
            # Check if it's potentially a double spend
            if tx_info.get('double_of'):
                status['status'] = 'double_spend'
                status['double_of'] = tx_info.get('double_of')
                
            return status
        except Exception as e:
            return {
                'exists': False,
                'error': str(e),
                'status': 'unknown'
            }
    
    def verify_transaction_amount(
        self,
        tx_hash: str,
        expected_amount: int,
        recipient_address: str
    ) -> bool:
        """
        Verify if a transaction sent the expected amount to a specific address.
        
        Args:
            tx_hash: Transaction hash to check
            expected_amount: Expected amount in satoshis
            recipient_address: Expected recipient address
            
        Returns:
            True if the transaction matches the expected parameters
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            # Check all outputs for matching address and amount
            for output in tx_info.get('outputs', []):
                # Check if this output is for our recipient
                if recipient_address in output.get('addresses', []):
                    # Check the amount
                    if output.get('value') == expected_amount:
                        return True
            
            return False
        except Exception:
            return False
    
    def verify_transaction_sender(
        self,
        tx_hash: str,
        expected_sender_address: str
    ) -> bool:
        """
        Verify if a transaction was sent from a specific address.
        
        Args:
            tx_hash: Transaction hash to check
            expected_sender_address: Expected sender address
            
        Returns:
            True if the transaction was sent from the expected address
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            # Check all inputs for matching address
            for input_data in tx_info.get('inputs', []):
                # Check if this input is from our sender
                if expected_sender_address in input_data.get('addresses', []):
                    return True
            
            return False
        except Exception:
            return False
    
    def get_confidence(self, tx_hash: str) -> float:
        """
        Get the confidence score for an unconfirmed transaction.
        
        Args:
            tx_hash: Transaction hash to check
            
        Returns:
            Confidence score (0-1) or 1.0 for confirmed transactions
        """
        try:
            # First check if the transaction is confirmed
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            # If confirmed, confidence is 1.0
            if tx_info.get('confirmations', 0) > 0:
                return 1.0
                
            # Otherwise get the confidence information
            confidence_info = self.make_request('GET', f'txs/{tx_hash}/confidence')
            return confidence_info.get('confidence', 0.0)
        except Exception:
            return 0.0
    
    def is_transaction_to_address(
        self,
        tx_hash: str,
        address: str
    ) -> bool:
        """
        Check if a transaction sends any amount to a specific address.
        
        Args:
            tx_hash: Transaction hash to check
            address: Address to check for
            
        Returns:
            True if the address is a recipient in the transaction
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            # Check all outputs for the address
            for output in tx_info.get('outputs', []):
                if address in output.get('addresses', []):
                    return True
                    
            return False
        except Exception:
            return False
    
    def is_transaction_from_address(
        self,
        tx_hash: str,
        address: str
    ) -> bool:
        """
        Check if a transaction was sent from a specific address.
        
        Args:
            tx_hash: Transaction hash to check
            address: Address to check for
            
        Returns:
            True if the address is a sender in the transaction
        """
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            
            # Check all inputs for the address
            for input_data in tx_info.get('inputs', []):
                if address in input_data.get('addresses', []):
                    return True
                    
            return False
        except Exception:
            return False
    
    def verify_complex_transaction(
        self,
        tx_hash: str,
        sender_addresses: Optional[List[str]] = None,
        recipient_addresses: Optional[List[str]] = None,
        expected_amounts: Optional[Dict[str, int]] = None,
        min_confirmations: int = 0
    ) -> Dict[str, Any]:
        """
        Perform comprehensive verification of a transaction.
        
        Args:
            tx_hash: Transaction hash to check
            sender_addresses: Optional list of expected sender addresses
            recipient_addresses: Optional list of expected recipient addresses
            expected_amounts: Optional dict mapping recipient addresses to expected amounts
            min_confirmations: Minimum confirmations required
            
        Returns:
            Dictionary with verification results
        """
        result = {
            'valid': False,
            'exists': False,
            'sender_match': None,
            'recipient_match': None,
            'amount_match': None,
            'confirmation_match': None,
            'details': {}
        }
        
        try:
            tx_info = self.make_request('GET', f'txs/{tx_hash}')
            result['exists'] = True
            result['details'] = tx_info
            
            # Check confirmations
            confirmations = tx_info.get('confirmations', 0)
            result['confirmation_match'] = confirmations >= min_confirmations
            
            # Extract transaction addresses
            tx_senders = set()
            for input_data in tx_info.get('inputs', []):
                tx_senders.update(input_data.get('addresses', []))
            
            tx_recipients = {}
            for output in tx_info.get('outputs', []):
                for addr in output.get('addresses', []):
                    tx_recipients[addr] = output.get('value', 0)
            
            # Check senders if specified
            if sender_addresses:
                result['sender_match'] = all(addr in tx_senders for addr in sender_addresses)
            
            # Check recipients if specified
            if recipient_addresses:
                result['recipient_match'] = all(addr in tx_recipients for addr in recipient_addresses)
            
            # Check amounts if specified
            if expected_amounts:
                amount_matches = True
                for addr, amount in expected_amounts.items():
                    if addr not in tx_recipients or tx_recipients[addr] != amount:
                        amount_matches = False
                        break
                result['amount_match'] = amount_matches
            
            # Overall validation result
            checks = [
                result['confirmation_match'],
                result['sender_match'] if sender_addresses else True,
                result['recipient_match'] if recipient_addresses else True,
                result['amount_match'] if expected_amounts else True
            ]
            
            result['valid'] = all(c for c in checks if c is not None)
            
            return result
        except Exception as e:
            result['error'] = str(e)
            return result 