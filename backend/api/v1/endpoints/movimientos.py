from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
import pandas as pd
from ..dependencies import get_db
from crud import crud_movimiento
from schemas import movimiento as sc_movimiento

router = APIRouter()

@router.get("/", response_model=list[sc_movimiento.Movimiento])
def read_movimientos(
    skip: int = Query(0, alias="skip"),
    limit: int = Query(100, alias="limit"),
    tipo: str = Query(None, alias="tipo"),
    fecha_inicio: date = Query(None, alias="fecha_inicio"),
    fecha_fin: date = Query(None, alias="fecha_fin"),
    search: str = Query(None, alias="search"),
    db: Session = Depends(get_db)
):
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        skip=skip,
        limit=limit,
        tipo=tipo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        search=search
    )
    return movimientos

@router.get("/stats/inventario-mensual")
def get_inventario_mensual(
    year: int = Query(..., alias="year"),
    db: Session = Depends(get_db)
):
    # Fetch all movements for the given year
    fecha_inicio = date(year, 1, 1)
    fecha_fin = date(year, 12, 31)
    total, movimientos = crud_movimiento.get_movimientos(
        db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    if not movimientos:
        return []

    # Convert to pandas DataFrame
    df = pd.DataFrame([m.__dict__ for m in movimientos])

    # Ensure 'fecha' is datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Calculate monthly initial value (simplistic approach, more complex logic needed for real inventory)
    # For simplicity here, we'll calculate month-end value and use it as start for next
    df['month'] = df['fecha'].dt.to_period('M')

    # Calculate total values per month and type
    monthly_summary = df.groupby(['month', 'tipo_movimiento'])['importe_total'].sum().unstack(fill_value=0)

    # Ensure both 'ENTRADA' and 'SALIDA' columns exist
    for col in ['ENTRADA', 'SALIDA']:
        if col not in monthly_summary.columns:
            monthly_summary[col] = 0

    monthly_summary['net_change'] = monthly_summary['ENTRADA'] - monthly_summary['SALIDA']

    # Calculate cumulative value
    monthly_summary['cumulative_value'] = monthly_summary['net_change'].cumsum()

    # Prepare data for the response
    monthly_inventory_stats = []
    previous_month_value = 0

    # Filter months within the requested year
    monthly_summary = monthly_summary[monthly_summary.index.to_timestamp().dt.year == year]


    for month, row in monthly_summary.iterrows():
        month_str = month.strftime('%b %Y')
        valor_inicial = previous_month_value
        total_entradas = row['ENTRADA']
        total_salidas = row['SALIDA']
        valor_final = valor_inicial + total_entradas - total_salidas #row['cumulative_value']

        monthly_inventory_stats.append({
            'mes': month_str,
            'valor_inicial': round(valor_inicial, 2),
            'total_entradas': round(total_entradas, 2),
            'total_salidas': round(total_salidas, 2),
            'valor_final': round(valor_final, 2),
        })
        previous_month_value = valor_final

    return monthly_inventory_stats