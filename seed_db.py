import os
import pandas as pd
from sqlalchemy import create_engine, text, Column, Integer, String, Date, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging
import enum

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a simplified Base and models within the script for seeding
Base = declarative_base()

class CapituloGasto(Base):
    __tablename__ = 'capitulosgasto'
    capitulo_gasto = Column(Integer, primary_key=True)
    denominacion_capitulo = Column(String)

class ConceptoGasto(Base):
    __tablename__ = 'conceptosgasto'
    concepto_gasto = Column(Integer, primary_key=True)
    denominacion_gasto = Column(String)
    capitulo_gasto = Column(Integer, ForeignKey('capitulosgasto.capitulo_gasto'))

class PartidaGenerica(Base):
    __tablename__ = 'partidasgenericas'
    partida_generica = Column(Integer, primary_key=True)
    denominacion_partida_generica = Column(String)
    concepto_gasto = Column(Integer, ForeignKey('conceptosgasto.concepto_gasto'))

class PartidaEspecifica(Base):
    __tablename__ = 'partidasespecificas'
    partida_especifica = Column(Integer, primary_key=True)
    denominacion_partida_especifica = Column(String)
    partida_generica = Column(Integer, ForeignKey('partidasgenericas.partida_generica'))

class Articulo(Base):
    __tablename__ = 'articulos'
    codigo_articulo = Column(String, primary_key=True)
    descripcion_articulo = Column(String)
    descripcion_larga_art = Column(String, nullable=True)
    unidad_medida = Column(String, nullable=True)
    partida_especifica = Column(Integer, ForeignKey('partidasespecificas.partida_especifica'))

class TipoMovEnum(enum.Enum):
    ENTRADA = 'ENTRADA'
    SALIDA = 'SALIDA'

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id_movimiento = Column(Integer, primary_key=True)
    codigo_articulo = Column(String, ForeignKey('articulos.codigo_articulo'))
    fecha = Column(Date)
    tipo_movimiento = Column(Enum(TipoMovEnum))
    cantidad = Column(Integer)
    importe_total = Column(DECIMAL(12, 2))
    precio_unitario_historico = Column(DECIMAL(10, 2), nullable=True)

def init_db(engine):
    """Drops all existing tables and creates new ones based on the models."""
    logging.info("Initializing database schema...")
    try:
        # Drop all tables to ensure a clean slate
        Base.metadata.drop_all(bind=engine)
        # Create all tables based on the model definitions
        Base.metadata.create_all(bind=engine)
        logging.info("Database schema initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database schema: {e}")
        raise

def cargar_catalogos(db):
    """Loads data into classification tables from CSV."""
    logging.info("Loading catalog data...")
    catalog_files = {
        'capitulosgasto': 'capitulos_gasto.csv',
        'conceptosgasto': 'conceptos_gasto.csv',
        'partidasgenericas': 'partidas_genericas.csv',
        'partidasespecificas': 'partidas_especificas.csv',
    }
    for table_name, file_name in catalog_files.items():
        file_path = os.path.join('data', file_name) # Assuming CSVs are in a 'data' folder
        if not os.path.exists(file_path):
            logging.warning(f"Catalog file not found: {file_path}")
            continue
        try:
            df = pd.read_csv(file_path)
            logging.info(f"Loading {len(df)} rows into {table_name} from {file_name}")
            df.to_sql(table_name, con=db.get_bind(), if_exists='append', index=False)
            db.commit()
            logging.info(f"Successfully loaded {table_name}.")
        except Exception as e:
            db.rollback()
            logging.error(f"Error loading {table_name}: {e}")
            raise

def cargar_articulos(db):
    """Loads data into the articles table from CSV."""
    logging.info("Loading articles data...")
    file_name = 'articulos.csv'
    file_path = os.path.join('data', file_name)
    if not os.path.exists(file_path):
        logging.warning(f"Articles file not found: {file_path}")
        return
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Loading {len(df)} rows into articulos from {file_name}")
        df.to_sql('articulos', con=db.get_bind(), if_exists='append', index=False)
        db.commit()
        logging.info("Successfully loaded articulos.")
    except Exception as e:
        db.rollback()
        logging.error(f"Error loading articulos: {e}")
        raise

def transformar_movimientos(db):
    """Transforms summary movements data and loads into the movements table."""
    logging.info("Transforming and loading movements data...")
    file_name = 'movimientos_resumen.csv' # Assuming a summary file
    file_path = os.path.join('data', file_name)
    if not os.path.exists(file_path):
        logging.warning(f"Movements summary file not found: {file_path}")
        return

    try:
        df = pd.read_csv(file_path)
        
        # Assuming the summary CSV has columns like:
        # fecha, codigo_articulo, cantidad_entrada, importe_entrada, cantidad_salida, importe_salida, precio_unitario_historico
        
        movement_records = []
        for index, row in df.iterrows():
            fecha = pd.to_datetime(row['fecha']).date()
            codigo_articulo = row['codigo_articulo']
            precio_unitario_historico = row.get('precio_unitario_historico') # Optional field

            if row.get('cantidad_entrada', 0) > 0:
                movement_records.append({
                    'codigo_articulo': codigo_articulo,
                    'fecha': fecha,
                    'tipo_movimiento': TipoMovEnum.ENTRADA,
                    'cantidad': int(row['cantidad_entrada']),
                    'importe_total': float(row['importe_entrada']),
                    'precio_unitario_historico': precio_unitario_historico
                })

            if row.get('cantidad_salida', 0) > 0:
                 movement_records.append({
                    'codigo_articulo': codigo_articulo,
                    'fecha': fecha,
                    'tipo_movimiento': TipoMovEnum.SALIDA,
                    'cantidad': int(row['cantidad_salida']),
                    'importe_total': float(row['importe_salida']),
                    'precio_unitario_historico': precio_unitario_historico
                })
        
        if movement_records:
            movements_df = pd.DataFrame(movement_records)
            logging.info(f"Loading {len(movements_df)} transformed movement rows.")
            # Need to handle the ENUM type carefully with to_sql
            # One approach is to map the enum value to string before to_sql
            movements_df['tipo_movimiento'] = movements_df['tipo_movimiento'].apply(lambda x: x.value)

            movements_df.to_sql('movimientos', con=db.get_bind(), if_exists='append', index=False)
            db.commit()
            logging.info("Successfully loaded movements.")
        else:
            logging.info("No movement records to load.")

    except Exception as e:
        db.rollback()
        logging.error(f"Error transforming and loading movements: {e}")
        raise


if __name__ == "__main__":
    db = None
    try:
        # Initialize schema (create tables) before loading data
        init_db(engine)

        db = SessionLocal() # Create a session for data loading
        cargar_catalogos(db)
        cargar_articulos(db)
        transformar_movimientos(db)
        logging.info("Database seeding completed successfully.")
    except Exception as e:
        logging.critical(f"Database seeding failed: {e}")
    finally:
        if db:
            db.close()
