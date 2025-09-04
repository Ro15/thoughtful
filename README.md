# Thoughtful

This repository contains a simple data ingestion example using SQLAlchemy and
WebSocket/REST clients.

## Data Ingestion

The `data` package exposes a `ProviderClient` capable of:

- Connecting to a WebSocket for streaming underlying price ticks.
- Querying a REST endpoint for option chain data.
- Persisting the received information into SQLite or PostgreSQL via SQLAlchemy.

See `data/ingestion.py` for an example entrypoint.
