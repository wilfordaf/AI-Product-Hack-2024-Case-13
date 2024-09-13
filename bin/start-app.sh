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
python3 /root/src/src/src/entrypoint/entrypoint.py
