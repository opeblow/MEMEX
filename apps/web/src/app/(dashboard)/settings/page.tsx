"use client";

import { api } from "@/lib/api/client";
import { Skeleton } from "@memex/ui";
import { motion } from "framer-motion";
import { Mail, Moon, User } from "lucide-react";
import { useEffect, useState } from "react";

const container = {
  animate: {
    transition: { staggerChildren: 0.06 },
  },
};

const item = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

interface Profile {
  display_name: string;
  email: string;
  avatar_url?: string;
  role: string;
  email_verified: boolean;
}

export default function SettingsPage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api
      .get<Profile>("/api/v1/memex/profile")
      .then((p) => {
        setProfile(p);
        setDisplayName(p.display_name);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    if (!displayName.trim() || saving) return;
    setSaving(true);
    try {
      const updated = await api.patch<Profile>("/api/v1/memex/profile", {
        display_name: displayName.trim(),
      });
      setProfile(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch {}
    setSaving(false);
  };

  if (loading) {
    return (
      <motion.div
        variants={container}
        initial="initial"
        animate="animate"
        className="flex flex-col gap-8 p-6 max-w-2xl mx-auto"
      >
        <motion.div variants={item}>
          <Skeleton className="h-8 w-44" />
        </motion.div>
        <motion.div variants={item} className="space-y-6">
          <div className="space-y-3">
            <Skeleton className="h-5 w-32" />
            <Skeleton className="h-10 w-full rounded-lg" />
            <Skeleton className="h-4 w-64" />
          </div>
          <div className="space-y-3">
            <Skeleton className="h-5 w-28" />
            <Skeleton className="h-10 w-full rounded-lg" />
            <Skeleton className="h-4 w-48" />
          </div>
          <div className="space-y-3">
            <Skeleton className="h-5 w-36" />
            <div className="flex items-center gap-4">
              <Skeleton className="h-6 w-12 rounded-full" />
              <Skeleton className="h-4 w-56" />
            </div>
          </div>
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-2xl mx-auto space-y-8 p-6"
    >
      <div>
        <h1 className="text-lg font-semibold text-white/80">Settings</h1>
        <p className="text-xs text-white/30 mt-1">Manage your account and preferences</p>
      </div>

      <div className="space-y-6">
        <div className="bg-white/[0.02] border border-white/10 rounded-xl p-4 space-y-4">
          <div className="flex items-center gap-2">
            <User size={14} className="text-amber-400" />
            <h2 className="text-sm font-medium text-white/70">Profile</h2>
          </div>

          <label className="block">
            <span className="text-xs text-white/40">Display name</span>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="mt-1.5 w-full h-10 bg-white/5 border border-white/10 rounded-lg px-3 text-sm text-white/80 focus:outline-none focus:border-amber-500/50 placeholder-white/20"
              placeholder="Your name"
            />
          </label>

          <button
            type="button"
            onClick={handleSave}
            disabled={saving || !displayName.trim() || displayName === profile?.display_name}
            className="h-9 px-4 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 disabled:opacity-50 transition-colors"
          >
            {saving ? "Saving..." : saved ? "Saved" : "Save changes"}
          </button>
        </div>

        <div className="bg-white/[0.02] border border-white/10 rounded-xl p-4 space-y-4">
          <div className="flex items-center gap-2">
            <Mail size={14} className="text-cyan-400" />
            <h2 className="text-sm font-medium text-white/70">Account</h2>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 text-sm font-bold text-black">
              {profile?.display_name?.charAt(0)?.toUpperCase() ?? "?"}
            </div>
            <div>
              <p className="text-sm text-white/80">{profile?.display_name}</p>
              <p className="text-xs text-white/40">{profile?.email}</p>
              <p className="text-[10px] text-white/20">
                {profile?.email_verified ? "Email verified" : "Not verified"}
                {profile?.role !== "user" && ` · ${profile?.role}`}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white/[0.02] border border-white/10 rounded-xl p-4 space-y-4">
          <div className="flex items-center gap-2">
            <Moon size={14} className="text-amber-400" />
            <h2 className="text-sm font-medium text-white/70">Appearance</h2>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Moon size={14} className="text-amber-400" />
              <span className="text-xs text-white/50">Dark mode</span>
            </div>
            <div className="h-6 w-11 rounded-full bg-amber-500/30 relative cursor-not-allowed">
              <div className="absolute top-0.5 left-0.5 h-5 w-5 rounded-full bg-amber-400 shadow" />
            </div>
          </div>
          <p className="text-[10px] text-white/20">
            Dark mode is the only available theme for MEMEX
          </p>
        </div>
      </div>
    </motion.div>
  );
}
