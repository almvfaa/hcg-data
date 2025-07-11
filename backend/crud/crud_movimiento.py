from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import date
from ..db import models as md

def get_movimientos(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    tipo: str = None,
    codigo_articulo: str | None = None,
    fecha_inicio: date = None,
    fecha_fin: date = None,
    search: str = None,
    sort_by: str | None = None,
    sort_direction: str | None = None,
):
    query = db.query(md.Movimiento).join(md.Articulo)

    filters = []
    if tipo:
        filters.append(md.Movimiento.tipo_movimiento == tipo)
    if fecha_inicio:
        filters.append(md.Movimiento.fecha >= fecha_inicio)
    if codigo_articulo:
        filters.append(md.Movimiento.codigo_articulo == codigo_articulo)
    if fecha_fin:
        filters.append(md.Movimiento.fecha <= fecha_fin)
    if search:
        search_filter = or_(
            md.Articulo.descripcion_articulo.ilike(f'%{search}%'),
            md.Movimiento.codigo_articulo.ilike(f'%{search}%')
        )
        filters.append(search_filter)

    if filters:
        query = query.filter(and_(*filters))

    if sort_by:
        try:
            if sort_direction == 'desc':
                query = query.order_by(md.Movimiento.__table__.columns[sort_by].desc())
            else:
                query = query.order_by(md.Movimiento.__table__.columns[sort_by].asc())
        except KeyError:
            # Handle or ignore invalid sort_by column
            pass
    total = query.count()
    movimientos = query.offset(skip).limit(limit).all()

    return total, movimientos