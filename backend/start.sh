#!/bin/bash

# Establecer el directorio de trabajo
cd /home/appuser/web

# Ejecutar las migraciones de la base de datos
echo "Running database migrations..."
PYTHONPATH=/home/appuser/web python -m alembic -c alembic.ini upgrade head

# Iniciar el servidor de la aplicación
echo "Starting Gunicorn server..."
PYTHONPATH=/home/appuser/web python -m gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 backend.main:app
