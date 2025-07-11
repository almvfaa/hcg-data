from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
import pandas as pd

from ..crud import crud_movimiento, crud_articulo
from ..schemas import movimiento as schemas
from ..db.database import get_db
from ..models import item_segmentation, anomaly_detection, time_series_forecasting

router = APIRouter()

@router.post("/run/segmentation")
async def run_segmentation(db: Session = Depends(get_db)):
    # Obtener todos los movimientos
    total, movimientos = crud_movimiento.get_movimientos(db, skip=0, limit=10000)
    
    if not movimientos:
        raise HTTPException(status_code=404, detail="No hay movimientos")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'codigo_articulo': mov.codigo_articulo,
        'fecha': mov.fecha,
        'cantidad': mov.cantidad,
        'importe_total': float(mov.importe_total)
    } for mov in movimientos])
    
    # Ejecutar análisis ABC
    result_df = item_segmentation.run_abc_analysis(df)
    
    # Convertir a formato JSON
    result = result_df.to_dict(orient='records')
    return {"data": result}

@router.post("/run/anomaly")
async def run_anomaly_detection(
    payload: schemas.AnomalyDetectionPayload,
    db: Session = Depends(get_db)
):
    # Obtener movimientos en el rango de fechas
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        fecha_inicio=payload.fecha_inicio,
        fecha_fin=payload.fecha_fin,
        skip=0,
        limit=10000
    )
    
    if not movimientos:
        raise HTTPException(status_code=404, detail="No hay movimientos en el rango de fechas")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'id_movimiento': mov.id_movimiento,
        'codigo_articulo': mov.codigo_articulo,
        'fecha': mov.fecha,
        'tipo_movimiento': mov.tipo_movimiento.value,
        'cantidad': mov.cantidad,
        'importe_total': float(mov.importe_total)
    } for mov in movimientos])
    
    # Ejecutar detección de anomalías
    result_df = anomaly_detection.run_isolation_forest(df, payload.contamination)
    
    # Filtrar solo anomalías
    anomalies = result_df[result_df['is_anomaly']]
    
    # Convertir a formato JSON
    result = anomalies.to_dict(orient='records')
    return {"data": result}

@router.post("/run/forecast")
async def run_forecast(
    payload: schemas.ForecastPayload,
    db: Session = Depends(get_db)
):
    # Obtener movimientos para el artículo específico
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        codigo_articulo=payload.codigo_articulo,
        tipo='SALIDA',
        skip=0,
        limit=10000
    )
    
    if not movimientos:
        raise HTTPException(status_code=404, detail="No hay movimientos para este artículo")
    
    # Convertir a DataFrame
    df = pd.DataFrame([{
        'fecha': mov.fecha,
        'cantidad': mov.cantidad
    } for mov in movimientos])
    
    # Ejecutar pronóstico
    forecast = time_series_forecasting.run_prophet_forecast(df, payload.horizon)
    
    # Convertir a formato JSON
    result = forecast.to_dict(orient='records')
    return {"data": result}
