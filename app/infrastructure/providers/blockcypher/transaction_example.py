"""
Example Usage of the TransactionManager Class
This file demonstrates common transaction operations using the BlockCypher API.
"""

import os
from dotenv import load_dotenv
from transaction import TransactionManager

# Load environment variables from .env file (if available)
load_dotenv()

def display_transaction_info(tx_hash):
    """Display detailed information about a transaction"""
    try:
        # Initialize the transaction manager
        manager = TransactionManager(coin_symbol="btc-testnet")
        
        # Get transaction details
        tx_details = manager.get_transaction(tx_hash)
        
        # Display basic transaction information
        print("\n===== TRANSACTION DETAILS =====")
        print(f"Hash: {tx_details.get('hash')}")
        print(f"Block Height: {tx_details.get('block_height', 'Unconfirmed')}")
        print(f"Confirmations: {tx_details.get('confirmations', 0)}")
        print(f"Total Value: {tx_details.get('total') / 100000000} BTC")
        print(f"Fee: {tx_details.get('fees', 0) / 100000000} BTC")
        
        # Display inputs
        print("\n----- INPUTS -----")
        for i, inp in enumerate(tx_details.get('inputs', [])):
            addresses = inp.get('addresses', ['Unknown'])
            print(f"Input {i+1}: {', '.join(addresses)}")
            print(f"   Value: {inp.get('output_value', 0) / 100000000} BTC")
        
        # Display outputs
        print("\n----- OUTPUTS -----")
        for i, out in enumerate(tx_details.get('outputs', [])):
            addresses = out.get('addresses', ['Unknown'])
            print(f"Output {i+1}: {', '.join(addresses)}")
            print(f"   Value: {out.get('value', 0) / 100000000} BTC")
            
        # Show confidence if unconfirmed
        if tx_details.get('confirmations', 0) == 0:
            confidence = manager.get_transaction_confidence(tx_hash)
            print(f"\nTransaction Confidence: {confidence.get('confidence', 0) * 100:.2f}%")
    
    except Exception as e:
        print(f"Error: {e}")

def create_and_send_simple_transaction():
    """Create and send a simple transaction (for demonstration only)"""
    try:
        # Initialize the transaction manager
        manager = TransactionManager(coin_symbol="btc-testnet")
        
        # IMPORTANT: This is just a demonstration.
        # In a real application, you would:
        # 1. Never hardcode addresses or private keys
        # 2. Keep private keys secure and preferably offline
        # 3. Validate inputs thoroughly
        
        # Placeholder values (these won't work)
        from_address = "REPLACE_WITH_YOUR_SOURCE_ADDRESS"
        to_address = "REPLACE_WITH_DESTINATION_ADDRESS"
        amount_btc = 0.001  # In BTC
        private_key = "REPLACE_WITH_PRIVATE_KEY"  # Never hardcode this in real applications
        
        # Convert BTC to satoshis
        amount_satoshis = int(amount_btc * 100000000)
        
        print("\n===== CREATING TRANSACTION =====")
        print(f"From: {from_address}")
        print(f"To: {to_address}")
        print(f"Amount: {amount_btc} BTC")
        
        # Create transaction structure without signing and broadcasting
        # This allows you to review the transaction before signing
        tx_skeleton = manager.simple_transaction(
            from_address=from_address,
            to_address=to_address,
            amount_satoshis=amount_satoshis,
            private_key=None  # Set to None to skip signing and broadcasting
        )
        
        print("\n----- TRANSACTION SKELETON -----")
        print(f"Transaction data created")
        print(f"Items to sign: {len(tx_skeleton.get('tosign', []))}")
        print(f"Fees: {tx_skeleton.get('fees', 0) / 100000000} BTC")
        
        # In a real application, you would sign the transaction at this point
        # For demonstration, we'll show what would happen if we signed and broadcast
        
        print("\n----- SIGN AND BROADCAST (SIMULATED) -----")
        print("Normally, you would sign the transaction and then broadcast it:")
        print("1. signed_tx = manager.sign_transaction(tx_skeleton, [private_key])")
        print("2. result = manager.broadcast_transaction(signed_tx)")
        
        # For this example, we won't actually broadcast anything
        print("\nTransaction broadcasting skipped for this example.")
    
    except Exception as e:
        print(f"Error: {e}")

