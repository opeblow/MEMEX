"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, ChevronDown, ChevronRight, Brain, Sparkles } from "lucide-react";
import type { Explanation, ChatMessage } from "@memex/types";
import { useStreamReason } from "@/hooks/use-reasoning";

interface AIChatProps {
  projectId: string;
}

function EvidenceChip({ label, score }: { label: string; score: number }) {
  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-white/5 border border-white/10 text-white/60">
      <Sparkles size={10} />
      {label}
      <span className="text-white/30">({(score * 100).toFixed(0)}%)</span>
    </span>
  );
}

function ReasoningPanel({ explanation }: { explanation: Explanation }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="mt-2 border border-white/10 rounded-lg overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 w-full px-3 py-2 text-xs text-white/50 hover:text-white/80 bg-white/5 hover:bg-white/10 transition-colors"
      >
        {expanded ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        <Brain size={12} />
        Reasoning
        {explanation.confidence && (
          <span className="ml-auto text-white/30">
            Confidence: {explanation.confidence.label}
          </span>
        )}
      </button>
      {expanded && (
        <div className="p-3 space-y-2 text-xs text-white/60">
          <p className="text-white/40">{explanation.summary}</p>
          {explanation.memories_used.length > 0 && (
            <div>
              <p className="text-white/30 mb-1">Sources ({explanation.memories_used.length}):</p>
              <div className="flex flex-wrap gap-1">
                {explanation.memories_used.slice(0, 5).map((m) => (
                  <EvidenceChip
                    key={m.memory_id}
                    label={m.title || m.memory_id.slice(0, 8)}
                    score={m.relevance}
                  />
                ))}
              </div>
            </div>
          )}
          {explanation.relationship_paths.length > 0 && (
            <div>
              <p className="text-white/30 mb-1">Relationships:</p>
              <div className="flex flex-wrap gap-1">
                {explanation.relationship_paths.slice(0, 3).map((r, i) => (
                  <span key={i} className="px-2 py-0.5 rounded bg-white/5 text-white/50">
                    {r.from_entity} → {r.to_entity}
                  </span>
                ))}
              </div>
            </div>
          )}
          {explanation.confidence && (
            <div className="flex flex-wrap gap-2 mt-1">
              <EvidenceChip label="Sources" score={explanation.confidence.factors.source_count} />
              <EvidenceChip label="Recency" score={explanation.confidence.factors.recency_score} />
              <EvidenceChip label="Agreement" score={explanation.confidence.factors.agreement_score} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export function AIChat({ projectId }: AIChatProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { streamReason, answer, steps, isStreaming, isComplete, explanation } = useStreamReason();
  const inputRef = useRef<HTMLInputElement>(null);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, answer]);

  useEffect(() => {
    if (isComplete && answer) {
      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last?.role === "assistant") {
          return prev.map((m, i) =>
            i === prev.length - 1
              ? { ...m, content: answer, explanation: explanation ?? undefined, trail_id: "" }
              : m,
          );
        }
        return [
          ...prev,
          {
            id: Date.now().toString(),
            role: "assistant",
            content: answer,
            explanation: explanation ?? undefined,
            timestamp: new Date().toISOString(),
          },
        ];
      });
    }
  }, [isComplete, answer, explanation]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isStreaming) return;
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now().toString(),
        role: "user",
        content: input,
        timestamp: new Date().toISOString(),
      },
      {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "",
        timestamp: new Date().toISOString(),
      },
    ]);
    streamReason(input, projectId);
    setInput("");
  };

  return (
    <div className="flex flex-col h-full bg-black/40 backdrop-blur-md border-l border-white/10">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-white/10">
        <Brain size={16} className="text-purple-400" />
        <span className="text-sm text-white/80">MEMEX Reasoning</span>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-white/20 space-y-2">
            <Brain size={48} className="text-white/10" />
            <p className="text-sm">Ask a question to start reasoning</p>
            <p className="text-xs">MEMEX will search memories, find relationships, and explain its reasoning</p>
          </div>
        )}
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                msg.role === "user"
                  ? "bg-purple-500/20 border border-purple-500/30"
                  : "bg-white/5 border border-white/10"
              }`}
            >
              {msg.role === "assistant" && msg.content === "" && isStreaming ? (
                <div className="flex items-center gap-2 text-white/40">
                  <Loader2 size={14} className="animate-spin" />
                  {steps.map((s) => s.name).join(" → ") || "Thinking..."}
                </div>
              ) : (
                <>
                  <p className="text-sm text-white/80 whitespace-pre-wrap">{msg.content}</p>
                  {msg.explanation && <ReasoningPanel explanation={msg.explanation} />}
                </>
              )}
            </div>
          </div>
        ))}
        <div ref={endRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-white/10">
        <div className="flex items-center gap-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your memories..."
            disabled={isStreaming}
            className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/80 placeholder-white/30 focus:outline-none focus:border-purple-500/50 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="p-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-purple-400 hover:bg-purple-500/30 transition-colors disabled:opacity-30"
          >
            {isStreaming ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
          </button>
        </div>
      </form>
    </div>
  );
}
