'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/Card';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface MonthlyInventory {
  mes: string;
  valor_final: number;
}

const monthlyData: MonthlyInventory[] = [
    { mes: 'Sep 2022', valor_final: 92000 },
    { mes: 'Oct 2022', valor_final: 95000 },
    { mes: 'Nov 2022', valor_final: 98000 },
    { mes: 'Dic 2022', valor_final: 105000 },
    { mes: 'Ene 2023', valor_final: 102000 },
    { mes: 'Feb 2023', valor_final: 112000 },
];

export default function InventariosPage() {
  // Mock summary data (you would fetch this from your backend)
  const totalValue = monthlyData.reduce((sum, item) => sum + item.valor_final, 0);
  const averageValue = totalValue / monthlyData.length;
  const currentValue = monthlyData[monthlyData.length - 1].valor_final;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Inventarios Mensuales</h1>
      
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { title: "Valor Inventario Actual", value: "€ 112,000", description: "Al final de Febrero 2023" },
          { title: "Total de Artículos en Stock", value: "1,250", description: "Unidades totales" },
          { title: "Mes de Mayor Crecimiento", value: "Febrero 2023", description: "+7% respecto a Enero" },
        ].map((stat, index) => (
          <Card key={index} className="p-4">
            <h3 className="text-sm font-medium text-gray-500">{stat.title}</h3>
            <p className="text-2xl font-bold">{stat.value}</p>
            <p className="text-xs text-gray-400">{stat.description}</p>
          </Card>
        ))}
      </div>

      <Card className="p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4">Evolución del Valor del Inventario</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="mes" />
            <YAxis />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="valor_final" 
              stroke="#8884d8" 
              name="Valor Final" 
              activeDot={{ r: 8 }}
              isAnimationActive={true}
              animationDuration={1000}
            />
          </LineChart>
        </ResponsiveContainer>
      </Card>

      <div>
        <h2 className="text-xl font-semibold mb-4">Datos Mensuales del Inventario</h2>
        <div className="rounded-md border overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Mes
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Valor (€)
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {monthlyData.map((item) => (
                <tr key={item.mes}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {item.mes}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {item.valor_final.toLocaleString('es-ES', {
                      style: 'currency',
                      currency: 'EUR',
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

// Componente CustomTooltip
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <Card className="p-4">
        <p className="font-medium">{label}</p>
        <p className="text-blue-600">
          {payload[0].name}: {payload[0].value.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' })}
        </p>
      </Card>
    );
  }
  return null;
};
