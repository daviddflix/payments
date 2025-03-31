import os
import unittest
from unittest.mock import patch, MagicMock
from .transaction import TransactionManager

class TestTransactionManager(unittest.TestCase):
    """Test cases for the BlockCypher TransactionManager class"""
    
    @patch.dict(os.environ, {"BLOCKCYPHER_API_TOKEN": "test_token"})
    def setUp(self):
        self.manager = TransactionManager(coin_symbol="btc-testnet")
        
    @patch('requests.get')
    def test_get_transaction(self, mock_get):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"hash": "test_hash", "total": 1000}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.manager.get_transaction("test_hash")
        
        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(result["hash"], "test_hash")
        self.assertEqual(result["total"], 1000)
        
    @patch('requests.get')
    def test_get_unconfirmed_transactions(self, mock_get):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"hash": "tx1", "total": 1000},
            {"hash": "tx2", "total": 2000}
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.manager.get_unconfirmed_transactions(limit=2)
        
        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["hash"], "tx1")
        
    @patch('requests.post')
    def test_create_transaction(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tx": {"hash": "new_tx"},
            "tosign": ["abc123", "def456"]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test inputs and outputs
        inputs = [{"addresses": ["source_addr"]}]
        outputs = [{"addresses": ["dest_addr"], "value": 50000}]
        
        # Call the method
        result = self.manager.create_transaction(inputs, outputs)
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["tx"]["hash"], "new_tx")
        self.assertEqual(len(result["tosign"]), 2)
        
    @patch('requests.post')
    def test_sign_transaction(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tx": {"hash": "signed_tx"},
            "signatures": ["sig1", "sig2"]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Mock transaction skeleton
        tx_skeleton = {
            "tx": {"hash": "new_tx"},
            "tosign": ["abc123", "def456"]
        }
        
        # Call the method
        result = self.manager.sign_transaction(tx_skeleton, ["priv_key1", "priv_key2"])
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["tx"]["hash"], "signed_tx")
        self.assertEqual(len(result["signatures"]), 2)
        
    @patch('requests.post')
    def test_broadcast_transaction(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "tx": {"hash": "broadcast_tx"},
            "received": "2023-01-01T00:00:00Z",
            "confirmed": None
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Mock signed transaction
        signed_tx = {
            "tx": {"hash": "signed_tx"},
            "signatures": ["sig1", "sig2"]
        }
        
        # Call the method
        result = self.manager.broadcast_transaction(signed_tx)
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["tx"]["hash"], "broadcast_tx")
        self.assertIsNotNone(result["received"])
        self.assertIsNone(result["confirmed"])
        
    @patch('requests.post')
    def test_decode_raw_transaction(self, mock_post):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "hash": "decoded_tx",
            "inputs": [{"addresses": ["input_addr"]}],
            "outputs": [{"addresses": ["output_addr"], "value": 50000}]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        result = self.manager.decode_raw_transaction("0100000001...")
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result["hash"], "decoded_tx")
        self.assertEqual(result["outputs"][0]["value"], 50000)
        
    @patch.object(TransactionManager, 'create_transaction')
    @patch.object(TransactionManager, 'sign_transaction')
    @patch.object(TransactionManager, 'broadcast_transaction')
    def test_simple_transaction(self, mock_broadcast, mock_sign, mock_create):
        # Setup mocks
        mock_create.return_value = {"tx": {"hash": "new_tx"}, "tosign": ["abc123"]}
        mock_sign.return_value = {"tx": {"hash": "signed_tx"}, "signatures": ["sig1"]}
        mock_broadcast.return_value = {"tx": {"hash": "broadcast_tx"}}
        
        # Call the method
        result = self.manager.simple_transaction(
            from_address="source_addr",
            to_address="dest_addr",
            amount_satoshis=50000,
            private_key="priv_key"
        )
        
        # Assertions
        mock_create.assert_called_once()
        mock_sign.assert_called_once()
        mock_broadcast.assert_called_once()
        self.assertEqual(result["tx"]["hash"], "broadcast_tx")
        
    @patch.object(TransactionManager, 'create_transaction')
    def test_create_multisig_transaction(self, mock_create):
        # Setup mock
        mock_create.return_value = {"tx": {"hash": "multisig_tx"}, "tosign": ["abc123", "def456", "ghi789"]}
        
        # Call the method
        result = self.manager.create_multisig_transaction(
            from_address="multisig_addr",
            to_address="dest_addr",
            amount_satoshis=50000,
            pubkeys=["pub1", "pub2", "pub3"],
            script_type="multisig-2-of-3"
        )
        
        # Assertions
        mock_create.assert_called_once()
        self.assertEqual(result["tx"]["hash"], "multisig_tx")
        self.assertEqual(len(result["tosign"]), 3)
        
    @patch.object(TransactionManager, 'simple_transaction')
    @patch.object(TransactionManager, 'get_transaction_confidence')
    def test_send_transaction_with_confidence(self, mock_confidence, mock_simple_tx):
        # Setup mocks
        mock_simple_tx.return_value = {"hash": "new_tx"}
        mock_confidence.return_value = {"confidence": 0.95}
        
        # Call the method
        result = self.manager.send_transaction_with_confidence(
            from_address="source_addr",
            to_address="dest_addr",
            amount_satoshis=50000,
            private_key="priv_key",
            min_confidence=0.90
        )
        
        # Assertions
        mock_simple_tx.assert_called_once()
        mock_confidence.assert_called_once_with("new_tx")
        self.assertEqual(result["confidence"], 0.95)

if __name__ == "__main__":
    unittest.main() 