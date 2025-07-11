from sqlalchemy.orm import Session
from ..db import models as md

def get_capitulos(db: Session, search: str = None):
    query = db.query(md.CapituloGasto)
    if search:
        query = query.filter(md.CapituloGasto.denominacion_capitulo.ilike(f'%{search}%'))
    return query.all()

def get_conceptos(db: Session, search: str = None):
    query = db.query(md.ConceptoGasto)
    if search:
        query = query.filter(md.ConceptoGasto.denominacion_gasto.ilike(f'%{search}%'))
    return query.all()

def get_partidas_genericas(db: Session, search: str = None):
    query = db.query(md.PartidaGenerica)
    if search:
        query = query.filter(md.PartidaGenerica.denominacion_partida_generica.ilike(f'%{search}%'))
    return query.all()

def get_partidas_especificas(db: Session, search: str = None):
    query = db.query(md.PartidaEspecifica)
    if search:
        query = query.filter(md.PartidaEspecifica.denominacion_partida_especifica.ilike(f'%{search}%'))
    return query.all()