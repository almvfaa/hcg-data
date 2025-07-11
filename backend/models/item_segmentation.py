import pandas as pd
import numpy as np

def run_abc_analysis(df_movements: pd.DataFrame) -> pd.DataFrame:
    # Calcular el valor total por artículo
    df_article_value = df_movements.groupby('codigo_articulo')['importe_total'].sum().reset_index()
    
    # Ordenar por valor descendente
    df_article_value = df_article_value.sort_values('importe_total', ascending=False)
    
    # Calcular porcentaje acumulado
    total_value = df_article_value['importe_total'].sum()
    df_article_value['porcentaje_acumulado'] = (df_article_value['importe_total'].cumsum() / total_value) * 100
    
    # Asignar clase ABC
    df_article_value['clase'] = 'C'
    df_article_value.loc[df_article_value['porcentaje_acumulado'] <= 80, 'clase'] = 'A'
    df_article_value.loc[(df_article_value['porcentaje_acumulado'] > 80) & 
                         (df_article_value['porcentaje_acumulado'] <= 95), 'clase'] = 'B'
    
    # Obtener descripción del artículo (asumiendo que tenemos esta información)
    # En una implementación real, haríamos JOIN con la tabla de artículos
    df_article_value['descripcion_articulo'] = "Artículo " + df_article_value['codigo_articulo'].astype(str)
    
    return df_article_value[['codigo_articulo', 'descripcion_articulo', 'importe_total', 'porcentaje_acumulado', 'clase']]
