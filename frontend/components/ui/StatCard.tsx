tsx
import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  description: string;
}

export function StatCard({ title, value, description }: StatCardProps) {
  return (
    <div className="flex flex-col p-6 bg-white rounded-lg shadow-md">
      <div className="text-sm font-medium text-gray-500">{title}</div>
      <div className="mt-1 text-3xl font-semibold text-gray-900">{value}</div>
      <div className="mt-2 text-sm text-gray-600">{description}</div>
    </div>
  );
}