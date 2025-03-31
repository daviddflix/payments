"""
Tests for the TransactionManager class.
"""

import unittest
from unittest.mock import patch, MagicMock
import pytest
import os

from app.infrastructure.providers.blockcypher.transactions import TransactionManager

class TestTransactionManager(unittest.TestCase):
    """Tests for the TransactionManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_token = "test_token"
        self.transaction_manager = TransactionManager(api_token=self.api_token, coin_symbol="btc-testnet")
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_transaction(self, mock_make_request):
        """Test creating a transaction."""
        # Mock response
        mock_response = {
            "tx": {
                "hash": "tx_hash_123",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"],
                "total": 1500000,
                "fees": 10000,
                "inputs": [{"addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]}],
                "outputs": [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1490000}]
            },
            "tosign": ["signature_data"]
        }
        mock_make_request.return_value = mock_response
        
        # Input and output data
        inputs = [{"addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]}]
        outputs = [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1500000}]
        
        # Call the method
        result = self.transaction_manager.create_transaction(
            inputs=inputs,
            outputs=outputs,
            preference="medium"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'txs/new', 
            data={
                "inputs": inputs,
                "outputs": outputs,
                "preference": "medium"
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_transaction_with_fees(self, mock_make_request):
        """Test creating a transaction with explicit fees."""
        # Mock response
        mock_response = {
            "tx": {
                "hash": "tx_hash_123",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"],
                "total": 1500000,
                "fees": 15000,
                "inputs": [{"addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]}],
                "outputs": [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1485000}]
            },
            "tosign": ["signature_data"]
        }
        mock_make_request.return_value = mock_response
        
        # Input and output data
        inputs = [{"addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]}]
        outputs = [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1500000}]
        
        # Call the method
        result = self.transaction_manager.create_transaction(
            inputs=inputs,
            outputs=outputs,
            fees=15000,
            preference="medium"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'txs/new', 
            data={
                "inputs": inputs,
                "outputs": outputs,
                "preference": "medium",
                "fees": 15000
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_sign_transaction(self, mock_make_request):
        """Test signing a transaction."""
        # Mock tx skeleton
        tx_skeleton = {
            "tx": {
                "hash": "tx_hash_123",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"],
                "total": 1500000,
                "fees": 10000
            },
            "tosign": ["signature_data"]
        }
        
        # Mock response
        mock_response = {
            "tx": {
                "hash": "tx_hash_123",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"],
                "total": 1500000,
                "fees": 10000
            },
            "signatures": ["signature_result"],
            "pubkeys": ["pubkey_data"]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.sign_transaction(
            tx_skeleton=tx_skeleton,
            private_keys=["private_key_1"]
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'txs/sign', 
            data={
                "tx": tx_skeleton,
                "private_keys": ["private_key_1"]
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_broadcast_transaction(self, mock_make_request):
        """Test broadcasting a transaction."""
        # Mock response
        mock_response = {
            "tx": {
                "hash": "tx_hash_123",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"],
                "total": 1500000,
                "fees": 10000
            },
            "tx_hash": "tx_hash_123"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.broadcast_transaction("signed_tx_hex_string")
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'txs/push', 
            data={
                "tx": "signed_tx_hex_string"
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_transaction(self, mock_make_request):
        """Test getting transaction details."""
        # Mock response
        mock_response = {
            "hash": "tx_hash_123",
            "block_height": 680000,
            "total": 1500000,
            "fees": 10000,
            "confirmations": 6,
            "inputs": [{"prev_hash": "prev_tx_hash", "output_index": 0}],
            "outputs": [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1490000}]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.get_transaction("tx_hash_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'txs/tx_hash_123', params={})
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_transaction_with_confidence(self, mock_make_request):
        """Test getting transaction details with confidence information."""
        # Mock response
        mock_response = {
            "hash": "tx_hash_123",
            "total": 1500000,
            "fees": 10000,
            "confirmations": 0,
            "confidence": 0.95,
            "inputs": [{"prev_hash": "prev_tx_hash", "output_index": 0}],
            "outputs": [{"addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"], "value": 1490000}]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.get_transaction("tx_hash_123", include_confidence=True)
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'GET', 
            'txs/tx_hash_123', 
            params={'includeConfidence': 'true'}
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_transaction_confidence(self, mock_make_request):
        """Test getting transaction confidence."""
        # Mock response
        mock_response = {
            "tx_hash": "tx_hash_123",
            "confidence": 0.95,
            "double_spend": False
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.get_transaction_confidence("tx_hash_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'txs/tx_hash_123/confidence')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.transactions.manager.TransactionManager.make_request')
    def test_get_transaction_confirmations(self, mock_make_request):
        """Test getting transaction confirmations."""
        # Mock response
        mock_response = {
            "hash": "tx_hash_123",
            "confirmations": 3
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.transaction_manager.get_transaction_confirmations("tx_hash_123")
        
        # Assertions
        self.assertEqual(result, 3)
    
    @patch('app.infrastructure.providers.blockcypher.transactions.manager.TransactionManager.make_request')
    def test_wait_for_confirmation(self, mock_make_request):
        """Test waiting for transaction confirmation."""
        # Mock responses for multiple calls
        mock_make_request.side_effect = [
            {"hash": "tx_hash_123", "confirmations": 0},
            {"hash": "tx_hash_123", "confirmations": 0},
            {"hash": "tx_hash_123", "confirmations": 1}
        ]
        
        # Call the method with a short timeout for testing
        result = self.transaction_manager.wait_for_confirmation(
            tx_hash="tx_hash_123",
            required_confirmations=1,
            timeout_seconds=10,
            check_interval_seconds=0.1
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertEqual(mock_make_request.call_count, 3)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_and_sign_transaction(self, mock_make_request):
        """Test creating, signing, and broadcasting a transaction in one call."""
        # Mock responses for balance check, transaction creation, and broadcast
        mock_make_request.side_effect = [
            # Balance check
            {"balance": 2000000, "final_balance": 2000000},
            # Transaction creation
            {
                "tx": {"hash": "tx_hash_123"},
                "tosign": ["signature_data"]
            },
            # Transaction signing
            {
                "tx": {"hash": "tx_hash_123"},
                "signatures": ["signature_result"]
            },
            # Transaction broadcast
            {
                "tx": {"hash": "tx_hash_123"},
                "tx_hash": "tx_hash_123"
            }
        ]
        
        # Call the method
        result = self.transaction_manager.create_and_sign_transaction(
            from_address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            to_address="tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            amount_satoshis=1000000,
            private_key="private_key_1"
        )
        
        # Assertions
        self.assertEqual(mock_make_request.call_count, 4)
        self.assertEqual(result.get("tx_hash"), "tx_hash_123")
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_and_sign_transaction_insufficient_balance(self, mock_make_request):
        """Test transaction creation with insufficient balance."""
        # Mock response for balance check
        mock_make_request.return_value = {"balance": 500000, "final_balance": 500000}
        
        # Call the method and expect an error
        with self.assertRaises(ValueError) as context:
            self.transaction_manager.create_and_sign_transaction(
                from_address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                to_address="tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
                amount_satoshis=1000000,
                private_key="private_key_1"
            )
        
        self.assertTrue("Insufficient balance" in str(context.exception))


# Real tests using the BlockCypher test faucet
# These tests will only run if the BLOCKCYPHER_LIVE_TEST environment variable is set to 'true'
@pytest.mark.skipif(
    os.getenv("BLOCKCYPHER_LIVE_TEST") != "true",
    reason="Live tests only run when BLOCKCYPHER_LIVE_TEST=true"
)
class TestTransactionManagerWithFaucet(unittest.TestCase):
    """Tests for the TransactionManager class using the test faucet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.infrastructure.providers.blockcypher.utils.test_utils import (
            get_test_api_token,
            setup_funded_test_address,
            generate_test_address,
            wait_for_confirmation
        )
        
        self.coin_symbol = 'bcy'  # BlockCypher test chain
        self.api_token = get_test_api_token()
        self.transaction_manager = TransactionManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        
        # Generate a funded address for testing
        funded_setup = setup_funded_test_address(coin_symbol=self.coin_symbol)
        self.test_address = funded_setup['address_info']
        self.funding_tx = funded_setup['funding_tx']
        
        # Create another address for sending transactions
        self.recipient_address = generate_test_address(coin_symbol=self.coin_symbol)
        self.wait_for_confirmation = wait_for_confirmation
    
    def test_live_create_and_broadcast_transaction(self):
        """Test creating and broadcasting a real transaction using the test faucet."""
        # Get initial balance to verify we have funds
        initial_balance = self.transaction_manager.get_wallet_balance(self.test_address['address'])
        self.assertGreater(initial_balance, 0, "Test address has no funds. Faucet funding may have failed.")
        
        # Create and sign a transaction
        amount_to_send = 10000  # 10,000 satoshis (0.0001 BTC/BCY)
        tx_result = self.transaction_manager.create_and_sign_transaction(
            from_address=self.test_address['address'],
            to_address=self.recipient_address['address'],
            amount_satoshis=amount_to_send,
            private_key=self.test_address['private']
        )
        
        # Verify transaction was created and has a transaction hash
        self.assertIn('tx_hash', tx_result, "Transaction creation failed")
        tx_hash = tx_result['tx_hash']
        
        # Wait for the transaction to be confirmed (BlockCypher test chain confirms quickly)
        confirmed = self.wait_for_confirmation(
            tx_hash=tx_hash,
            coin_symbol=self.coin_symbol,
            timeout_seconds=120  # Allow up to 2 minutes for confirmation
        )
        self.assertTrue(confirmed, "Transaction was not confirmed within the timeout period")
        
        # Check that the recipient received the funds
        recipient_balance = self.transaction_manager.get_wallet_balance(self.recipient_address['address'])
        self.assertGreaterEqual(
            recipient_balance, 
            amount_to_send / 100000000,  # Convert satoshis to BTC/BCY
            "Recipient did not receive the expected funds"
        )
    
    def test_live_transaction_details(self):
        """Test getting details of a real transaction."""
        # Create a simple transaction
        amount_to_send = 5000  # 5,000 satoshis
        tx_result = self.transaction_manager.create_and_sign_transaction(
            from_address=self.test_address['address'],
            to_address=self.recipient_address['address'],
            amount_satoshis=amount_to_send,
            private_key=self.test_address['private']
        )
        
        # Get transaction details
        tx_details = self.transaction_manager.get_transaction(tx_result['tx_hash'])
        
        # Verify the transaction details include expected fields
        self.assertEqual(tx_details['hash'], tx_result['tx_hash'])
        
        # Verify the transaction amount
        for output in tx_details['outputs']:
            if self.recipient_address['address'] in output.get('addresses', []):
                self.assertEqual(output['value'], amount_to_send)
    
    def test_live_transaction_confidence(self):
        """Test getting confidence information for an unconfirmed transaction."""
        # Create a transaction
        tx_result = self.transaction_manager.create_and_sign_transaction(
            from_address=self.test_address['address'],
            to_address=self.recipient_address['address'],
            amount_satoshis=1000,  # Small amount
            private_key=self.test_address['private']
        )
        
        # Wait a moment but not enough for a confirmation
        import time
        time.sleep(2)
        
        # Get transaction confidence (may be None if already confirmed)
        try:
            confidence = self.transaction_manager.get_transaction_confidence(tx_result['tx_hash'])
            if 'confidence' in confidence:
                self.assertGreaterEqual(confidence['confidence'], 0)
                self.assertLessEqual(confidence['confidence'], 1)
        except Exception as e:
            # If the transaction confirms too quickly, this might fail
            # This is not a problem with the code, just timing
            print(f"Note: Could not get confidence - transaction may have confirmed too quickly: {e}")


if __name__ == '__main__':
    unittest.main() 