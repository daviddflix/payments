#!/bin/bash
set -e

# This script creates a PostgreSQL database named 'payment_gateway' if it doesn't already exist
# and grants all permissions to the postgres user
create_db() {
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
        SELECT 'CREATE DATABASE payment_gateway'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'payment_gateway')\gexec
        GRANT ALL PRIVILEGES ON DATABASE payment_gateway TO postgres;
EOSQL
}

# Create the database
create_db 