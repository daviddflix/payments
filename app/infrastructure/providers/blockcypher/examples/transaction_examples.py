"""
Example code for transaction management using BlockCypher.

This module demonstrates common transaction operations using the TransactionManager.
"""

from app.infrastructure.providers.blockcypher import TransactionManager, WalletManager

def create_transaction_example():
    """Example of creating and broadcasting a transaction."""
    # Initialize the managers
    tx_manager = TransactionManager(coin_symbol="btc-testnet")
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # Generate addresses for testing
    # In a real application, you would use existing addresses
    from_address_info = wallet_manager.generate_address()
    to_address_info = wallet_manager.generate_address()
    
    from_address = from_address_info["address"]
    to_address = to_address_info["address"]
    private_key = from_address_info["private_key"]
    
    print(f"Sender address: {from_address}")
    print(f"Recipient address: {to_address}")
    
    # NOTE: In a real scenario, the sender address would need to have funds
    # For testnet, you can request test coins from a faucet
    
    try:
        # Create and sign a transaction in one step
        # This would normally fail unless the address has funds
        tx_result = tx_manager.create_and_sign_transaction(
            from_address=from_address,
            to_address=to_address,
            amount_satoshis=1000000,  # 0.01 BTC
            private_key=private_key
        )
        
        print(f"Transaction created and broadcast: {tx_result.get('tx_hash')}")
        return tx_result.get('tx_hash')
    except Exception as e:
        print(f"Transaction creation failed (expected if address has no funds): {e}")
        # For demo purposes, return a sample transaction hash
        return "7d067bf6a89f4b1407a14a6704447f8e5e2ac5cfc0fd6395a4eb56cb6b7e6f40"

def transaction_details_example(tx_hash):
    """Example of getting transaction details."""
    # Initialize the transaction manager
    tx_manager = TransactionManager(coin_symbol="btc-testnet")
    
    # Get transaction details
    tx_details = tx_manager.get_transaction(tx_hash)
    print(f"Transaction details for {tx_hash}:")
    print(f"  Confirmations: {tx_details.get('confirmations', 0)}")
    print(f"  Amount: {sum(o.get('value', 0) for o in tx_details.get('outputs', []))} satoshis")
    print(f"  Block height: {tx_details.get('block_height', 'unconfirmed')}")
    
    return tx_details

def monitor_transaction_example(tx_hash):
    """Example of monitoring a transaction for confirmations."""
    # Initialize the transaction manager
    tx_manager = TransactionManager(coin_symbol="btc-testnet")
    
    # Get current confirmations
    confirmations = tx_manager.get_transaction_confirmations(tx_hash)
    print(f"Current confirmations for {tx_hash}: {confirmations}")
    
    # For unconfirmed transactions, check confidence
    if confirmations == 0:
        confidence = tx_manager.get_transaction_confidence(tx_hash)
        print(f"Transaction confidence: {confidence.get('confidence', 0)}")
    
    return confirmations

def fee_estimation_example():
    """Example of estimating transaction fees."""
    # Initialize the transaction manager
    tx_manager = TransactionManager(coin_symbol="btc-testnet")
    
    # Example addresses
    from_address = "mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS"
    to_address = "mteBzZDP2LN41SfkJLRfV6JM2s8bPMES93"
    
    # Estimate fee for a transaction
    estimated_fee = tx_manager.get_transaction_fee_estimate(
        from_address=from_address,
        to_address=to_address,
        amount_satoshis=1000000  # 0.01 BTC
    )
    
    print(f"Estimated fee for transaction: {estimated_fee} satoshis")
    
    return estimated_fee

if __name__ == "__main__":
    print("\n===== TRANSACTION CREATION =====")
    tx_hash = create_transaction_example()
    
    print("\n===== TRANSACTION DETAILS =====")
    tx_details = transaction_details_example(tx_hash)
    
    print("\n===== TRANSACTION MONITORING =====")
    confirmations = monitor_transaction_example(tx_hash)
    
    print("\n===== FEE ESTIMATION =====")
    estimated_fee = fee_estimation_example() 