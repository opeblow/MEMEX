export const config = {
  app: {
    name: "MEMEX",
    tagline: "The Operating System for Artificial Memory",
    url: process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000",
    apiUrl: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  },
  auth: {
    googleClientId: process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID,
    redirectUri: `${process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000"}/auth/callback`,
  },
  pagination: {
    defaultPageSize: 20,
    maxPageSize: 100,
  },
  upload: {
    maxFileSize: 100 * 1024 * 1024,
    acceptedMimeTypes: [
      "text/plain",
      "text/markdown",
      "application/pdf",
      "application/json",
      "text/csv",
      "image/png",
      "image/jpeg",
      "image/webp",
      "audio/mpeg",
      "audio/wav",
      "video/mp4",
    ],
  },
} as const;
