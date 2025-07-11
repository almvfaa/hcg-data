import pandas as pd

def run_isolation_forest(df: pd.DataFrame, contamination: float = 0.01) -> pd.DataFrame:
    """
    Runs anomaly detection using Isolation Forest.
    The scikit-learn library is imported on-demand to save memory on application startup.
    """
    # --- Lazy Import ---
    # Import IsolationForest only when this function is called.
    try:
        from sklearn.ensemble import IsolationForest
    except ImportError:
        raise RuntimeError(
            "The 'scikit-learn' library is not installed. "
            "Please install it with 'pip install scikit-learn' to use anomaly detection features."
        )

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
