from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import models as md
from .. import schemas as sc
from sqlalchemy import desc, asc

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

    if sort_by:
        # Using md.Articulo.c[sort_by] accesses the column directly from the table object
        # Need to handle potential KeyError if sort_by is not a valid column
        if sort_direction == 'desc':
            query = query.order_by(desc(md.Articulo.c[sort_by]))
        else:
            # Default to ascending if sort_direction is not 'desc'
            query = query.order_by(asc(md.Articulo.c[sort_by]))

    total_results = query.count()
    articulos = query.offset(skip).limit(limit).all()

    return total_results, articulos