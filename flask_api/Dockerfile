# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# System deps (kept minimal because we use psycopg2-binary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy app
COPY . /app

EXPOSE 8000

# Default command runs the app via gunicorn; docker-compose will wait for DB first
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:create_app()"]