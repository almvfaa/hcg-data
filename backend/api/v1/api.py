from fastapi import APIRouter

from .endpoints import catalogo, movimientos, clasificador, lab

api_router = APIRouter()

api_router.include_router(catalogo.router, prefix="/catalogo", tags=["catalogo"])
api_router.include_router(movimientos.router, prefix="/movimientos", tags=["movimientos"])
api_router.include_router(clasificador.router, prefix="/clasificador", tags=["clasificador"])
api_router.include_router(lab.router, prefix="/lab", tags=["lab"])
