"use client";

import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { resetPassword, requestPasswordReset } from "@/lib/auth";

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  async function handleRequestReset(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await requestPasswordReset(email);
      setSent(true);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(e: React.FormEvent) {
    e.preventDefault();
    if (!token) return;
    setError("");
    setLoading(true);
    try {
      await resetPassword(token, password);
      router.push("/login");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Reset failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-black px-6">
      <motion.div
        className="relative z-10 flex w-full max-w-xs flex-col items-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="mb-6 h-14 w-14 rounded-full bg-cyan-500/20">
          <div className="flex h-full w-full items-center justify-center text-cyan-400">
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
            </svg>
          </div>
        </div>

        {!token ? (
          <>
            <h1 className="mb-2 text-center text-xl font-bold text-white">
              Reset your password
            </h1>
            <p className="mb-8 text-center text-sm text-white/30">
              Enter your email and we'll send you a reset link
            </p>
            {sent ? (
              <p className="text-sm text-green-400/80">
                Check your email for the reset link
              </p>
            ) : (
              <form onSubmit={handleRequestReset} className="flex w-full flex-col gap-4">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email"
                  required
                  className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
                />
                {error && <p className="text-xs text-red-400">{error}</p>}
                <button
                  type="submit"
                  disabled={loading}
                  className="flex h-12 w-full items-center justify-center rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-600 text-sm font-medium text-black transition-all hover:from-cyan-400 hover:to-cyan-500 disabled:opacity-50"
                >
                  {loading ? "Sending..." : "Send Reset Link"}
                </button>
              </form>
            )}
          </>
        ) : (
          <>
            <h1 className="mb-2 text-center text-xl font-bold text-white">
              New password
            </h1>
            <p className="mb-8 text-center text-sm text-white/30">
              Enter your new password
            </p>
            <form onSubmit={handleResetPassword} className="flex w-full flex-col gap-4">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="New password"
                required
                minLength={8}
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
              />
              {error && <p className="text-xs text-red-400">{error}</p>}
              <button
                type="submit"
                disabled={loading}
                className="flex h-12 w-full items-center justify-center rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-600 text-sm font-medium text-black transition-all hover:from-cyan-400 hover:to-cyan-500 disabled:opacity-50"
              >
                {loading ? "Resetting..." : "Reset Password"}
              </button>
            </form>
          </>
        )}

        <Link
          href="/login"
          className="mt-6 text-xs text-white/30 hover:text-white/60"
        >
          Back to login
        </Link>
      </motion.div>
    </div>
  );
}
