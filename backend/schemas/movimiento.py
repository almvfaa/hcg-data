from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal
from typing import Optional
from .articulo import Articulo

class MovimientoBase(BaseModel):
    fecha: date = Field(..., description="Fecha del movimiento")
    tipo_movimiento: str = Field(
        ..., 
        pattern="^(ENTRADA|SALIDA)$",
        description="Tipo de movimiento: ENTRADA o SALIDA"
    )
    cantidad: int = Field(
        ..., 
        gt=0,
        description="Cantidad de artículos movidos (debe ser mayor que 0)"
    )
    importe_total: Decimal = Field(
        ..., 
        ge=Decimal('0.00'),
        decimal_places=2,
        description="Importe total del movimiento"
    )
    precio_unitario_historico: Optional[Decimal] = Field(
        None,
        ge=Decimal('0.00'),
        decimal_places=2,
        description="Precio unitario histórico del artículo"
    )
    codigo_articulo: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Código único del artículo"
    )

    @field_validator("fecha")
    def fecha_no_futura(cls, v):
        if v > date.today():
            raise ValueError("La fecha no puede ser futura")
        return v

    @field_validator("importe_total")
    def validar_importe_total(cls, v, values):
        if "cantidad" in values.data and "precio_unitario_historico" in values.data:
            cantidad = values.data["cantidad"]
            precio = values.data["precio_unitario_historico"]
            if precio and abs(v - (cantidad * precio)) > Decimal("0.01"):
                raise ValueError(
                    "El importe total debe ser igual a la cantidad por el precio unitario"
                )
        return v

class MovimientoCreate(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id_movimiento: int
    articulo: Optional[Articulo] = None

    class Config:
        from_attributes = True

class AnomalyDetectionPayload(BaseModel):
    fecha_inicio: date = Field(..., description="Fecha de inicio del análisis")
    fecha_fin: date = Field(..., description="Fecha final del análisis")
    contamination: float = Field(
        0.01,
        gt=0,
        lt=0.5,
        description="Proporción esperada de anomalías en los datos"
    )

    @field_validator("fecha_fin")
    def fecha_fin_posterior(cls, v, values):
        if "fecha_inicio" in values.data and v <= values.data["fecha_inicio"]:
            raise ValueError("La fecha final debe ser posterior a la fecha inicial")
        return v

class ForecastPayload(BaseModel):
    codigo_articulo: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Código del artículo para el pronóstico"
    )
    horizon: int = Field(
        6,
        gt=0,
        le=24,
        description="Número de períodos a pronosticar (máximo 24)"
    )
