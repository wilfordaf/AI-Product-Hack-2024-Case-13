#!/bin/bash

/bin/ollama serve &
pid=$!

sleep 5

echo "🔴 Retrieve model..."
ollama pull jpacifico/chocolatine-3b
echo "🟢 Done!"

wait $pid