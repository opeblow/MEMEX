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

export interface TrailStep {
  step: number;
  name: string;
  description: string;
  data: Record<string, unknown>;
  memory_ids: string[];
  duration_ms: number;
}

export interface ConfidenceFactors {
  source_count: number;
  relationship_strength: number;
  recency_score: number;
  agreement_score: number;
  entity_consistency: number;
  graph_connectivity: number;
}

export interface MemoryConfidence {
  score: number;
  factors: ConfidenceFactors;
  label: string;
}

export interface MemoryContribution {
  memory_id: string;
  title?: string;
  relevance: number;
  evidence?: string;
  explanation?: string;
}

export interface RelationshipPath {
  from_entity: string;
  to_entity: string;
  relationship_type: string;
  strength: number;
}

export interface TimelinePath {
  event_type: string;
  memory_id: string;
  timestamp?: string;
  description?: string;
}

export interface Explanation {
  summary: string;
  memories_used: MemoryContribution[];
  relationship_paths: RelationshipPath[];
  timeline_paths: TimelinePath[];
  confidence?: MemoryConfidence;
}

export interface ReasoningRequest {
  query: string;
  project_id: string;
  include_trail?: boolean;
  include_explanation?: boolean;
  top_k?: number;
}

export interface ReasoningResponse {
  answer: string;
  trail_id?: string;
  explanation?: Explanation;
  trail?: TrailStep[];
  processing_time_ms: number;
}

export interface ReasoningStreamEvent {
  event: "start" | "step" | "token" | "complete";
  data?: Record<string, unknown>;
  content?: string;
}

export interface MemoryTrailResponse {
  id: string;
  project_id: string;
  question: string;
  answer?: string;
  trail_steps: TrailStep[];
  memory_ids: string[];
  confidence_score?: number;
  processing_time_ms?: number;
  explanation?: Explanation;
  created_at: string;
}

export interface MemoryEvidenceResponse {
  memory_id: string;
  content_preview?: string;
  source?: string;
  memory_type?: string;
  importance: number;
  tags?: string[];
  relationships: Record<string, unknown>[];
  timeline_events: Record<string, unknown>[];
  created_at?: string;
}

export interface Entity {
  id: string;
  name: string;
  entity_type: string;
  description?: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface EntityListResponse {
  entities: Entity[];
  total: number;
}

export interface Relationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  strength: number;
  metadata?: Record<string, unknown>;
  created_at: string;
}

export interface RelationshipListResponse {
  relationships: Relationship[];
  total: number;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  explanation?: Explanation;
  trail_id?: string;
  timestamp: string;
}

export interface ReasonHookResult {
  execute: (query: string, includeTrail?: boolean) => void;
  answer: string | null;
  explanation: Explanation | null;
  trail: TrailStep[] | null;
  trailId: string | null;
  confidence: MemoryConfidence | null;
  isLoading: boolean;
  processingTimeMs: number | null;
}

export interface StreamReasonHookResult {
  streamReason: (query: string, includeTrail?: boolean) => void;
  answer: string;
  steps: TrailStep[];
  memoryIds: string[];
  isStreaming: boolean;
  isComplete: boolean;
  trailId: string | null;
  explanation: Explanation | null;
}
