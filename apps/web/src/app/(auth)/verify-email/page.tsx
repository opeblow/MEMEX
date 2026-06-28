"use client";

import { verifyEmail } from "@/lib/auth";
import { motion } from "framer-motion";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<"verifying" | "success" | "error">("verifying");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("No verification token provided");
      return;
    }
    verifyEmail(token)
      .then((res) => {
        setStatus("success");
        setMessage(res.message);
      })
      .catch((err) => {
        setStatus("error");
        setMessage(err instanceof Error ? err.message : "Verification failed");
      });
  }, [token]);

  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-black px-6">
      <motion.div
        className="relative z-10 flex flex-col items-center text-center"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div
          className={`mb-6 h-16 w-16 rounded-full ${
            status === "verifying"
              ? "bg-amber-500/20"
              : status === "success"
                ? "bg-green-500/20"
                : "bg-red-500/20"
          }`}
        >
          <div
            className={`flex h-full w-full items-center justify-center text-2xl ${
              status === "verifying"
                ? "animate-pulse text-amber-400"
                : status === "success"
                  ? "text-green-400"
                  : "text-red-400"
            }`}
          >
            {status === "verifying" ? "..." : status === "success" ? "✓" : "!"}
          </div>
        </div>
        <h1 className="mb-2 text-xl font-bold text-white">
          {status === "verifying"
            ? "Verifying..."
            : status === "success"
              ? "Email Verified"
              : "Verification Failed"}
        </h1>
        <p className="mb-8 max-w-xs text-sm text-white/40">{message}</p>
        {status !== "verifying" && (
          <Link
            href="/login"
            className="rounded-lg bg-white/10 px-6 py-3 text-sm text-white transition-all hover:bg-white/20"
          >
            {status === "success" ? "Sign In" : "Back to Login"}
          </Link>
        )}
      </motion.div>
    </div>
  );
}
