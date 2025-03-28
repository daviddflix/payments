# Payment Gateway

A modern payment gateway supporting both traditional banking and cryptocurrency payments, with initial support for Bitcoin.

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Data Validation**: Pydantic
- **Cryptocurrency Integration**: BlockCypher API
- **Architecture**: Domain-Driven Design (DDD)
- **Containerization**: Docker & Docker Compose

## Features (MVP)

- User authentication and authorization
- Bitcoin wallet management
- Payment processing
- Transaction history
- Basic error handling

## Project Structure

```
payment-gateway/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configuration
│   ├── domain/         # Domain models and business logic
│   ├── infrastructure/ # External services integration
│   └── services/       # Application services
├── tests/              # Test files
├── alembic/            # Database migrations
├── requirements.txt    # Project dependencies
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
pip install -r requirements.txt
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

## Security Considerations

### Environment Variables

1. Never commit the `.env` file to version control
2. Use strong, unique values for sensitive variables:
   - `JWT_SECRET_KEY`: Use a cryptographically secure random string
   - `POSTGRES_PASSWORD`: Use a strong password
   - `BLOCKCYPHER_TOKEN`: Use your BlockCypher API token

3. In production:
   - Use a secrets management service
   - Rotate secrets regularly
   - Use different values for development and production

### Docker Security

1. The application runs as a non-root user inside the container
2. Database credentials are managed through environment variables
3. Network isolation is implemented using Docker networks
4. Sensitive data is stored in Docker volumes

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

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
