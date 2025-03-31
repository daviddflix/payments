"""
BlockCypher Webhook Handler

This module contains the handler for BlockCypher webhook callbacks for blockchain events,
including transaction notifications and confirmations.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Optional

# In a real application, you would use a database instead of this in-memory storage
transaction_db = {}


class BlockcypherWebhookHandler:
    """Handler for BlockCypher webhook callbacks"""
    
    @staticmethod
    def handle_payment_webhook(request_data: bytes, request_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle payment notifications from BlockCypher.
        This processes both unconfirmed and confirmed transaction events.
        
        Args:
            request_data: Raw request data for signature verification
            request_json: Parsed JSON data from the request
            
        Returns:
            Response data
        """
        
        # Extract key information from the webhook
        event_type = request_json.get('event')
        address = request_json.get('address')
        tx_hash = request_json.get('hash')
        confirmations = request_json.get('confirmations', 0)
        value_satoshis = 0
        
        # Process based on event type
        if event_type == 'unconfirmed-tx':
            return BlockcypherWebhookHandler._handle_unconfirmed_tx(
                request_json, address, tx_hash, value_satoshis
            )
                
        elif event_type == 'tx-confirmation':
            return BlockcypherWebhookHandler._handle_tx_confirmation(
                tx_hash, confirmations
            )
                
        elif event_type == 'double-spend-tx':
            return BlockcypherWebhookHandler._handle_double_spend(tx_hash)
                
        # Return a success response to BlockCypher
        # Always return 200 OK for webhooks to prevent retries
        return {
            "received": True,
            "tx_hash": tx_hash,
            "event": event_type
        }
    
    @staticmethod
    def _handle_unconfirmed_tx(data: Dict[str, Any], address: str, tx_hash: str, value_satoshis: int) -> Dict[str, Any]:
        """
        Handle an unconfirmed transaction notification
        
        Args:
            data: The transaction data
            address: The receiving address
            tx_hash: The transaction hash
            value_satoshis: Initial value in satoshis
            
        Returns:
            Response data
        """
        try:
            # Find the output that matches our address
            for output in data.get('outputs', []):
                if address in output.get('addresses', []):
                    value_satoshis += output.get('value', 0)
                    
            # Save transaction to our database
            transaction_db[tx_hash] = {
                'address': address,
                'value_satoshis': value_satoshis,
                'value_btc': value_satoshis / 100000000.0,  # Convert to BTC
                'confirmations': 0,
                'status': 'unconfirmed',
                'timestamp': datetime.now().isoformat(),
                'tx_hash': tx_hash
            }
            
            # Here you would typically:
            # 1. Record the payment in your database
            # 2. Update user account/credits
            # 3. Mark invoice as "pending confirmation"
            print(f"Unconfirmed payment of {value_satoshis / 100000000.0} BTC to {address} detected")
            
            return {
                "received": True,
                "tx_hash": tx_hash,
                "event": "unconfirmed-tx",
                "value_satoshis": value_satoshis
            }
        except Exception as e:
            print(f"Error processing unconfirmed transaction: {e}")
            return {"error": str(e)}
    
    @staticmethod
    def _handle_tx_confirmation(tx_hash: str, confirmations: int) -> Dict[str, Any]:
        """
        Handle a transaction confirmation notification
        
        Args:
            tx_hash: The transaction hash
            confirmations: Number of confirmations
            
        Returns:
            Response data
        """
        if tx_hash in transaction_db:
            transaction_db[tx_hash]['confirmations'] = confirmations
            
            # Typically you would update the payment status based on confirmations
            if confirmations >= 6:
                transaction_db[tx_hash]['status'] = 'confirmed'
                print(f"Transaction {tx_hash} is now fully confirmed with {confirmations} confirmations")
                
                # Here you would typically:
                # 1. Mark the payment as fully confirmed in your database
                # 2. Trigger fulfillment process (deliver digital goods, ship physical goods)
                # 3. Send confirmation email to customer
            else:
                print(f"Transaction {tx_hash} now has {confirmations} confirmations")
                
            return {
                "received": True,
                "tx_hash": tx_hash,
                "event": "tx-confirmation",
                "confirmations": confirmations,
                "status": transaction_db[tx_hash]['status']
            }
        else:
            # Handle case where confirmation arrives before the unconfirmed-tx event
            print(f"Received confirmation for unknown transaction {tx_hash}")
            return {
                "received": True,
                "tx_hash": tx_hash,
                "event": "tx-confirmation",
                "confirmations": confirmations,
                "status": "unknown_transaction"
            }
    
    @staticmethod
    def _handle_double_spend(tx_hash: str) -> Dict[str, Any]:
        """
        Handle a double-spend detection
        
        Args:
            tx_hash: The transaction hash
            
        Returns:
            Response data
        """
        if tx_hash in transaction_db:
            transaction_db[tx_hash]['status'] = 'double-spend'
            print(f"WARNING: Double spend detected for transaction {tx_hash}")
            
            # Here you would typically:
            # 1. Mark the payment as invalid in your database
            # 2. Revert any credits or fulfillment
            # 3. Flag the account for potential fraud
                
        return {
            "received": True,
            "tx_hash": tx_hash,
            "event": "double-spend-tx",
            "status": "fraud_detected"
        }
    
    @staticmethod
    def get_transaction_status(tx_hash: str) -> Dict[str, Any]:
        """
        Get the status of a transaction from our database
        
        Args:
            tx_hash: The transaction hash to look up
            
        Returns:
            Transaction details if found
        """
        if tx_hash in transaction_db:
            return transaction_db[tx_hash]
        return {"error": "Transaction not found"}
    
    @staticmethod
    def get_all_transactions() -> List[Dict[str, Any]]:
        """
        Get all transactions in the database
        
        Returns:
            List of all transactions
        """
        return list(transaction_db.values())


