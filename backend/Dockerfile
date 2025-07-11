# Usar imagen oficial de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Crear un usuario y grupo no privilegiado
RUN addgroup --system app && adduser --system --group app

# Copiar e instalar dependencias primero para caché
# We only copy and install production requirements into the final image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer puerto 8000
EXPOSE 8000

# Cambiar al usuario no privilegiado
USER app

# Comando para iniciar la aplicación con Gunicorn en producción
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
