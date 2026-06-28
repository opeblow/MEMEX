import { api } from "../api/client";

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  displayName: string;
}

export interface AuthResponse {
  user: {
    id: string;
    email: string;
    displayName: string;
    avatarUrl?: string;
    role: string;
  };
  accessToken: string;
  refreshToken: string;
}

function setCookie(name: string, value: string, days: number) {
  if (typeof document === "undefined") return;
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function removeCookie(name: string) {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax`;
}

export function setTokens(accessToken: string, refreshToken: string) {
  localStorage.setItem("memex_access_token", accessToken);
  localStorage.setItem("memex_refresh_token", refreshToken);
  setCookie("memex_access_token", accessToken, 1);
  setCookie("memex_refresh_token", refreshToken, 7);
}

export function clearTokens() {
  localStorage.removeItem("memex_access_token");
  localStorage.removeItem("memex_refresh_token");
  removeCookie("memex_access_token");
  removeCookie("memex_refresh_token");
}

export async function loginWithEmail(credentials: LoginCredentials) {
  const response = await api.post<AuthResponse>("/api/v1/memex/auth/login", credentials);
  setTokens(response.accessToken, response.refreshToken);
  return response;
}

export async function registerWithEmail(credentials: RegisterCredentials) {
  const response = await api.post<AuthResponse>("/api/v1/memex/auth/register", credentials);
  setTokens(response.accessToken, response.refreshToken);
  return response;
}

export async function loginWithGoogle(token: string) {
  const response = await api.post<AuthResponse>("/api/v1/memex/auth/google", { token });
  setTokens(response.accessToken, response.refreshToken);
  return response;
}

export async function refreshTokens(refreshToken: string) {
  const response = await api.post<{ accessToken: string; refreshToken: string }>(
    "/api/v1/memex/auth/refresh",
    { refreshToken },
  );
  setTokens(response.accessToken, response.refreshToken);
  return response;
}

export async function logout() {
  try {
    await api.post("/api/v1/memex/auth/logout");
  } finally {
    clearTokens();
  }
}

export async function getCurrentUser() {
  return api.get<AuthResponse["user"]>("/api/v1/memex/auth/me");
}

export async function verifyEmail(token: string) {
  return api.post<{ status: string; message: string }>("/api/v1/memex/auth/verify-email", {
    token,
  });
}

export async function requestPasswordReset(email: string) {
  return api.post<{ status: string; message: string }>("/api/v1/memex/auth/request-reset", {
    email,
  });
}

export async function resetPassword(token: string, password: string) {
  return api.post<{ status: string; message: string }>("/api/v1/memex/auth/reset-password", {
    token,
    password,
  });
}

export async function createWorkspace(data: {
  name: string;
  role: string;
  company?: string;
  primaryGoal: string;
}) {
  return api.post<{
    id: string;
    name: string;
    slug: string;
    owner_id: string;
    created_at: string;
  }>("/api/v1/memex/workspaces", data);
}

export async function markOnboarded() {
  return api.post<{ status: string }>("/api/v1/memex/profile/onboarded");
}

export async function getProfile() {
  return api.get<{
    id: string;
    email: string;
    display_name: string;
    avatar_url?: string;
    role: string;
    email_verified: boolean;
    is_onboarded: boolean;
    created_at: string;
    updated_at: string;
  }>("/api/v1/memex/profile");
}

export async function updateProfile(data: {
  display_name?: string;
  avatar_url?: string;
}) {
  return api.patch<{
    id: string;
    email: string;
    display_name: string;
    avatar_url?: string;
    role: string;
    email_verified: boolean;
    is_onboarded: boolean;
  }>("/api/v1/memex/profile", data);
}
