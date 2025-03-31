# BlockCypher Provider

This directory contains a comprehensive implementation of the BlockCypher API client for interacting with cryptocurrency networks, including Bitcoin (BTC), Bitcoin Testnet, and BlockCypher's Test Chain (BCY).

## Directory Structure

- **common**: Base classes and shared utilities
- **forwarding**: Address forwarding and webhook functionality
- **transactions**: Transaction creation and validation
- **wallets**: Wallet management functionality
- **webhooks**: Webhook handling
- **utils**: Helper utilities
- **examples**: Example code for each component

## Key Features

- Wallet management (creation, listing, balance checking)
- Transaction processing (creation, signing, broadcasting)
- Address forwarding and webhook setup
- Blockchain information retrieval
- Test utilities for automated testing

## Testing with BlockCypher Test Chain

This package includes comprehensive test utilities that leverage BlockCypher's Test Chain (BCY), which provides a more reliable and predictable test environment compared to public testnets.

### Setup for Testing

1. **Get a BlockCypher API Token**: Create an account at [blockcypher.com](https://www.blockcypher.com/) and obtain an API token.

2. **Set Environment Variables**:
   ```
   export BLOCKCYPHER_API_TOKEN=your_api_token
   export BLOCKCYPHER_LIVE_TEST=true  # Only set this when you want to run integration tests
   ```

3. **Run Tests**:
   - Run unit tests only: `pytest app/infrastructure/providers/blockcypher`
   - Run integration tests: `pytest app/infrastructure/providers/blockcypher/test_integration.py --integration`

### Using the Test Utilities

The package provides test utilities in `utils/test_utils.py` that make it easy to:

1. **Generate Test Addresses**:
   ```python
   from app.infrastructure.providers.blockcypher.utils.test_utils import generate_test_address
   
   # Generate a new address on the BlockCypher test chain
   address_info = generate_test_address(coin_symbol='bcy')
   print(f"Address: {address_info['address']}")
   print(f"Private Key: {address_info['private']}")
   ```

2. **Fund Test Addresses**:
   ```python
   from app.infrastructure.providers.blockcypher.utils.test_utils import fund_test_address
   
   # Fund an address with 100,000 satoshis (0.001 BCY)
   funding_tx = fund_test_address(
       address='your_test_address',
       amount_satoshis=100000,
       coin_symbol='bcy'
   )
   print(f"Funding TX: {funding_tx['tx_hash']}")
   ```

3. **Create Pre-funded Addresses** (combines generation and funding):
   ```python
   from app.infrastructure.providers.blockcypher.utils.test_utils import setup_funded_test_address
   
   # Generate and fund an address in one step
   funded_setup = setup_funded_test_address(coin_symbol='bcy')
   address = funded_setup['address_info']['address']
   private_key = funded_setup['address_info']['private']
   funding_tx_hash = funded_setup['funding_tx']['tx_hash']
   ```

4. **Wait for Transaction Confirmations**:
   ```python
   from app.infrastructure.providers.blockcypher.utils.test_utils import wait_for_confirmation
   
   # Wait for a transaction to be confirmed
   confirmed = wait_for_confirmation(
       tx_hash='transaction_hash',
       coin_symbol='bcy',
       target_confirmations=1
   )
   ```

## Integration Test Classes

The package includes specialized test classes that use the BlockCypher test faucet:

1. **TestTransactionManagerWithFaucet**: Tests real transaction creation, broadcasting, and confirmation
2. **TestWalletManagerWithFaucet**: Tests wallet creation, balance retrieval, and address management
3. **TestBlockCypherIntegration**: Tests the complete flow of wallet creation, transaction sending, and forwarding

## Example Usage

The `examples` directory contains practical examples for each component:

- **wallet_examples.py**: Creating wallets, adding addresses, checking balances
- **transaction_examples.py**: Creating and sending transactions
- **forwarding_examples.py**: Setting up address forwarding and webhooks

## Notes on Test Chain Usage

- The BlockCypher Test Chain (BCY) is more reliable than public testnets for automated testing
- Test chain funds have no real-world value and are provided through the faucet
- Default faucet funding is limited to 0.001 BCY (100,000 satoshis) per request
- The test chain confirms blocks much faster than real networks, making it ideal for quick tests 