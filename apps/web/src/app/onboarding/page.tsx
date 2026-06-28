"use client";

import { createWorkspace, markOnboarded } from "@/lib/auth";
import { AnimatePresence, motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

type Phase = "awakening" | "workspace" | "complete";

const GOALS = ["Build products", "Research", "Engineering", "AI Agents", "Knowledge Base", "Other"];

export default function OnboardingPage() {
  const router = useRouter();
  const [phase, setPhase] = useState<Phase>("awakening");
  const [awakeningStep, setAwakeningStep] = useState(0);
  const [name, setName] = useState("");
  const [role, setRole] = useState("individual");
  const [company, setCompany] = useState("");
  const [primaryGoal, setPrimaryGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (phase !== "awakening") return;
    const timers = [
      setTimeout(() => setAwakeningStep(0), 0),
      setTimeout(() => setAwakeningStep(1), 800),
      setTimeout(() => setAwakeningStep(2), 1600),
      setTimeout(() => setAwakeningStep(3), 2600),
      setTimeout(() => setAwakeningStep(4), 3600),
      setTimeout(() => setPhase("workspace"), 4400),
    ];
    return () => timers.forEach(clearTimeout);
  }, [phase]);

  const handleCreate = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setError("");
      setLoading(true);
      try {
        await createWorkspace({
          name,
          role,
          company: company || undefined,
          primaryGoal: primaryGoal || "research",
        });
        await markOnboarded();
        setPhase("complete");
        setTimeout(() => router.push("/recall"), 1200);
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : "Failed to create workspace");
      } finally {
        setLoading(false);
      }
    },
    [name, role, company, primaryGoal, router],
  );

  return (
    <div className="relative flex min-h-dvh items-center justify-center overflow-hidden bg-black px-6">
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute left-1/2 top-1/3 h-96 w-96 -translate-x-1/2 -translate-y-1/2 rounded-full bg-amber-500/5 blur-[150px]" />
      </div>

      <AnimatePresence mode="wait">
        {phase === "awakening" && (
          <motion.div
            key="awakening"
            className="relative z-10 flex flex-col items-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <svg width="160" height="160" viewBox="0 0 160 160" className="mb-8 overflow-visible">
              <title>Neural network animation</title>
              <defs>
                <radialGradient id="awake-glow">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.6" />
                  <stop offset="100%" stopColor="#f59e0b" stopOpacity="0" />
                </radialGradient>
              </defs>

              <circle cx="80" cy="80" r="20" fill="url(#awake-glow)">
                {awakeningStep >= 0 && (
                  <animate attributeName="r" values="10;25;10" dur="2s" repeatCount="indefinite" />
                )}
              </circle>

              {awakeningStep >= 1 && (
                <>
                  <motion.line
                    x1="80"
                    y1="80"
                    x2="80"
                    y2="25"
                    stroke="#f59e0b"
                    strokeWidth="1.5"
                    strokeOpacity="0.5"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6 }}
                  />
                  <motion.line
                    x1="80"
                    y1="80"
                    x2="135"
                    y2="60"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    strokeOpacity="0.4"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                  />
                  <motion.line
                    x1="80"
                    y1="80"
                    x2="25"
                    y2="100"
                    stroke="#f59e0b"
                    strokeWidth="1.5"
                    strokeOpacity="0.4"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                  />
                  <motion.line
                    x1="80"
                    y1="80"
                    x2="120"
                    y2="130"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    strokeOpacity="0.5"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6, delay: 0.15 }}
                  />
                  <motion.line
                    x1="80"
                    y1="80"
                    x2="40"
                    y2="35"
                    stroke="#22d3ee"
                    strokeWidth="1.5"
                    strokeOpacity="0.3"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.6, delay: 0.25 }}
                  />
                </>
              )}

              {awakeningStep >= 2 && (
                <>
                  <motion.line
                    x1="25"
                    y1="100"
                    x2="120"
                    y2="130"
                    stroke="#f59e0b"
                    strokeWidth="0.8"
                    strokeOpacity="0.2"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.5, delay: 0.1 }}
                  />
                  <motion.line
                    x1="135"
                    y1="60"
                    x2="40"
                    y2="35"
                    stroke="#22d3ee"
                    strokeWidth="0.8"
                    strokeOpacity="0.2"
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ duration: 0.5, delay: 0.2 }}
                  />
                </>
              )}

              {awakeningStep >= 3 &&
                [0, 1, 2, 3, 4, 5].map((i) => (
                  <circle key={i} r="2" fill="#f59e0b" opacity="0.6">
                    <animateMotion
                      dur="2s"
                      repeatCount="indefinite"
                      path={`M${80} ${80} L${[80, 135, 25, 120, 40][i] || 80} ${[25, 60, 100, 130, 35][i] || 80}`}
                    />
                  </circle>
                ))}
            </svg>

            <motion.p
              className="text-sm font-medium tracking-wider text-amber-500/60"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              {awakeningStep < 3 ? "Initializing neural network..." : "Initializing Memory Core..."}
            </motion.p>
          </motion.div>
        )}

        {phase === "workspace" && (
          <motion.div
            key="workspace"
            className="relative z-10 flex w-full max-w-sm flex-col items-center"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          >
            <motion.h2
              className="mb-2 text-center text-2xl font-bold tracking-tight text-white"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              Name your memory space
            </motion.h2>
            <motion.p
              className="mb-8 text-sm text-white/30"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
            >
              Your workspace is where memories live
            </motion.p>

            <motion.form
              onSubmit={handleCreate}
              className="flex w-full flex-col gap-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Workspace name"
                required
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
              />

              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white transition-all duration-200 focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
              >
                <option value="individual" className="bg-black">
                  Individual
                </option>
                <option value="team" className="bg-black">
                  Team
                </option>
                <option value="organization" className="bg-black">
                  Organization
                </option>
              </select>

              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Company (optional)"
                className="h-12 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white placeholder-white/20 backdrop-blur-xl transition-all duration-200 focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
              />

              <div className="flex flex-col gap-2">
                <p className="text-xs text-white/30">Primary goal</p>
                <div className="grid grid-cols-2 gap-2">
                  {GOALS.map((goal) => (
                    <button
                      key={goal}
                      type="button"
                      onClick={() => setPrimaryGoal(goal)}
                      className={`rounded-lg border px-3 py-2 text-xs transition-all duration-200 ${
                        primaryGoal === goal
                          ? "border-amber-500/50 bg-amber-500/10 text-amber-300"
                          : "border-white/10 bg-white/5 text-white/40 hover:border-white/20"
                      }`}
                    >
                      {goal}
                    </button>
                  ))}
                </div>
              </div>

              {error && (
                <motion.p
                  className="text-xs text-red-400"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  {error}
                </motion.p>
              )}

              <button
                type="submit"
                disabled={loading || !name}
                className="relative flex h-12 w-full items-center justify-center overflow-hidden rounded-lg bg-gradient-to-r from-amber-500 to-amber-600 text-sm font-medium text-black transition-all duration-300 hover:from-amber-400 hover:to-amber-500 active:scale-[0.98] disabled:opacity-50"
              >
                {loading ? (
                  <div className="h-5 w-5 animate-spin rounded-full border-2 border-black/30 border-t-black" />
                ) : (
                  "Initialize Memory Core"
                )}
              </button>
            </motion.form>
          </motion.div>
        )}

        {phase === "complete" && (
          <motion.div
            key="complete"
            className="relative z-10 flex flex-col items-center"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            <motion.div
              className="mb-6 h-24 w-24 rounded-full bg-gradient-to-br from-amber-400 to-amber-600"
              animate={{ scale: [1, 1.1, 1] }}
              transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY }}
            />
            <h2 className="text-2xl font-bold text-white">Memory Core Initialized</h2>
            <p className="mt-2 text-sm text-white/30">Entering your artificial brain...</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
