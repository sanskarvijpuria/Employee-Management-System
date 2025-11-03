#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Running database initializations..."
flask --app app/run.py init-db

exec "$@"
