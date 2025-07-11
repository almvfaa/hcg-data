// frontend/hooks/useArticulos.ts
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api'; // Using the new, more robust api client
import { components } from '@/src/types/api.d'; // Import generated types

// --- Type Definitions ---
// These types are now sourced directly from the backend's OpenAPI schema.
// There is no need to manually define them on the frontend anymore.
type Articulo = components['schemas']['Articulo'];

// We can create a more specific type for the API response if the backend provides it.
// If not, we can assume it's an array of Articulos.
// For this example, let's assume the API returns an object with a 'total' and 'articulos' property.
interface ArticulosApiResponse {
  total: number;
  articulos: Articulo[];
}

// Parameters for the hook remain the same.
interface UseArticulosParams {
  page?: number;
  limit?: number;
  search?: string;
}

/**
 * A fully type-safe custom hook to fetch and manage articles.
 * It uses types generated directly from the backend's OpenAPI specification.
 * @param {UseArticulosParams} params - The parameters for filtering and pagination.
 * @returns The result of the useQuery hook, strongly typed.
 */
export const useArticulos = (params: UseArticulosParams = {}) => {
  const { page = 1, limit = 10, search = '' } = params;

  return useQuery<ArticulosApiResponse, Error>({
    queryKey: ['articulos', { page, limit, search }],
    
    queryFn: async () => {
      // The apiClient is already configured with the base URL.
      // We pass the generic type to apiClient.get to get a typed response.
      const response = await apiClient.get<ArticulosApiResponse>('/catalogo/articulos', {
        params: {
          skip: (page - 1) * limit,
          limit: limit,
          search: search,
        }
      });
      // The Axios interceptor in api.ts now handles unwrapping the .data property
      return response.data; 
    },
    
    // Keep previous data for a smoother pagination experience
    placeholderData: (previousData) => previousData,
  });
};
