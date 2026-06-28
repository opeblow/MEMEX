"use client";

import { Slot } from "@radix-ui/react-slot";
import { type VariantProps, cva } from "class-variance-authority";
import { type ButtonHTMLAttributes, type ReactNode, forwardRef } from "react";
import { cn } from "../lib/cn";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-lg text-sm font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-500/50 focus-visible:ring-offset-2 focus-visible:ring-offset-black disabled:pointer-events-none disabled:opacity-50 cursor-pointer",
  {
    variants: {
      variant: {
        primary: "bg-white text-black hover:bg-white/90 active:scale-[0.98]",
        secondary:
          "border border-white/10 bg-white/5 text-white hover:bg-white/10 active:scale-[0.98]",
        ghost: "text-white/60 hover:text-white hover:bg-white/5 active:scale-[0.98]",
        danger:
          "bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 active:scale-[0.98]",
        glass:
          "bg-white/5 backdrop-blur-xl border border-white/10 text-white hover:bg-white/10 active:scale-[0.98]",
        link: "text-amber-400 underline-offset-4 hover:underline",
        glow: [
          "relative bg-black text-white border border-amber-500/30 overflow-hidden",
          "before:absolute before:inset-0 before:rounded-lg before:bg-gradient-to-r before:from-amber-500/0 before:via-amber-500/20 before:to-amber-500/0 before:animate-energy-flow before:bg-[length:200%_100%]",
          "hover:border-amber-500/60 hover:shadow-[0_0_20px_rgba(245,158,11,0.3)]",
          "active:scale-[0.98]",
        ].join(" "),
        energy: [
          "relative bg-black text-white border border-cyan-500/30 overflow-hidden",
          "before:absolute before:inset-0 before:rounded-lg before:bg-gradient-to-r before:from-cyan-500/0 before:via-cyan-500/20 before:to-cyan-500/0 before:animate-energy-flow before:bg-[length:200%_100%]",
          "hover:border-cyan-500/60 hover:shadow-[0_0_20px_rgba(6,182,212,0.3)]",
          "active:scale-[0.98]",
        ].join(" "),
      },
      size: {
        sm: "h-8 px-3 text-xs gap-1.5",
        md: "h-10 px-4 text-sm gap-2",
        lg: "h-12 px-6 text-base gap-2.5",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  },
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      asChild = false,
      loading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref,
  ) => {
    const Comp = asChild ? Slot : "button";

    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || loading}
        {...props}
      >
        {loading ? (
          <svg
            className="h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        ) : (
          leftIcon
        )}
        {children}
        {!loading && rightIcon}
      </Comp>
    );
  },
);

Button.displayName = "Button";

export { Button, buttonVariants };
