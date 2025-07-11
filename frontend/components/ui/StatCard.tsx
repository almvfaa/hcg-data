// frontend/components/ui/StatCard.tsx
import { cn } from "@/lib/utils"

interface StatCardProps {
  title: string
  value: string
  className?: string
}

export function StatCard({ title, value, className }: StatCardProps) {
  return (
    <div className={cn("p-4 border rounded-lg", className)}>
      <h3 className="text-sm text-muted-foreground">{title}</h3>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  )
}