def simulate_webhook(event_type: str = 'unconfirmed-tx', 
                    address: Optional[str] = None,
                    confirmations: int = 1) -> Dict[str, Any]:
    """
    Simulate a webhook call for testing.
    
    Args:
        event_type: Type of event to simulate
        address: The address to use in the simulation
        confirmations: Number of confirmations (for tx-confirmation events)
        
    Returns:
        Simulated webhook response
    """
    address = address or 'simulated_address'
    
    # Create a simulated webhook payload based on the event type
    if event_type == 'unconfirmed-tx':
        # Simulate an unconfirmed transaction
        simulated_data = {
            "event": "unconfirmed-tx",
            "address": address,
            "hash": "simulated_tx_" + datetime.now().strftime("%Y%m%d%H%M%S"),
            "confirmations": 0,
            "outputs": [
                {
                    "addresses": [address],
                    "value": 1500000  # 0.015 BTC in satoshis
                }
            ]
        }
    elif event_type == 'tx-confirmation':
        # Simulate a confirmation event
        tx_hash = list(transaction_db.keys())[0] if transaction_db else "no_transactions"
        
        simulated_data = {
            "event": "tx-confirmation",
            "hash": tx_hash,
            "confirmations": confirmations
        }
    elif event_type == 'double-spend-tx':
        # Simulate a double-spend event
        tx_hash = list(transaction_db.keys())[0] if transaction_db else "no_transactions"
        
        simulated_data = {
            "event": "double-spend-tx",
            "hash": tx_hash
        }
    else:
        return {"error": "Unsupported event type for simulation"}
    
    # Process the simulated webhook
    simulated_bytes = json.dumps(simulated_data).encode('utf-8')
    webhook_response = BlockcypherWebhookHandler.handle_payment_webhook(
        simulated_bytes, 
        simulated_data
    )
    
    # Return both the simulated request and the handler's response
    return {
        "simulated_request": simulated_data,
        "webhook_response": webhook_response
    } 