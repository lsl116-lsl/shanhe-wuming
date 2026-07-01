import type {
  Condition,
  ContentBundle,
  Primitive,
  RecordChannel,
  RecordEntry,
  StoryChoice,
  StoryEffect,
  StoryEvent,
  StoryNode,
  StoryState
} from "./types";

const clone = <T>(value: T): T => structuredClone(value);

function getAtPath(source: unknown, path: string): unknown {
  return path.split(".").reduce<unknown>((current, segment) => {
    if (current && typeof current === "object" && segment in current) {
      return (current as Record<string, unknown>)[segment];
    }
    return undefined;
  }, source);
}

function setAtPath(target: Record<string, Primitive>, key: string, value: Primitive): void {
  target[key] = value;
}

export function matchesCondition(state: StoryState, condition: Condition): boolean {
  const actual = getAtPath(state, condition.path);
  switch (condition.operator) {
    case "equals":
      return actual === condition.value;
    case "notEquals":
      return actual !== condition.value;
    case "gte":
      return typeof actual === "number" && actual >= Number(condition.value);
    case "lte":
      return typeof actual === "number" && actual <= Number(condition.value);
    case "exists":
      return actual !== undefined && actual !== null;
  }
}

export function matchesAll(state: StoryState, conditions: Condition[] = []): boolean {
  return conditions.every((condition) => matchesCondition(state, condition));
}

export function createInitialState(bundle: ContentBundle): StoryState {
  const relations = Object.fromEntries(
    bundle.characters.map((character) => [character.id, clone(character.initialRelationship)])
  );
  const causes = Object.fromEntries(bundle.causes.map((cause) => [cause.id, "dormant" as const]));
  const memories = Object.fromEntries(
    bundle.memories.map((memory) => [memory.id, "locked" as const])
  );

  return {
    currentNode: "",
    world: {
      chapter: bundle.manifest.id,
      rain: true,
      daylight: "暮色将近"
    },
    player: {
      resources: {
        daylight: 5,
        grain: 3,
        strength: 4
      },
      flags: {}
    },
    relations,
    facts: {},
    knowledge: {},
    records: {
      official: { integrity: 0, exposure: 0, entries: [] },
      private: { integrity: 0, exposure: 0, entries: [] },
      oral: { integrity: 0, exposure: 0, entries: [] }
    },
    causes,
    memories,
    visitedNodes: [],
    selectedChoices: []
  };
}

function upsertRecord(entries: RecordEntry[], record: RecordEntry): RecordEntry[] {
  const index = entries.findIndex((entry) => entry.id === record.id);
  if (index < 0) return [...entries, clone(record)];
  return entries.map((entry, entryIndex) => (entryIndex === index ? clone(record) : entry));
}

export function reduceEvent(state: StoryState, event: StoryEvent): StoryState {
  const next: StoryState = {
    ...state,
    world: { ...state.world },
    player: {
      resources: { ...state.player.resources },
      flags: { ...state.player.flags }
    },
    relations: Object.fromEntries(
      Object.entries(state.relations).map(([id, relation]) => [id, { ...relation }])
    ),
    facts: { ...state.facts },
    knowledge: { ...state.knowledge },
    records: {
      official: { ...state.records.official, entries: [...state.records.official.entries] },
      private: { ...state.records.private, entries: [...state.records.private.entries] },
      oral: { ...state.records.oral, entries: [...state.records.oral.entries] }
    },
    causes: { ...state.causes },
    memories: { ...state.memories },
    visitedNodes: [...state.visitedNodes],
    selectedChoices: [...state.selectedChoices]
  };
  const payload = event.payload;

  switch (event.type) {
    case "scene.enter": {
      const nodeId = String(payload.nodeId);
      next.currentNode = nodeId;
      if (!next.visitedNodes.includes(nodeId)) next.visitedNodes.push(nodeId);
      break;
    }
    case "choice.select": {
      if (event.choiceId && !next.selectedChoices.includes(event.choiceId)) {
        next.selectedChoices.push(event.choiceId);
      }
      break;
    }
    case "fact.set":
      setAtPath(next.facts, String(payload.key), payload.value as Primitive);
      break;
    case "flag.set":
      setAtPath(next.player.flags, String(payload.key), payload.value as Primitive);
      break;
    case "testimony.learn":
      setAtPath(next.knowledge, String(payload.key), payload.value as Primitive);
      break;
    case "resource.set": {
      const key = String(payload.key);
      next.player.resources[key] = Number(payload.value);
      break;
    }
    case "resource.change": {
      const key = String(payload.key);
      next.player.resources[key] = (next.player.resources[key] ?? 0) + Number(payload.amount);
      break;
    }
    case "relationship.change": {
      const character = String(payload.character);
      const field = String(payload.field) as keyof typeof next.relations[string];
      const relation = next.relations[character];
      if (relation) relation[field] += Number(payload.amount);
      break;
    }
    case "record.write": {
      const channel = String(payload.channel) as RecordChannel;
      const record = payload.record as unknown as RecordEntry;
      next.records[channel].entries = upsertRecord(next.records[channel].entries, record);
      next.records[channel].integrity = Math.min(10, next.records[channel].integrity + 1);
      if (record.sensitivity === "high") {
        next.records[channel].exposure = Math.min(10, next.records[channel].exposure + 2);
      } else if (record.sensitivity === "medium") {
        next.records[channel].exposure = Math.min(10, next.records[channel].exposure + 1);
      }
      break;
    }
    case "record.redact": {
      const channel = String(payload.channel) as RecordChannel;
      const recordId = String(payload.recordId);
      next.records[channel].entries = next.records[channel].entries.map((record) =>
        record.id === recordId ? { ...record, redacted: true } : record
      );
      next.records[channel].exposure = Math.max(0, next.records[channel].exposure - 1);
      break;
    }
    case "cause.activate":
      next.causes[String(payload.causeId)] = "active";
      break;
    case "cause.resolve":
      next.causes[String(payload.causeId)] = "resolved";
      break;
    case "memory.trigger":
      next.memories[String(payload.memoryId)] = "triggered";
      break;
  }

  return next;
}

