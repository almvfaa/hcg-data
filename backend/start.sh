#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define the application directory
APP_DIR="/home/appuser/web"

# Change to the application directory. This is crucial.
cd "$APP_DIR"

echo "--- Starting Gunicorn server ---"

# Start the Gunicorn server.
# Gunicorn will find 'main:app' because we are in the correct directory.
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 "main:app"

services:
  # Backend FastAPI
  - type: web
    name: hcg-backend
    env: docker
    repo: https://github.com/almvfaa/hcg-data.git
    dockerfilePath: ./backend/Dockerfile
    # ... (tus envVars actuales)

  # Frontend Next.js
  - type: web
    name: hcg-frontend
    # ... (tu configuración de frontend)

jobs:
  # Job para ejecutar migraciones de la base de datos
  - type: job
    name: migrate
    plan: free # o el plan que prefieras
    dockerfilePath: ./backend/Dockerfile
    # El comando a ejecutar para este job
    startCommand: alembic upgrade head
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: hcg-db # El nombre de tu servicio de base de datos en Render
          property: connectionString
      # ... (otras variables que necesite el proceso de migración)
