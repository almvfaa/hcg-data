#!/bin/bash

# Ejecutar las migraciones de la base de datos
# Se usa -c para especificar la ruta del archivo de configuración de alembic
echo "Running database migrations..."
python -m alembic -c alembic.ini upgrade head

# Iniciar el servidor de la aplicación usando python -m gunicorn
# Esto asegura que las rutas de importación de Python se resuelvan correctamente
echo "Starting Gunicorn server..."
python -m gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 main:app
