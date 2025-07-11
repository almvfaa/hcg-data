import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Sidebar from '@/components/layout/Sidebar';
import TopBar from '@/components/layout/TopBar';
import { AnimatePresence } from 'framer-motion';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Sistema de Inventarios',
  description: 'Sistema de gestión de inventarios',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es">
      <body className={inter.className}>
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1 flex flex-col">
            <TopBar />
            <main className="flex-1 p-6 bg-gray-50">
              <AnimatePresence mode="wait">
                {children}
              </AnimatePresence>
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
