// frontend/app/lab/segmentacion/page.tsx
'use client';

import { Button } from '@/components/ui/button';
import { DataTable } from '@/components/ui/DataTable';
import { Skeleton } from '@/components/ui/Skeleton';
import { useAsyncTask } from '@/hooks/useAsyncTask';
import apiClient from '@/lib/axios';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Terminal } from 'lucide-react';

// Define the shape of the result data
interface SegmentationResult {
  codigo_articulo: string;
  descripcion_articulo: string;
  valor_total_movimiento: number;
  clase_abc: 'A' | 'B' | 'C';
}

export default function SegmentacionPage() {
  // Use the generic hook for async task management.
  // The component is completely unaware of polling or task IDs.
  const { execute, isLoading, isSuccess, isError, error, result } = useAsyncTask<SegmentationResult[]>();

  // This function tells the hook how to start the task.
  const startAnalysis = () => {
    // The hook's 'execute' function takes our API call as an argument.
    execute(() => apiClient.post('/lab/run/segmentation'));
  };

  return (
    <div className="p-4 md:p-6">
      <h1 className="text-2xl font-bold mb-4">Análisis de Segmentación ABC</h1>
      <p className="text-muted-foreground mb-6">
        Clasifique los artículos en categorías A, B y C según su valor de movimiento para priorizar la gestión del inventario.
      </p>
      
      <Button 
        onClick={startAnalysis}
        disabled={isLoading}
        className="mb-6"
      >
        {isLoading ? 'Procesando en segundo plano...' : 'Iniciar Análisis Asíncrono'}
      </Button>

      {/* Loading state while the task is running */}
      {isLoading && (
        <div className="space-y-4">
          <Alert>
            <Terminal className="h-4 w-4" />
            <AlertTitle>Tarea en Progreso</AlertTitle>
            <AlertDescription>
              El análisis se está ejecutando en el servidor. Los resultados aparecerán aquí automáticamente cuando estén listos.
            </AlertDescription>
          </Alert>
          <Skeleton className="w-full h-48 rounded-lg" />
        </div>
      )}

      {/* Error state */}
      {isError && (
          <Alert variant="destructive">
            <Terminal className="h-4 w-4" />
            <AlertTitle>Error en la Tarea</AlertTitle>
            <AlertDescription>
              {error?.message || "Ocurrió un error al procesar la tarea."}
            </AlertDescription>
          </Alert>
      )}

      {/* Success state with results */}
      {isSuccess && result && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-4">Resultados del Análisis</h2>
          <DataTable 
            columns={[
              { header: 'Código', accessorKey: 'codigo_articulo' },
              { header: 'Descripción', accessorKey: 'descripcion_articulo' },
              { 
                header: 'Valor Total Movimiento', 
                accessorKey: 'valor_total_movimiento',
                cell: ({ row }) => {
                    const amount = parseFloat(row.getValue('valor_total_movimiento'))
                    const formatted = new Intl.NumberFormat('es-ES', {
                        style: 'currency',
                        currency: 'EUR'
                    }).format(amount)
                    return <div className="text-right font-medium">{formatted}</div>
                }
              },
              { header: 'Clase ABC', accessorKey: 'clase_abc' },
            ]}
            data={result}
          />
        </div>
      )}
    </div>
  );
}
