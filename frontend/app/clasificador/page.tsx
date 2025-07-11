'use client';

import { useState, useEffect } from 'react';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';
import { DataTable } from '@/components/ui/DataTable';
import { ColumnDef } from '@tanstack/react-table';

// Interfaces
interface Capitulo {
  capitulo_gasto: number;
  denominacion_capitulo: string;
}

interface Concepto {
  concepto_gasto: number;
  denominacion_gasto: string;
  capitulo_gasto: number;
}

interface PartidaGenerica {
  partida_generica: number;
  denominacion_partida_generica: string;
  concepto_gasto: number;
}

interface PartidaEspecifica {
  partida_especifica: number;
  denominacion_partida_especifica: string;
  partida_generica: number;
}

// Column Definitions
const capituloColumns: ColumnDef<Capitulo>[] = [
  { accessorKey: 'capitulo_gasto', header: 'Capítulo' },
  { accessorKey: 'denominacion_capitulo', header: 'Denominación' },
];

const conceptoColumns: ColumnDef<Concepto>[] = [
  { accessorKey: 'concepto_gasto', header: 'Concepto' },
  { accessorKey: 'denominacion_gasto', header: 'Denominación' },
  { accessorKey: 'capitulo_gasto', header: 'Capítulo' },
];

const partidaGenericaColumns: ColumnDef<PartidaGenerica>[] = [
  { accessorKey: 'partida_generica', header: 'Partida Genérica' },
  { accessorKey: 'denominacion_partida_generica', header: 'Denominación' },
  { accessorKey: 'concepto_gasto', header: 'Concepto' },
];

const partidaEspecificaColumns: ColumnDef<PartidaEspecifica>[] = [
  { accessorKey: 'partida_especifica', header: 'Partida Específica' },
  { accessorKey: 'denominacion_partida_especifica', header: 'Denominación' },
  { accessorKey: 'partida_generica', header: 'Partida Genérica' },
];

// Data Fetching Functions
async function fetchData<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch data from ${url}`);
  }
  return res.json();
}

// Reusable Component for Tab Content
function ClasificadorTab<T>({
  columns,
  endpoint,
  placeholder,
}: {
  columns: ColumnDef<T>[];
  endpoint: string;
  placeholder: string;
}) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const fetchedData = await fetchData<T[]>(`/api/v1/clasificador/${endpoint}`);
        setData(fetchedData);
        setError(null);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [endpoint]);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <DataTable columns={columns} data={data} placeholder={placeholder} />;
}


export default function ClasificadorPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Clasificador Económico</h1>
      <Tabs defaultValue="capitulos" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="capitulos">Capítulos</TabsTrigger>
          <TabsTrigger value="conceptos">Conceptos</TabsTrigger>
          <TabsTrigger value="genericas">Partidas Genéricas</TabsTrigger>
          <TabsTrigger value="especificas">Partidas Específicas</TabsTrigger>
        </TabsList>
        <TabsContent value="capitulos">
          <ClasificadorTab
            columns={capituloColumns}
            endpoint="capitulos"
            placeholder="Buscar capítulos..."
          />
        </TabsContent>
        <TabsContent value="conceptos">
          <ClasificadorTab
            columns={conceptoColumns}
            endpoint="conceptos"
            placeholder="Buscar conceptos..."
          />
        </TabsContent>
        <TabsContent value="genericas">
           <ClasificadorTab
            columns={partidaGenericaColumns}
            endpoint="partidas-genericas"
            placeholder="Buscar partidas genéricas..."
          />
        </TabsContent>
        <TabsContent value="especificas">
           <ClasificadorTab
            columns={partidaEspecificaColumns}
            endpoint="partidas-especificas"
            placeholder="Buscar partidas específicas..."
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
