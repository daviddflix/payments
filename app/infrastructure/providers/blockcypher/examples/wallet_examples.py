"""
Example code for wallet management using BlockCypher.

This module demonstrates common wallet operations using the WalletManager.
"""

from app.infrastructure.providers.blockcypher import WalletManager

def create_wallet_example():
    """Example of creating a wallet."""
    # Initialize the wallet manager
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # Generate a new address
    address_info = wallet_manager.generate_address()
    address = address_info["address"]
    private_key = address_info["private_key"]
    
    print(f"Generated new address: {address}")
    print(f"Private key: {private_key}")
    
    # Create a wallet for this address
    wallet_name = f"wallet-{address[:8]}"
    wallet = wallet_manager.create_wallet(address, wallet_name=wallet_name)
    
    print(f"Created wallet: {wallet_name}")
    
    return wallet_name, address

def wallet_operations_example(wallet_name, address):
    """Example of common wallet operations."""
    # Initialize the wallet manager
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # Get wallet details
    wallet_info = wallet_manager.get_wallet(wallet_name)
    print(f"Wallet info: {wallet_info}")
    
    # Generate a new address in the wallet
    new_address = wallet_manager.generate_address_in_wallet(wallet_name)
    print(f"Generated new address in wallet: {new_address}")
    
    # Get wallet balance
    balance = wallet_manager.get_wallet_balance(address)
    print(f"Wallet balance: {balance} BTC")
    
    # Get wallet transactions
    transactions = wallet_manager.get_wallet_transactions(address, limit=5)
    print(f"Recent transactions: {len(transactions)}")
    
    return new_address["address"] if isinstance(new_address, dict) else None

def multisig_wallet_example():
    """Example of creating a multi-signature wallet."""
    # Initialize the wallet manager
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # Generate addresses for the multi-signature wallet
    address1 = wallet_manager.generate_address()
    address2 = wallet_manager.generate_address()
    address3 = wallet_manager.generate_address()
    
    # Extract public keys
    pubkey1 = address1["public_key"]
    pubkey2 = address2["public_key"]
    pubkey3 = address3["public_key"]
    
    # Create a 2-of-3 multisig wallet
    multisig_wallet = wallet_manager.create_multisig_wallet(
        [pubkey1, pubkey2, pubkey3], 
        script_type="multisig-2-of-3"
    )
    
    print(f"Created multisig wallet: {multisig_wallet}")
    print(f"Multisig address: {multisig_wallet.get('address')}")
    
    return multisig_wallet

def list_wallets_example():
    """Example of listing wallets."""
    # Initialize the wallet manager
    wallet_manager = WalletManager(coin_symbol="btc-testnet")
    
    # List all wallets
    wallets = wallet_manager.list_wallets()
    print(f"Found {len(wallets)} wallets:")
    
    for wallet in wallets:
        print(f"- Wallet: {wallet.get('name')}")
        print(f"  Addresses: {len(wallet.get('addresses', []))}")
    
    return wallets

if __name__ == "__main__":
    import time
    
    print("\n===== WALLET CREATION =====")
    wallet_name, address = create_wallet_example()
    
    time.sleep(1)  # Give the API a moment
    
    print("\n===== WALLET OPERATIONS =====")
    new_address = wallet_operations_example(wallet_name, address)
    
    print("\n===== MULTISIG WALLET =====")
    multisig_wallet = multisig_wallet_example()
    
    print("\n===== LIST WALLETS =====")
    wallets = list_wallets_example() 