"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { getProfile, updateProfile } from "@/lib/auth";

export default function ProfilePage() {
  const [profile, setProfile] = useState<{
    display_name: string;
    email: string;
    avatar_url?: string;
    role: string;
    email_verified: boolean;
    created_at: string;
  } | null>(null);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    getProfile()
      .then((p) => {
        setProfile(p);
        setName(p.display_name);
      })
      .finally(() => setLoading(false));
  }, []);

  async function handleSave() {
    setSaving(true);
    try {
      await updateProfile({ display_name: name });
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-6 w-6 animate-spin rounded-full border-2 border-white/10 border-t-white/30" />
      </div>
    );
  }

  return (
    <motion.div
      className="mx-auto max-w-2xl space-y-8 p-6 pt-12"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div>
        <h1 className="text-2xl font-bold text-white">Profile</h1>
        <p className="mt-1 text-sm text-white/30">Manage your account settings</p>
      </div>

      <div className="space-y-6 rounded-xl border border-white/5 bg-white/[0.02] p-6 backdrop-blur-xl">
        <div className="flex items-center gap-4">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-amber-400 to-amber-600 text-lg font-bold text-black">
            {profile?.display_name?.charAt(0)?.toUpperCase() ?? "?"}
          </div>
          <div>
            <p className="font-medium text-white">{profile?.display_name}</p>
            <p className="text-sm text-white/40">{profile?.email}</p>
            <p className="text-xs text-white/20">
              {profile?.email_verified ? "Verified" : "Not verified"}
              {profile?.role !== "user" && ` · ${profile?.role}`}
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-4 rounded-xl border border-white/5 bg-white/[0.02] p-6 backdrop-blur-xl">
        <label className="block">
          <span className="text-sm text-white/60">Display name</span>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="mt-1.5 h-11 w-full rounded-lg border border-white/10 bg-white/5 px-4 text-sm text-white transition-all focus:border-amber-500/50 focus:outline-none focus:ring-1 focus:ring-amber-500/20"
          />
        </label>

        <button
          onClick={handleSave}
          disabled={saving || name === profile?.display_name}
          className="h-10 rounded-lg bg-amber-500 px-5 text-sm font-medium text-black transition-all hover:bg-amber-400 disabled:opacity-50"
        >
          {saving ? "Saving..." : saved ? "Saved" : "Save changes"}
        </button>
      </div>
    </motion.div>
  );
}
