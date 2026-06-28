import type { User } from "@memex/types";
import { create } from "zustand";
import * as auth from "../auth";

interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  login: (token: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: true,
  isAuthenticated: false,

  setUser: (user) => set({ user, isAuthenticated: !!user, isLoading: false }),

  login: async (token: string) => {
    set({ isLoading: true });
    try {
      localStorage.setItem("memex_access_token", token);
      const user = await auth.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      localStorage.removeItem("memex_access_token");
      set({ user: null, isAuthenticated: false, isLoading: false });
      throw new Error("Login failed");
    }
  },

  logout: async () => {
    set({ isLoading: true });
    try {
      await auth.logout();
    } catch {
      // proceed with local logout
    }
    set({ user: null, isAuthenticated: false, isLoading: false });
  },

  checkAuth: async () => {
    set({ isLoading: true });
    const token = typeof window !== "undefined" ? localStorage.getItem("memex_access_token") : null;

    if (!token) {
      set({ user: null, isAuthenticated: false, isLoading: false });
      return;
    }

    try {
      const user = await auth.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      localStorage.removeItem("memex_access_token");
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
