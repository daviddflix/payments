"""
Tests for the BlockchainService class.
"""

import unittest
from unittest.mock import patch, MagicMock
import warnings

from app.infrastructure.providers.blockcypher.blockchain import BlockchainService

class TestBlockchainService(unittest.TestCase):
    """Tests for the BlockchainService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_token = "test_token"
        self.blockchain_service = BlockchainService(api_token=self.api_token, coin_symbol="btc-testnet")
    
    @patch('blockcypher.get_latest_block_height')
    def test_get_latest_block_height(self, mock_get_latest_block_height):
        """Test getting the latest block height."""
        # Mock response
        mock_get_latest_block_height.return_value = 680000
        
        # Call the method
        result = self.blockchain_service.get_latest_block_height()
        
        # Assertions
        mock_get_latest_block_height.assert_called_once_with(coin_symbol="btc-testnet")
        self.assertEqual(result, 680000)
    
    @patch('blockcypher.get_block_details')
    def test_get_block_details(self, mock_get_block_details):
        """Test getting block details."""
        # Mock response
        mock_response = {
            "hash": "000000000000000000071bc8d13abe4b242163c099a8e36600a84f51424e2aef",
            "height": 680000,
            "time": "2021-04-01T01:23:45Z",
            "n_tx": 1000,
            "total": 1000000000,
            "fees": 500000,
            "size": 1000000,
            "ver": 1,
            "prev_block": "000000000000000000071bc8d13abe4b242163c099a8e36600a84f5142410abc",
            "mrkl_root": "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b",
            "txids": ["tx1", "tx2", "tx3"]
        }
        mock_get_block_details.return_value = mock_response
        
        # Call the method
        result = self.blockchain_service.get_block_details(680000)
        
        # Assertions
        mock_get_block_details.assert_called_once_with(680000, coin_symbol="btc-testnet")
        self.assertEqual(result["hash"], mock_response["hash"])
        self.assertEqual(result["height"], mock_response["height"])
        self.assertEqual(result["time"], mock_response["time"])
        self.assertEqual(result["n_tx"], mock_response["n_tx"])
        self.assertEqual(result["total"], mock_response["total"])
        self.assertEqual(result["fees"], mock_response["fees"])
        self.assertEqual(result["size"], mock_response["size"])
        self.assertEqual(result["ver"], mock_response["ver"])
        self.assertEqual(result["prev_block"], mock_response["prev_block"])
        self.assertEqual(result["mrkl_root"], mock_response["mrkl_root"])
        self.assertEqual(result["txids"], mock_response["txids"])
    
    @patch('blockcypher.get_block_overview')
    def test_get_block_overview(self, mock_get_block_overview):
        """Test getting block overview."""
        # Mock response
        mock_response = {
            "hash": "000000000000000000071bc8d13abe4b242163c099a8e36600a84f51424e2aef",
            "height": 680000,
            "time": "2021-04-01T01:23:45Z",
            "n_tx": 1000
        }
        mock_get_block_overview.return_value = mock_response
        
        # Call the method
        result = self.blockchain_service.get_block_overview(680000)
        
        # Assertions
        mock_get_block_overview.assert_called_once_with(680000, coin_symbol="btc-testnet")
        self.assertEqual(result, mock_response)
    
    @patch('blockcypher.get_blockchain_overview')
    def test_get_network_info(self, mock_get_blockchain_overview):
        """Test getting network information."""
        # Mock response
        mock_response = {
            "name": "BTC.test3",
            "height": 680000,
            "hash": "000000000000000000071bc8d13abe4b242163c099a8e36600a84f51424e2aef",
            "time": "2021-04-01T01:23:45Z",
            "latest_url": "https://api.blockcypher.com/v1/btc/test3/blocks/000000000000000000071bc8d13abe4b242163c099a8e36600a84f51424e2aef",
            "previous_hash": "000000000000000000071bc8d13abe4b242163c099a8e36600a84f5142410abc",
            "previous_url": "https://api.blockcypher.com/v1/btc/test3/blocks/000000000000000000071bc8d13abe4b242163c099a8e36600a84f5142410abc",
            "peer_count": 100,
            "unconfirmed_count": 1000,
            "high_fee_per_kb": 50000,
            "medium_fee_per_kb": 25000,
            "low_fee_per_kb": 10000
        }
        mock_get_blockchain_overview.return_value = mock_response
        
        # Call the method
        result = self.blockchain_service.get_network_info()
        
        # Assertions
        mock_get_blockchain_overview.assert_called_once_with(coin_symbol="btc-testnet")
        self.assertEqual(result, mock_response)
    
    @patch('blockcypher.get_blockchain_overview')
    def test_get_fee_estimates(self, mock_get_blockchain_overview):
        """Test getting fee estimates."""
        # Mock response
        mock_response = {
            "high_fee_per_kb": 50000,
            "medium_fee_per_kb": 25000,
            "low_fee_per_kb": 10000
        }
        mock_get_blockchain_overview.return_value = mock_response
        
        # Call the method
        result = self.blockchain_service.get_fee_estimates()
        
        # Assertions
        mock_get_blockchain_overview.assert_called_once_with(coin_symbol="btc-testnet")
        self.assertEqual(result["high_fee_per_kb"], mock_response["high_fee_per_kb"])
        self.assertEqual(result["medium_fee_per_kb"], mock_response["medium_fee_per_kb"])
        self.assertEqual(result["low_fee_per_kb"], mock_response["low_fee_per_kb"])
    
    @patch('app.infrastructure.providers.blockcypher.wallets.WalletManager.get_wallet_balance')
    def test_get_address_balance_deprecation(self, mock_get_wallet_balance):
        """Test that the get_address_balance method is deprecated and calls the appropriate method."""
        # Mock response
        mock_get_wallet_balance.return_value = 0.05
        
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            # Call the method
            result = self.blockchain_service.get_address_balance("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
            
            # Check that a deprecation warning was issued
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Use WalletManager.get_wallet_balance() instead", str(w[0].message))
        
        # Assertions
        mock_get_wallet_balance.assert_called_once()
        self.assertEqual(result, 0.05)
    
    @patch('app.infrastructure.providers.blockcypher.wallets.WalletManager.get_wallet_details')
    def test_get_address_details_deprecation(self, mock_get_wallet_details):
        """Test that the get_address_details method is deprecated and calls the appropriate method."""
        # Mock response
        mock_response = {
            "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "balance": 5000000,
            "total_received": 10000000,
            "total_sent": 5000000,
            "n_tx": 10,
            "unconfirmed_balance": 0,
            "final_balance": 5000000
        }
        mock_get_wallet_details.return_value = mock_response
        
        # Capture warnings
        with warnings.catch_warnings(record=True) as w:
            # Call the method
            result = self.blockchain_service.get_address_details("tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx")
            
            # Check that a deprecation warning was issued
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Use WalletManager.get_wallet_details() instead", str(w[0].message))
        
        # Assertions
        mock_get_wallet_details.assert_called_once()
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main() 