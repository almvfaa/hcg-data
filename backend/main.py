from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.middleware import rate_limit_middleware
from core.exceptions import http_exception_handler
from core.logging import app_logger, log_request, log_error
from starlette.exceptions import HTTPException
import time

app = FastAPI(
    title="HCG Data API",
    description="API para el sistema de gestión de inventario HCG",
    version="1.0.0"
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Rate Limiting
app.middleware("http")(rate_limit_middleware)

# Middleware para logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    await log_request(request)
    start_time = time.time()
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        log_error(e, request)
        raise

# Manejador global de excepciones
app.add_exception_handler(HTTPException, http_exception_handler)

# Router principal
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    app_logger.info("Application starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Application shutting down...")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the HCG Data API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }