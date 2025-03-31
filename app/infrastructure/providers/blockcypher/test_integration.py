"""
Integration tests for BlockCypher API.

These tests interact with the actual BlockCypher API using the bcy test chain.
They require a valid BlockCypher API token set via the BLOCKCYPHER_API_TOKEN environment variable.

To run these tests:
    1. Set the BLOCKCYPHER_API_TOKEN environment variable
    2. Run pytest with the --integration flag: pytest test_integration.py -v --integration

Note: These tests use the test faucet, which has rate limits. Running them frequently 
may result in errors due to reaching these limits.
"""

import unittest
import os
import pytest
import time
from typing import Dict, Any

from app.infrastructure.providers.blockcypher.utils.test_utils import (
    get_test_api_token,
    generate_test_address,
    fund_test_address,
    generate_random_wallet_name,
    setup_funded_test_address,
    wait_for_confirmation
)

from app.infrastructure.providers.blockcypher.wallets import WalletManager
from app.infrastructure.providers.blockcypher.transactions import TransactionManager
from app.infrastructure.providers.blockcypher.forwarding import ForwardingManager
from app.infrastructure.providers.blockcypher.blockchain import BlockchainService

# Skip these tests unless the BLOCKCYPHER_LIVE_TEST environment variable is set to 'true'
@pytest.mark.skipif(
    os.getenv("BLOCKCYPHER_LIVE_TEST") != "true",
    reason="Integration tests only run when BLOCKCYPHER_LIVE_TEST=true"
)
class TestBlockCypherIntegration(unittest.TestCase):
    """Integration tests for BlockCypher API."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_token = get_test_api_token()
        self.coin_symbol = 'bcy'  # BlockCypher test chain
        
        # Initialize managers
        self.wallet_manager = WalletManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        self.tx_manager = TransactionManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        self.forwarding_manager = ForwardingManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        self.blockchain_service = BlockchainService(api_token=self.api_token, coin_symbol=self.coin_symbol)
        
        # Generate a funded address for testing
        funded_setup = setup_funded_test_address(coin_symbol=self.coin_symbol)
        self.test_address = funded_setup['address_info']
        self.funding_tx = funded_setup['funding_tx']
        
        # Create another address for sending transactions
        self.recipient_address = generate_test_address(coin_symbol=self.coin_symbol)
    
    def test_wallet_operations(self):
        """Test wallet creation and management."""
        # Generate a random wallet name
        wallet_name = generate_random_wallet_name()
        
        # Create a wallet
        wallet = self.wallet_manager.create_wallet(
            name=wallet_name,
            addresses=[self.test_address['address']]
        )
        
        # Verify wallet was created
        self.assertEqual(wallet['name'], wallet_name)
        self.assertIn(self.test_address['address'], wallet['addresses'])
        
        # Get wallet balance
        balance = self.wallet_manager.get_wallet_balance(wallet_name)
        self.assertGreater(balance['balance'], 0)
        
        # Get wallet details
        wallet_info = self.wallet_manager.get_wallet(wallet_name)
        self.assertEqual(wallet_info['name'], wallet_name)
        
        # Clean up - delete wallet
        deleted = self.wallet_manager.delete_wallet(wallet_name)
        self.assertTrue(deleted['deleted'])
    
    def test_transaction_operations(self):
        """Test transaction creation and querying."""
        # Create a transaction
        amount_to_send = 10000  # 10,000 satoshis
        tx_result = self.tx_manager.create_and_sign_transaction(
            from_address=self.test_address['address'],
            to_address=self.recipient_address['address'],
            amount_satoshis=amount_to_send,
            private_key=self.test_address['private']
        )
        
        # Verify transaction was created
        self.assertIn('tx_hash', tx_result)
        
        # Wait for the transaction to be included in a block
        confirmed = wait_for_confirmation(
            tx_hash=tx_result['tx_hash'],
            coin_symbol=self.coin_symbol,
            target_confirmations=1
        )
        self.assertTrue(confirmed)
        
        # Get transaction details
        tx_details = self.tx_manager.get_transaction(tx_result['tx_hash'])
        self.assertEqual(tx_details['hash'], tx_result['tx_hash'])
        self.assertGreaterEqual(tx_details['confirmations'], 1)
    
    def test_forwarding_operations(self):
        """Test address forwarding and webhooks."""
        # Create a forwarding address
        forwarding = self.forwarding_manager.create_forwarding_address(
            destination=self.recipient_address['address']
        )
        
        # Verify forwarding was created
        self.assertIn('input_address', forwarding)
        self.assertEqual(forwarding['destination'], self.recipient_address['address'])
        
        # Get the list of forwarding addresses
        forwards = self.forwarding_manager.list_forwarding_addresses()
        self.assertGreater(len(forwards), 0)
        
        # Delete the forwarding address
        result = self.forwarding_manager.delete_forwarding_address(forwarding['id'])
        self.assertTrue(result.get('deleted', False))
    
    def test_blockchain_operations(self):
        """Test blockchain information retrieval."""
        # Get the latest block height
        height = self.blockchain_service.get_latest_block_height()
        self.assertGreater(height, 0)
        
        # Get fee estimates
        fees = self.blockchain_service.get_fee_estimates()
        self.assertIn('high_fee_per_kb', fees)
        self.assertIn('medium_fee_per_kb', fees)
        self.assertIn('low_fee_per_kb', fees)
        
        # Get block details
        block = self.blockchain_service.get_block_details(height - 1)
        self.assertEqual(block['height'], height - 1)
        self.assertIn('hash', block)


# Define a pytest plugin hook to add the integration option
def pytest_addoption(parser):
    """Add integration option to pytest."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )


if __name__ == '__main__':
    unittest.main() 