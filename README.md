# Payment Gateway

A modern payment gateway supporting both traditional banking and cryptocurrency payments, with initial support for Bitcoin.

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Data Validation**: Pydantic
- **Cryptocurrency Integration**: BlockCypher API
  - Supported Networks:
    - Bitcoin (BTC) - Mainnet & Testnet
    - Litecoin (LTC)
    - Dogecoin (DOGE)
    - Dash (DASH)
- **Architecture**: Domain-Driven Design (DDD)
- **Containerization**: Docker & Docker Compose

## Features (MVP)

- User authentication and authorization
- Multi-cryptocurrency wallet management
  - Bitcoin (BTC)
  - Litecoin (LTC)
  - Dogecoin (DOGE)
  - Dash (DASH)
- Payment processing across supported networks
- Transaction history and monitoring
- Network-specific transaction status tracking
- Basic error handling

## Project Structure

```
payment-gateway/
├── app/
│   ├── api/            # API endpoints
│   │   └── v1/         # API version 1
│   ├── core/           # Core configuration
│   ├── domain/         # Domain models and business logic
│   ├── infrastructure/ # External services integration
│   │   └── providers/  # External service providers
│   │       └── blockcypher/  # BlockCypher API integration
│   │           ├── common/       # Shared utilities and base classes
│   │           ├── forwarding/   # Address forwarding and webhook management
│   │           ├── transactions/ # Transaction creation and validation
│   │           ├── wallets/      # Wallet management
│   │           ├── utils/        # Helper utilities
│   │           ├── webhooks/     # Webhook handlers
│   │           └── examples/     # Example usage of components
│   └── services/       # Application services
├── tests/              # Test files
├── alembic/            # Database migrations
├── pyproject.toml      # Project configuration and dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
├── .env.example       # Environment variables template
└── README.md          # Project documentation
```

## Setup

### Option 1: Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

### Option 2: Docker Development

1. Make sure you have Docker and Docker Compose installed on your system.

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. To stop the containers:
```bash
docker-compose down
```

5. To view logs:
```bash
docker-compose logs -f
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

The API is versioned using URL prefixes:
- Version 1: `/api/v1`

## BlockCypher API Integration

This project includes a comprehensive integration with the BlockCypher API for cryptocurrency wallet management and transaction processing.

### Features

#### Wallet Management
- Create and manage standard and HD wallets
- Generate addresses and retrieve wallet information
- Handle multisignature addresses and transactions
- View wallet balances and transactions

#### Transaction Management
- Query transaction details by hash
- View unconfirmed transactions
- Create, sign, and broadcast transactions
- Work with raw transactions (decode/encode)
- Support for multisignature transactions
- Transaction confidence tracking

#### Address Forwarding
- Automatically forward cryptocurrency payments to destination addresses
- Set up notifications for blockchain events (transactions, confirmations)
- WebSocket support for real-time monitoring of blockchain events

### Environment Variables

Create a `.env` file in your project root with the following variables:
```
BLOCKCYPHER_API_TOKEN=your_blockcypher_api_token
```

You can obtain an API token by registering at [BlockCypher's website](https://www.blockcypher.com/).

### Usage Examples

#### Wallet Management

```python
from app.infrastructure.providers.blockcypher import WalletManager

# Create a wallet manager for Bitcoin testnet
wallet_manager = WalletManager(coin_symbol="btc-testnet")

# Create a new wallet
wallet = wallet_manager.create_wallet("my_test_wallet")
print(f"Wallet Name: {wallet['name']}")
print(f"Wallet Addresses: {wallet['addresses']}")

# Generate a new address for the wallet
address = wallet_manager.generate_address_in_wallet("my_test_wallet")
print(f"New Address: {address['address']}")

# Get wallet balance
balance = wallet_manager.get_wallet_balance("my_test_wallet")
print(f"Total Balance: {balance} BTC")
```

#### Transaction Management

```python
from app.infrastructure.providers.blockcypher import TransactionManager

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
private_key = "your_private_key"  # Keep this secure!

# Create and broadcast a transaction
tx_result = tx_manager.create_and_sign_transaction(
    from_address=from_address,
    to_address=to_address,
    amount_satoshis=amount_satoshis,
    private_key=private_key
)
print(f"Transaction created: {tx_result['tx_hash']}")
```

#### Address Forwarding and Webhooks

```python
from app.infrastructure.providers.blockcypher import ForwardingManager

# Initialize the manager
manager = ForwardingManager(coin_symbol="btc-testnet")

# Create a forwarding address
forwarding = manager.create_forwarding_address(
    destination="YOUR_DESTINATION_ADDRESS",
    callback_url="https://your-app.com/api/v1/webhooks/payment"
)

# The forwarding details
input_address = forwarding.get('input_address')
print(f"Share this address with customers: {input_address}")
print(f"Payments to this address will be forwarded to your destination")

# Monitor an address for new unconfirmed transactions
webhook = manager.create_address_webhook(
    address="ADDRESS_TO_MONITOR",
    url="https://your-app.com/api/v1/webhooks/payment",
    event_type="unconfirmed-tx"
)

