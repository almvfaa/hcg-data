from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..dependencies import get_db
from schemas import clasificador as sc_clasificador
from crud import crud_clasificador

router = APIRouter()

@router.get("/capitulos", response_model=list[sc_clasificador.Capitulo])
def read_capitulos(
    search: str = Query(None, alias="search"),
    db: Session = Depends(get_db)
):
    capitulos = crud_clasificador.get_capitulos(db, search=search)
    return capitulos

@router.get("/conceptos", response_model=list[sc_clasificador.Concepto])
def read_conceptos(
    search: str = Query(None, alias="search"),
    db: Session = Depends(get_db)
):
    conceptos = crud_clasificador.get_conceptos(db, search=search)
    return conceptos

@router.get("/partidas-genericas", response_model=list[sc_clasificador.PartidaGenerica])
def read_partidas_genericas(
    search: str = Query(None, alias="search"),
    db: Session = Depends(get_db)
):
    partidas_genericas = crud_clasificador.get_partidas_genericas(db, search=search)
    return partidas_genericas

@router.get("/partidas-especificas", response_model=list[sc_clasificador.PartidaEspecifica])
def read_partidas_especificas(
    search: str = Query(None, alias="search"),
    db: Session = Depends(get_db)
):
    partidas_especificas = crud_clasificador.get_partidas_especificas(db, search=search)
    return partidas_especificas