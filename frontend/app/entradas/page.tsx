'use client';

import { useState, useEffect } from 'react';
import { DataTable } from '@/components/ui/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { FilterBar, DateRangePicker } from '@/components/ui/FilterBar';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { format } from 'date-fns';
import { es } from 'date-fns/locale';

interface MovimientoEntrada {
  id_movimiento: number;
  codigo_articulo: string;
  fecha: Date; // Changed from FECHA to fecha for consistency
  cantidad: number;
  importe_total: number;
  precio_unitario_historico?: number;
}

const columns: ColumnDef<MovimientoEntrada>[] = [
  {
    accessorKey: 'id_movimiento',
    header: 'ID Movimiento',
  },
  {
    accessorKey: 'codigo_articulo',
    header: 'Código Artículo',
  },
  {
    accessorKey: 'fecha', // Changed from FECHA
    header: 'Fecha',
    cell: ({ row }) => {
      const date = new Date(row.getValue('fecha')); // Ensure date is parsed correctly
      return format(date, 'dd/MM/yyyy', { locale: es });
    },
  },
  {
    accessorKey: 'cantidad',
    header: 'Cantidad',
  },
  {
    accessorKey: 'importe_total',
    header: 'Importe Total',
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue('importe_total'));
      const formatted = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
      }).format(amount);

      return <div className="text-right">{formatted}</div>;
    },
  },
  {
    accessorKey: 'precio_unitario_historico',
    header: 'Precio Unitario Histórico',
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue('precio_unitario_historico'));
      if (isNaN(amount)) return null;
      const formatted = new Intl.NumberFormat('es-MX', {
        style: 'currency',
        currency: 'MXN',
      }).format(amount);

      return <div className="text-right">{formatted}</div>;
    },
  },
];

async function fetchEntradas(): Promise<MovimientoEntrada[]> {
  const res = await fetch('/api/v1/movimientos/entradas');
  if (!res.ok) {
    throw new Error('Failed to fetch entradas data');
  }
  return res.json();
}

export default function EntradasPage() {
  const [data, setData] = useState<MovimientoEntrada[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [dateRange, setDateRange] = useState<{ start?: Date; end?: Date }>({});
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const entradas = await fetchEntradas();
        setData(entradas);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);
  
  const filteredData = data.filter(item =>
    (item.codigo_articulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.cantidad.toString().includes(searchTerm) ||
    item.importe_total.toString().includes(searchTerm) ||
    (item.precio_unitario_historico?.toString() || '').includes(searchTerm)) &&
    (!dateRange.start || new Date(item.fecha) >= dateRange.start) &&
    (!dateRange.end || new Date(item.fecha) <= dateRange.end)
  );

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Entradas de Almacén</h1>
      <FilterBar>
        <DateRangePicker dateRange={dateRange} onDateRangeChange={setDateRange} />
        <Input
          placeholder="Buscar por código, cantidad, importe..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-sm"
        />
      </FilterBar>
      <DataTable
        columns={columns}
        data={filteredData}
        placeholder="Buscar en la tabla..."
      />
    </div>
  );
}
