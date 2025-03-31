import os
import unittest
from unittest.mock import patch, MagicMock
from .forwarding import ForwardingManager

class TestForwardingManager(unittest.TestCase):
    """Test cases for the BlockCypher ForwardingManager class"""
    
    @patch.dict(os.environ, {"BLOCKCYPHER_API_TOKEN": "test_token"})
    def setUp(self):
        self.manager = ForwardingManager(coin_symbol="btc-testnet")
        
    # ======== Address Forwarding Tests ========
    
    @patch('requests.post')
    def test_create_forwarding_address(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-forward-id",
            "token": "test_token",
            "destination": "dest_address123",
            "input_address": "input_address456",
            "callback_url": "https://example.com/callback"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.manager.create_forwarding_address(
            destination_address="dest_address123",
            callback_url="https://example.com/callback"
        )
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["id"], "test-forward-id")
        self.assertEqual(result["destination"], "dest_address123")
        self.assertEqual(result["input_address"], "input_address456")
    
    @patch('requests.post')
    def test_create_forwarding_address_with_fee(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-forward-id",
            "token": "test_token",
            "destination": "dest_address123",
            "input_address": "input_address456",
            "process_fee_address": "fee_address789",
            "process_fee_percent": 2.5
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.manager.create_forwarding_address(
            destination_address="dest_address123",
            process_fee_percent=2.5,
            process_fee_address="fee_address789"
        )
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["process_fee_percent"], 2.5)
        self.assertEqual(result["process_fee_address"], "fee_address789")
    
    @patch('requests.get')
    def test_list_forwarding_addresses(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "forward-id-1",
                "destination": "dest_address1",
                "input_address": "input_address1"
            },
            {
                "id": "forward-id-2",
                "destination": "dest_address2",
                "input_address": "input_address2"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.manager.list_forwarding_addresses()
        
        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "forward-id-1")
        self.assertEqual(result[1]["id"], "forward-id-2")
    
    @patch('requests.delete')
    def test_delete_forwarding_address(self, mock_delete):
        # Setup mock response
        mock_response = MagicMock()
        # Status code 204 for successful deletion
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the method
        result = self.manager.delete_forwarding_address("test-forward-id")
        
        # Assertions
        mock_delete.assert_called_once()
        self.assertTrue(result)
    
    # ======== Webhook Tests ========
    
    @patch('requests.post')
    def test_create_webhook(self, mock_post):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-webhook-id",
            "token": "test_token",
            "url": "https://example.com/webhook",
            "event": "unconfirmed-tx",
            "address": "test_address123"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.manager.create_webhook(
            event_type="unconfirmed-tx",
            url="https://example.com/webhook",
            address="test_address123"
        )
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["id"], "test-webhook-id")
        self.assertEqual(result["event"], "unconfirmed-tx")
        self.assertEqual(result["address"], "test_address123")
    
    @patch('requests.post')
    def test_create_webhook_invalid_event(self, mock_post):
        # Test with invalid event type
        with self.assertRaises(ValueError) as context:
            self.manager.create_webhook(
                event_type="invalid-event",
                url="https://example.com/webhook"
            )
            
        # Verify the exception message
        self.assertTrue("Invalid event type" in str(context.exception))
        
        # Ensure the API was not called
        mock_post.assert_not_called()
    
    @patch('requests.get')
    def test_list_webhooks(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "webhook-id-1",
                "event": "unconfirmed-tx",
                "url": "https://example.com/webhook1"
            },
            {
                "id": "webhook-id-2",
                "event": "tx-confirmation",
                "url": "https://example.com/webhook2"
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.manager.list_webhooks()
        
        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "webhook-id-1")
        self.assertEqual(result[1]["id"], "webhook-id-2")
    
    @patch('requests.get')
    def test_get_webhook(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-webhook-id",
            "event": "tx-confirmation",
            "url": "https://example.com/webhook",
            "address": "test_address123",
            "confirmations": 6
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.manager.get_webhook("test-webhook-id")
        
        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(result["id"], "test-webhook-id")
        self.assertEqual(result["event"], "tx-confirmation")
        self.assertEqual(result["confirmations"], 6)
    
    @patch('requests.delete')
    def test_delete_webhook(self, mock_delete):
        # Setup mock response
        mock_response = MagicMock()
        # Status code 204 for successful deletion
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the method
        result = self.manager.delete_webhook("test-webhook-id")
        
        # Assertions
        mock_delete.assert_called_once()
        self.assertTrue(result)
    
    # ======== Utility Method Tests ========
    
    def test_get_websocket_url(self):
        # Test the websocket URL generation
        url = self.manager.get_websocket_url()
        expected_url = "wss://socket.blockcypher.com/v1/btc/test3?token=test_token"
        self.assertEqual(url, expected_url)
    
    @patch.object(ForwardingManager, 'create_webhook')
    def test_create_address_webhook(self, mock_create_webhook):
        # Setup mock return value
        mock_create_webhook.return_value = {"id": "webhook-id"}
        
        # Call the method
        result = self.manager.create_address_webhook(
            address="test_address",
            url="https://example.com/webhook"
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            event_type='unconfirmed-tx',
            url='https://example.com/webhook',
            address='test_address',
            confirmations=6
        )
        self.assertEqual(result["id"], "webhook-id")
    
    @patch.object(ForwardingManager, 'create_webhook')
    def test_create_transaction_webhook(self, mock_create_webhook):
        # Setup mock return value
        mock_create_webhook.return_value = {"id": "webhook-id"}
        
        # Call the method
        result = self.manager.create_transaction_webhook(
            transaction_hash="tx_hash_123",
            url="https://example.com/webhook"
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            event_type='tx-confirmation',
            url='https://example.com/webhook',
            hash_or_height='tx_hash_123',
            confirmations=6
        )
        self.assertEqual(result["id"], "webhook-id")
    
    @patch.object(ForwardingManager, 'create_webhook')
    def test_create_confidence_webhook(self, mock_create_webhook):
        # Setup mock return value
        mock_create_webhook.return_value = {"id": "webhook-id"}
        
        # Call the method
        result = self.manager.create_confidence_webhook(
            address="test_address",
            url="https://example.com/webhook",
            confidence_threshold=0.95
        )
        
        # Assertions
        mock_create_webhook.assert_called_once_with(
            event_type='tx-confidence',
            url='https://example.com/webhook',
            address='test_address',
            confidence=0.95
        )
        self.assertEqual(result["id"], "webhook-id")

if __name__ == "__main__":
    unittest.main() 