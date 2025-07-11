from sqlalchemy.orm import Session
import pandas as pd

class SegmentationService:
    """
    Encapsulates the business logic for ABC segmentation analysis.
    """
    def __init__(self, db: Session):
        """
        Initializes the service with a database session.
        :param db: The SQLAlchemy Session to use for database operations.
        """
        self.db = db

    def run_abc_analysis(self) -> pd.DataFrame:
        """
        Performs ABC analysis on inventory items based on their movement value.

        Returns:
            A pandas DataFrame with articles classified into 'A', 'B', or 'C' categories.
        """
        # This query joins movements with articles and calculates the total value of each movement.
        # It assumes that 'importe_total' represents the value of the movement.
        query = """
        SELECT
            m.codigo_articulo,
            a.descripcion_articulo,
            m.importe_total
        FROM movimientos AS m
        JOIN articulos AS a ON m.codigo_articulo = a.codigo_articulo
        WHERE m.importe_total IS NOT NULL AND m.importe_total > 0
        """
        
        # Use pandas to read data directly from the database connection
        df = pd.read_sql(query, self.db.bind)

        if df.empty:
            return pd.DataFrame(columns=[
                'codigo_articulo', 'descripcion_articulo', 
                'valor_total_movimiento', 'clase_abc'
            ])

        # Group by article to get the total movement value per article
        df_grouped = df.groupby(['codigo_articulo', 'descripcion_articulo'])['importe_total'].sum().reset_index()
        df_grouped.rename(columns={'importe_total': 'valor_total_movimiento'}, inplace=True)

        # Sort by the total value in descending order
        df_sorted = df_grouped.sort_values(by='valor_total_movimiento', ascending=False)
        
        # Calculate the cumulative sum and the cumulative percentage
        df_sorted['valor_acumulado'] = df_sorted['valor_total_movimiento'].cumsum()
        total_value = df_sorted['valor_total_movimiento'].sum()
        df_sorted['porcentaje_acumulado'] = 100 * df_sorted['valor_acumulado'] / total_value

        # Assign ABC class based on the cumulative percentage
        def assign_class(percentage: float) -> str:
            if percentage <= 80:
                return 'A'
            elif percentage <= 95:
                return 'B'
            else:
                return 'C'

        df_sorted['clase_abc'] = df_sorted['porcentaje_acumulado'].apply(assign_class)
        
        return df_sorted[[
            'codigo_articulo', 
            'descripcion_articulo', 
            'valor_total_movimiento', 
            'porcentaje_acumulado',
            'clase_abc'
        ]]

