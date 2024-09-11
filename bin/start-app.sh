#!/bin/sh

while ! nc -z db 5432; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

while ! nc -z ollama 11434; do
  echo "Waiting for Ollama..."
  sleep 1
done

echo "Satellite services are up - executing command"
uvicorn src.entrypoint.api_ui:app --host 0.0.0.0 --port 9090