# Monitor a transaction for confirmations
tx_webhook = manager.create_transaction_webhook(
    transaction_hash="TX_HASH_TO_MONITOR",
    url="https://your-app.com/api/v1/webhooks/payment",
    confirmations=6  # Notify after 6 confirmations
)
```

#### WebSockets

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

### Webhook API (v1)

The payment gateway includes webhook endpoints for receiving and processing cryptocurrency transaction notifications from BlockCypher.

#### Webhook Endpoints

##### POST `/api/v1/webhooks/payment`

Receives webhook callbacks from BlockCypher for cryptocurrency transactions. This endpoint handles:

- Unconfirmed transactions
- Transaction confirmations
- Double-spend detections

**Usage with BlockCypher:**

When creating a webhook with BlockCypher's API, use this URL as the callback URL:

```
https://your-domain.com/api/v1/webhooks/payment
```

**Example request body** (sent by BlockCypher):

```json
{
  "event": "unconfirmed-tx",
  "address": "mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS",
  "hash": "7d067bf6a89f4b1407a14a6704447f8e5e2ac5cfc0fd6395a4eb56cb6b7e6f40",
  "confirmations": 0,
  "outputs": [
    {
      "addresses": ["mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS"],
      "value": 1500000
    }
  ]
}
```

**Response:**

```json
{
  "received": true,
  "tx_hash": "7d067bf6a89f4b1407a14a6704447f8e5e2ac5cfc0fd6395a4eb56cb6b7e6f40",
  "event": "unconfirmed-tx",
  "value_satoshis": 1500000
}
```

##### GET `/api/v1/webhooks/transactions/{tx_hash}`

Retrieves information about a transaction that was previously received via webhook.

**Parameters:**
- `tx_hash`: The transaction hash to look up

**Response:**

```json
{
  "address": "mwAjEY8t6HFVUrdnRfikV3Pg68AQ6uKxeS",
  "value_satoshis": 1500000,
  "value_btc": 0.015,
  "confirmations": 2,
  "status": "unconfirmed",
  "timestamp": "2023-03-31T02:50:12.345678",
  "tx_hash": "7d067bf6a89f4b1407a14a6704447f8e5e2ac5cfc0fd6395a4eb56cb6b7e6f40"
}
```

##### POST `/api/v1/webhooks/simulate` (Development Only)

Simulates a webhook callback for testing purposes. This endpoint should be disabled in production.

**Query Parameters:**
- `event_type`: Type of event to simulate (default: "unconfirmed-tx")
- `address`: Optional address to use in the simulation
- `confirmations`: Number of confirmations for tx-confirmation events (default: 1)

## Testing with BlockCypher Test Chain

The project includes comprehensive test utilities that leverage BlockCypher's Test Chain (BCY), which provides a more reliable and predictable test environment compared to public testnets.

### Setup for Testing

1. **Get a BlockCypher API Token**: Create an account at [blockcypher.com](https://www.blockcypher.com/) and obtain an API token.

2. **Set Environment Variables**:
   ```bash
   export BLOCKCYPHER_API_TOKEN=your_api_token
   # On Windows: set BLOCKCYPHER_API_TOKEN=your_api_token
   ```

### Running Tests

The payment gateway has several test suites with different purposes:

#### Unit Tests

Run unit tests (no API calls to BlockCypher) with:

```bash
# Run all tests with mocked API calls
python -m pytest app/infrastructure/providers/blockcypher
```

#### Integration Tests

Integration tests make real API calls to the BlockCypher test chain. These require:
- A valid BlockCypher API token
- The `BLOCKCYPHER_LIVE_TEST` environment variable to be set to `true`

```bash
# Set the environment variable
export BLOCKCYPHER_LIVE_TEST=true
# On Windows: set BLOCKCYPHER_LIVE_TEST=true

# Run the integration tests
python -m pytest app/infrastructure/providers/blockcypher/test_integration.py -v
```

#### Testing Specific Components

```bash
# Test only the transaction manager
python -m pytest app/infrastructure/providers/blockcypher/transactions/test_transaction_manager.py -v

# Test only the wallet manager
python -m pytest app/infrastructure/providers/blockcypher/wallets/test_wallet_manager.py -v

