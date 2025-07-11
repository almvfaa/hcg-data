'use client';

import { useState, useEffect } from 'react';
import { DataTable } from '@/components/ui/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { FilterBar, DateRangePicker } from '@/components/ui/FilterBar';
import { Button } from '@/components/ui/button';

interface MovimientoSalida {
  id_movimiento: number;
  fecha: Date;
  codigo_articulo: string;
  descripcion_articulo: string;
  cantidad: number;
  importe_total: number;
  precio_unitario: number;
}

const columns: ColumnDef<MovimientoSalida>[] = [
  {
    accessorKey: 'fecha',
    header: 'Fecha',
    cell: ({ row }) => {
      const fecha = new Date(row.getValue('fecha'));
      return fecha.toLocaleDateString('es-ES');
    },
  },
  {
    accessorKey: 'codigo_articulo',
    header: 'Código Artículo',
  },
  {
    accessorKey: 'descripcion_articulo',
    header: 'Descripción',
  },
  {
    accessorKey: 'cantidad',
    header: 'Cantidad',
  },
  {
    accessorKey: 'precio_unitario',
    header: 'Precio Unitario',
    cell: ({ row }) => {
      const precio = row.getValue('precio_unitario') as number;
      return precio.toLocaleString('es-ES', {
        style: 'currency',
        currency: 'EUR',
      });
    },
  },
  {
    accessorKey: 'importe_total',
    header: 'Importe Total',
    cell: ({ row }) => {
      const importe = row.getValue('importe_total') as number;
      return importe.toLocaleString('es-ES', {
        style: 'currency',
        currency: 'EUR',
      });
    },
  },
];

interface FetchParams {
  searchTerm?: string;
  startDate?: string;
  endDate?: string;
}

async function fetchSalidas(params: FetchParams = {}): Promise<MovimientoSalida[]> {
  const query = new URLSearchParams();
  if (params.searchTerm) query.append('q', params.searchTerm);
  if (params.startDate) query.append('start_date', params.startDate);
  if (params.endDate) query.append('end_date', params.endDate);

  // Asume que el backend está corriendo en el puerto 8000
  // y Next.js está configurado para proxyar las peticiones a /api
  const res = await fetch(`/api/v1/movimientos/salidas?${query.toString()}`);
  if (!res.ok) {
    // Esto podría ser manejado de forma más robusta con un sistema de notificaciones
    throw new Error('Failed to fetch data');
  }
  const data = await res.json();
  return data;
}


export default function SalidasPage() {
  const [data, setData] = useState<MovimientoSalida[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [dateRange, setDateRange] = useState<{ start?: Date; end?: Date }>({});
  const [searchTerm, setSearchTerm] = useState('');
  
  // El useEffect ahora dependerá de los filtros para volver a cargar los datos
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        // Prepara los parámetros para la API
        const params: FetchParams = {
          searchTerm: searchTerm,
          startDate: dateRange.start?.toISOString().split('T')[0],
          endDate: dateRange.end?.toISOString().split('T')[0],
        };
        // Solo busca si el término de búsqueda tiene más de 2 caracteres, por ejemplo
        const salidas = await fetchSalidas(params);
        setData(salidas);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
    // Se vuelve a ejecutar cuando cambia el término de búsqueda o el rango de fechas
  }, [searchTerm, dateRange]);

  // El filtrado en el cliente ya no es necesario, los datos ya vienen filtrados del backend

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Salidas</h1>
      <FilterBar>
        <DateRangePicker
          dateRange={dateRange}
          onDateRangeChange={setDateRange}
        />
        <input
          type="text"
          placeholder="Buscar artículo..."
          className="border rounded p-2"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button variant="outline">Exportar CSV</Button>
      </FilterBar>
      <DataTable
        columns={columns}
        data={data} // Usamos 'data' directamente
        placeholder="Filtrar salidas..."
      />
    </div>
  );
}
