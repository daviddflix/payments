"""
Example Usage of the ForwardingManager Class
This file demonstrates address forwarding and webhook functionality using the BlockCypher API.
"""

import os
import json
from dotenv import load_dotenv
from forwarding import ForwardingManager

# Load environment variables from .env file (if available)
load_dotenv()

def address_forwarding_example():
    """Demonstrate the address forwarding functionality"""
    try:
        # Initialize the forwarding manager for Bitcoin testnet
        manager = ForwardingManager(coin_symbol="btc-testnet")
        
        print("\n===== ADDRESS FORWARDING EXAMPLES =====")
        
        # Example 1: Basic forwarding setup
        print("\n----- Basic Forwarding Setup -----")
        print("This creates an address that will automatically forward payments to your destination address.")
        
        # Replace with your actual destination address
        destination_address = "REPLACE_WITH_YOUR_DESTINATION_ADDRESS"
        
        print(f"Creating forwarding address to: {destination_address}")
        print("Note: This code is commented out to prevent accidental API calls.")
        
        # Uncomment to create a real forwarding address
        # forwarding = manager.create_forwarding_address(
        #     destination_address=destination_address,
        #     callback_url="https://example.com/payment/callback"
        # )
        # print(f"Forwarding setup created!")
        # print(f"Input Address: {forwarding.get('input_address')}")
        # print(f"Destination: {forwarding.get('destination')}")
        # print(f"ID: {forwarding.get('id')}")
        
        # Example 2: Forwarding with processing fee
        print("\n----- Forwarding With Processing Fee -----")
        print("You can add a processing fee that will be deducted from each payment.")
        print("This can be either a fixed amount in satoshis or a percentage.")
        
        # Uncomment to create a forwarding address with fee
        # forwarding_with_fee = manager.create_forwarding_address(
        #     destination_address=destination_address,
        #     process_fee_percent=1.0,  # 1% fee
        #     process_fee_address=destination_address  # Fee goes to same destination
        # )
        # print(f"Forwarding with fee created!")
        # print(f"Input Address: {forwarding_with_fee.get('input_address')}")
        # print(f"Fee: 1.0% to {forwarding_with_fee.get('process_fee_address')}")
        
        # Example 3: List existing forwarding addresses
        print("\n----- List Existing Forwarding Addresses -----")
        forwards = manager.list_forwarding_addresses()
        
        if forwards:
            print(f"Found {len(forwards)} active forwarding addresses:")
            for idx, forward in enumerate(forwards, 1):
                print(f"\n  Forward {idx}:")
                print(f"  ID: {forward.get('id')}")
                print(f"  Input Address: {forward.get('input_address')}")
                print(f"  Destination: {forward.get('destination')}")
                
                # Check if this forwarding has a callback URL
                if 'callback_url' in forward:
                    print(f"  Callback URL: {forward.get('callback_url')}")
                
                # Check if this forwarding has a processing fee
                if 'process_fee_percent' in forward:
                    print(f"  Fee: {forward.get('process_fee_percent')}%")
                elif 'process_fee_satoshis' in forward:
                    print(f"  Fee: {forward.get('process_fee_satoshis')} satoshis")
        else:
            print("No active forwarding addresses found.")
        
        # Example 4: Deleting a forwarding address
        print("\n----- Deleting a Forwarding Address -----")
        if forwards:
            forwarding_id = forwards[0]['id']
            print(f"To delete the forwarding address with ID {forwarding_id}, uncomment the code below.")
            
            # Uncomment to delete a forwarding address
            # success = manager.delete_forwarding_address(forwarding_id)
            # if success:
            #     print(f"Successfully deleted forwarding address with ID: {forwarding_id}")
            # else:
            #     print(f"Failed to delete forwarding address.")
        else:
            print("No forwarding addresses to delete.")
        
    except Exception as e:
        print(f"Error in address forwarding examples: {e}")

