export type MemoryType =
  | "text" | "file" | "code" | "image" | "audio" | "video"
  | "url" | "conversation" | "meeting_note" | "github_issue"
  | "support_ticket" | "research" | "decision";

export type MemoryStatus = "processing" | "indexed" | "failed" | "deleted" | "archived";

export type SourceTag = "session" | "graph" | "graph_context" | "trace" | "vector" | "timeline";

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

export interface MemoryDetail {
  id: string;
  project_id: string;
  user_id: string;
  session_id?: string;
  title: string;
  memory_type: string;
  status: string;
  source?: string;
  source_url?: string;
  file_path?: string;
  mime_type?: string;
  content_preview?: string;
  size_bytes?: number;
  token_count?: number;
  chunk_count?: number;
  importance: number;
  tags: string[];
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export type QueryType =
  | "graph_completion" | "rag_completion" | "hybrid_completion"
  | "chunks" | "summaries" | "temporal" | "cypher" | "feeling_lucky" | null;

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
  explanation?: string;
}

export interface RecallResponse {
  answer: string;
  sources: RecallSource[];
  processingTimeMs: number;
}

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

export interface TimelineEvent {
  id: string;
  project_id: string;
  user_id: string;
  event_type: string;
  data: Record<string, unknown>;
  created_at: string;
}

export interface TimelineQuery {
  projectId: string;
  fromDate?: string;
  toDate?: string;
  eventTypes?: string[];
  limit?: number;
  offset?: number;
}

export interface TimelineResponse {
  events: TimelineEvent[];
  total: number;
  summary: Record<string, unknown>;
}

export interface SearchRequest {
  query: string;
  projectId: string;
  limit?: number;
}

export interface SearchResponse {
  results: MemoryDetail[];
  total: number;
  processingTimeMs: number;
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
  nodesEnriched: number;
  edgesAdded: number;
  summariesGenerated: number;
  processingTimeMs: number;
}

export interface ForgetOutput {
  status: string;
  deletedDataIds: string[];
  deletedGraphNodes: number;
  deletedVectors: number;
}

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
  getEvents(projectId: string, options?: TimelineQuery): Promise<TimelineEvent[]>;
  recordEvent(projectId: string, type: string, data?: Record<string, unknown>): Promise<string>;
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
