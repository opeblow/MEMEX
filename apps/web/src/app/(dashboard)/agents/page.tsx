"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot, Plus, Trash2, Play, Activity,
  ChevronDown, ChevronRight, Loader2, Brain, Users, Lock, Globe,
  GitBranch,
} from "lucide-react";
import type {
  Agent, Workflow as WorkflowType, TaskExecution, Decision, ObservabilityEvent,
} from "@memex/types";
import {
  useAgents, useCreateAgent, useUpdateAgent, useDeleteAgent,
  useWorkflows, useAgentTasks,
  useAgentDecisions, useObservabilityEvents,
} from "@/hooks";

const SCOPE_ICONS: Record<string, React.ReactNode> = {
  private: <Lock size={12} />,
  workspace: <Users size={12} />,
  team: <Brain size={12} />,
  global: <Globe size={12} />,
};

const STATUS_COLORS: Record<string, string> = {
  active: "text-emerald-400 bg-emerald-500/10",
  inactive: "text-white/30 bg-white/5",
  paused: "text-yellow-400 bg-yellow-500/10",
};

const WORKFLOW_STATUS_COLORS: Record<string, string> = {
  completed: "text-emerald-400",
  failed: "text-red-400",
  running: "text-purple-400",
  queued: "text-white/30",
  paused: "text-yellow-400",
};

