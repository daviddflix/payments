"""
Tests for the WalletManager class.
"""

import unittest
from unittest.mock import patch, MagicMock
import pytest
import os

from app.infrastructure.providers.blockcypher.wallets import WalletManager

class TestWalletManager(unittest.TestCase):
    """Tests for the WalletManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_token = "test_token"
        self.wallet_manager = WalletManager(api_token=self.api_token, coin_symbol="btc-testnet")
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_wallet(self, mock_make_request):
        """Test creating a wallet."""
        # Mock response
        mock_response = {
            "name": "test_wallet",
            "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"],
            "token": "wallet_token_123",
            "wallet": {
                "token": "wallet_token_123",
                "name": "test_wallet",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
            }
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.create_wallet(
            name="test_wallet",
            addresses=["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'wallets', 
            data={
                "name": "test_wallet",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_wallet_with_multiple_addresses(self, mock_make_request):
        """Test creating a wallet with multiple addresses."""
        # Mock response
        mock_response = {
            "name": "multi-address-wallet",
            "addresses": [
                "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
            ],
            "token": self.api_token
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.create_wallet(
            addresses=[
                "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
            ],
            wallet_name="multi-address-wallet"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'wallets', 
            data={
                "name": "multi-address-wallet",
                "addresses": [
                    "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                    "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
                ]
            }
        )
        self.assertEqual(result, mock_response)
    
    def test_create_wallet_invalid_name(self):
        """Test creating a wallet with an invalid name."""
        # Test with name that's too long
        with self.assertRaises(ValueError) as context:
            self.wallet_manager.create_wallet(
                addresses="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                wallet_name="this-name-is-way-too-long-for-a-wallet-name"
            )
        
        self.assertTrue("Wallet name must be between 1-25 characters" in str(context.exception))
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_list_wallets(self, mock_make_request):
        """Test listing wallets."""
        # Mock response
        mock_response = [
            {
                "token": "wallet_token_123",
                "name": "test_wallet_1",
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
            },
            {
                "token": "wallet_token_456",
                "name": "test_wallet_2",
                "addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"]
            }
        ]
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.list_wallets()
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'wallets')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_wallet(self, mock_make_request):
        """Test getting a wallet."""
        # Mock response
        mock_response = {
            "token": "wallet_token_123",
            "name": "test_wallet",
            "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.get_wallet("wallet_token_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'wallets/wallet_token_123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_add_addresses_to_wallet(self, mock_make_request):
        """Test adding addresses to a wallet."""
        # Mock response
        mock_response = {
            "token": "wallet_token_123",
            "name": "test_wallet",
            "addresses": [
                "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
            ]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.add_addresses_to_wallet(
            wallet_name_or_id="wallet_token_123", 
            addresses=["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"]
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'wallets/wallet_token_123/addresses', 
            data={
                "addresses": ["tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"]
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_generate_address_for_wallet(self, mock_make_request):
        """Test generating an address for a wallet."""
        # Mock response
        mock_response = {
            "token": "wallet_token_123",
            "name": "test_wallet",
            "addresses": [
                "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "new_address_123"
            ],
            "private": "private_key_for_new_address",
            "public": "public_key_for_new_address",
            "address": "new_address_123"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.generate_address_for_wallet("wallet_token_123")
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'wallets/wallet_token_123/addresses/generate'
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_remove_address_from_wallet(self, mock_make_request):
        """Test removing an address from a wallet."""
        # Mock response
        mock_response = {
            "token": "wallet_token_123",
            "name": "test_wallet",
            "addresses": []
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.remove_address_from_wallet(
            wallet_name_or_id="wallet_token_123",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'DELETE', 
            'wallets/wallet_token_123/addresses',
            data={
                "addresses": ["tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"]
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_delete_wallet(self, mock_make_request):
        """Test deleting a wallet."""
        # Mock response
        mock_response = {
            "deleted": True
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.delete_wallet("wallet_token_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('DELETE', 'wallets/wallet_token_123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_wallet_transactions(self, mock_make_request):
        """Test getting wallet transactions."""
        # Mock response
        mock_response = {
            "total_count": 2,
            "txs": [
                {
                    "hash": "tx_hash_123",
                    "total": 1500000,
                    "fees": 10000,
                    "confirmations": 6
                },
                {
                    "hash": "tx_hash_456",
                    "total": 2000000,
                    "fees": 12000,
                    "confirmations": 3
                }
            ]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.get_wallet_transactions("wallet_token_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'wallets/wallet_token_123/txs')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_wallet_balance(self, mock_make_request):
        """Test getting wallet balance."""
        # Mock response
        mock_response = {
            "balance": 1500000,
            "final_balance": 1500000,
            "unconfirmed_balance": 0
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.get_wallet_balance("wallet_token_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'wallets/wallet_token_123/balance')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_address_balance(self, mock_make_request):
        """Test getting address balance."""
        # Mock response
        mock_response = {
            "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "balance": 1500000,
            "final_balance": 1500000,
            "unconfirmed_balance": 0
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.get_address_balance("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'addrs/tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx/balance')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_address_transactions(self, mock_make_request):
        """Test getting address transactions."""
        # Mock response
        mock_response = {
            "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "txs": [
                {
                    "hash": "tx_hash_123",
                    "total": 1500000,
                    "fees": 10000,
                    "confirmations": 6
                },
                {
                    "hash": "tx_hash_456",
                    "total": 2000000,
                    "fees": 12000,
                    "confirmations": 3
                }
            ]
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.wallet_manager.get_address_transactions("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'addrs/tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx')
        self.assertEqual(result, mock_response)


# Real tests using the BlockCypher test faucet
# These tests will only run if the BLOCKCYPHER_LIVE_TEST environment variable is set to 'true'
@pytest.mark.skipif(
    os.getenv("BLOCKCYPHER_LIVE_TEST") != "true", 
    reason="Live tests only run when BLOCKCYPHER_LIVE_TEST=true"
)
class TestWalletManagerWithFaucet(unittest.TestCase):
    """Tests for the WalletManager class using the test faucet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.infrastructure.providers.blockcypher.utils.test_utils import (
            get_test_api_token,
            setup_funded_test_address,
            generate_test_address,
            generate_random_wallet_name
        )
        
        self.coin_symbol = 'bcy'  # BlockCypher test chain
        self.api_token = get_test_api_token()
        self.wallet_manager = WalletManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        
        # Generate a funded address for testing
        funded_setup = setup_funded_test_address(coin_symbol=self.coin_symbol)
        self.test_address = funded_setup['address_info']
        self.funding_tx = funded_setup['funding_tx']
        
        # Generate a random wallet name for testing
        self.test_wallet_name = generate_random_wallet_name()
    
    def tearDown(self):
        """Clean up after tests."""
        # Try to delete the wallet if it exists
        try:
            wallet_info = self.wallet_manager.get_wallet(self.test_wallet_name)
            if wallet_info:
                self.wallet_manager.delete_wallet(self.test_wallet_name)
        except:
            pass  # Wallet might not exist, that's fine
    
    def test_live_create_and_get_wallet(self):
        """Test creating a wallet and retrieving it."""
        # Create a wallet with our funded test address
        wallet_response = self.wallet_manager.create_wallet(
            name=self.test_wallet_name,
            addresses=[self.test_address['address']]
        )
        
        self.assertEqual(wallet_response['name'], self.test_wallet_name)
        self.assertIn(self.test_address['address'], wallet_response['addresses'])
        
        # Get the wallet we just created
        wallet_info = self.wallet_manager.get_wallet(self.test_wallet_name)
        self.assertEqual(wallet_info['name'], self.test_wallet_name)
        self.assertIn(self.test_address['address'], wallet_info['addresses'])
    
    def test_live_wallet_balance(self):
        """Test retrieving a wallet's balance."""
        # Create a wallet with our funded test address
        wallet_response = self.wallet_manager.create_wallet(
            name=self.test_wallet_name,
            addresses=[self.test_address['address']]
        )
        
        # Get the wallet balance
        balance_info = self.wallet_manager.get_wallet_balance(self.test_wallet_name)
        
        # Verify we have a balance (should be funded from the test faucet)
        self.assertIsNotNone(balance_info['balance'])
        self.assertGreater(balance_info['balance'], 0)
    
    def test_live_generate_address_for_wallet(self):
        """Test generating a new address for a wallet."""
        # Create a wallet
        wallet_response = self.wallet_manager.create_wallet(
            name=self.test_wallet_name,
            addresses=[]  # Start with empty wallet
        )
        
        # Generate a new address for the wallet
        address_response = self.wallet_manager.generate_address_for_wallet(self.test_wallet_name)
        
        # Verify the address was generated
        self.assertIn('address', address_response)
        self.assertIn('private', address_response)
        
        # Get the wallet to confirm the address was added
        wallet_info = self.wallet_manager.get_wallet(self.test_wallet_name)
        self.assertIn(address_response['address'], wallet_info['addresses'])
    
    def test_live_add_and_remove_address(self):
        """Test adding and removing addresses from a wallet."""
        # Create a wallet
        wallet_response = self.wallet_manager.create_wallet(
            name=self.test_wallet_name,
            addresses=[]  # Start with empty wallet
        )
        
        # Add our test address to the wallet
        updated_wallet = self.wallet_manager.add_addresses_to_wallet(
            wallet_name_or_id=self.test_wallet_name,
            addresses=[self.test_address['address']]
        )
        
        # Verify the address was added
        self.assertIn(self.test_address['address'], updated_wallet['addresses'])
        
        # Remove the address
        removed_wallet = self.wallet_manager.remove_address_from_wallet(
            wallet_name_or_id=self.test_wallet_name,
            address=self.test_address['address']
        )
        
        # Verify the address was removed
        self.assertNotIn(self.test_address['address'], removed_wallet['addresses'])
    
    def test_live_wallet_transactions(self):
        """Test getting transactions for a wallet with a funded address."""
        # Create a wallet with our funded test address
        wallet_response = self.wallet_manager.create_wallet(
            name=self.test_wallet_name,
            addresses=[self.test_address['address']]
        )
        
        # Get the wallet transactions
        transactions = self.wallet_manager.get_wallet_transactions(self.test_wallet_name)
        
        # We should have at least one transaction (the funding transaction)
        self.assertGreater(transactions['total_count'], 0)
        self.assertGreaterEqual(len(transactions['txs']), 1)
        
        # One of the transactions should be our funding transaction
        tx_hashes = [tx['hash'] for tx in transactions['txs']]
        self.assertIn(self.funding_tx['tx_hash'], tx_hashes)


if __name__ == '__main__':
    unittest.main() 