# Test only the forwarding manager
python -m pytest app/infrastructure/providers/blockcypher/forwarding/test_forwarding_manager.py -v
```

#### Debugging Test Failures

If tests fail, you can use the `-vv` flag for more verbose output:

```bash
python -m pytest app/infrastructure/providers/blockcypher -vv
```

For even more detailed output, use:

```bash
python -m pytest app/infrastructure/providers/blockcypher -vv --log-cli-level=DEBUG
```

### Rate Limits and Test Chain Usage

BlockCypher's test chain has rate limits:

- API requests are limited to 200 per hour and 3 per second
- Faucet funding is limited to 0.001 BCY (100,000 satoshis) per request
- Running full test suites frequently may result in rate limit errors

If you encounter rate limit errors, wait an hour before trying again or reduce the scope of your testing to specific components.

### Test Utilities

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

### Integration Test Classes

The package includes specialized test classes that use the BlockCypher test faucet:

1. **TestTransactionManagerWithFaucet**: Tests real transaction creation, broadcasting, and confirmation
2. **TestWalletManagerWithFaucet**: Tests wallet creation, balance retrieval, and address management
3. **TestBlockCypherIntegration**: Tests the complete flow of wallet creation, transaction sending, and forwarding

### Advantages of BlockCypher Test Chain

- More reliable than public testnets for automated testing
- Test chain funds have no real-world value and are provided through the faucet
- Default faucet funding is limited to 0.001 BCY (100,000 satoshis) per request
- The test chain confirms blocks much faster than real networks, making it ideal for quick tests

## Security Considerations

### Environment Variables

1. Never commit the `.env` file to version control
2. Use strong, unique values for sensitive variables:
   - `JWT_SECRET_KEY`: Use a cryptographically secure random string
   - `POSTGRES_PASSWORD`: Use a strong password
   - `BLOCKCYPHER_TOKEN`: Use your BlockCypher API token
   - `WEBHOOK_SECRET`: Use a strong secret for webhook signature verification

3. In production:
   - Use a secrets management service
   - Rotate secrets regularly
   - Use different values for development and production

### Docker Security

1. The application runs as a non-root user inside the container
2. Database credentials are managed through environment variables
3. Network isolation is implemented using Docker networks
4. Sensitive data is stored in Docker volumes

### Cryptocurrency Security

1. **NEVER** hardcode private keys in your application
2. Always keep private keys secure and preferably offline
3. Use environment variables for sensitive information
4. Consider using hardware wallets for production environments
5. Test thoroughly on testnet before moving to mainnet

### Webhook Security

1. **Webhook Signature Verification:** Enable signature verification in the webhook handler to ensure requests are coming from BlockCypher.
2. **Use HTTPS:** Always use HTTPS for webhook endpoints to ensure secure data transmission.
3. **Rate Limiting:** Implement rate limiting to protect against DoS attacks.
4. **Idempotency:** Ensure webhook processing is idempotent to handle potential duplicate webhook deliveries.
5. **Logging:** Implement comprehensive logging for webhook events for debugging and audit purposes.

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use conventional commits

## Docker Commands Reference

```bash
# Build and start containers
docker-compose up --build

# Start containers in detached mode
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f

# Rebuild a specific service
docker-compose up -d --build web

# Access PostgreSQL CLI
docker-compose exec db psql -U postgres -d payment_gateway

# Run migrations manually
docker-compose exec web alembic upgrade head
```

## Development and Debugging

### Environment Setup

1. **Install Required Packages**:
   For development, install additional packages for testing and debugging:
   ```bash
   pip install pytest pytest-cov ipython
   ```

2. **IDE Configuration**:
   - For VS Code, create a `.vscode/launch.json` file for debugging
   - For PyCharm, set up a Run Configuration with environment variables

### Common Issues and Solutions

#### BlockCypher API Issues

1. **Rate Limiting**: 
   If you encounter HTTP 429 errors, you've hit the rate limit. Wait an hour or reduce testing frequency.

2. **Authentication Failed**: 
   Check your API token is set correctly in the environment variables.

3. **Invalid Address Format**: 
   Ensure addresses match the expected format for the specific network (Bitcoin, Litecoin, etc.).

4. **Transaction Creation Failures**:
   - Insufficient balance: Check address balance before creating transactions
   - Invalid inputs/outputs: Ensure transaction parameters are correct
   - Dust limit: Transaction outputs must be above the dust limit (typically 546 satoshis)

#### Webhook Testing

1. **Local Testing**:
   - Use a service like ngrok to expose your local server for webhook testing
   - Use the simulate webhook endpoint for local development

2. **Verifying Webhook Signatures**:
   ```python
   from app.infrastructure.providers.blockcypher.webhooks.handler import verify_webhook_signature
   
   # In your webhook handling code
   is_valid = verify_webhook_signature(
       request_data=request.body,             # Raw request body
       signature=request.headers.get('X-Signature', ''),
       webhook_secret='your_webhook_secret'   # From environment variables
   )
   
   if not is_valid:
       return {"error": "Invalid signature"}, 401
   ```

3. **Webhook Timeouts**:
   BlockCypher expects a 200 response within 5 seconds. Keep webhook handlers lightweight.

### Development Best Practices

1. **Code Style**:
   - Run linting before committing: `flake8 app tests`
   - Format code with black: `black app tests`

2. **Test Coverage**:
   - Generate coverage reports: `pytest --cov=app tests/`
   - Aim for at least 80% coverage for new code

3. **Commit Guidelines**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/) format
   - Example: `feat(wallet): add multi-signature support`

4. **Documentation**:
   - Document public methods and classes with docstrings
   - Update README when adding significant features
   - Include examples for new functionality

## License

Proprietary. All rights reserved.

This software is the confidential and proprietary information of the copyright holder.
Unauthorized copying, transferring, or reproduction of this software, in any medium, 
is strictly prohibited.
