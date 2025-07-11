#!/bin/bash

# Ejecutar las migraciones de la base de datos
echo "Running database migrations..."
alembic upgrade head

# Iniciar el servidor de la aplicación
echo "Starting Gunicorn server..."
gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
