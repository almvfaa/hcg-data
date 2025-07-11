'use client';

import { useState, useCallback } from 'react';
import { useArticulos } from '@/hooks/useArticulos';
import { Skeleton } from '@/components/ui/Skeleton';
import ArticuloCard from '@/components/ui/ArticuloCard'; // Import the new memoized component
import { Input } from '@/components/ui/input';
import { useRouter } from 'next/navigation'; // Import the router

export default function CatalogoPage() {
  const [search, setSearch] = useState('');
  const { data, isLoading, isError, error } = useArticulos({ search });

  const router = useRouter();

  // The handleSelect function is wrapped in useCallback.
  // This ensures that the function reference is stable across re-renders,
  // preventing the ArticuloCard components from re-rendering unnecessarily.
  const handleSelect = useCallback((codigo: string) => {
    // We can add navigation logic here, for example.
    console.log(`Selected article code: ${codigo}`);
    // router.push(`/articulos/${codigo}`); // Example of navigation
  }, [router]); // router is stable, so this function is created only once.

  if (isError) {
    return (
      <div className="p-4 bg-red-100 text-red-700 rounded">
        Error: {error?.message || 'Error desconocido'}
      </div>
    );
  }

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-4">Catálogo de Artículos</h1>
      
      <Input
        type="text"
        placeholder="Buscar por descripción o código..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="border rounded p-2 mb-6 w-full max-w-md"
      />
      
      {isLoading && !data ? (
        // Show skeleton loader on initial load
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => <Skeleton key={i} className="w-full h-24 rounded-lg" />)}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data?.articulos?.map(articulo => (
            <ArticuloCard 
              key={articulo.codigo_articulo} 
              articulo={articulo} 
              onSelect={handleSelect} 
            />
          ))}
        </div>
      )}

      {data?.articulos?.length === 0 && !isLoading && (
        <p>No se encontraron artículos.</p>
      )}
    </div>
  );
}
