"use client";

import type { ReactNode } from "react";
import { QueryClientProvider, QueryClient } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { AnimationProvider } from "@memex/animations";
import { useReducedMotion } from "@memex/hooks";
import { TooltipProvider } from "@radix-ui/react-tooltip";

let queryClient: QueryClient;

function getQueryClient() {
  if (!queryClient) {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          staleTime: 1000 * 60 * 5,
          gcTime: 1000 * 60 * 30,
          retry: 2,
          refetchOnWindowFocus: false,
        },
        mutations: {
          retry: 1,
        },
      },
    });
  }
  return queryClient;
}

interface ProvidersProps {
  children: ReactNode;
}

function ProvidersInner({ children }: ProvidersProps) {
  const reducedMotion = useReducedMotion();

  return (
    <AnimationProvider reducedMotion={reducedMotion}>
      <TooltipProvider delayDuration={300}>
        {children}
      </TooltipProvider>
    </AnimationProvider>
  );
}

export function Providers({ children }: ProvidersProps) {
  return (
    <QueryClientProvider client={getQueryClient()}>
      <ProvidersInner>
        {children}
      </ProvidersInner>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
