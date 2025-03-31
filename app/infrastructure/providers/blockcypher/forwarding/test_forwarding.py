"""
Tests for the ForwardingManager class.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from app.infrastructure.providers.blockcypher.forwarding import ForwardingManager

class TestForwardingManager(unittest.TestCase):
    """Tests for the ForwardingManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_token = "test_token"
        self.forwarding_manager = ForwardingManager(api_token=self.api_token, coin_symbol="btc-testnet")
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_forwarding_address(self, mock_make_request):
        """Test creating a forwarding address."""
        # Mock response
        mock_response = {
            "id": "payment123",
            "token": self.api_token,
            "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "input_address": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            "process_fees_satoshis": 0,
            "forward_callback_url": None
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_forwarding_address(
            destination="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'payments', 
            data={
                "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_forwarding_address_with_fee(self, mock_make_request):
        """Test creating a forwarding address with processing fee."""
        # Mock response
        mock_response = {
            "id": "payment123",
            "token": self.api_token,
            "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "input_address": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            "process_fees_satoshis": 1000,
            "forward_callback_url": "https://example.com/callback"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_forwarding_address(
            destination="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            callback_url="https://example.com/callback",
            process_fees_satoshis=1000
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'payments', 
            data={
                "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "callback_url": "https://example.com/callback",
                "process_fees_satoshis": 1000
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_list_forwarding_addresses(self, mock_make_request):
        """Test listing forwarding addresses."""
        # Mock response
        mock_response = [
            {
                "id": "payment123",
                "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "input_address": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
            },
            {
                "id": "payment456",
                "destination": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzs2",
                "input_address": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzs2"
            }
        ]
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.list_forwarding_addresses()
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'payments')
        self.assertEqual(result, mock_response)
        self.assertEqual(len(result), 2)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_delete_forwarding_address(self, mock_make_request):
        """Test deleting a forwarding address."""
        # Mock response
        mock_response = {"deleted": True}
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.delete_forwarding_address("payment123")
        
        # Assertions
        mock_make_request.assert_called_once_with('DELETE', 'payments/payment123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_webhook(self, mock_make_request):
        """Test creating a webhook."""
        # Mock response
        mock_response = {
            "id": "hook123",
            "token": self.api_token,
            "url": "https://example.com/webhook",
            "event": "unconfirmed-tx",
            "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_webhook(
            url="https://example.com/webhook",
            event="unconfirmed-tx",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'hooks', 
            data={
                "url": "https://example.com/webhook",
                "event": "unconfirmed-tx",
                "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
            }
        )
        self.assertEqual(result, mock_response)
    
    def test_create_webhook_invalid_event(self):
        """Test creating a webhook with invalid event type."""
        with self.assertRaises(ValueError) as context:
            self.forwarding_manager.create_webhook(
                url="https://example.com/webhook",
                event="invalid-event",
                address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
            )
        
        self.assertTrue("Invalid event type" in str(context.exception))
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_list_webhooks(self, mock_make_request):
        """Test listing webhooks."""
        # Mock response
        mock_response = [
            {
                "id": "hook123",
                "url": "https://example.com/webhook1",
                "event": "unconfirmed-tx"
            },
            {
                "id": "hook456",
                "url": "https://example.com/webhook2",
                "event": "tx-confirmation"
            }
        ]
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.list_webhooks()
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'hooks')
        self.assertEqual(result, mock_response)
        self.assertEqual(len(result), 2)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_webhook(self, mock_make_request):
        """Test getting a webhook by ID."""
        # Mock response
        mock_response = {
            "id": "hook123",
            "url": "https://example.com/webhook",
            "event": "unconfirmed-tx"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.get_webhook("hook123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'hooks/hook123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_delete_webhook(self, mock_make_request):
        """Test deleting a webhook."""
        # Mock response
        mock_response = {"deleted": True}
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.delete_webhook("hook123")
        
        # Assertions
        mock_make_request.assert_called_once_with('DELETE', 'hooks/hook123')
        self.assertEqual(result, mock_response)
    
    def test_get_websocket_url(self):
        """Test getting websocket URL."""
        # Call the method
        result = self.forwarding_manager.get_websocket_url()
        
        # Assertions
        self.assertEqual(result, "wss://api.blockcypher.com/v1/btc-testnet/ws")
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_address_webhook(self, mock_create_webhook):
        """Test creating an address webhook."""
        # Mock response
        mock_response = {"id": "hook123"}
        mock_create_webhook.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_address_webhook(
            url="https://example.com/webhook",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="unconfirmed-tx",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_transaction_webhook(self, mock_create_webhook):
        """Test creating a transaction webhook."""
        # Mock response
        mock_response = {"id": "hook123"}
        mock_create_webhook.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_transaction_webhook(
            url="https://example.com/webhook",
            transaction="abc123",
            confirmations=3
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="tx-confirmation",
            transaction="abc123",
            confirmations=3
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_confidence_webhook(self, mock_create_webhook):
        """Test creating a confidence webhook."""
        # Mock response
        mock_response = {"id": "hook123"}
        mock_create_webhook.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_confidence_webhook(
            url="https://example.com/webhook",
            transaction="abc123",
            confidence=0.95
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="tx-confidence",
            transaction="abc123",
            confidence=0.95
        )
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main() 