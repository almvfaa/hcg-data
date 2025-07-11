# backend/api/v1/endpoints/lab.py
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

# Import the specific task
from ...tasks.modeling_tasks import run_abc_analysis_task

# Keep other original dependencies for other endpoints
from ...schemas import movimiento as schemas
from ...db.database import get_db
from ...models import anomaly_detection, time_series_forecasting
from ...crud import crud_movimiento
import pandas as pd
from datetime import date


router = APIRouter()

@router.post("/run/segmentation", 
             status_code=status.HTTP_202_ACCEPTED,
             summary="Starts an asynchronous ABC segmentation analysis")
def start_segmentation_analysis():
    """
    Queues the ABC analysis task to be run in the background by a Celery worker.
    This endpoint returns immediately with a task ID.
    """
    task = run_abc_analysis_task.delay()
    return {"task_id": task.id, "status": "Task accepted for processing."}


# --- Other Endpoints (Unchanged) ---

@router.post("/run/anomaly")
async def run_anomaly_detection(
    payload: schemas.AnomalyDetectionPayload,
    db: Session = Depends(get_db)
):
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        fecha_inicio=payload.fecha_inicio,
        fecha_fin=payload.fecha_fin,
        skip=0,
        limit=10000
    )
    
    if not movimientos:
        raise HTTPException(status_code=404, detail="No hay movimientos en el rango de fechas")
    
    df = pd.DataFrame([{
        'id_movimiento': mov.id_movimiento,
        'codigo_articulo': mov.codigo_articulo,
        'fecha': mov.fecha,
        'tipo_movimiento': mov.tipo_movimiento.value,
        'cantidad': mov.cantidad,
        'importe_total': float(mov.importe_total)
    } for mov in movimientos])
    
    result_df = anomaly_detection.run_isolation_forest(df, payload.contamination)
    anomalies = result_df[result_df['is_anomaly']]
    result = anomalies.to_dict(orient='records')
    return {"data": result}


@router.post("/run/forecast")
async def run_forecast(
    payload: schemas.ForecastPayload,
    db: Session = Depends(get_db)
):
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        codigo_articulo=payload.codigo_articulo,
        tipo='SALIDA',
        skip=0,
        limit=10000
    )
    
    if not movimientos:
        raise HTTPException(status_code=404, detail="No hay movimientos para este artículo")
    
    df = pd.DataFrame([{
        'fecha': mov.fecha,
        'cantidad': mov.cantidad
    } for mov in movimientos])
    
    forecast = time_series_forecasting.run_prophet_forecast(df, payload.horizon)
    result = forecast.to_dict(orient='records')
    return {"data": result}
