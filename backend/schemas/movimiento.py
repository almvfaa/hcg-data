from pydantic import BaseModel
from datetime import date
from .articulo import Articulo

class MovimientoBase(BaseModel):
    fecha: date
    tipo_movimiento: str
    cantidad: int
    importe_total: float
    precio_unitario_historico: float | None = None
    codigo_articulo: str

class MovimientoCreate(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id_movimiento: int
    articulo: Articulo | None = None

    class Config:
        orm_mode = True

class AnomalyDetectionPayload(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    contamination: float = 0.01

class ForecastPayload(BaseModel):
    codigo_articulo: str
    horizon: int = 6
