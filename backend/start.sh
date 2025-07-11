#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the application directory
APP_DIR="/home/appuser/web"

# Change to the application directory. This is crucial.
cd "$APP_DIR"

echo "--- Running database migrations ---"

# Run Alembic migrations. Since we are now in the correct directory,
# Alembic will find alembic.ini automatically.
alembic upgrade head

echo "--- Migrations complete ---"

echo "--- Starting Gunicorn server ---"

# Start the Gunicorn server.
# Gunicorn will find 'main:app' because we are in the correct directory.
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 "main:app"
