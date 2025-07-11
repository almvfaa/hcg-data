from typing import Optional
from pydantic import BaseModel

class ArticuloBase(BaseModel):
    codigo_articulo: str
    descripcion_articulo: str
    unidad_medida: Optional[str] = None
    partida_especifica: int

class ArticuloCreate(ArticuloBase):
    pass

class Articulo(ArticuloBase):
    class Config:
        orm_mode = True