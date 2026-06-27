"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { loginWithEmail, loginWithGoogle } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await loginWithEmail({ email, password });
      router.push("/onboarding");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Invalid email or password");
    } finally {
      setLoading(false);
    }
  }

  async function handleGoogleLogin() {
    setError("");
    setLoading(true);
    try {
      const token = "mock-google-token";
      await loginWithGoogle(token);
      router.push("/onboarding");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Google login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-black px-6">
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute left-1/2 top-1/3 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-amber-500/10 blur-[120px]" />
        <div className="absolute right-1/4 top-2/3 h-48 w-48 rounded-full bg-cyan-500/10 blur-[100px]" />
      </div>

      <motion.div
        className="relative z-10 flex flex-col items-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <motion.div
          className="mb-8 h-16 w-16 rounded-full"
          animate={{
            boxShadow: [
              "0 0 20px rgba(245,158,11,0.3), 0 0 40px rgba(245,158,11,0.1)",
              "0 0 40px rgba(245,158,11,0.5), 0 0 80px rgba(245,158,11,0.2)",
              "0 0 20px rgba(245,158,11,0.3), 0 0 40px rgba(245,158,11,0.1)",
            ],
          }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
        >
          <div className="h-full w-full rounded-full bg-gradient-to-br from-amber-400 to-amber-600" />
        </motion.div>

        <motion.h1
          className="mb-2 text-center text-3xl font-bold tracking-tight text-white md:text-4xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          Every intelligence begins
          <br />
          with a memory.
        </motion.h1>

        <motion.p
          className="mb-10 text-sm text-white/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          Enter your artificial memory
        </motion.p>

        <AnimatePresence mode="wait">
          {!showForm ? (
            <motion.div
              key="choices"
              className="flex w-full max-w-xs flex-col gap-3"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              <button
                onClick={handleGoogleLogin}
                disabled={loading}
                className="group relative flex h-12 w-full items-center justify-center gap-3 overflow-hidden rounded-lg border border-white/10 bg-white/5 text-sm text-white backdrop-blur-xl transition-all duration-300 hover:border-white/20 hover:bg-white/10 disabled:opacity-50"
              >
                <svg className="h-5 w-5" viewBox="0 0 24 24">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
                </svg>
                Continue with Google
              </button>

              <button
                onClick={() => setShowForm(true)}
                className="group relative flex h-12 w-full items-center justify-center gap-2 overflow-hidden rounded-lg border border-white/5 bg-white/[0.02] text-sm text-white/60 backdrop-blur-xl transition-all duration-300 hover:border-white/10 hover:text-white"
              >
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                </svg>
                Continue with Email
              </button>
            </motion.div>
          ) : (
            <motion.form
              key="form"
              onSubmit={handleEmailLogin}
              className="flex w-full max-w-xs flex-col gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4 }}
            >
              <div className="relative">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                  required
                  className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
                />
              </div>
              <div className="relative">
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Password"
                  required
                  className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
                />
              </div>

              <div className="flex items-center justify-between text-xs">
                <label className="flex items-center gap-2 text-white/30">
                  <input type="checkbox" className="rounded border-white/20 bg-white/5 accent-amber-500" />
                  Remember me
                </label>
                <Link href="/reset-password" className="text-amber-500/60 hover:text-amber-500">
                  Forgot?
                </Link>
              </div>

              {error && (
                <motion.p
                  className="text-xs text-red-400"
                  initial={{ opacity: 0, y: -4 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {error}
                </motion.p>
              )}

              <button
                type="submit"
                disabled={loading}
                className="relative flex h-12 w-full items-center justify-center overflow-hidden rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 text-sm font-medium text-black transition-all duration-300 hover:from-amber-400 hover:to-amber-500 active:scale-[0.98] disabled:opacity-50"
              >
                {loading ? (
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-black/30 border-t-black" />
                ) : (
                  "Sign In"
                )}
              </button>

              <p className="text-center text-xs text-white/20">
                No account?{" "}
                <Link href="/register" className="text-amber-500/60 hover:text-amber-500">
                  Create one
                </Link>
              </p>
            </motion.form>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}
