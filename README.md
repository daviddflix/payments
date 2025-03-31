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

#### Setting Up BlockCypher Webhooks

To set up a webhook with BlockCypher, you can use the `ForwardingManager` class from the BlockCypher provider:

```python
from app.infrastructure.providers.blockcypher.forwarding import ForwardingManager

# Initialize the manager
manager = ForwardingManager(coin_symbol="btc-testnet")

# Create a webhook for an address
webhook = manager.create_address_webhook(
    address="YOUR_ADDRESS_TO_MONITOR",
    url="https://your-domain.com/api/v1/webhooks/payment",
    event_type="unconfirmed-tx"
)

# Create a webhook for transaction confirmations
tx_webhook = manager.create_transaction_webhook(
    transaction_hash="TRANSACTION_HASH_TO_MONITOR",
    url="https://your-domain.com/api/v1/webhooks/payment",
    confirmations=6  # Notify after 6 confirmations
)
```

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

## License

MIT