function effectPayload(effect: StoryEffect): Record<string, unknown> {
  return {
    key: effect.key,
    value: effect.value,
    amount: effect.amount,
    character: effect.character,
    field: effect.field,
    channel: effect.channel,
    record: effect.record,
    recordId: effect.recordId,
    causeId: effect.causeId,
    memoryId: effect.memoryId
  };
}

export class StoryEngine {
  private state: StoryState;
  private events: StoryEvent[] = [];
  private listeners = new Set<() => void>();
  private sequence = 0;

  constructor(private readonly bundle: ContentBundle) {
    this.state = createInitialState(bundle);
    const startNode = bundle.scenes[0]?.startNode;
    if (!startNode) throw new Error("内容包没有可进入的起点");
    this.enterNode(startNode, "核心原型开始");
  }

  getBundle(): ContentBundle {
    return this.bundle;
  }

  getState(): StoryState {
    return clone(this.state);
  }

  getEvents(): StoryEvent[] {
    return clone(this.events);
  }

  fork(): StoryEngine {
    const branch = new StoryEngine(this.bundle);
    branch.state = clone(this.state);
    branch.events = clone(this.events);
    branch.sequence = this.sequence;
    return branch;
  }

  getCurrentNode(): StoryNode {
    const node = this.findNode(this.state.currentNode);
    if (!node) throw new Error(`找不到当前节点：${this.state.currentNode}`);
    return node;
  }

  getCurrentScene() {
    const node = this.getCurrentNode();
    const scene = this.bundle.scenes.find((candidate) => candidate.id === node.sceneId);
    if (!scene) throw new Error(`找不到节点 ${node.id} 所属场景 ${node.sceneId}`);
    return scene;
  }

  getVisibleParagraphs(node = this.getCurrentNode()): string[] {
    const matching = node.variants?.filter((variant) => matchesAll(this.state, variant.conditions)) ?? [];
    return [
      ...node.paragraphs,
      ...matching.flatMap((variant) => variant.paragraphs)
    ];
  }

  getAvailableChoices(node = this.getCurrentNode()): StoryChoice[] {
    return node.choices.filter((choice) => matchesAll(this.state, choice.conditions));
  }

  choose(choiceId: string): void {
    const node = this.getCurrentNode();
    const choice = this.getAvailableChoices(node).find((candidate) => candidate.id === choiceId);
    if (!choice) throw new Error(`节点 ${node.id} 没有可用选择 ${choiceId}`);

    this.dispatch("choice.select", node.id, choice.label, { choiceId }, choice.id);
    for (const effect of choice.effects) {
      this.dispatch(effect.type, node.id, effect.label, effectPayload(effect), choice.id);
    }
    this.enterNode(choice.next, `进入「${this.findNode(choice.next).title}」`);
    this.emit();
  }

  replaceFromEvents(events: StoryEvent[]): void {
    this.state = createInitialState(this.bundle);
    this.events = [];
    this.sequence = 0;
    for (const event of events) {
      this.state = reduceEvent(this.state, event);
      this.events.push(clone(event));
      this.sequence = Math.max(this.sequence, event.id);
    }
    this.emit();
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private findNode(nodeId: string): StoryNode {
    const node = this.bundle.scenes
      .flatMap((scene) => scene.nodes)
      .find((candidate) => candidate.id === nodeId);
    if (!node) throw new Error(`内容引用了不存在的节点：${nodeId}`);
    return node;
  }

  private enterNode(nodeId: string, label: string): void {
    this.findNode(nodeId);
    this.dispatch("scene.enter", nodeId, label, { nodeId });
  }

  private dispatch(
    type: StoryEvent["type"],
    nodeId: string,
    label: string,
    payload: Record<string, unknown>,
    choiceId?: string
  ): void {
    const event: StoryEvent = {
      id: ++this.sequence,
      type,
      at: new Date().toISOString(),
      nodeId,
      choiceId,
      payload,
      label
    };
    this.state = reduceEvent(this.state, event);
    this.events.push(event);
  }

  private emit(): void {
    this.listeners.forEach((listener) => listener());
  }
}
