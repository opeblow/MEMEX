"use client";

import { registerWithEmail } from "@/lib/auth";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await registerWithEmail({ email, password, displayName: name });
      router.push("/onboarding");
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-black px-6">
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute left-1/3 top-1/4 h-64 w-64 -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-500/10 blur-[120px]" />
        <div className="absolute right-1/3 bottom-1/4 h-48 w-48 rounded-full bg-amber-500/10 blur-[100px]" />
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
              "0 0 20px rgba(34,211,238,0.3), 0 0 40px rgba(34,211,238,0.1)",
              "0 0 40px rgba(34,211,238,0.5), 0 0 80px rgba(34,211,238,0.2)",
              "0 0 20px rgba(34,211,238,0.3), 0 0 40px rgba(34,211,238,0.1)",
            ],
          }}
          transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY, ease: "easeInOut" }}
        >
          <div className="h-full w-full rounded-full bg-gradient-to-br from-cyan-400 to-cyan-600" />
        </motion.div>

        <motion.h1
          className="mb-2 text-center text-3xl font-bold tracking-tight text-white md:text-4xl"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        >
          Initialize your
          <br />
          memory core.
        </motion.h1>

        <motion.p
          className="mb-10 text-sm text-white/30"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.6 }}
        >
          Create your artificial memory
        </motion.p>

        <motion.form
          onSubmit={handleRegister}
          className="flex w-full max-w-xs flex-col gap-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.6 }}
        >
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Display name"
            required
            className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
          />
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
            className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
            minLength={8}
            className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
          />

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
            className="relative flex h-12 w-full items-center justify-center overflow-hidden rounded-lg bg-gradient-to-r from-cyan-500 to-cyan-600 text-sm font-medium text-black transition-all duration-300 hover:from-cyan-400 hover:to-cyan-500 active:scale-[0.98] disabled:opacity-50"
          >
            {loading ? (
              <div className="h-5 w-5 animate-spin rounded-full border-2 border-black/30 border-t-black" />
            ) : (
              "Create Account"
            )}
          </button>

          <p className="text-center text-xs text-white/20">
            Already have an account?{" "}
            <Link href="/login" className="text-cyan-500/60 hover:text-cyan-500">
              Sign in
            </Link>
          </p>
        </motion.form>
      </motion.div>
    </div>
  );
}
