"use client";

import { api } from "@/lib/api/client";
import type { Project } from "@memex/types";
import { Skeleton } from "@memex/ui";
import { AnimatePresence, motion } from "framer-motion";
import { FolderKanban, Plus } from "lucide-react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

const container = {
  animate: {
    transition: { staggerChildren: 0.08 },
  },
};

const item = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.4, ease: "easeOut" } },
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [newName, setNewName] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api
      .get<Project[]>("/api/v1/memex/projects")
      .then((data) => setProjects(Array.isArray(data) ? data : []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (showCreate && inputRef.current) {
      inputRef.current.focus();
    }
  }, [showCreate]);

  const handleCreate = async () => {
    if (!newName.trim() || creating) return;
    setCreating(true);
    try {
      const created = await api.post<Project>("/api/v1/memex/projects", {
        name: newName.trim(),
      });
      setProjects((prev) => [...prev, created]);
      setNewName("");
      setShowCreate(false);
    } catch {}
    setCreating(false);
  };

  if (loading) {
    return (
      <motion.div
        variants={container}
        initial="initial"
        animate="animate"
        className="flex flex-col gap-6 p-6"
      >
        <div className="flex items-center justify-between">
          <motion.div variants={item}>
            <Skeleton className="h-8 w-40" />
          </motion.div>
          <motion.div variants={item}>
            <Skeleton className="h-9 w-32 rounded-lg" />
          </motion.div>
        </div>
        <motion.div
          variants={item}
          className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3"
        >
          {Array.from({ length: 3 }).map((_, i) => (
            // biome-ignore lint/suspicious/noArrayIndexKey: static skeleton list
            <Skeleton key={i} className="h-48 rounded-xl" />
          ))}
        </motion.div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-4xl mx-auto space-y-6 p-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-white/80">Projects</h1>
          <p className="text-xs text-white/30 mt-1">Organize your memories into projects</p>
        </div>
        <button
          type="button"
          onClick={() => setShowCreate(!showCreate)}
          className="flex items-center gap-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 transition-colors"
        >
          <Plus size={14} />
          New Project
        </button>
      </div>

      <AnimatePresence>
        {showCreate && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="flex gap-2"
          >
            <input
              ref={inputRef}
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleCreate()}
              placeholder="Project name"
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-amber-500/50 placeholder-white/20"
            />
            <button
              type="button"
              onClick={handleCreate}
              disabled={!newName.trim() || creating}
              className="px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 disabled:opacity-30 transition-colors"
            >
              {creating ? "Creating..." : "Create"}
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {projects.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <FolderKanban size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No projects yet</p>
          <p className="text-xs text-white/30 max-w-sm">
            Create your first project to organize related memories.
          </p>
          <button
            type="button"
            onClick={() => setShowCreate(true)}
            className="mt-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-400 hover:bg-amber-500/20 transition-colors"
          >
            Create Project
          </button>
        </div>
      )}

      <motion.div
        variants={container}
        initial="initial"
        animate="animate"
        className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3"
      >
        {projects.map((project) => (
          <motion.div key={project.id} variants={item}>
            <Link
              href={"/recall"}
              className="block p-4 bg-white/[0.02] border border-white/10 rounded-xl hover:bg-white/5 hover:border-white/20 transition-all h-full"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 rounded-lg bg-amber-500/10">
                  <FolderKanban size={16} className="text-amber-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-medium text-white/80 truncate">{project.name}</h3>
                  <p className="text-[10px] text-white/30">{project.slug}</p>
                </div>
              </div>
              {project.description && (
                <p className="text-xs text-white/30 line-clamp-2 mb-2">{project.description}</p>
              )}
              <p className="text-[10px] text-white/20">
                Created{" "}
                {new Date(
                  (project as { created_at?: string }).created_at ?? project.createdAt,
                ).toLocaleDateString()}
              </p>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </motion.div>
  );
}
