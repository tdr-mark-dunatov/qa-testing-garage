# 🏁 Webhook Pitstop API

FastAPI backend with WebSockets for real-time webhook inspection.

## Setup

### With Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Run development server
poetry run uvicorn main:app --reload

# Add a new dependency
poetry add package-name

# Add a dev dependency
poetry add --group dev package-name
```

### Alternative: pip (if Poetry not available)

```bash
# Generate requirements.txt from Poetry
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install with pip
pip install -r requirements.txt
```

## API Endpoints

- **GET /** - Welcome message
- **GET /health** - Health check
- **POST /api/pit/new** - Create new pit lane (webhook URL)
- **ALL /pit/{pit_id}** - Webhook capture endpoint
- **GET /api/pit/{pit_id}/requests** - Get captured requests
- **GET /api/pit/{pit_id}/diagnostics** - Get performance metrics
- **DELETE /api/pit/{pit_id}/requests** - Clear requests
- **WS /ws/{pit_id}** - WebSocket for real-time updates

## Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

Default: SQLite (`data/pitstop.db`)

To use PostgreSQL, set environment variable:
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/webhooks
```

## Development

```bash
# Run with auto-reload
poetry run uvicorn main:app --reload

# Run with custom port
poetry run uvicorn main:app --reload --port 9000

# Run tests (when available)
poetry run pytest
```

## Docker

```bash
# Build image
docker build -t webhook-pitstop-api .

# Run container
docker run -p 8000:8000 webhook-pitstop-api
```
