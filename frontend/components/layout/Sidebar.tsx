'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  Package, 
  Book, 
  MoveRight, 
  MoveLeft, 
  BarChart, 
  Warehouse,
  LayoutGrid,
  ArrowRightLeft,
  Beaker
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { name: 'Catálogo', href: '/catalogo', icon: LayoutGrid },
  { name: 'Clasificador', href: '/clasificador', icon: Book },
  { name: 'Entradas', href: '/entradas', icon: MoveRight },
  { name: 'Salidas', href: '/salidas', icon: MoveLeft },
  { name: 'Inventarios', href: '/inventarios', icon: BarChart },
  { name: 'Almacenes', href: '/almacenes', icon: Warehouse },
  { name: 'Laboratorio', href: '/lab', icon: Beaker },
];

export default function Sidebar() {
  const pathname = usePathname();
  
  return (
    <div className="w-64 bg-white text-gray-800 min-h-screen p-4 border-r">
      <div className="text-xl font-bold mb-8 px-3">Inventarios</div>
      <nav>
        <ul className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <li key={item.name}>
                <Link 
                  href={item.href}
                  className={cn(
                    "flex items-center gap-3 p-3 rounded-lg transition-all duration-300",
                    isActive 
                      ? "bg-blue-100 text-blue-600 font-medium" 
                      : "text-gray-600 hover:bg-gray-100"
                  )}
                >
                  <item.icon size={20} className={isActive ? "text-blue-600" : "text-gray-500"} />
                  <span>{item.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
}
