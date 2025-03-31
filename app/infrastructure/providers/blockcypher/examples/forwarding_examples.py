"""
Example code for address forwarding and webhooks using BlockCypher.

This module demonstrates how to create address forwarding and webhooks.
"""

from app.infrastructure.providers.blockcypher import ForwardingManager, WalletManager

def create_forwarding_address_example():
    """Example of creating a forwarding address."""
    # Initialize the managers
    forwarding_manager = ForwardingManager(coin_symbol="btc-testnet")
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # Generate a destination address
    # In a real application, you would use an existing address
    destination_info = wallet_manager.generate_address()
    destination_address = destination_info["address"]
    
    print(f"Destination address: {destination_address}")
    
    # Create a forwarding address that sends to the destination
    forwarding_info = forwarding_manager.create_forwarding_address(
        destination=destination_address,
        callback_url="https://your-domain.com/api/v1/webhooks/payment"
    )
    
    print(f"Forwarding address created: {forwarding_info.get('input_address')}")
    print(f"Any funds sent to {forwarding_info.get('input_address')} will be forwarded to {destination_address}")
    
    return forwarding_info

def list_forwarding_addresses_example():
    """Example of listing forwarding addresses."""
    # Initialize the forwarding manager
    forwarding_manager = ForwardingManager(coin_symbol="btc-testnet")
    
    # List all forwarding addresses
    forwarding_addresses = forwarding_manager.list_forwarding_addresses()
    
    print(f"Found {len(forwarding_addresses)} forwarding addresses:")
    for forwarding in forwarding_addresses:
        print(f"- Input: {forwarding.get('input_address')}")
        print(f"  Destination: {forwarding.get('destination')}")
        print(f"  Created: {forwarding.get('created_at')}")
    
    return forwarding_addresses

def create_webhook_example():
    """Example of creating different types of webhooks."""
    # Initialize the forwarding manager
    forwarding_manager = ForwardingManager(coin_symbol="btc-testnet")
    
    # Example addresses and transaction hash
    address = "mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS"
    tx_hash = "7d067bf6a89f4b1407a14a6704447f8e5e2ac5cfc0fd6395a4eb56cb6b7e6f40"
    
    # Create a webhook for a specific address (unconfirmed transactions)
    address_webhook = forwarding_manager.create_address_webhook(
        url="https://your-domain.com/api/v1/webhooks/payment",
        address=address,
        event="unconfirmed-tx"
    )
    
    print(f"Address webhook created: {address_webhook.get('id')}")
    
    # Create a webhook for transaction confirmations
    tx_webhook = forwarding_manager.create_transaction_webhook(
        url="https://your-domain.com/api/v1/webhooks/payment",
        transaction=tx_hash,
        confirmations=6
    )
    
    print(f"Transaction confirmation webhook created: {tx_webhook.get('id')}")
    
    # Create a webhook for transaction confidence
    confidence_webhook = forwarding_manager.create_confidence_webhook(
        url="https://your-domain.com/api/v1/webhooks/payment",
        transaction=tx_hash,
        confidence=0.95
    )
    
    print(f"Confidence webhook created: {confidence_webhook.get('id')}")
    
    return {
        "address_webhook": address_webhook,
        "tx_webhook": tx_webhook,
        "confidence_webhook": confidence_webhook
    }

def list_webhooks_example():
    """Example of listing webhooks."""
    # Initialize the forwarding manager
    forwarding_manager = ForwardingManager(coin_symbol="btc-testnet")
    
    # List all webhooks
    webhooks = forwarding_manager.list_webhooks()
    
    print(f"Found {len(webhooks)} webhooks:")
    for webhook in webhooks:
        print(f"- ID: {webhook.get('id')}")
        print(f"  Event: {webhook.get('event')}")
        print(f"  URL: {webhook.get('url')}")
        
        # Print additional details based on event type
        if webhook.get('event') == 'unconfirmed-tx':
            print(f"  Address: {webhook.get('address')}")
        elif webhook.get('event') == 'tx-confirmation':
            print(f"  Transaction: {webhook.get('hash')}")
            print(f"  Confirmations: {webhook.get('confirmations')}")
    
    return webhooks

def delete_examples(forwarding_id=None, webhook_id=None):
    """Example of deleting forwarding addresses and webhooks."""
    # Initialize the forwarding manager
    forwarding_manager = ForwardingManager(coin_symbol="btc-testnet")
    
    # Delete a forwarding address if ID is provided
    if forwarding_id:
        result = forwarding_manager.delete_forwarding_address(forwarding_id)
        print(f"Deleted forwarding address {forwarding_id}: {result.get('deleted', False)}")
    
    # Delete a webhook if ID is provided
    if webhook_id:
        result = forwarding_manager.delete_webhook(webhook_id)
        print(f"Deleted webhook {webhook_id}: {result.get('deleted', False)}")

if __name__ == "__main__":
    print("\n===== CREATE FORWARDING ADDRESS =====")
    forwarding_info = create_forwarding_address_example()
    
    print("\n===== LIST FORWARDING ADDRESSES =====")
    forwarding_addresses = list_forwarding_addresses_example()
    
    print("\n===== CREATE WEBHOOKS =====")
    webhooks = create_webhook_example()
    
    print("\n===== LIST WEBHOOKS =====")
    all_webhooks = list_webhooks_example()
    
    # Uncomment to test deletion
    # print("\n===== DELETE RESOURCES =====")
    # if forwarding_info:
    #     delete_examples(forwarding_id=forwarding_info.get('id'))
    # if webhooks and webhooks.get('address_webhook'):
    #     delete_examples(webhook_id=webhooks['address_webhook'].get('id')) 