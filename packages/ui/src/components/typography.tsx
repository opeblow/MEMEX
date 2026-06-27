import type { ReactNode, HTMLAttributes } from "react";
import { cn } from "../lib/cn";
import { cva, type VariantProps } from "class-variance-authority";

const typographyVariants = cva("", {
  variants: {
    variant: {
      h1: "text-4xl font-bold tracking-tight text-white sm:text-5xl",
      h2: "text-3xl font-semibold tracking-tight text-white",
      h3: "text-2xl font-semibold tracking-tight text-white",
      h4: "text-xl font-semibold tracking-tight text-white",
      body: "text-base text-white/70 leading-relaxed",
      bodySm: "text-sm text-white/60 leading-relaxed",
      caption: "text-xs text-white/40",
      lead: "text-lg text-white/80 leading-relaxed",
      code: "font-mono text-sm text-cyan-400 bg-cyan-500/10 rounded-md px-1.5 py-0.5",
    },
  },
  defaultVariants: {
    variant: "body",
  },
});

type TypographyElement = "h1" | "h2" | "h3" | "h4" | "p" | "span";

const variantMap: Record<string, TypographyElement> = {
  h1: "h1",
  h2: "h2",
  h3: "h3",
  h4: "h4",
  body: "p",
  bodySm: "p",
  caption: "span",
  lead: "p",
};

interface TypographyProps
  extends HTMLAttributes<HTMLElement>,
    VariantProps<typeof typographyVariants> {
  as?: TypographyElement;
  children: ReactNode;
}

export function Typography({
  className,
  variant = "body",
  as,
  children,
  ...props
}: TypographyProps) {
  const Comp = as ?? variantMap[variant ?? "body"] ?? "p";

  return (
    <Comp
      className={cn(typographyVariants({ variant, className }))}
      {...(props as HTMLAttributes<HTMLElement>)}
    >
      {children}
    </Comp>
  );
}
