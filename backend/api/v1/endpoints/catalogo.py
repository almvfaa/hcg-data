from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from backend.db.session import get_db
from backend.crud import crud_articulo
from backend.schemas import articulo as sc_articulo

router = APIRouter()

@router.post(
    "/articulos",
    response_model=sc_articulo.Articulo,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo artículo"
)
def create_new_articulo(
    articulo: sc_articulo.ArticuloCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo artículo en la base de datos.
    - **articulo**: Objeto con los datos del artículo a crear.
    """
    db_articulo = crud_articulo.get_articulo(db, codigo_articulo=articulo.codigo_articulo)
    if db_articulo:
        raise HTTPException(
            status_code=400,
            detail="Un artículo con este código ya existe."
        )
    return crud_articulo.create_articulo(db=db, articulo=articulo)

@router.get(
    "/articulos",
    response_model=List[sc_articulo.Articulo],
    summary="Leer una lista de artículos"
)
def read_articulos_list(
    skip: int = Query(0, description="Número de registros a omitir"),
    limit: int = Query(100, description="Número máximo de registros a retornar"),
    search: str | None = Query(None, description="Término de búsqueda en la descripción"),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada y filtrable de artículos.
    """
    total, articulos = crud_articulo.get_articulos(db, skip=skip, limit=limit, search=search)
    return articulos

@router.get(
    "/articulos/{codigo_articulo}",
    response_model=sc_articulo.Articulo,
    summary="Leer un artículo por su código"
)
def read_single_articulo(codigo_articulo: str, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de un artículo específico por su `codigo_articulo`.
    """
    db_articulo = crud_articulo.get_articulo(db, codigo_articulo=codigo_articulo)
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return db_articulo

@router.put(
    "/articulos/{codigo_articulo}",
    response_model=sc_articulo.Articulo,
    summary="Actualizar un artículo existente"
)
def update_existing_articulo(
    codigo_articulo: str,
    articulo: sc_articulo.ArticuloUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza los campos de un artículo existente.
    - **codigo_articulo**: El código del artículo a actualizar.
    - **articulo**: Objeto con los campos a actualizar. Solo se modificarán los campos presentes en el request.
    """
    db_articulo = crud_articulo.update_articulo(db, codigo_articulo=codigo_articulo, articulo=articulo)
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return db_articulo

@router.delete(
    "/articulos/{codigo_articulo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un artículo"
)
def delete_existing_articulo(codigo_articulo: str, db: Session = Depends(get_db)):
    """
    Elimina un artículo de la base de datos.
    """
    db_articulo = crud_articulo.delete_articulo(db, codigo_articulo=codigo_articulo)
    if db_articulo is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return
