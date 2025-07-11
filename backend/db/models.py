from sqlalchemy import Column, Integer, String, ForeignKey, Date, DECIMAL, Enum, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum

class TipoMovEnum(enum.Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class CapitulosGasto(Base):
    __tablename__ = "CapitulosGasto"

    capitulo_gasto = Column(Integer, primary_key=True)
    denominacion_capitulo = Column(String(255), nullable=False)

    conceptos = relationship("ConceptosGasto", back_populates="capitulo")

class ConceptosGasto(Base):
    __tablename__ = "ConceptosGasto"

    concepto_gasto = Column(Integer, primary_key=True)
    denominacion_gasto = Column(String(255), nullable=False)
    capitulo_gasto = Column(Integer, ForeignKey("CapitulosGasto.capitulo_gasto"), nullable=False)

    capitulo = relationship("CapitulosGasto", back_populates="conceptos")
    partidas_genericas = relationship("PartidasGenericas", back_populates="concepto")

class PartidasGenericas(Base):
    __tablename__ = "PartidasGenericas"

    partida_generica = Column(Integer, primary_key=True)
    denominacion_partida_generica = Column(String(255), nullable=False)
    concepto_gasto = Column(Integer, ForeignKey("ConceptosGasto.concepto_gasto"), nullable=False)

    concepto = relationship("ConceptosGasto", back_populates="partidas_genericas")
    partidas_especificas = relationship("PartidasEspecificas", back_populates="partida_generica_rel")

class PartidasEspecificas(Base):
    __tablename__ = "PartidasEspecificas"

    partida_especifica = Column(Integer, primary_key=True)
    denominacion_partida_especifica = Column(String(255), nullable=False)
    partida_generica = Column(Integer, ForeignKey("PartidasGenericas.partida_generica"), nullable=False)

    partida_generica_rel = relationship("PartidasGenericas", back_populates="partidas_especificas")
    articulos = relationship("Articulos", back_populates="partida_especifica_rel")

class Articulos(Base):
    __tablename__ = "Articulos"

    codigo_articulo = Column(String(50), primary_key=True)
    descripcion_articulo = Column(String, nullable=False)
    descripcion_larga_art = Column(String, nullable=True)
    unidad_medida = Column(String(50), nullable=True)
    partida_especifica = Column(Integer, ForeignKey("PartidasEspecificas.partida_especifica"), nullable=False)

    partida_especifica_rel = relationship("PartidasEspecificas", back_populates="articulos")
    movimientos = relationship("Movimientos", back_populates="articulo")

class Movimientos(Base):
    __tablename__ = "Movimientos"

    id_movimiento = Column(Integer, primary_key=True, index=True)
    codigo_articulo = Column(String(50), ForeignKey("Articulos.codigo_articulo"), nullable=False)
    fecha = Column(Date, nullable=False)
    tipo_movimiento = Column(Enum(TipoMovEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    importe_total = Column(DECIMAL(12, 2), nullable=False)
    precio_unitario_historico = Column(DECIMAL(10, 2), nullable=True)

    articulo = relationship("Articulos", back_populates="movimientos")