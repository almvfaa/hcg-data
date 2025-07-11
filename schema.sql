-- Crear el tipo ENUM para movimientos
CREATE TYPE tipo_mov AS ENUM ('ENTRADA', 'SALIDA');

-- Tabla CapitulosGasto
CREATE TABLE CapitulosGasto (
    capitulo_gasto INTEGER PRIMARY KEY,
    denominacion_capitulo VARCHAR(255) NOT NULL
);

-- Tabla ConceptosGasto
CREATE TABLE ConceptosGasto (
    concepto_gasto INTEGER PRIMARY KEY,
    denominacion_gasto VARCHAR(255) NOT NULL,
    capitulo_gasto INTEGER NOT NULL,
    FOREIGN KEY (capitulo_gasto) REFERENCES CapitulosGasto(capitulo_gasto)
);

-- Tabla PartidasGenericas
CREATE TABLE PartidasGenericas (
    partida_generica INTEGER PRIMARY KEY,
    denominacion_partida_generica VARCHAR(255) NOT NULL,
    concepto_gasto INTEGER NOT NULL,
    FOREIGN KEY (concepto_gasto) REFERENCES ConceptosGasto(concepto_gasto)
);

-- Tabla PartidasEspecificas
CREATE TABLE PartidasEspecificas (
    partida_especifica INTEGER PRIMARY KEY,
    denominacion_partida_especifica VARCHAR(255) NOT NULL,
    partida_generica INTEGER NOT NULL,
    FOREIGN KEY (partida_generica) REFERENCES PartidasGenericas(partida_generica)
);

-- Tabla Articulos
CREATE TABLE Articulos (
    codigo_articulo VARCHAR(50) PRIMARY KEY,
    descripcion_articulo TEXT NOT NULL,
    descripcion_larga_art TEXT,
    unidad_medida VARCHAR(50),
    partida_especifica INTEGER NOT NULL,
    FOREIGN KEY (partida_especifica) REFERENCES PartidasEspecificas(partida_especifica)
);

-- Tabla Movimientos
CREATE TABLE Movimientos (
    id_movimiento SERIAL PRIMARY KEY,
    codigo_articulo VARCHAR(50) NOT NULL,
    FECHA DATE NOT NULL,
    tipo_movimiento tipo_mov NOT NULL,
    cantidad INTEGER NOT NULL,
    importe_total DECIMAL(12, 2) NOT NULL,
    precio_unitario_historico DECIMAL(10, 2),
    FOREIGN KEY (codigo_articulo) REFERENCES Articulos(codigo_articulo)
);