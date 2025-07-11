// frontend/components/ui/ArticuloCard.tsx
import React, { memo } from 'react';
// Assuming the generated types are in this path.
// You might need to adjust if your tsconfig paths are different.
import { components } from '@/src/types/api.d';

// Get the specific type for a single article from our generated types.
type Articulo = components['schemas']['Articulo'];

interface ArticuloCardProps {
  articulo: Articulo;
  // The onSelect function will receive the article's unique code.
  onSelect: (codigo: string) => void;
}

/**
 * A memoized component to display a single article.
 * It will only re-render if its `articulo` or `onSelect` props change.
 */
const ArticuloCard = memo(({ articulo, onSelect }: ArticuloCardProps) => {
  console.log(`Rendering ArticuloCard: ${articulo.codigo_articulo}`); // For debugging re-renders

  return (
    <div 
      className="p-4 border rounded-lg shadow-sm hover:shadow-md hover:-translate-y-1 transition-all cursor-pointer"
      onClick={() => onSelect(articulo.codigo_articulo)}
    >
      <h3 className="font-bold text-lg">{articulo.descripcion_articulo}</h3>
      <p className="text-sm text-muted-foreground">Código: {articulo.codigo_articulo}</p>
      {articulo.unidad_medida && (
        <p className="text-sm text-gray-500 mt-2">Unidad: {articulo.unidad_medida}</p>
      )}
    </div>
  );
});

// Set a display name for easier debugging in React DevTools
ArticuloCard.displayName = 'ArticuloCard';

export default ArticuloCard;
