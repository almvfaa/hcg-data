#!/bin/bash

# Establecer variables de entorno
export PYTHONPATH="${PYTHONPATH}:/home/appuser/web"
cd /home/appuser/web

echo "Current PYTHONPATH: $PYTHONPATH"
echo "Current directory: $(pwd)"
echo "Listing directory contents:"
ls -la

# Ejecutar las migraciones de la base de datos
echo "Running database migrations..."
python -m alembic -c alembic.ini upgrade head

# Iniciar el servidor de la aplicación
echo "Starting Gunicorn server..."
python -m gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
