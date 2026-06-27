"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload, FileText, ChevronDown, ChevronRight,
  CheckCircle2, XCircle, Loader2, Globe, Github,
  Table, Braces, File,
} from "lucide-react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const SOURCE_ICONS: Record<string, React.ReactNode> = {
  markdown: <FileText size={14} />,
  plain_text: <FileText size={14} />,
  csv: <Table size={14} />,
  json: <Braces size={14} />,
  url: <Globe size={14} />,
  github: <Github size={14} />,
  pdf: <File size={14} />,
};

const SOURCE_LABELS: Record<string, string> = {
  markdown: "Markdown",
  plain_text: "Plain Text",
  csv: "CSV",
  json: "JSON",
  url: "URL",
  github: "GitHub",
  pdf: "PDF",
  meeting_note: "Meeting Note",
};

interface ImportProgressProps {
  jobId: string;
  onComplete: () => void;
}

function ImportProgress({ jobId, onComplete }: ImportProgressProps) {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("queued");
  const [step, setStep] = useState("");

  useEffect(() => {
    const es = new EventSource(`${API_BASE}/api/v1/memex/imports/${jobId}/stream`);
    es.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.event === "progress") {
          setProgress(msg.data.progress_pct);
          setStatus(msg.data.status);
          setStep(msg.data.current_step || "");
        } else if (msg.event === "completed") {
          setProgress(100);
          setStatus("completed");
          es.close();
          setTimeout(onComplete, 1500);
        } else if (msg.event === "failed") {
          setStatus("failed");
          es.close();
        }
      } catch {}
    };
    es.onerror = () => { es.close(); };
    return () => es.close();
  }, [jobId, onComplete]);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-xs">
        <span className="text-white/60">{step || status}</span>
        <span className={`${status === "failed" ? "text-red-400" : "text-white/40"}`}>
          {status === "completed" ? "100%" : `${progress}%`}
        </span>
      </div>
      <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
          className={`h-full rounded-full ${
            status === "failed" ? "bg-red-500"
            : status === "completed" ? "bg-emerald-500"
            : "bg-purple-500"
          }`}
        />
      </div>
      <div className="flex items-center gap-2 text-xs">
        {status === "running" && <Loader2 size={12} className="animate-spin text-purple-400" />}
        {status === "completed" && <CheckCircle2 size={12} className="text-emerald-400" />}
        {status === "failed" && <XCircle size={12} className="text-red-400" />}
        <span className={
          status === "failed" ? "text-red-400"
          : status === "completed" ? "text-emerald-400"
          : "text-white/40"
        }>
          {status === "completed" ? "Import complete"
           : status === "failed" ? "Import failed"
           : status === "queued" ? "Waiting..."
           : "Processing..."}
        </span>
      </div>
    </div>
  );
}

function detectSourceType(file: File): string {
  const name = file.name.toLowerCase();
  if (name.endsWith(".md") || name.endsWith(".markdown")) return "markdown";
  if (name.endsWith(".txt")) return "plain_text";
  if (name.endsWith(".csv")) return "csv";
  if (name.endsWith(".json")) return "json";
  if (name.endsWith(".pdf")) return "pdf";
  return "plain_text";
}

