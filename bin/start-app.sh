#!/bin/sh

while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

echo "PostgreSQL is up - executing command"
uvicorn src.entrypoint.api_ui:app --host 0.0.0.0 --port 9090
