'use client';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/Card';
import { DateRangePicker } from '@/components/ui/DateRangePicker';
import { useState, useEffect } from 'react';
import { useQuery, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, ZAxis, LineChart, Line } from 'recharts';
import { DataTable } from '@/components/ui/DataTable';
import { Combobox } from '@/components/ui/combobox';
import { Beaker } from 'lucide-react';

const queryClient = new QueryClient();

function LabPageContent() {
  const [dateRange, setDateRange] = useState<{ start?: Date; end?: Date }>({});
  const [selectedArticle, setSelectedArticle] = useState<string | null>(null);
  const [horizon, setHorizon] = useState<number>(6);
  const [articles, setArticles] = useState<{ value: string; label: string }[]>([]);

  useEffect(() => {
    async function fetchArticles() {
      const response = await fetch('/api/v1/catalogo');
      const data = await response.json();
      const articleOptions = data.articulos.map((articulo: any) => ({
        value: articulo.codigo_articulo,
        label: articulo.descripcion_articulo
      }));
      setArticles(articleOptions);
    }
    fetchArticles();
  }, []);

  // Fetch para segmentación
  const { data: segmentationData, refetch: runSegmentation, isLoading: segmentationLoading } = useQuery({
    queryKey: ['segmentation'],
    queryFn: async () => {
      const response = await fetch('http://localhost:8000/api/v1/lab/run/segmentation', { method: 'POST' });
      return response.json();
    },
    enabled: false,
  });

  // Fetch para anomalías
  const { data: anomalyData, refetch: runAnomalyDetection, isLoading: anomalyLoading } = useQuery({
    queryKey: ['anomaly', dateRange],
    queryFn: async () => {
      const payload = {
        fecha_inicio: dateRange.start?.toISOString().split('T')[0],
        fecha_fin: dateRange.end?.toISOString().split('T')[0],
      };
      const response = await fetch('http://localhost:8000/api/v1/lab/run/anomaly', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    },
    enabled: false,
  });

  // Fetch para pronóstico
  const { data: forecastData, refetch: runForecast, isLoading: forecastLoading } = useQuery({
    queryKey: ['forecast', selectedArticle, horizon],
    queryFn: async () => {
      if (!selectedArticle) throw new Error('Artículo no seleccionado');
      
      const payload = {
        codigo_articulo: selectedArticle,
        horizon: horizon
      };
      const response = await fetch('http://localhost:8000/api/v1/lab/run/forecast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      return response.json();
    },
    enabled: false,
  });

  // Agrupar datos para el gráfico ABC
  const abcChartData = segmentationData?.data
    ? Object.entries(
        segmentationData.data.reduce((acc: Record<string, number>, item: any) => {
          acc[item.clase] = (acc[item.clase] || 0) + 1;
          return acc;
        }, {})
      ).map(([clase, count]) => ({ clase, count }))
    : [];

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Beaker className="text-blue-600" size={24} />
        Laboratorio de Modelos
      </h1>
      
      <Tabs defaultValue="segmentation">
        <TabsList>
          <TabsTrigger value="segmentation">Segmentación ABC</TabsTrigger>
          <TabsTrigger value="anomaly">Detección de Anomalías</TabsTrigger>
          <TabsTrigger value="forecast">Pronóstico</TabsTrigger>
        </TabsList>
        
        <TabsContent value="segmentation">
          <Card className="p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Segmentación ABC de Artículos</h2>
            <p className="text-gray-600 mb-4">
              Clasifica los artículos según su valor total de movimiento (principio de Pareto)
            </p>
            
            <Button onClick={() => runSegmentation()} disabled={segmentationLoading}>
              {segmentationLoading ? 'Procesando...' : 'Ejecutar Análisis ABC'}
            </Button>
            
            {abcChartData.length > 0 && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Distribución de Clases</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={abcChartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="clase" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" fill="#8884d8" name="Número de Artículos" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
            
            {segmentationData?.data && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Artículos Clasificados</h3>
                <DataTable
                  columns={[
                    { accessorKey: 'codigo_articulo', header: 'Código' },
                    { accessorKey: 'descripcion_articulo', header: 'Descripción' },
                    { accessorKey: 'clase', header: 'Clase' },
                    { accessorKey: 'importe_total', header: 'Valor Total', 
                      cell: (row: any) => row.importe_total.toLocaleString('es-ES', { 
                        style: 'currency', currency: 'EUR' 
                      }) 
                    },
                    { accessorKey: 'porcentaje_acumulado', header: '% Acumulado', 
                      cell: (row: any) => `${row.porcentaje_acumulado.toFixed(2)}%` 
                    },
                  ]}
                  data={segmentationData.data}
                  searchColumn="descripcion_articulo"
                  placeholder="Buscar artículos..."
                />
              </div>
            )}
          </Card>
        </TabsContent>
        
        <TabsContent value="anomaly">
          <Card className="p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Detección de Anomalías</h2>
            <p className="text-gray-600 mb-4">
              Identifica transacciones inusuales en cantidad o valor total
            </p>
            
            <div className="flex items-center gap-4 mb-4">
              <DateRangePicker
                dateRange={dateRange}
                onDateRangeChange={setDateRange}
              />
              <Button 
                onClick={() => runAnomalyDetection()} 
                disabled={!dateRange.start || !dateRange.end || anomalyLoading}
              >
                {anomalyLoading ? 'Buscando anomalías...' : 'Buscar Anomalías'}
              </Button>
            </div>
            
            {anomalyData?.data && (
              <>
                <div className="mb-6">
                  <h3 className="font-medium mb-2">Gráfico de Dispersión</h3>
                  <ResponsiveContainer width="100%" height={400}>
                    <ScatterChart
                      margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" dataKey="cantidad" name="Cantidad" />
                      <YAxis type="number" dataKey="importe_total" name="Importe Total" />
                      <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                      <Legend />
                      <Scatter 
                        name="Normal" 
                        data={anomalyData.data.filter((d: any) => !d.is_anomaly)} 
                        fill="#8884d8" 
                      />
                      <Scatter 
                        name="Anomalía" 
                        data={anomalyData.data.filter((d: any) => d.is_anomaly)} 
                        fill="#ff0000" 
                      />
                    </ScatterChart>
                  </ResponsiveContainer>
                </div>
                
                <h3 className="font-medium mb-2">Transacciones Anómalas</h3>
                <DataTable
                  columns={[
                    { accessorKey: 'codigo_articulo', header: 'Código Artículo' },
                    { accessorKey: 'fecha', header: 'Fecha' },
                    { accessorKey: 'tipo_movimiento', header: 'Tipo' },
                    { accessorKey: 'cantidad', header: 'Cantidad' },
                    { accessorKey: 'importe_total', header: 'Importe Total', 
                      cell: (row: any) => row.importe_total.toLocaleString('es-ES', { 
                        style: 'currency', currency: 'EUR' 
                      }) 
                    },
                  ]}
                  data={anomalyData.data}
                  searchColumn="codigo_articulo"
                  placeholder="Buscar transacciones..."
                />
              </>
            )}
          </Card>
        </TabsContent>
        
        <TabsContent value="forecast">
          <Card className="p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Pronóstico de Demanda</h2>
            <p className="text-gray-600 mb-4">
              Predice la demanda futura de un artículo específico
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seleccionar artículo
                </label>
                <Combobox 
                  options={articles}
                  selectedValue={selectedArticle}
                  onSelect={setSelectedArticle}
                  placeholder="Buscar artículo..."
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Horizonte de pronóstico
                </label>
                <select 
                  className="w-full border rounded p-2"
                  value={horizon}
                  onChange={(e) => setHorizon(Number(e.target.value))}
                >
                  <option value={3}>3 meses</option>
                  <option value={6}>6 meses</option>
                  <option value={12}>12 meses</option>
                </select>
              </div>
            </div>
            
            <Button 
              onClick={() => runForecast()} 
              disabled={!selectedArticle || forecastLoading}
            >
              {forecastLoading ? 'Generando pronóstico...' : 'Generar Pronóstico'}
            </Button>
            
            {forecastData?.data && (
              <div className="mt-6">
                <h3 className="font-medium mb-2">Pronóstico de Demanda</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart
                    data={forecastData.data}
                    margin={{ top: 20, right: 30, left: 20, bottom: 30 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="ds" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="yhat" 
                      stroke="#8884d8" 
                      name="Pronóstico" 
                      activeDot={{ r: 8 }} 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="yhat_lower" 
                      stroke="#82ca9d" 
                      name="Límite inferior" 
                      strokeDasharray="3 3" 
                    />
                    <Line 
                      type="monotone" 
                      dataKey="yhat_upper" 
                      stroke="#82ca9d" 
                      name="Límite superior" 
                      strokeDasharray="3 3" 
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

export default function LabPage() {
  return (
    <QueryClientProvider client={queryClient}>
      <LabPageContent />
    </QueryClientProvider>
  );
}
