import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { StoryEngine } from "../../../packages/story-core/src/engine";
import { createSave, validateSave } from "../../../packages/story-core/src/save";
import { validateBundle } from "../../../packages/story-core/src/validation";
import type {
  CauseFile,
  ChapterManifest,
  CharacterFile,
  ContentBundle,
  MemoryFile,
  RecordFile,
  SceneFile
} from "../../../packages/story-core/src/types";

const root = process.cwd();
const contentRoot = resolve(root, "content");

async function readJson<T>(path: string): Promise<T> {
  const normalized = path.replace(/^[/\\]+/, "");
  return JSON.parse(await readFile(resolve(contentRoot, normalized), "utf8")) as T;
}

async function loadBundle(): Promise<ContentBundle> {
  const manifest = await readJson<ChapterManifest>("chapters/ch01/chapter.json");
  const [scenes, characters, causes, records, memories] = await Promise.all([
    Promise.all(manifest.sceneFiles.map((path) => readJson<SceneFile>(path))),
    readJson<CharacterFile>(manifest.characterFile),
    readJson<CauseFile>(manifest.causeFile),
    readJson<RecordFile>(manifest.recordFile),
    readJson<MemoryFile>(manifest.memoryFile)
  ]);
  return {
    manifest,
    scenes,
    characters: characters.characters,
    causes: causes.causes,
    recordChannels: records.channels,
    memories: memories.memories
  };
}

interface AuditStats {
  routeCount: number;
  endingNodes: Set<string>;
  minimumEvents: number;
  maximumEvents: number;
  minimumRecords: number;
  maximumRecords: number;
  replayedSaves: number;
}

function auditRoutes(bundle: ContentBundle): AuditStats {
  const stats: AuditStats = {
    routeCount: 0,
    endingNodes: new Set(),
    minimumEvents: Number.POSITIVE_INFINITY,
    maximumEvents: 0,
    minimumRecords: Number.POSITIVE_INFINITY,
    maximumRecords: 0,
    replayedSaves: 0
  };

  const visit = (engine: StoryEngine, path: string[]): void => {
    const node = engine.getCurrentNode();
    if (node.ending) {
      const state = engine.getState();
      const eventCount = engine.getEvents().length;
      const recordCount = Object.values(state.records).reduce(
        (total, channel) => total + channel.entries.length,
        0
      );
      if (recordCount === 0) throw new Error(`路线 ${path.join(" > ")} 没有生成记录`);

      const save = createSave(engine, 300);
      const saveErrors = validateSave(bundle, save);
      if (saveErrors.length) {
        throw new Error(`路线 ${path.join(" > ")} 存档回放失败：${saveErrors.join("；")}`);
      }

      stats.routeCount += 1;
      stats.endingNodes.add(node.id);
      stats.minimumEvents = Math.min(stats.minimumEvents, eventCount);
      stats.maximumEvents = Math.max(stats.maximumEvents, eventCount);
      stats.minimumRecords = Math.min(stats.minimumRecords, recordCount);
      stats.maximumRecords = Math.max(stats.maximumRecords, recordCount);
      stats.replayedSaves += 1;
      return;
    }
    const choices = engine.getAvailableChoices();
    if (node.textEntry) {
      const branch = engine.fork();
      branch.submitText(node.textEntry.id, node.textEntry.defaultValue);
      visit(branch, [...path, `${node.textEntry.id}=${node.textEntry.defaultValue}`]);
      return;
    }
    if (!choices.length) throw new Error(`路线在 ${node.id} 无法继续`);
    for (const choice of choices) {
      const branch = engine.fork();
      branch.choose(choice.id);
      visit(branch, [...path, choice.id]);
    }
  };

  visit(new StoryEngine(bundle), []);
  return stats;
}

async function main(): Promise<void> {
  const bundle = await loadBundle();
  const issues = validateBundle(bundle);
  const errors = issues.filter((issue) => issue.level === "error");
  if (errors.length) {
    errors.forEach((issue) =>
      console.error(`[${issue.code}] ${issue.location ?? "内容"}：${issue.message}`)
    );
    process.exitCode = 1;
    return;
  }

  const stats = auditRoutes(bundle);
  console.log("《山河无名》序章—ACT02 核心原型路线审计通过");
  console.log(`- 场景文件：${bundle.scenes.length}`);
  console.log(`- 节点：${bundle.scenes.reduce((total, scene) => total + scene.nodes.length, 0)}`);
  console.log(
    `- 预计时长：${bundle.scenes.reduce((total, scene) => total + scene.estimatedMinutes, 0)} 分钟`
  );
  console.log(`- 完整路线：${stats.routeCount}`);
  console.log(`- 结局节点：${stats.endingNodes.size}`);
  console.log(`- 单路线事件：${stats.minimumEvents}—${stats.maximumEvents}`);
  console.log(`- 单路线记录：${stats.minimumRecords}—${stats.maximumRecords}`);
  console.log(`- 存档回放：${stats.replayedSaves}/${stats.routeCount}`);
  if (issues.length) console.log(`- 非阻断提示：${issues.length}`);
}

void main();
