import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional
from fastapi import Request
import json
from datetime import datetime

# Configuración base del logger
def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) -> logging.Logger:
    """
    Configura y devuelve un logger con el formato y nivel especificados
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(format)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo si se especifica
    if log_file:
        log_path = Path("logs")
        log_path.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_path / log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Logger principal de la aplicación
app_logger = setup_logger("hcg_data", "app.log")

# Logger para accesos
access_logger = setup_logger(
    "hcg_data.access",
    "access.log",
    format='%(message)s'
)

# Logger para errores
error_logger = setup_logger(
    "hcg_data.error",
    "error.log",
    level=logging.ERROR
)

async def log_request(request: Request) -> None:
    """
    Registra información detallada de cada solicitud
    """
    timestamp = datetime.utcnow().isoformat()
    log_data = {
        "timestamp": timestamp,
        "client_ip": request.client.host if request.client else "unknown",
        "method": request.method,
        "path": request.url.path,
        "query_params": str(request.query_params),
        "headers": dict(request.headers)
    }
    
    access_logger.info(json.dumps(log_data))

def log_error(error: Exception, request: Optional[Request] = None) -> None:
    """
    Registra errores con contexto adicional si está disponible
    """
    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
    }
    
    if request:
        error_data.update({
            "path": request.url.path,
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        })
    
    error_logger.error(json.dumps(error_data))
