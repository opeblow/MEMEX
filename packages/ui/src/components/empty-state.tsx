import type { ReactNode } from "react";
import { cn } from "../lib/cn";

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({
  icon,
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-3 py-16 text-center",
        className,
      )}
    >
      {icon && (
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
          {icon}
        </div>
      )}
      <p className="text-base font-medium text-white/50">{title}</p>
      {description && (
        <p className="max-w-sm text-sm text-white/30">{description}</p>
      )}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}
