// frontend/providers/QueryProvider.tsx
'use client';

import { QueryClient, QueryClientProvider, QueryClientProviderProps } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

/**
 * A custom provider component that sets up the TanStack Query client.
 * This centralizes the configuration for data fetching and caching.
 * @param {object} props - The component props.
 * @param {React.ReactNode} props.children - The child components to render.
 */
export default function QueryProvider({ children }: { children: React.ReactNode }) {
  // Use useState to create a stable QueryClient instance,
  // preventing it from being recreated on every render.
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        // It's often useful to disable refetching on window focus during development
        // to avoid unexpected API calls.
        refetchOnWindowFocus: false,
        
        // Default to retrying failed queries once.
        retry: 1,
        
        // Set a default stale time to avoid immediate refetches.
        // For example, 5 minutes.
        staleTime: 1000 * 60 * 5,
      }
    }
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {/* Render the rest of the application */}
      {children}
      
      {/* 
        The React Query Devtools are invaluable for debugging.
        They will only be included in development builds.
      */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
