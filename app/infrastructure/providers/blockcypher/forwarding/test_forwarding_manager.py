"""
Tests for the ForwardingManager class.
"""

import unittest
from unittest.mock import patch, MagicMock
import pytest
import os

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
            "id": "forwarding_id_123",
            "token": "test_token",
            "input_address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            "callback_url": "https://example.com/callback",
            "transaction_url": "https://example.com/tx"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_forwarding_address(
            destination="tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            callback_url="https://example.com/callback",
            transaction_url="https://example.com/tx"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'payments', 
            data={
                "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
                "callback_url": "https://example.com/callback",
                "transaction_url": "https://example.com/tx"
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_forwarding_address_with_fee(self, mock_make_request):
        """Test creating a forwarding address with a processing fee."""
        # Mock response
        mock_response = {
            "id": "forwarding_id_123",
            "token": "test_token",
            "input_address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            "callback_url": "https://example.com/callback",
            "transaction_url": "https://example.com/tx",
            "processing_fees": {
                "satoshis": 10000
            }
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_forwarding_address(
            destination="tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
            callback_url="https://example.com/callback",
            transaction_url="https://example.com/tx",
            processing_fee_satoshis=10000
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'payments', 
            data={
                "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx",
                "callback_url": "https://example.com/callback",
                "transaction_url": "https://example.com/tx",
                "processing_fees": {
                    "satoshis": 10000
                }
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_list_forwarding_addresses(self, mock_make_request):
        """Test listing forwarding addresses."""
        # Mock response
        mock_response = [
            {
                "id": "forwarding_id_123",
                "input_address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
                "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
            },
            {
                "id": "forwarding_id_456",
                "input_address": "tb1qnkrer6qnrqdznq0207z2rf2vh3zg0n92j9thsk",
                "destination": "tb1qejxtdg4y5r3zarvary0c5xw7kx508d6q3jzsx"
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
        result = self.forwarding_manager.delete_forwarding_address("forwarding_id_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('DELETE', 'payments/forwarding_id_123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_webhook(self, mock_make_request):
        """Test creating a webhook."""
        # Mock response
        mock_response = {
            "id": "webhook_id_123",
            "token": "test_token",
            "url": "https://example.com/webhook",
            "event": "confirmed-tx"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.create_webhook(
            url="https://example.com/webhook",
            event="confirmed-tx"
        )
        
        # Assertions
        mock_make_request.assert_called_once_with(
            'POST', 
            'hooks', 
            data={
                "url": "https://example.com/webhook",
                "event": "confirmed-tx"
            }
        )
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_create_webhook_invalid_event(self, mock_make_request):
        """Test creating a webhook with an invalid event type."""
        # Call the method with an invalid event type
        with self.assertRaises(ValueError) as context:
            self.forwarding_manager.create_webhook(
                url="https://example.com/webhook",
                event="invalid-event"
            )
        
        # Verify error message
        self.assertTrue("not a valid event type" in str(context.exception))
        
        # Verify no request was made
        mock_make_request.assert_not_called()
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_list_webhooks(self, mock_make_request):
        """Test listing webhooks."""
        # Mock response
        mock_response = [
            {
                "id": "webhook_id_123",
                "url": "https://example.com/webhook1",
                "event": "confirmed-tx"
            },
            {
                "id": "webhook_id_456",
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
        """Test getting a webhook."""
        # Mock response
        mock_response = {
            "id": "webhook_id_123",
            "url": "https://example.com/webhook",
            "event": "confirmed-tx"
        }
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.get_webhook("webhook_id_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('GET', 'hooks/webhook_id_123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_delete_webhook(self, mock_make_request):
        """Test deleting a webhook."""
        # Mock response
        mock_response = {"deleted": True}
        mock_make_request.return_value = mock_response
        
        # Call the method
        result = self.forwarding_manager.delete_webhook("webhook_id_123")
        
        # Assertions
        mock_make_request.assert_called_once_with('DELETE', 'hooks/webhook_id_123')
        self.assertEqual(result, mock_response)
    
    @patch('app.infrastructure.providers.blockcypher.common.base.BlockCypherProvider.make_request')
    def test_get_websocket_url(self, mock_make_request):
        """Test getting a WebSocket URL."""
        # Call the method
        result = self.forwarding_manager.get_websocket_url()
        
        # Assertions
        self.assertTrue(result.startswith("wss://socket.blockcypher.com/v1/btc/test3?token="))
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_address_webhook(self, mock_create_webhook):
        """Test creating a webhook for an address."""
        # Mock response
        mock_create_webhook.return_value = {
            "id": "webhook_id_123",
            "url": "https://example.com/webhook",
            "event": "unconfirmed-tx",
            "address": "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx"
        }
        
        # Call the method
        result = self.forwarding_manager.create_address_webhook(
            url="https://example.com/webhook",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            event="unconfirmed-tx"
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="unconfirmed-tx",
            address="tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx",
            filter=None
        )
        self.assertEqual(result, mock_create_webhook.return_value)
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_transaction_webhook(self, mock_create_webhook):
        """Test creating a webhook for a transaction."""
        # Mock response
        mock_create_webhook.return_value = {
            "id": "webhook_id_123",
            "url": "https://example.com/webhook",
            "event": "confirmed-tx",
            "hash": "tx_hash_123"
        }
        
        # Call the method
        result = self.forwarding_manager.create_transaction_webhook(
            url="https://example.com/webhook",
            transaction_hash="tx_hash_123",
            confirmations=6
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="tx-confirmation",
            hash="tx_hash_123",
            confirmations=6
        )
        self.assertEqual(result, mock_create_webhook.return_value)
    
    @patch('app.infrastructure.providers.blockcypher.forwarding.manager.ForwardingManager.create_webhook')
    def test_create_confidence_webhook(self, mock_create_webhook):
        """Test creating a webhook for confidence monitoring."""
        # Mock response
        mock_create_webhook.return_value = {
            "id": "webhook_id_123",
            "url": "https://example.com/webhook",
            "event": "tx-confidence",
            "hash": "tx_hash_123",
            "confidence": 0.9
        }
        
        # Call the method
        result = self.forwarding_manager.create_confidence_webhook(
            url="https://example.com/webhook",
            transaction_hash="tx_hash_123",
            confidence=0.9
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            url="https://example.com/webhook",
            event="tx-confidence",
            hash="tx_hash_123",
            confidence=0.9
        )
        self.assertEqual(result, mock_create_webhook.return_value)


# Real tests using the BlockCypher test faucet
# These tests will only run if the BLOCKCYPHER_LIVE_TEST environment variable is set to 'true'
@pytest.mark.skipif(
    os.getenv("BLOCKCYPHER_LIVE_TEST") != "true",
    reason="Live tests only run when BLOCKCYPHER_LIVE_TEST=true"
)
class TestForwardingManagerWithFaucet(unittest.TestCase):
    """Tests for the ForwardingManager class using the test faucet."""
    
    def setUp(self):
        """Set up test fixtures."""
        from app.infrastructure.providers.blockcypher.utils.test_utils import (
            get_test_api_token,
            setup_funded_test_address,
            generate_test_address
        )
        
        self.coin_symbol = 'bcy'  # BlockCypher test chain
        self.api_token = get_test_api_token()
        self.forwarding_manager = ForwardingManager(api_token=self.api_token, coin_symbol=self.coin_symbol)
        
        # Generate a funded address for testing
        funded_setup = setup_funded_test_address(coin_symbol=self.coin_symbol)
        self.test_address = funded_setup['address_info']
        self.funding_tx = funded_setup['funding_tx']
        
        # Create another address to use as destination
        self.destination_address = generate_test_address(coin_symbol=self.coin_symbol)
        
        # Test webhook URL (This is just for testing - in real usage you'd use a public URL)
        self.test_webhook_url = "https://webhook.site/your-unique-id"
    
    def tearDown(self):
        """Clean up after tests."""
        # Try to clean up any created webhooks
        try:
            webhooks = self.forwarding_manager.list_webhooks()
            for hook in webhooks:
                if hook.get('url') == self.test_webhook_url:
                    self.forwarding_manager.delete_webhook(hook['id'])
        except:
            pass
    
    def test_live_create_and_list_forwarding_address(self):
        """Test creating and listing forwarding addresses."""
        # Create a forwarding address
        forwarding = self.forwarding_manager.create_forwarding_address(
            destination=self.destination_address['address']
        )
        
        # Verify the forwarding address was created
        self.assertIn('input_address', forwarding)
        self.assertEqual(forwarding['destination'], self.destination_address['address'])
        
        # Get the list of forwarding addresses
        forwarding_list = self.forwarding_manager.list_forwarding_addresses()
        
        # Verify our forwarding address is in the list
        found = False
        for addr in forwarding_list:
            if addr.get('id') == forwarding['id']:
                found = True
                break
        
        self.assertTrue(found, "Created forwarding address not found in list")
        
        # Clean up - delete the forwarding address
        result = self.forwarding_manager.delete_forwarding_address(forwarding['id'])
        self.assertTrue(result.get('deleted', False))
    
    def test_live_create_forwarding_with_fee(self):
        """Test creating a forwarding address with a processing fee."""
        # Create a forwarding address with a small processing fee
        fee_satoshis = 1000  # 1000 satoshis (0.00001 BCY)
        forwarding = self.forwarding_manager.create_forwarding_address(
            destination=self.destination_address['address'],
            processing_fee_satoshis=fee_satoshis
        )
        
        # Verify the forwarding address was created with the fee
        self.assertIn('input_address', forwarding)
        self.assertEqual(forwarding['destination'], self.destination_address['address'])
        self.assertIn('processing_fees', forwarding)
        self.assertEqual(forwarding['processing_fees']['satoshis'], fee_satoshis)
        
        # Clean up
        result = self.forwarding_manager.delete_forwarding_address(forwarding['id'])
        self.assertTrue(result.get('deleted', False))
    
    def test_live_webhook_creation_and_management(self):
        """Test creating, listing, and deleting webhooks."""
        # Create a webhook for a transaction
        webhook = self.forwarding_manager.create_webhook(
            url=self.test_webhook_url,
            event="unconfirmed-tx"
        )
        
        # Verify the webhook was created
        self.assertEqual(webhook['url'], self.test_webhook_url)
        self.assertEqual(webhook['event'], "unconfirmed-tx")
        
        # Get the webhook by ID
        retrieved_webhook = self.forwarding_manager.get_webhook(webhook['id'])
        self.assertEqual(retrieved_webhook['id'], webhook['id'])
        
        # List webhooks and verify ours is included
        webhook_list = self.forwarding_manager.list_webhooks()
        found = False
        for hook in webhook_list:
            if hook.get('id') == webhook['id']:
                found = True
                break
        
        self.assertTrue(found, "Created webhook not found in list")
        
        # Delete the webhook
        result = self.forwarding_manager.delete_webhook(webhook['id'])
        self.assertTrue(result.get('deleted', False))
    
    def test_live_address_webhook(self):
        """Test creating a webhook for a specific address."""
        # Create an address-specific webhook
        webhook = self.forwarding_manager.create_address_webhook(
            url=self.test_webhook_url,
            address=self.test_address['address']
        )
        
        # Verify the webhook was created correctly
        self.assertEqual(webhook['url'], self.test_webhook_url)
        self.assertEqual(webhook['event'], "unconfirmed-tx")  # Default event
        self.assertEqual(webhook['address'], self.test_address['address'])
        
        # Clean up
        result = self.forwarding_manager.delete_webhook(webhook['id'])
        self.assertTrue(result.get('deleted', False))
    
    def test_live_websocket_url(self):
        """Test getting the WebSocket URL."""
        # Get the WebSocket URL
        ws_url = self.forwarding_manager.get_websocket_url()
        
        # Verify the URL format is correct
        self.assertTrue(ws_url.startswith("wss://socket.blockcypher.com/v1/bcy/test"))
        self.assertIn(f"token={self.api_token}", ws_url)


if __name__ == '__main__':
    unittest.main() 