import pandas as pd

def run_prophet_forecast(df_sales: pd.DataFrame, horizon: int = 12) -> pd.DataFrame:
    """
    Runs a time series forecast using Prophet.
    The Prophet library is imported on-demand to save memory on application startup.
    """
    # --- Lazy Import ---
    # Import Prophet only when this function is called.
    try:
        from prophet import Prophet
    except ImportError:
        raise RuntimeError(
            "The 'prophet' library is not installed. "
            "Please install it with 'pip install prophet' to use forecasting features."
        )

    # Preparar datos para Prophet
    df_prophet = df_sales.rename(columns={'fecha': 'ds', 'cantidad': 'y'})
    df_prophet = df_prophet[['ds', 'y']].groupby('ds').sum().reset_index()
    
    # Entrenar modelo
    model = Prophet(weekly_seasonality=True, yearly_seasonality=True)
    model.fit(df_prophet)
    
    # Crear dataframe futuro
    future = model.make_future_dataframe(periods=horizon, freq='M')
    
    # Predecir
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
