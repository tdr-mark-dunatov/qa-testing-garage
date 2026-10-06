# 🏁 Webhook Pitstop Backend - Docker Image
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to not create virtual env (we're in Docker)
RUN poetry config virtualenvs.create false

# Generate lock file if missing, then install dependencies
RUN if [ ! -f poetry.lock ]; then poetry lock --no-update; fi && \
    poetry install --no-interaction --no-ansi --no-root --only main

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
