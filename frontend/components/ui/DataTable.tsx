'use client';

import * as React from 'react';
import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  useReactTable,
  getSortedRowModel,
  SortingState,
} from '@tanstack/react-table';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons'; // Import the centralized icons object

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { MotionButton } from '@/components/ui/motion-button';
import { Skeleton } from '@/components/ui/Skeleton';

// ... (interfaces remain the same)

// Example of a sortable header using the new icon system
export const SortableHeader = ({ column, children }: { column: any, children: React.ReactNode }) => (
  <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}>
    {children}
    {column.getIsSorted() === 'asc' && <Icons.chevronUp className="ml-2 h-4 w-4" />}
    {column.getIsSorted() === 'desc' && <Icons.chevronDown className="ml-2 h-4 w-4" />}
    {!column.getIsSorted() && <Icons.sort className="ml-2 h-4 w-4" />}
  </Button>
);

export function DataTable<TData extends { id: any } >({
  columns,
  data,
  isLoading = false,
  pagination,
  primaryColumnKey,
}: any) { // Simplified props for example
  const [sorting, setSorting] = React.useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    manualPagination: true,
    state: {
      sorting,
    },
  });

  const rowVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.3 } },
    exit: { opacity: 0, transition: { duration: 0.2 } },
  };

  return (
    <div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup:any) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header:any) => (
                  <TableHead key={header.id}>{header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}</TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            <AnimatePresence>
              {isLoading ? (
                // Skeleton rows...
              ) : (
                table.getRowModel().rows?.length ? (
                  table.getRowModel().rows.map((row:any) => (
                    <motion.tr
                      key={row.original.id}
                      variants={rowVariants}
                      initial="hidden"
                      animate="visible"
                      exit="exit"
                      layout
                      className="hover:bg-muted/50"
                      data-state={row.getIsSelected() && 'selected'}
                    >
                      {row.getVisibleCells().map((cell:any) => (
                        <TableCell key={cell.id} className={cn("py-4", primaryColumnKey === cell.column.id && "font-medium text-foreground")}>
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </TableCell>
                      ))}
                    </motion.tr>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={columns.length} className="h-24 text-center">No se encontraron resultados.</TableCell>
                  </TableRow>
                )
              )}
            </AnimatePresence>
          </TableBody>
        </Table>
      </div>
      
      {pagination && (
        <div className="flex items-center justify-end space-x-2 py-4">
          <span className="text-sm text-muted-foreground">
            Página {pagination.currentPage} de {pagination.totalPages}
          </span>
          <MotionButton variant="outline" size="sm" onClick={() => pagination.onPageChange(pagination.currentPage - 1)} disabled={pagination.currentPage <= 1}>
            <Icons.chevronLeft className="h-4 w-4" />
          </MotionButton>
          <MotionButton variant="outline" size="sm" onClick={() => pagination.onPageChange(pagination.currentPage + 1)} disabled={pagination.currentPage >= pagination.totalPages}>
            <Icons.chevronRight className="h-4 w-4" />
          </MotionButton>
        </div>
      )}
    </div>
  );
}
