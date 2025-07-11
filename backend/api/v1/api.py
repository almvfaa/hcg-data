from fastapi import APIRouter

# Import all the endpoint routers
from .endpoints import catalogo, movimientos, clasificador, lab, tasks

api_router = APIRouter()

# Include each router with a specific prefix and tags for organization
api_router.include_router(catalogo.router, prefix="/catalogo", tags=["catalogo"])
api_router.include_router(movimientos.router, prefix="/movimientos", tags=["movimientos"])
api_router.include_router(clasificador.router, prefix="/clasificador", tags=["clasificador"])
api_router.include_router(lab.router, prefix="/lab", tags=["lab"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"]) # <-- New router for tasks
