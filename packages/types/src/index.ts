// ──────────────────────────────────────
// Memory Types
// ──────────────────────────────────────

export type MemoryType =
  | "text"
  | "file"
  | "code"
  | "image"
  | "audio"
  | "video"
  | "url"
  | "conversation"
  | "meeting_note"
  | "github_issue"
  | "support_ticket"
  | "research"
  | "decision";

export type MemoryStatus = "processing" | "indexed" | "failed" | "deleted";

export type SourceTag = "session" | "graph" | "graph_context" | "trace";

export interface MemoryMetadata {
  title?: string;
  tags?: string[];
  source?: string;
  sourceUrl?: string;
  filePath?: string;
  mimeType?: string;
  tokenCount?: number;
  chunkCount?: number;
  importance?: number;
}

export interface Memory {
  id: string;
  projectId: string;
  userId: string;
  sessionId?: string;
  title: string;
  memoryType: MemoryType;
  status: MemoryStatus;
  contentPreview?: string;
  tags: string[];
  importance: number;
  createdAt: string;
  updatedAt: string;
  metadata: MemoryMetadata;
}

// ──────────────────────────────────────
// Recall Types
// ──────────────────────────────────────

export type QueryType =
  | "graph_completion"
  | "rag_completion"
  | "hybrid_completion"
  | "chunks"
  | "summaries"
  | "temporal"
  | "cypher"
  | "feeling_lucky"
  | null;

export interface RecallRequest {
  query: string;
  projectId: string;
  sessionId?: string;
  sessionOnly?: boolean;
  datasets?: string[];
  queryType?: QueryType;
  topK?: number;
  onlyContext?: boolean;
  stream?: boolean;
}

export interface RecallSource {
  text: string;
  source: SourceTag;
  memoryId: string;
  chunkId?: string;
  relevanceScore: number;
  evidence?: string;
}

export interface RecallResponse {
  answer: string;
  sources: RecallSource[];
  processingTimeMs: number;
}

// ──────────────────────────────────────
// Graph Types
// ──────────────────────────────────────

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  importance: number;
  position: { x: number; y: number; z: number };
  metadata?: Record<string, unknown>;
}

export interface GraphEdge {
  source: string;
  target: string;
  label: string;
  weight: number;
  metadata?: Record<string, unknown>;
}

export interface GraphSnapshot {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

// ──────────────────────────────────────
// Auth Types
// ──────────────────────────────────────

export interface User {
  id: string;
  email: string;
  displayName: string;
  avatarUrl?: string;
  role: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
}

export interface ApiKey {
  id: string;
  name: string;
  keyPrefix: string;
  createdAt: string;
  lastUsedAt?: string;
  isActive: boolean;
}

// ──────────────────────────────────────
// Project Types
// ──────────────────────────────────────

export interface Project {
  id: string;
  workspaceId: string;
  name: string;
  slug: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Workspace {
  id: string;
  name: string;
  slug: string;
  description?: string;
  ownerId: string;
  createdAt: string;
}

// ──────────────────────────────────────
// Session Types
// ──────────────────────────────────────

export interface Session {
  id: string;
  projectId: string;
  userId: string;
  cogneeSessionId?: string;
  title?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

// ──────────────────────────────────────
// Phase 4 — Service Interfaces
// ──────────────────────────────────────

export interface ServiceProvider {
  memory: MemoryService;
  cognee: CogneeService;
  knowledgeGraph: KnowledgeGraph;
  memoryTimeline: MemoryTimeline;
  ai: AIService;
}

export interface MemoryService {
  remember(input: RememberInput): Promise<RememberOutput>;
  improve(projectId: string, sessionIds?: string[]): Promise<ImproveOutput>;
  forget(projectId: string, dataId?: string): Promise<ForgetOutput>;
}

export interface RememberInput {
  data: string;
  projectId: string;
  sessionId?: string;
  memoryType?: string;
  title?: string;
  tags?: string[];
  runInBackground?: boolean;
}

export interface RememberOutput {
  memoryId: string;
  datasetId: string;
  chunkCount: number;
  tokenCount: number;
  processingTimeMs: number;
  status: string;
}

export interface ImproveOutput {
  projectId: string;
  status: string;
  processingTimeMs: number;
}

export interface ForgetOutput {
  status: string;
  deletedDataIds: string[];
  deletedGraphNodes: number;
  deletedVectors: number;
}

export interface CogneeService {
  recall(input: RecallRequest): Promise<RecallResponse>;
  recallStream(input: RecallRequest, signal: AbortSignal): Promise<Response>;
  checkHealth(): Promise<boolean>;
}

export interface KnowledgeGraph {
  getSnapshot(projectId: string): Promise<GraphSnapshot>;
  getNeighborhood(memoryId: string, depth?: number): Promise<GraphSnapshot>;
  searchNodes(projectId: string, query: string): Promise<GraphNode[]>;
}

export interface MemoryTimeline {
  getEvents(projectId: string, options?: { from?: string; to?: string; limit?: number }): Promise<TimelineEvent[]>;
  recordEvent(projectId: string, type: string, data?: Record<string, unknown>): Promise<string>;
}

export interface TimelineEvent {
  id: string;
  projectId: string;
  eventType: string;
  timestamp: string;
  data?: Record<string, unknown>;
}

export interface AIService {
  complete(prompt: string, options?: { systemPrompt?: string; maxTokens?: number; temperature?: number }): Promise<string>;
  embed(texts: string[]): Promise<number[][]>;
  summarize(text: string, maxLength?: number): Promise<string>;
}

export interface WorkspaceSettings {
  theme: string;
  language: string;
  notificationsEnabled: boolean;
  emailDigest: boolean;
}
