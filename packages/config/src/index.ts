import { z } from "zod";

export const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.coerce.number().default(3000),
  API_PORT: z.coerce.number().default(8000),
  NEXT_PUBLIC_API_URL: z.string().url().default("http://localhost:8000"),
  NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),
  DATABASE_URL: z.string().default("postgresql+asyncpg://memex:memex@localhost:5432/memex"),
  JWT_SECRET: z.string().min(16),
  JWT_ALGORITHM: z.string().default("HS256"),
  JWT_ACCESS_EXPIRE_MINUTES: z.coerce.number().default(15),
  JWT_REFRESH_EXPIRE_DAYS: z.coerce.number().default(7),
  GOOGLE_CLIENT_ID: z.string().optional(),
  GOOGLE_CLIENT_SECRET: z.string().optional(),
  RESEND_API_KEY: z.string().optional(),
  OPENAI_API_KEY: z.string().optional(),
  COGNEE_API_KEY: z.string().optional(),
  COGNEE_URL: z.string().default("http://localhost:8001"),
});

export type Env = z.infer<typeof envSchema>;

export const siteConfig = {
  name: "MEMEX",
  description: "The Operating System for Artificial Memory",
  url: "https://memex.sh",
  ogImage: "https://memex.sh/og.png",
  links: {
    twitter: "https://x.com/memex",
    github: "https://github.com/memex",
  },
} as const;

export type SiteConfig = typeof siteConfig;
