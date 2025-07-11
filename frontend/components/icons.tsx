// frontend/components/icons.tsx
import { 
  LucideIcon,
  Edit, 
  Trash2, 
  Settings, 
  Plus, 
  Search,
  ArrowUpDown,
  ChevronDown,
  ChevronUp,
  ChevronLeft,
  ChevronRight,
  MoreHorizontal,
  FileText,
  AlertTriangle,
  CheckCircle2,
  XCircle
} from 'lucide-react'

// Define a type for the Icons object for better type-safety.
export type Icon = LucideIcon

export const Icons = {
  // General Actions
  add: Plus,
  edit: Edit,
  delete: Trash2,
  settings: Settings,
  search: Search,

  // Table / Sorting
  sort: ArrowUpDown,
  chevronDown: ChevronDown,
  chevronUp: ChevronUp,
  chevronLeft: ChevronLeft,
  chevronRight: ChevronRight,
  
  // Misc
  more: MoreHorizontal,
  file: FileText,
  warning: AlertTriangle,
  success: CheckCircle2,
  error: XCircle,
}
