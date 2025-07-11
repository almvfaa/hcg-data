from pydantic import BaseModel

# Capitulo Schemas
class CapituloBase(BaseModel):
    capitulo_gasto: int
    denominacion_capitulo: str

class Capitulo(CapituloBase):
    class Config:
        orm_mode = True

# Concepto Schemas
class ConceptoBase(BaseModel):
    concepto_gasto: int
    denominacion_gasto: str
    capitulo_gasto: int

class Concepto(ConceptoBase):
    class Config:
        orm_mode = True

# PartidaGenerica Schemas
class PartidaGenericaBase(BaseModel):
    partida_generica: int
    denominacion_partida_generica: str
    concepto_gasto: int

class PartidaGenerica(PartidaGenericaBase):
    class Config:
        orm_mode = True

# PartidaEspecifica Schemas
class PartidaEspecificaBase(BaseModel):
    partida_especifica: int
    denominacion_partida_especifica: str
    partida_generica: int

class PartidaEspecifica(PartidaEspecificaBase):
    class Config:
        orm_mode = True