def create_multisig_example():
    """Demonstrate creating a multisig transaction structure"""
    try:
        # Initialize the transaction manager
        manager = TransactionManager(coin_symbol="btc-testnet")
        
        # Multisig address and public keys (example values)
        multisig_address = "REPLACE_WITH_MULTISIG_ADDRESS"
        pubkeys = [
            "REPLACE_WITH_PUBKEY1",
            "REPLACE_WITH_PUBKEY2",
            "REPLACE_WITH_PUBKEY3"
        ]
        to_address = "REPLACE_WITH_DESTINATION_ADDRESS"
        amount_btc = 0.001  # In BTC
        
        # Convert BTC to satoshis
        amount_satoshis = int(amount_btc * 100000000)
        
        print("\n===== CREATING MULTISIG TRANSACTION =====")
        print(f"From Multisig: {multisig_address}")
        print(f"To: {to_address}")
        print(f"Amount: {amount_btc} BTC")
        print(f"Script Type: multisig-2-of-3")
        
        # Create multisig transaction structure
        tx_skeleton = manager.create_multisig_transaction(
            from_address=multisig_address,
            to_address=to_address,
            amount_satoshis=amount_satoshis,
            pubkeys=pubkeys,
            script_type="multisig-2-of-3"
        )
        
        print("\n----- MULTISIG TRANSACTION SKELETON -----")
        print(f"Transaction data created")
        print(f"Items to sign: {len(tx_skeleton.get('tosign', []))}")
        print(f"Fees: {tx_skeleton.get('fees', 0) / 100000000} BTC")
        
        print("\nIn a real application, this skeleton would be shared with the key holders")
        print("Each party would sign their portion, and when enough signatures are collected,")
        print("the transaction would be broadcast to the network.")
    
    except Exception as e:
        print(f"Error: {e}")

def decode_raw_transaction_example():
    """Demonstrate decoding a raw transaction hex string"""
    try:
        # Initialize the transaction manager
        manager = TransactionManager(coin_symbol="btc-testnet")
        
        # Example transaction hex (this is just a placeholder)
        tx_hex = "01000000012d6d5b2b6cd9b8e797f9c121f6afd8d93ded8c599aeb2982005bd9825879c33b010000006b483045022100df73e6f1d2fac61c1db5c9a35e0115d0abd3b2b5a535a5d36ea6c7ceef1cb1c7022071cfd902083e1b0d18a7ac4b40067c5cfc01d79c9260c9a6182c7b561a28a9ba012103c4b95d394f0b1118d0fec17f1fcb8e44640a76d58ac4b6cd274a3d43f472f637ffffffff0210270000000000001976a9142dae4b14646df7baf5be93b97d39979add02c7f588ac7b030100000000001976a9141007dd02ee3cee9eacfef999e7a90ddcdea1c7a288ac00000000"
        
        print("\n===== DECODING RAW TRANSACTION =====")
        
        # Decode the transaction
        tx_decoded = manager.decode_raw_transaction(tx_hex)
        
        print("\n----- DECODED TRANSACTION -----")
        print(f"Hash: {tx_decoded.get('hash')}")
        
        # Display inputs
        print("\nInputs:")
        for i, inp in enumerate(tx_decoded.get('inputs', [])):
            addresses = inp.get('addresses', ['Unknown'])
            print(f"Input {i+1}: {', '.join(addresses)}")
        
        # Display outputs
        print("\nOutputs:")
        for i, out in enumerate(tx_decoded.get('outputs', [])):
            addresses = out.get('addresses', ['Unknown'])
            print(f"Output {i+1}: {', '.join(addresses)}")
            print(f"   Value: {out.get('value', 0) / 100000000} BTC")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("BLOCKCYPHER TRANSACTION API EXAMPLES")
    print("=" * 60)
    
    # Example 1: Display information about an existing transaction
    # Replace with a real transaction hash from testnet
    sample_tx_hash = "67b5c8a1c5e1dcbd5f3b8a246153433572a17a59ffec27329be12ecce1221a7e"
    display_transaction_info(sample_tx_hash)
    
    # Uncomment to run these examples
    # create_and_send_simple_transaction()
    # create_multisig_example()
    # decode_raw_transaction_example()
    
    print("\n" + "=" * 60) 