from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from ..db import models as md
from ..schemas import articulo as sc

def get_articulos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    partida_especifica: int | None = None,
    unidad_medida: str | None = None,
    sort_by: str | None = None,
    sort_direction: str | None = None
):
    query = db.query(md.Articulo)

    if search:
        query = query.filter(
            func.lower(md.Articulo.descripcion_articulo).contains(func.lower(search))
        )
    if partida_especifica is not None:
        query = query.filter(md.Articulo.partida_especifica == partida_especifica)
    if unidad_medida:
        query = query.filter(md.Articulo.unidad_medida.ilike(f'%{unidad_medida}%'))

    if sort_by and hasattr(md.Articulo, sort_by):
        column = getattr(md.Articulo, sort_by)
        if sort_direction == 'desc':
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    total_results = query.count()
    articulos = query.offset(skip).limit(limit).all()
    return total_results, articulos

def get_articulo(db: Session, codigo_articulo: str) -> md.Articulo | None:
    """Gets a single article by its primary key."""
    return db.query(md.Articulo).filter(md.Articulo.codigo_articulo == codigo_articulo).first()

def create_articulo(db: Session, articulo: sc.ArticuloCreate) -> md.Articulo:
    """Creates a new article in the database."""
    db_articulo = md.Articulo(**articulo.model_dump())
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

def update_articulo(db: Session, codigo_articulo: str, articulo: sc.ArticuloUpdate) -> md.Articulo | None:
    """Updates an existing article in the database."""
    db_articulo = get_articulo(db, codigo_articulo)
    if not db_articulo:
        return None
    
    update_data = articulo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_articulo, key, value)
    
    db.add(db_articulo)
    db.commit()
    db.refresh(db_articulo)
    return db_articulo

def delete_articulo(db: Session, codigo_articulo: str) -> md.Articulo | None:
    """Deletes an article from the database."""
    db_articulo = get_articulo(db, codigo_articulo)
    if not db_articulo:
        return None
    
    db.delete(db_articulo)
    db.commit()
    return db_articulo