export function ImportPanel({ projectId }: { projectId: string }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [importing, setImporting] = useState(false);
  const [jobs, setJobs] = useState<ImportJob[]>([]);
  const [importsOpen, setImportsOpen] = useState(false);
  const [urlInput, setUrlInput] = useState("");
  const [showUrlInput, setShowUrlInput] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const refreshJobs = useCallback(async () => {
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/memex/imports?project_id=${projectId}&limit=10`,
        { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } },
      );
      if (res.ok) {
        const data = await res.json();
        setJobs(data.jobs || []);
      }
    } catch {}
  }, [projectId]);

  useEffect(() => {
    if (projectId) refreshJobs();
  }, [projectId, refreshJobs]);

  const startImport = useCallback(async (sourceType: string, body: Record<string, unknown>) => {
    setImporting(true);
    try {
      const accessToken = localStorage.getItem("access_token");
      const res = await fetch(`${API_BASE}/api/v1/memex/imports`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        },
        body: JSON.stringify({ ...body, project_id: projectId, source_type: sourceType }),
      });
      if (res.ok) {
        const data = await res.json();
        setJobs((prev) => [{
          id: data.job_id,
          project_id: projectId,
          source_type: sourceType,
          status: "queued",
          progress_pct: 0,
          total_items: 0,
          processed_items: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }, ...prev]);
      }
    } catch {}
    setImporting(false);
  }, [projectId]);

  const uploadFile = useCallback(async (file: File) => {
    setImporting(true);
    try {
      const accessToken = localStorage.getItem("access_token");
      const formData = new FormData();
      formData.append("file", file);
      formData.append("project_id", projectId);
      formData.append("source_type", detectSourceType(file));
      const res = await fetch(`${API_BASE}/api/v1/memex/imports/upload`, {
        method: "POST",
        ...(accessToken ? { headers: { Authorization: `Bearer ${accessToken}` } } : {}),
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        setJobs((prev) => [{
          id: data.job_id,
          project_id: projectId,
          source_type: detectSourceType(file),
          status: "queued",
          progress_pct: 0,
          total_items: 0,
          processed_items: 0,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }, ...prev]);
      }
    } catch {}
    setImporting(false);
  }, [projectId]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = Array.from(e.dataTransfer.files);
    for (const file of files) uploadFile(file);
  }, [uploadFile]);

  const handleUrlSubmit = useCallback(() => {
    if (!urlInput.trim()) return;
    const isGithub = urlInput.includes("github.com");
    startImport(isGithub ? "github" : "url", {
      url: urlInput,
      display_name: urlInput,
    });
    setUrlInput("");
    setShowUrlInput(false);
  }, [urlInput, startImport]);

  const activeJob = jobs.find((j) => j.status === "running" || j.status === "queued");

  return (
    <div className="space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
          isDragOver
            ? "border-purple-500 bg-purple-500/10 scale-[1.02]"
            : "border-white/10 hover:border-white/20 bg-white/[0.02]"
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          className="hidden"
          onChange={(e) => {
            const files = Array.from(e.target.files || []);
            for (const file of files) uploadFile(file);
          }}
        />
        <motion.div
          animate={isDragOver ? { scale: 1.1, y: -5 } : { scale: 1, y: 0 }}
          className="flex flex-col items-center gap-3"
        >
          <div className={`p-3 rounded-full ${isDragOver ? "bg-purple-500/20" : "bg-white/5"}`}>
            <Upload size={24} className={isDragOver ? "text-purple-400" : "text-white/30"} />
          </div>
          <div>
            <p className="text-sm text-white/60">
              {isDragOver ? "Drop to import" : "Drop files here or click to browse"}
            </p>
            <p className="text-xs text-white/30 mt-1">
              Markdown, PDF, CSV, JSON, Plain Text
            </p>
          </div>
        </motion.div>
        {importing && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4"
          >
            <div className="flex items-center gap-2 text-xs text-purple-400 justify-center">
              <Loader2 size={14} className="animate-spin" />
              Uploading...
            </div>
          </motion.div>
        )}
      </div>

      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setShowUrlInput(!showUrlInput)}
          className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/60 hover:text-white/80 hover:bg-white/10 transition-colors"
        >
          <Globe size={14} />
          Import from URL
        </button>
        <button
          onClick={() => startImport("markdown", { data: "# New Memory\n\nContent here...", display_name: "Quick Note" })}
          className="flex items-center gap-2 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/60 hover:text-white/80 hover:bg-white/10 transition-colors"
        >
          <FileText size={14} />
          Quick Note
        </button>
      </div>

      <AnimatePresence>
        {showUrlInput && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="flex gap-2"
          >
            <input
              type="text"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleUrlSubmit()}
              placeholder="https://github.com/user/repo or any URL..."
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50 placeholder-white/20"
            />
            <button
              onClick={handleUrlSubmit}
              disabled={!urlInput.trim() || importing}
              className="px-3 py-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-xs text-purple-400 hover:bg-purple-500/30 disabled:opacity-30 transition-colors"
            >
              Import
            </button>
          </motion.div>
        )}
      </AnimatePresence>

      {activeJob && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 bg-white/5 border border-white/10 rounded-xl"
        >
          <div className="flex items-center gap-2 mb-2">
            {SOURCE_ICONS[activeJob.source_type] || <FileText size={14} />}
            <span className="text-xs text-white/60">
              {SOURCE_LABELS[activeJob.source_type] || activeJob.source_type}
            </span>
          </div>
          <ImportProgress
            jobId={activeJob.id}
            onComplete={refreshJobs}
          />
        </motion.div>
      )}

      {jobs.length > 0 && (
        <div>
          <button
            onClick={() => setImportsOpen(!importsOpen)}
            className="flex items-center gap-2 text-xs text-white/40 hover:text-white/60 transition-colors"
          >
            {importsOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
            Recent imports ({jobs.length})
          </button>
          <AnimatePresence>
            {importsOpen && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-2 space-y-1"
              >
                {jobs.map((job) => (
                  <div
                    key={job.id}
                    className="flex items-center gap-3 px-3 py-2 rounded-lg bg-white/[0.02] hover:bg-white/5 transition-colors"
                  >
                    {SOURCE_ICONS[job.source_type] || <FileText size={12} />}
                    <span className="text-xs text-white/60 flex-1">
                      {SOURCE_LABELS[job.source_type] || job.source_type}
                      {job.processed_items > 0 && ` (${job.processed_items})`}
                    </span>
                    <span className={`text-xs ${
                      job.status === "completed" ? "text-emerald-400"
                      : job.status === "failed" ? "text-red-400"
                      : job.status === "running" ? "text-purple-400"
                      : "text-white/30"
                    }`}>
                      {job.progress_pct}%
                    </span>
                    {job.status === "completed" && <CheckCircle2 size={12} className="text-emerald-400" />}
                    {job.status === "failed" && <XCircle size={12} className="text-red-400" />}
                    {job.status === "running" && <Loader2 size={12} className="animate-spin text-purple-400" />}
                  </div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}

interface ImportJob {
  id: string;
  project_id: string;
  source_type: string;
  status: string;
  progress_pct: number;
  total_items: number;
  processed_items: number;
  created_at: string;
  updated_at: string;
}
