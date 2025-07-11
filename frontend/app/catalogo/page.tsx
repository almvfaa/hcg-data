'use client';

import { useState, useEffect } from 'react';
import { DataTable } from '@/components/ui/DataTable';
import { ColumnDef } from '@tanstack/react-table';
import { Input } from '@/components/ui/input';

interface Articulo {
  codigo_articulo: string;
  descripcion_articulo: string;
  unidad_medida: string;
  partida_especifica: string;
}

const columns: ColumnDef<Articulo>[] = [
  {
    accessorKey: 'codigo_articulo',
    header: 'Código',
  },
  {
    accessorKey: 'descripcion_articulo',
    header: 'Descripción',
  },
  {
    accessorKey: 'unidad_medida',
    header: 'Unidad',
  },
  {
    accessorKey: 'partida_especifica',
    header: 'Partida Específica',
  },
];

async function fetchArticulos(): Promise<Articulo[]> {
  const res = await fetch('/api/v1/catalogo');
  if (!res.ok) {
    throw new Error('Failed to fetch articulos');
  }
  return res.json();
}

export default function CatalogoPage() {
  const [data, setData] = useState<Articulo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const articulos = await fetchArticulos();
        setData(articulos);
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
    item.descripcion_articulo.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.codigo_articulo.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-6">Catálogo de Artículos</h1>
       <Input
          placeholder="Buscar artículos..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-sm mb-4"
        />
      <DataTable
        columns={columns}
        data={filteredData}
        placeholder="Buscar artículos..."
      />
    </div>
  );
}
