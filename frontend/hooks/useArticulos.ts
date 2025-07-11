// frontend/hooks/useArticulos.ts
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/axios';

// Define the shape of a single article object
export interface Articulo {
  codigo_articulo: string;
  descripcion_articulo: string;
  unidad_medida: string;
  // Add other properties from your API response as needed
}

// Define the shape of the API response
// This often includes pagination details and the data array
interface ArticulosApiResponse {
  total: number;
  articulos: Articulo[];
}

// Define the parameters for the hook
interface UseArticulosParams {
  page?: number;
  limit?: number;
  search?: string;
}

/**
 * Custom hook to fetch and manage a paginated and searchable list of articles.
 * @param {UseArticulosParams} params - The parameters for filtering and pagination.
 * @returns The result of the useQuery hook.
 */
export const useArticulos = (params: UseArticulosParams = {}) => {
  const { page = 1, limit = 10, search = '' } = params;

  return useQuery<ArticulosApiResponse, Error>({
    // The query key is an array that uniquely identifies this query.
    // It includes the resource name and any parameters that affect the data.
    queryKey: ['articulos', { page, limit, search }],
    
    // The query function is responsible for fetching the data.
    queryFn: async () => {
      // Use the centralized apiClient to make the GET request.
      const response = await apiClient.get<ArticulosApiResponse>('/catalogo/articulos', {
        params: {
          skip: (page - 1) * limit,
          limit: limit,
          search: search,
        }
      });
      return response; // Axios interceptor already unwraps response.data
    },
    
    // This option is great for paginated tables. It keeps showing the old data
    // while the new data is being fetched in the background, preventing UI flickering.
    placeholderData: (previousData) => previousData,
  });
};
