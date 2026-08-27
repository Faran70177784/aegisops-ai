#!/bin/sh
set -eu

echo "Running database migrations..."
alembic upgrade head

echo "Starting AegisOps AI..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
