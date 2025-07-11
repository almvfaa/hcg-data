import pandas as pd
from sklearn.ensemble import IsolationForest

def run_isolation_forest(df: pd.DataFrame, contamination: float = 0.01) -> pd.DataFrame:
    # Seleccionar características
    features = df[['cantidad', 'importe_total']].copy()
    
    # Normalizar características
    features['cantidad'] = (features['cantidad'] - features['cantidad'].mean()) / features['cantidad'].std()
    features['importe_total'] = (features['importe_total'] - features['importe_total'].mean()) / features['importe_total'].std()
    
    # Entrenar modelo
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(features)
    
    # Predecir anomalías
    predictions = model.predict(features)
    
    # Convertir a booleano: True para anomalía
    df['is_anomaly'] = predictions == -1
    
    return df
