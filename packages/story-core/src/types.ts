export type Primitive = string | number | boolean | null;

export interface Condition {
  path: string;
  operator: "equals" | "notEquals" | "gte" | "lte" | "exists";
  value?: Primitive;
}

export interface StoryEffect {
  type:
    | "fact.set"
    | "flag.set"
    | "resource.change"
    | "relationship.change"
    | "record.write"
    | "record.redact"
    | "testimony.learn"
    | "cause.activate"
    | "cause.resolve"
    | "memory.trigger";
  key?: string;
  value?: Primitive;
  amount?: number;
  character?: string;
  field?: string;
  channel?: RecordChannel;
  record?: RecordEntry;
  recordId?: string;
  causeId?: string;
  memoryId?: string;
  label: string;
}

export interface StoryChoice {
  id: string;
  label: string;
  detail: string;
  tone?: "care" | "record" | "collective" | "caution";
  conditions?: Condition[];
  effects: StoryEffect[];
  next: string;
}

export interface TextVariant {
  conditions: Condition[];
  paragraphs: string[];
}

export interface StoryNode {
  id: string;
  sceneId: string;
  act: string;
  title: string;
  speaker: string;
  location: string;
  time: string;
  paragraphs: string[];
  variants?: TextVariant[];
  visual: {
    motif: "river" | "slip" | "bell" | "song" | "archive";
    caption: string;
  };
  choices: StoryChoice[];
  ending?: boolean;
}

export interface SceneFile {
  schemaVersion: string;
  id: string;
  title: string;
  estimatedMinutes: number;
  startNode: string;
  nodes: StoryNode[];
}

export interface CharacterDefinition {
  id: string;
  name: string;
  role: string;
  voice: string;
  desire: string;
  fear: string;
  color: string;
  initialRelationship: RelationshipState;
}

export interface CharacterFile {
  schemaVersion: string;
  characters: CharacterDefinition[];
}

export interface CauseDefinition {
  id: string;
  name: string;
  description: string;
  firstAct: string;
  futureReturn: string;
}

export interface CauseFile {
  schemaVersion: string;
  causes: CauseDefinition[];
}

export type RecordChannel = "official" | "private" | "oral";

export interface RecordEntry {
  id: string;
  title: string;
  text: string;
  source: string;
  confidence: "confirmed" | "partial" | "contested";
  sensitivity?: "low" | "medium" | "high";
  redacted?: boolean;
}

export interface RecordChannelDefinition {
  id: RecordChannel;
  name: string;
  description: string;
}

export interface RecordFile {
  schemaVersion: string;
  channels: RecordChannelDefinition[];
}

export interface ChapterManifest {
  schemaVersion: string;
  contentVersion: string;
  runtimeVersion: string;
  id: string;
  title: string;
  subtitle: string;
  sampleTitle: string;
  description: string;
  sceneFiles: string[];
  characterFile: string;
  causeFile: string;
  recordFile: string;
}

export interface ContentBundle {
  manifest: ChapterManifest;
  scene: SceneFile;
  characters: CharacterDefinition[];
  causes: CauseDefinition[];
  recordChannels: RecordChannelDefinition[];
}

export interface RelationshipState {
  trust: number;
  sharedDebt: number;
  rift: number;
}

export interface RecordState {
  integrity: number;
  exposure: number;
  entries: RecordEntry[];
}

export interface StoryState {
  currentNode: string;
  world: Record<string, Primitive>;
  player: {
    resources: Record<string, number>;
    flags: Record<string, Primitive>;
  };
  relations: Record<string, RelationshipState>;
  facts: Record<string, Primitive>;
  knowledge: Record<string, Primitive>;
  records: Record<RecordChannel, RecordState>;
  causes: Record<string, "dormant" | "active" | "resolved">;
  memories: Record<string, "locked" | "triggered">;
  visitedNodes: string[];
  selectedChoices: string[];
}

export interface StoryEvent {
  id: number;
  type: StoryEffect["type"] | "scene.enter" | "choice.select";
  at: string;
  nodeId: string;
  choiceId?: string;
  payload: Record<string, unknown>;
  label: string;
}

export interface SaveFile {
  saveVersion: string;
  contentVersion: string;
  runtimeVersion: string;
  chapterId: string;
  currentNode: string;
  stateSnapshot: StoryState;
  eventLog: StoryEvent[];
  chapterHandoffs: Record<string, unknown>[];
  playtimeSeconds: number;
  createdAt: string;
  updatedAt: string;
}

export interface ValidationIssue {
  level: "error" | "warning";
  code: string;
  message: string;
  location?: string;
}
