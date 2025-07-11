from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .dependencies import get_db
from crud import crud_articulo
from schemas import articulo as sc_articulo

router = APIRouter()

@router.get("/articulos", response_model=list[sc_articulo.Articulo])
def read_articulos(
    skip: int = Query(0, description="Número de registros a omitir"),
    limit: int = Query(100, description="Número máximo de registros a retornar", alias="pageSize"),
    search: str | None = Query(None, description="Término de búsqueda en la descripción"),
    db: Session = Depends(get_db)
):
    total, articulos = crud_articulo.get_articulos(db, skip=skip, limit=limit, search=search)
    return articulos