def webhook_example():
    """Demonstrate the webhook functionality"""
    try:
        # Initialize the forwarding manager for Bitcoin testnet
        manager = ForwardingManager(coin_symbol="btc-testnet")
        
        print("\n===== WEBHOOK EXAMPLES =====")
        
        # Example 1: Create address monitoring webhook
        print("\n----- Address Monitoring Webhook -----")
        print("This creates a webhook that will notify you of events related to a specific address.")
        
        # Replace with address to monitor
        monitor_address = "REPLACE_WITH_ADDRESS_TO_MONITOR"
        
        print(f"Creating webhook for address: {monitor_address}")
        print("Note: This code is commented out to prevent accidental API calls.")
        
        # Uncomment to create a real webhook
        # webhook = manager.create_address_webhook(
        #     address=monitor_address,
        #     url="https://example.com/webhook/callback",
        #     event_type="unconfirmed-tx"
        # )
        # print(f"Webhook created with ID: {webhook.get('id')}")
        # print(f"Will trigger on: {webhook.get('event')}")
        
        # Example 2: Transaction confirmation webhook
        print("\n----- Transaction Confirmation Webhook -----")
        print("This creates a webhook that will notify you when a transaction reaches a certain number of confirmations.")
        
        # Replace with transaction hash to monitor
        tx_hash = "REPLACE_WITH_TRANSACTION_HASH"
        
        print(f"Creating webhook for transaction: {tx_hash}")
        
        # Uncomment to create a transaction confirmation webhook
        # webhook = manager.create_transaction_webhook(
        #     transaction_hash=tx_hash,
        #     url="https://example.com/webhook/tx_confirmed",
        #     confirmations=3  # Notify after 3 confirmations
        # )
        # print(f"Webhook created with ID: {webhook.get('id')}")
        # print(f"Will trigger when transaction has {webhook.get('confirmations')} confirmations")
        
        # Example 3: Transaction confidence webhook
        print("\n----- Transaction Confidence Webhook -----")
        print("This creates a webhook that will notify you when an unconfirmed transaction reaches a certain confidence level.")
        
        # Uncomment to create a confidence webhook
        # webhook = manager.create_confidence_webhook(
        #     address=monitor_address,
        #     url="https://example.com/webhook/confidence",
        #     confidence_threshold=0.95  # 95% confidence
        # )
        # print(f"Webhook created with ID: {webhook.get('id')}")
        # print(f"Will trigger when transactions to {webhook.get('address')} reach {webhook.get('confidence')*100}% confidence")
        
        # Example 4: List existing webhooks
        print("\n----- List Existing Webhooks -----")
        webhooks = manager.list_webhooks()
        
        if webhooks:
            print(f"Found {len(webhooks)} active webhooks:")
            for idx, webhook in enumerate(webhooks, 1):
                print(f"\n  Webhook {idx}:")
                print(f"  ID: {webhook.get('id')}")
                print(f"  Event: {webhook.get('event')}")
                print(f"  URL: {webhook.get('url')}")
                
                # Print additional details based on webhook type
                if 'address' in webhook:
                    print(f"  Address: {webhook.get('address')}")
                if 'hash' in webhook:
                    print(f"  Transaction/Block: {webhook.get('hash')}")
                if 'confirmations' in webhook:
                    print(f"  Confirmations: {webhook.get('confirmations')}")
                if 'confidence' in webhook:
                    print(f"  Confidence Threshold: {webhook.get('confidence')}")
        else:
            print("No active webhooks found.")
        
        # Example 5: Delete a webhook
        print("\n----- Deleting a Webhook -----")
        if webhooks:
            webhook_id = webhooks[0]['id']
            print(f"To delete the webhook with ID {webhook_id}, uncomment the code below.")
            
            # Uncomment to delete a webhook
            # success = manager.delete_webhook(webhook_id)
            # if success:
            #     print(f"Successfully deleted webhook with ID: {webhook_id}")
            # else:
            #     print(f"Failed to delete webhook.")
        else:
            print("No webhooks to delete.")
            
        # Example 6: WebSocket connection info
        print("\n----- WebSocket Connection -----")
        ws_url = manager.get_websocket_url()
        print(f"WebSocket URL: {ws_url}")
        print("To use WebSockets in JavaScript:")
        print(f"  const socket = new WebSocket(\"{ws_url}\");")
        print("  socket.onopen = function() {")
        print("    // Send an event definition")
        print("    socket.send(JSON.stringify({")
        print("      'event': 'unconfirmed-tx',")
        print("      'address': 'your_address_here'")
        print("    }));")
        print("  };")
        print("  socket.onmessage = function(event) {")
        print("    const data = JSON.parse(event.data);")
        print("    console.log('Received event:', data);")
        print("  };")
        
    except Exception as e:
        print(f"Error in webhook examples: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("BLOCKCYPHER ADDRESS FORWARDING AND WEBHOOK EXAMPLES")
    print("=" * 80)
    print("\nNote: Most API calls are commented out in this example to prevent accidental creation.")
    print("Uncomment the relevant sections to actually execute the API calls.")
    
    # Run the examples
    address_forwarding_example()
    webhook_example()
    
    print("\n" + "=" * 80) 