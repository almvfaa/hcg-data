import pandas as pd
from prophet import Prophet

def run_prophet_forecast(df_sales: pd.DataFrame, horizon: int = 12) -> pd.DataFrame:
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
