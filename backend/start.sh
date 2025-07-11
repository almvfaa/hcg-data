#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the application directory
APP_DIR="/home/appuser/web"

# Change to the application directory
cd "$APP_DIR"

echo "--- Running database migrations ---"

# Run Alembic migrations. The -c flag specifies the config file path.
# This ensures Alembic can find its configuration regardless of where the script is called from.
alembic -c "$APP_DIR/alembic.ini" upgrade head

echo "--- Migrations complete ---"

echo "--- Starting Gunicorn server ---"

# Start the Gunicorn server.
# -w: Number of worker processes
# -k: The type of worker to use (Uvicorn for FastAPI)
# -b: The address and port to bind to
# The last argument is the application instance to run.
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 "main:app"
