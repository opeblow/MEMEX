"use client";

import { Skeleton } from "@memex/ui";
import { motion } from "framer-motion";
import { ArrowRight, Brain, Network } from "lucide-react";
import Link from "next/link";
import { useEffect, useState } from "react";

interface GraphNode {
  id: string;
  label: string;
  type: string;
  importance: number;
}

interface GraphEdge {
  source: string;
  target: string;
  label: string;
  weight: number;
}

export default function GraphPage() {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const baseUrl =
      typeof window !== "undefined"
        ? (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000")
        : "http://localhost:8000";
    fetch(`${baseUrl}/api/v1/memex/graph/snapshot?project_id=default`)
      .then((res) => (res.ok ? res.json() : { nodes: [], edges: [] }))
      .then((data) => {
        const d = "data" in data ? data.data : data;
        setNodes(d.nodes ?? []);
        setEdges(d.edges ?? []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex flex-col gap-6 p-6"
      >
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-4 w-96" />
        <div className="mt-4 grid grid-cols-3 gap-4">
          <Skeleton className="h-64 rounded-xl" />
          <Skeleton className="h-64 rounded-xl" />
          <Skeleton className="h-64 rounded-xl" />
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-3xl mx-auto space-y-6 p-6"
    >
      <div>
        <h1 className="text-lg font-semibold text-white/80">Knowledge Graph</h1>
        <p className="text-xs text-white/30 mt-1">Entity relationships and graph overview</p>
      </div>

      <Link
        href="/recall"
        className="flex items-center gap-4 p-4 bg-gradient-to-br from-cyan-500/10 to-blue-500/5 border border-cyan-500/20 rounded-xl group hover:from-cyan-500/15 hover:to-blue-500/10 transition-all"
      >
        <div className="p-3 rounded-xl bg-cyan-500/10">
          <Brain size={24} className="text-cyan-400" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-medium text-white/80 group-hover:text-white transition-colors">
            3D Memory Universe
          </p>
          <p className="text-xs text-white/30 mt-0.5">
            Explore memories in the interactive 3D recall space
          </p>
        </div>
        <ArrowRight
          size={16}
          className="text-cyan-400/50 group-hover:text-cyan-400 transition-colors"
        />
      </Link>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
          <div className="flex items-center gap-2 mb-3">
            <Network size={14} className="text-amber-400" />
            <span className="text-xs font-medium text-white/60">Entities</span>
          </div>
          <p className="text-2xl font-bold text-white">{nodes.length}</p>
          <div className="mt-2 flex flex-wrap gap-1">
            {Array.from(new Set(nodes.map((n) => n.type))).map((type) => (
              <span key={type} className="px-2 py-0.5 rounded text-[10px] bg-white/5 text-white/40">
                {type}
              </span>
            ))}
          </div>
        </div>

        <div className="p-4 bg-white/[0.02] border border-white/10 rounded-xl">
          <div className="flex items-center gap-2 mb-3">
            <Network size={14} className="text-purple-400" />
            <span className="text-xs font-medium text-white/60">Relationships</span>
          </div>
          <p className="text-2xl font-bold text-white">{edges.length}</p>
          <div className="mt-2 flex flex-wrap gap-1">
            {Array.from(new Set(edges.map((e) => e.label)))
              .slice(0, 6)
              .map((label) => (
                <span
                  key={label}
                  className="px-2 py-0.5 rounded text-[10px] bg-white/5 text-white/40"
                >
                  {label}
                </span>
              ))}
          </div>
        </div>
      </div>

      {nodes.length > 0 && (
        <div className="space-y-2">
          <h2 className="text-xs font-semibold text-white/40">Top Entities</h2>
          <div className="space-y-1">
            {[...nodes]
              .sort((a, b) => b.importance - a.importance)
              .slice(0, 10)
              .map((node) => (
                <div
                  key={node.id}
                  className="flex items-center gap-3 px-3 py-2 rounded-lg bg-white/[0.02] hover:bg-white/5 transition-colors"
                >
                  <span className="text-xs text-white/60 flex-1 truncate">{node.label}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-white/40">
                    {node.type}
                  </span>
                  <span className="text-[10px] text-amber-400/60">
                    {node.importance.toFixed(1)}
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}

      {nodes.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/5">
            <Network size={20} className="text-white/30" />
          </div>
          <p className="text-sm text-white/50">No entities yet</p>
          <p className="text-xs text-white/30 max-w-sm">
            Entities appear as you add memories through the import or recall features.
          </p>
          <Link
            href="/ingest"
            className="mt-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/60 hover:text-white/80 transition-colors"
          >
            Import data
          </Link>
        </div>
      )}
    </motion.div>
  );
}
