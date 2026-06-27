"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api/client";
import type {
  Agent,
  AgentListResponse,
  AgentCreateRequest,
  AgentUpdateRequest,
  Workflow,
  WorkflowListResponse,
  WorkflowCreateRequest,
  WorkflowUpdateRequest,
  TaskExecutionListResponse,
  Decision,
  DecisionListResponse,
  DecisionCreateRequest,
  ObservabilityEvent,
  ObservabilityEventListResponse,
  HandoffRequest,
  HandoffResponse,
} from "@memex/types";

export function useAgents(projectId: string) {
  return useQuery({
    queryKey: ["agents", projectId],
    queryFn: () =>
      api.get<AgentListResponse>(`/api/v1/memex/agents?project_id=${projectId}`),
    enabled: !!projectId,
  });
}

export function useAgent(agentId: string | null) {
  return useQuery({
    queryKey: ["agent", agentId],
    queryFn: () => api.get<Agent>(`/api/v1/memex/agents/${agentId}`),
    enabled: !!agentId,
  });
}

export function useCreateAgent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ projectId, ...data }: AgentCreateRequest & { projectId: string }) => {
      return api.post<Agent>(`/api/v1/memex/agents?project_id=${projectId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
    },
  });
}

export function useUpdateAgent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ agentId, ...data }: AgentUpdateRequest & { agentId: string }) => {
      return api.patch<Agent>(`/api/v1/memex/agents/${agentId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
      queryClient.invalidateQueries({ queryKey: ["agent"] });
    },
  });
}

export function useDeleteAgent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (agentId: string) => {
      return api.delete<{ status: string }>(`/api/v1/memex/agents/${agentId}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agents"] });
    },
  });
}

export function useWorkflows(projectId: string) {
  return useQuery({
    queryKey: ["workflows", projectId],
    queryFn: () =>
      api.get<WorkflowListResponse>(`/api/v1/memex/workflows?project_id=${projectId}`),
    enabled: !!projectId,
  });
}

export function useAgentWorkflows(agentId: string | null) {
  return useQuery({
    queryKey: ["agentWorkflows", agentId],
    queryFn: () => {
      if (!agentId) return Promise.resolve({ workflows: [], total: 0 });
      return api.get<WorkflowListResponse>(`/api/v1/memex/agents/${agentId}/workflows`);
    },
    enabled: false,
  });
}

export function useWorkflow(workflowId: string | null) {
  return useQuery({
    queryKey: ["workflow", workflowId],
    queryFn: () => api.get<Workflow>(`/api/v1/memex/workflows/${workflowId}`),
    enabled: !!workflowId,
  });
}

export function useCreateWorkflow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ projectId, ...data }: WorkflowCreateRequest & { projectId: string }) => {
      return api.post<Workflow>(`/api/v1/memex/agents/${data.agent_id}/workflows?project_id=${projectId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
    },
  });
}

export function useUpdateWorkflow() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ workflowId, ...data }: WorkflowUpdateRequest & { workflowId: string }) => {
      return api.patch<Workflow>(`/api/v1/memex/workflows/${workflowId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
      queryClient.invalidateQueries({ queryKey: ["workflow"] });
    },
  });
}

export function useAgentTasks(agentId: string | null, limit = 20) {
  return useQuery({
    queryKey: ["agentTasks", agentId, limit],
    queryFn: () =>
      api.get<TaskExecutionListResponse>(
        `/api/v1/memex/agents/${agentId}/tasks?limit=${limit}`,
      ),
    enabled: !!agentId,
  });
}

export function useWorkflowTasks(workflowId: string | null) {
  return useQuery({
    queryKey: ["workflowTasks", workflowId],
    queryFn: () =>
      api.get<TaskExecutionListResponse>(`/api/v1/memex/workflows/${workflowId}/tasks`),
    enabled: !!workflowId,
  });
}

export function useAgentDecisions(agentId: string | null, limit = 20) {
  return useQuery({
    queryKey: ["agentDecisions", agentId, limit],
    queryFn: () =>
      api.get<DecisionListResponse>(
        `/api/v1/memex/agents/${agentId}/decisions?limit=${limit}`,
      ),
    enabled: !!agentId,
  });
}

export function useWorkflowDecisions(workflowId: string | null) {
  return useQuery({
    queryKey: ["workflowDecisions", workflowId],
    queryFn: () =>
      api.get<DecisionListResponse>(`/api/v1/memex/workflows/${workflowId}/decisions`),
    enabled: !!workflowId,
  });
}

export function useRecordDecision() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ projectId, ...data }: DecisionCreateRequest & { projectId: string }) => {
      return api.post<Decision>(`/api/v1/memex/decisions?project_id=${projectId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["agentDecisions"] });
      queryClient.invalidateQueries({ queryKey: ["workflowDecisions"] });
    },
  });
}

export function useObservabilityEvents(projectId: string, agentId?: string, eventType?: string) {
  const params = new URLSearchParams({ project_id: projectId });
  if (agentId) params.set("agent_id", agentId);
  if (eventType) params.set("event_type", eventType);
  return useQuery({
    queryKey: ["observabilityEvents", projectId, agentId, eventType],
    queryFn: () =>
      api.get<ObservabilityEventListResponse>(
        `/api/v1/memex/observability/events?${params.toString()}`,
      ),
    enabled: !!projectId,
  });
}

export function useRecordObservabilityEvent() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ projectId, ...data }: { projectId: string; agent_id?: string; workflow_id?: string; task_id?: string; event_type: string; event_name: string; data?: Record<string, unknown>; duration_ms?: number; level?: string }) => {
      return api.post<ObservabilityEvent>(`/api/v1/memex/observability/events?project_id=${projectId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["observabilityEvents"] });
    },
  });
}

export function useHandoff() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ projectId, ...data }: HandoffRequest & { projectId: string }) => {
      return api.post<HandoffResponse>(`/api/v1/memex/agents/handoff?project_id=${projectId}`, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
    },
  });
}
