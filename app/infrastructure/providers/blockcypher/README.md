# BlockCypher API Integration

This module provides a comprehensive integration with the BlockCypher API for cryptocurrency transactions and wallet management.

## Features

### Wallet Management
- Create and manage standard and HD wallets
- Generate addresses and retrieve wallet information
- Handle multisignature addresses and transactions
- View wallet balances and transactions

### Transaction Management
- Query transaction details by hash
- View unconfirmed transactions
- Create, sign, and broadcast transactions
- Work with raw transactions (decode/encode)
- Support for multisignature transactions
- Transaction confidence tracking

## Setup

### Requirements
- Python 3.6+
- Required packages: `requests`, `python-dotenv`

### Environment Variables
Create a `.env` file in your project root with the following variables:
```
BLOCKCYPHER_API_TOKEN=your_blockcypher_api_token
```

You can obtain an API token by registering at [BlockCypher's website](https://www.blockcypher.com/).

## Usage Examples

### Wallet Management

```python
from app.infrastructure.providers.blockcypher.wallet import WalletManager

# Create a wallet manager for Bitcoin testnet
wallet_manager = WalletManager(coin_symbol="btc-testnet")

# Create a new wallet
wallet = wallet_manager.create_wallet("my_test_wallet")
print(f"Wallet Name: {wallet['name']}")
print(f"Wallet Addresses: {wallet['addresses']}")

# Generate a new address for the wallet
address = wallet_manager.generate_address("my_test_wallet")
print(f"New Address: {address['address']}")

# Get wallet balance
balance = wallet_manager.get_wallet_balance("my_test_wallet")
print(f"Total Balance: {balance['final_balance'] / 100000000} BTC")
```

### Transaction Management

```python
from app.infrastructure.providers.blockcypher.transaction import TransactionManager

# Create a transaction manager for Bitcoin testnet
tx_manager = TransactionManager(coin_symbol="btc-testnet")

# Get transaction details
tx_hash = "your_transaction_hash"
tx_details = tx_manager.get_transaction(tx_hash)
print(f"Transaction Hash: {tx_details['hash']}")
print(f"Confirmations: {tx_details.get('confirmations', 0)}")

# Create a simple transaction
from_address = "your_source_address" 
to_address = "destination_address"
amount_satoshis = 1000000  # 0.01 BTC

# Create transaction without signing (returns a skeleton)
tx_skeleton = tx_manager.simple_transaction(
    from_address=from_address,
    to_address=to_address,
    amount_satoshis=amount_satoshis,
    private_key=None  # Set to None to skip signing and broadcasting
)

# In production, you would sign with the private key client-side
# Then broadcast the signed transaction
```

### Multisignature Transactions

```python
# Create a 2-of-3 multisig transaction
multisig_address = "your_multisig_address"
pubkeys = [
    "public_key1",
    "public_key2", 
    "public_key3"
]
to_address = "destination_address"
amount_satoshis = 1000000  # 0.01 BTC

# Create transaction skeleton
tx_skeleton = tx_manager.create_multisig_transaction(
    from_address=multisig_address,
    to_address=to_address,
    amount_satoshis=amount_satoshis,
    pubkeys=pubkeys,
    script_type="multisig-2-of-3"
)

# Each party would sign their portion offline
# Once you have enough signatures, you can broadcast
```

## Notes on Security

- **NEVER** hardcode private keys in your application
- Always keep private keys secure and preferably offline
- Use environment variables for sensitive information
- Consider using hardware wallets for production environments
- Test thoroughly on testnet before moving to mainnet

## Supported Cryptocurrencies

- Bitcoin (BTC) - Main network and Testnet
- Litecoin (LTC)
- Dogecoin (DOGE)
- Dash
- BlockCypher Test (BCY)

# BlockCypher Payment Integration

This directory contains the implementation of payment functionality using the BlockCypher API for blockchain interactions.

## Features

- **Address Forwarding**: Automatically forward cryptocurrency payments to destination addresses
- **Webhook Integration**: Set up notifications for blockchain events (transactions, confirmations, etc.)
- **WebSocket Support**: Real-time monitoring of blockchain events
- **Support for Multiple Cryptocurrencies**: Bitcoin, Ethereum, and more (via BlockCypher API)

## Files

- `forwarding.py`: Contains the ForwardingManager class for handling address forwarding and webhooks
- `test_forwarding.py`: Unit tests for the ForwardingManager class
- `forwarding_example.py`: Example usage of the ForwardingManager class

## Usage

### Requirements

- Python 3.6+
- BlockCypher API token (get one for free at [https://accounts.blockcypher.com/](https://accounts.blockcypher.com/))

### Setting Up

1. Install required dependencies:
   ```
   pip install requests python-dotenv
   ```

2. Set your BlockCypher API token as an environment variable or in a `.env` file:
   ```
   BLOCKCYPHER_TOKEN=your_api_token_here
   ```

### Example: Address Forwarding

Address forwarding allows you to create addresses that automatically forward funds to your destination address.

```python
from forwarding import ForwardingManager

# Initialize the manager (defaults to Bitcoin testnet)
manager = ForwardingManager(coin_symbol="btc-testnet")

# Create a forwarding address
forwarding = manager.create_forwarding_address(
    destination_address="YOUR_DESTINATION_ADDRESS",
    callback_url="https://your-app.com/payment/callback"
)

# The forwarding details
input_address = forwarding.get('input_address')
forwarding_id = forwarding.get('id')

print(f"Share this address with customers: {input_address}")
print(f"Payments to this address will be forwarded to your destination")
```

### Example: Webhooks

Webhooks allow you to receive notifications about blockchain events.

```python
from forwarding import ForwardingManager

# Initialize the manager
manager = ForwardingManager(coin_symbol="btc-testnet")

# Monitor an address for new unconfirmed transactions
webhook = manager.create_address_webhook(
    address="ADDRESS_TO_MONITOR",
    url="https://your-app.com/webhook/callback",
    event_type="unconfirmed-tx"  # Options: "unconfirmed-tx", "confirmed-tx", "tx-confirmation"
)

# Monitor a transaction for confirmations
tx_webhook = manager.create_transaction_webhook(
    transaction_hash="TX_HASH_TO_MONITOR",
    url="https://your-app.com/webhook/tx_confirmed",
    confirmations=6  # Notify after 6 confirmations
)

# List all active webhooks
webhooks = manager.list_webhooks()
```

### Example: WebSockets

WebSockets provide real-time updates for blockchain events.

```javascript
// JavaScript code to use with WebSockets
const wsUrl = "wss://socket.blockcypher.com/v1/btc/test3";
const socket = new WebSocket(wsUrl);

socket.onopen = function() {
  // Subscribe to events for an address
  socket.send(JSON.stringify({
    'event': 'unconfirmed-tx',
    'address': 'YOUR_ADDRESS_HERE'
  }));
};

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received event:', data);
};
```

## Running Examples

To run the example file:

```
cd app/infrastructure/providers/blockcypher
python forwarding_example.py
```

Note: The example file has most API calls commented out to prevent accidental creation. Uncomment the relevant sections to actually execute the API calls.

## Running Tests

To run the unit tests:

```
cd app/infrastructure/providers/blockcypher
python -m unittest test_forwarding.py
```

## Production Considerations

- For production use, switch from testnet to mainnet by using `coin_symbol="btc"` instead of `"btc-testnet"`
- Secure your API token and never expose it in client-side code
- Implement webhook verification to ensure callbacks are legitimate
- Consider implementing retry logic for API calls
- Monitor your API usage to stay within BlockCypher's rate limits

## Documentation

For more details on the BlockCypher API:
- [BlockCypher API Documentation](https://www.blockcypher.com/dev/bitcoin/)
- [Address Forwarding Documentation](https://www.blockcypher.com/dev/bitcoin/#forward-endpoints)
- [Webhook Documentation](https://www.blockcypher.com/dev/bitcoin/#webhook-endpoints) 