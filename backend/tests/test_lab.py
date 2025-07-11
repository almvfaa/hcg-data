import pandas as pd
from fastapi.testclient import TestClient
from ..main import app
from ..api.v1.dependencies import get_segmentation_service
from ..services.segmentation import SegmentationService

# 1. Mock del servicio: Una clase falsa que imita el comportamiento del servicio real
class MockSegmentationService:
    def run_abc_analysis(self) -> pd.DataFrame:
        # Devuelve datos de prueba predefinidos, sin tocar la base de datos.
        return pd.DataFrame({
            'codigo_articulo': ['ART-001', 'ART-002', 'ART-003'],
            'descripcion_articulo': ['Producto A', 'Producto B', 'Producto C'],
            'valor_total_movimiento': [15000, 5000, 500],
            'porcentaje_acumulado': [75.0, 95.0, 100.0],
            'clase_abc': ['A', 'B', 'C']
        })

# 2. Mock del proveedor de dependencias: Una función que devuelve el servicio mockeado
def get_mock_segmentation_service():
    """Esta función sobreescribirá la dependencia real en las pruebas."""
    return MockSegmentationService()

# 3. Prueba del endpoint
def test_run_segmentation_endpoint_with_mock():
    """
    Prueba el endpoint de segmentación usando un mock del servicio
    para asegurar que el endpoint responde correctamente sin depender de la DB.
    """
    # Reemplazar la dependencia real (get_segmentation_service) con nuestra versión mock.
    # Cualquier llamada al endpoint durante esta prueba usará get_mock_segmentation_service.
    app.dependency_overrides[get_segmentation_service] = get_mock_segmentation_service

    client = TestClient(app)
    response = client.post("/api/v1/lab/run/segmentation")
    
    # Verificar los resultados
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]['codigo_articulo'] == 'ART-001'
    assert data[0]['clase_abc'] == 'A'
    assert data[1]['clase_abc'] == 'B'
    assert data[2]['clase_abc'] == 'C'

    # Limpiar el override después de la prueba para no afectar otras pruebas
    app.dependency_overrides = {}

# (Opcional) Prueba de integración que usa la base de datos real
# def test_run_segmentation_integration(test_db_session):
#     # Esta sería una prueba más compleja que requiere una base de datos de prueba
#     # poblada con datos de antemano.
#     service = SegmentationService(db=test_db_session)
#     results = service.run_abc_analysis()
#     assert not results.empty
#     assert 'clase_abc' in results.columns