function CreateAgentModal({
  open,
  onClose,
  projectId,
}: {
  open: boolean;
  onClose: () => void;
  projectId: string;
}) {
  const createAgent = useCreateAgent();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [agentType, setAgentType] = useState("custom");
  const [memoryScope, setMemoryScope] = useState("workspace");
  const [capabilitiesText, setCapabilitiesText] = useState("");

  const handleSubmit = async () => {
    if (!name.trim()) return;
    await createAgent.mutateAsync({
      projectId,
      name: name.trim(),
      description: description.trim() || undefined,
      agent_type: agentType,
      memory_scope: memoryScope,
      capabilities: capabilitiesText
        ? capabilitiesText.split(",").map((s) => s.trim()).filter(Boolean)
        : undefined,
    });
    setName("");
    setDescription("");
    setCapabilitiesText("");
    onClose();
  };

  if (!open) return null;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.95, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        className="bg-[#0a0a0f] border border-white/10 rounded-xl p-6 w-full max-w-md mx-4"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-sm font-semibold text-white/80 mb-4">New Agent</h2>
        <div className="space-y-3">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Agent name"
            className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50 placeholder-white/20"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            rows={2}
            className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50 placeholder-white/20 resize-none"
          />
          <div className="flex gap-2">
            <select
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50"
            >
              <option value="custom">Custom</option>
              <option value="assistant">Assistant</option>
              <option value="researcher">Researcher</option>
              <option value="analyst">Analyst</option>
              <option value="workflow">Workflow</option>
            </select>
            <select
              value={memoryScope}
              onChange={(e) => setMemoryScope(e.target.value)}
              className="flex-1 bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50"
            >
              <option value="private">Private</option>
              <option value="workspace">Workspace</option>
              <option value="team">Team</option>
              <option value="global">Global</option>
            </select>
          </div>
          <input
            type="text"
            value={capabilitiesText}
            onChange={(e) => setCapabilitiesText(e.target.value)}
            placeholder="Capabilities (comma-separated, e.g. search, summarize, reason)"
            className="w-full bg-white/5 border border-white/10 rounded-lg px-3 py-2 text-sm text-white/60 focus:outline-none focus:border-purple-500/50 placeholder-white/20"
          />
          <div className="flex gap-2 pt-2">
            <button
              onClick={onClose}
              className="flex-1 px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-xs text-white/60 hover:bg-white/10 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleSubmit}
              disabled={!name.trim() || createAgent.isPending}
              className="flex-1 px-3 py-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-xs text-purple-400 hover:bg-purple-500/30 disabled:opacity-30 transition-colors flex items-center justify-center gap-2"
            >
              {createAgent.isPending ? <Loader2 size={12} className="animate-spin" /> : <Plus size={12} />}
              Create
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

function AgentCard({ agent, projectId }: { agent: Agent; projectId: string }) {
  const [expanded, setExpanded] = useState(false);
  const updateAgent = useUpdateAgent();
  const deleteAgent = useDeleteAgent();
  const { data: tasksData } = useAgentTasks(expanded ? agent.id : null, 10);
  const { data: decisionsData } = useAgentDecisions(expanded ? agent.id : null, 10);
  const { data: eventsData } = useObservabilityEvents(
    projectId,
    expanded ? agent.id : undefined,
  );

  const tasks = tasksData?.tasks || [];
  const decisions = decisionsData?.decisions || [];
  const events = eventsData?.events || [];

  const toggleStatus = () => {
    updateAgent.mutate({
      agentId: agent.id,
      status: agent.status === "active" ? "paused" : "active",
    });
  };

  return (
    <motion.div
      layout
      className="bg-white/[0.02] border border-white/10 rounded-xl overflow-hidden"
    >
      <div
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-3 px-4 py-3 cursor-pointer hover:bg-white/[0.02] transition-colors"
      >
        <div className="p-1.5 rounded-lg bg-purple-500/10">
          <Bot size={14} className="text-purple-400" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="text-sm text-white/80 truncate">{agent.name}</span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] ${STATUS_COLORS[agent.status] || "text-white/30 bg-white/5"}`}>
              {agent.status}
            </span>
            <span className="text-[10px] text-white/30">{agent.agent_type}</span>
          </div>
          {agent.description && (
            <p className="text-xs text-white/30 mt-0.5 truncate">{agent.description}</p>
          )}
          <div className="flex items-center gap-2 mt-1">
            <div className="flex items-center gap-1 text-[10px] text-white/30">
              {SCOPE_ICONS[agent.memory_scope] || null}
              {agent.memory_scope}
            </div>
            {agent.capabilities && agent.capabilities.length > 0 && (
              <div className="flex gap-1 flex-wrap">
                {agent.capabilities.slice(0, 3).map((cap) => (
                  <span key={cap} className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-white/40">
                    {cap}
                  </span>
                ))}
                {agent.capabilities.length > 3 && (
                  <span className="text-[10px] text-white/20">+{agent.capabilities.length - 3}</span>
                )}
              </div>
            )}
          </div>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={(e) => { e.stopPropagation(); toggleStatus(); }}
            className="p-1.5 rounded-lg hover:bg-white/5 text-white/30 hover:text-white/60 transition-colors"
            title={agent.status === "active" ? "Pause" : "Activate"}
          >
            <Play size={12} />
          </button>
          <button
            onClick={(e) => { e.stopPropagation(); deleteAgent.mutate(agent.id); }}
            className="p-1.5 rounded-lg hover:bg-white/5 text-white/30 hover:text-red-400 transition-colors"
            title="Delete"
          >
            <Trash2 size={12} />
          </button>
          {expanded ? <ChevronDown size={12} className="text-white/30" /> : <ChevronRight size={12} className="text-white/30" />}
        </div>
      </div>

      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-white/5"
          >
            <div className="grid grid-cols-3 gap-px bg-white/5">
              <div className="p-3 bg-[#0a0a0f]">
                <div className="flex items-center gap-1.5 text-[10px] text-white/30 mb-2">
                  <GitBranch size={10} /> Tasks ({tasks.length})
                </div>
                <div className="space-y-1">
                  {tasks.length === 0 && <p className="text-[10px] text-white/20">No tasks</p>}
                  {tasks.map((t: TaskExecution) => (
                    <div key={t.id} className="flex items-center gap-2 text-[10px]">
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        t.status === "completed" ? "bg-emerald-500"
                        : t.status === "failed" ? "bg-red-500"
                        : t.status === "running" ? "bg-purple-500"
                        : "bg-white/20"
                      }`} />
                      <span className="text-white/50 truncate flex-1">{t.name}</span>
                      {t.duration_ms && <span className="text-white/20">{t.duration_ms}ms</span>}
                    </div>
                  ))}
                </div>
              </div>
              <div className="p-3 bg-[#0a0a0f]">
                <div className="flex items-center gap-1.5 text-[10px] text-white/30 mb-2">
                  <Brain size={10} /> Decisions ({decisions.length})
                </div>
                <div className="space-y-1">
                  {decisions.length === 0 && <p className="text-[10px] text-white/20">No decisions</p>}
                  {decisions.map((d: Decision) => (
                    <div key={d.id} className="flex items-center gap-2 text-[10px]">
                      <span className="text-white/40 truncate flex-1">{d.decision_type}</span>
                      {d.confidence != null && (
                        <span className={`${d.confidence > 0.7 ? "text-emerald-400" : d.confidence > 0.4 ? "text-yellow-400" : "text-red-400"}`}>
                          {(d.confidence * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              </div>
              <div className="p-3 bg-[#0a0a0f]">
                <div className="flex items-center gap-1.5 text-[10px] text-white/30 mb-2">
                  <Activity size={10} /> Events ({events.length})
                </div>
                <div className="space-y-1">
                  {events.length === 0 && <p className="text-[10px] text-white/20">No events</p>}
                  {events.slice(0, 5).map((e: ObservabilityEvent) => (
                    <div key={e.id} className="flex items-center gap-2 text-[10px]">
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        e.level === "error" ? "bg-red-500"
                        : e.level === "warn" ? "bg-yellow-500"
                        : "bg-white/20"
                      }`} />
                      <span className="text-white/50 truncate flex-1">{e.event_name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default function AgentsPage() {
  const [projectId, setProjectId] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [filterScope, setFilterScope] = useState("");

  useEffect(() => {
    const stored = localStorage.getItem("memex_active_project");
    if (stored) {
      try { setProjectId(JSON.parse(stored).id || stored); } catch { setProjectId(stored); }
    }
  }, []);

  const { data: agentsData } = useAgents(projectId);
  const { data: workflowsData } = useWorkflows(projectId);
  const agents = agentsData?.agents || [];
  const workflows = workflowsData?.workflows || [];

  const filteredAgents = filterScope
    ? agents.filter((a: Agent) => a.memory_scope === filterScope)
    : agents;

  if (!projectId) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-sm text-white/30">Select a project to manage agents</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="max-w-3xl mx-auto space-y-6"
    >
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-white/80">AI Agents</h1>
          <p className="text-xs text-white/30 mt-1">
            Autonomous memory agents with memory scopes and workflows
          </p>
        </div>
        <button
          onClick={() => setShowCreate(true)}
          className="flex items-center gap-2 px-3 py-2 bg-purple-500/20 border border-purple-500/30 rounded-lg text-xs text-purple-400 hover:bg-purple-500/30 transition-colors"
        >
          <Plus size={14} />
          New Agent
        </button>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["", "private", "workspace", "team", "global"].map((scope) => (
          <button
            key={scope}
            onClick={() => setFilterScope(scope === filterScope ? "" : scope)}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs border transition-colors ${
              filterScope === scope
                ? "bg-purple-500/10 border-purple-500/30 text-purple-400"
                : "bg-white/5 border-white/10 text-white/40 hover:text-white/60"
            }`}
          >
            {scope ? <>{SCOPE_ICONS[scope]} {scope}</> : "All"}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {filteredAgents.length === 0 && (
          <p className="text-xs text-white/20 text-center py-8">
            {agents.length === 0 ? "No agents yet. Create your first agent." : "No agents match the selected scope."}
          </p>
        )}
        {filteredAgents.map((agent: Agent) => (
          <AgentCard key={agent.id} agent={agent} projectId={projectId} />
        ))}
      </div>

      <div className="space-y-3">
        <h2 className="text-xs font-semibold text-white/40 flex items-center gap-2">
          <GitBranch size={12} />
          Recent Workflows ({workflows.length})
        </h2>
        <div className="space-y-1">
          {workflows.length === 0 && (
            <p className="text-xs text-white/20">No workflows yet</p>
          )}
          {workflows.slice(0, 10).map((wf: WorkflowType) => (
            <div
              key={wf.id}
              className="flex items-center gap-3 px-3 py-2 rounded-lg bg-white/[0.02] hover:bg-white/5 transition-colors"
            >
              <div className="p-1 rounded bg-white/5">
                <GitBranch size={10} className="text-white/40" />
              </div>
              <span className="text-xs text-white/60 flex-1 truncate">{wf.name}</span>
              <span className={`text-xs ${WORKFLOW_STATUS_COLORS[wf.status] || "text-white/30"}`}>
                {wf.status}
              </span>
              {wf.progress_pct > 0 && (
                <span className="text-xs text-white/30">{wf.progress_pct}%</span>
              )}
              {wf.started_at && (
                <span className="text-[10px] text-white/20">
                  {new Date(wf.started_at).toLocaleDateString()}
                </span>
              )}
            </div>
          ))}
        </div>
      </div>

      <CreateAgentModal
        open={showCreate}
        onClose={() => setShowCreate(false)}
        projectId={projectId}
      />
    </motion.div>
  );
}
