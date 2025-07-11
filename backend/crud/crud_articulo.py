from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from sqlalchemy.exc import SQLAlchemyError
from ..db import models as md
from ..schemas import articulo as sc
from ..core.db_errors import handle_db_error, NotFoundError

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
    try:
        query = db.query(md.Articulos)

        if search:
            query = query.filter(
                func.lower(md.Articulos.descripcion_articulo).contains(func.lower(search))
            )
        if partida_especifica is not None:
            query = query.filter(md.Articulos.partida_especifica == partida_especifica)
        if unidad_medida:
            query = query.filter(md.Articulos.unidad_medida.ilike(f'%{unidad_medida}%'))

        if sort_by and hasattr(md.Articulos, sort_by):
            column = getattr(md.Articulos, sort_by)
            if sort_direction == 'desc':
                query = query.order_by(desc(column))
            else:
                query = query.order_by(asc(column))

        total_results = query.count()
        articulos = query.offset(skip).limit(limit).all()
        return total_results, articulos
    except SQLAlchemyError as e:
        handle_db_error(e, "fetching articulos")

def get_articulo(db: Session, codigo_articulo: str) -> md.Articulos:
    """Gets a single article by its primary key."""
    try:
        articulo = db.query(md.Articulos).filter(
            md.Articulos.codigo_articulo == codigo_articulo
        ).first()
        if not articulo:
            raise NotFoundError("Artículo", codigo_articulo)
        return articulo
    except SQLAlchemyError as e:
        handle_db_error(e, f"fetching articulo {codigo_articulo}")

def create_articulo(db: Session, articulo: sc.ArticuloCreate) -> md.Articulos:
    """Creates a new article in the database."""
    try:
        db_articulo = md.Articulos(**articulo.model_dump())
        db.add(db_articulo)
        db.commit()
        db.refresh(db_articulo)
        return db_articulo
    except SQLAlchemyError as e:
        db.rollback()
        handle_db_error(e, "creating articulo")

def update_articulo(db: Session, codigo_articulo: str, articulo: sc.ArticuloUpdate) -> md.Articulos:
    """Updates an existing article in the database."""
    try:
        db_articulo = get_articulo(db, codigo_articulo)
        for field, value in articulo.model_dump(exclude_unset=True).items():
            setattr(db_articulo, field, value)
        db.commit()
        db.refresh(db_articulo)
        return db_articulo
    except SQLAlchemyError as e:
        db.rollback()
        handle_db_error(e, f"updating articulo {codigo_articulo}")

def delete_articulo(db: Session, codigo_articulo: str) -> md.Articulos:
    """Deletes an article from the database."""
    try:
        db_articulo = get_articulo(db, codigo_articulo)
        db.delete(db_articulo)
        db.commit()
        return db_articulo
    except SQLAlchemyError as e:
        db.rollback()
        handle_db_error(e, f"deleting articulo {codigo_articulo}")
