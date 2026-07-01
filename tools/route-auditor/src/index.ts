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
  const [scene, characters, causes, records] = await Promise.all([
    readJson<SceneFile>(manifest.sceneFiles[0] ?? ""),
    readJson<CharacterFile>(manifest.characterFile),
    readJson<CauseFile>(manifest.causeFile),
    readJson<RecordFile>(manifest.recordFile)
  ]);
  return {
    manifest,
    scene,
    characters: characters.characters,
    causes: causes.causes,
    recordChannels: records.channels
  };
}

interface RouteResult {
  choices: string[];
  endingNode: string;
  eventCount: number;
  recordCount: number;
}

function playRoute(bundle: ContentBundle, choiceIds: string[]): StoryEngine {
  const engine = new StoryEngine(bundle);
  choiceIds.forEach((choiceId) => engine.choose(choiceId));
  return engine;
}

function enumerateRoutes(bundle: ContentBundle): RouteResult[] {
  const results: RouteResult[] = [];
  const visit = (path: string[]): void => {
    const engine = playRoute(bundle, path);
    const node = engine.getCurrentNode();
    if (node.ending) {
      const state = engine.getState();
      results.push({
        choices: path,
        endingNode: node.id,
        eventCount: engine.getEvents().length,
        recordCount: Object.values(state.records).reduce(
          (total, channel) => total + channel.entries.length,
          0
        )
      });
      return;
    }
    const choices = engine.getAvailableChoices();
    if (!choices.length) throw new Error(`路线在 ${node.id} 无法继续`);
    for (const choice of choices) visit([...path, choice.id]);
  };
  visit([]);
  return results;
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

  const routes = enumerateRoutes(bundle);
  const endings = new Set(routes.map((route) => route.endingNode));
  const zeroRecordRoutes = routes.filter((route) => route.recordCount === 0);
  if (zeroRecordRoutes.length) throw new Error(`${zeroRecordRoutes.length} 条路线没有生成记录`);

  for (const route of routes) {
    const engine = playRoute(bundle, route.choices);
    const save = createSave(engine, 300);
    const saveErrors = validateSave(bundle, save);
    if (saveErrors.length) {
      throw new Error(`路线 ${route.choices.join(" > ")} 存档回放失败：${saveErrors.join("；")}`);
    }
  }

  const eventCounts = routes.map((route) => route.eventCount);
  const recordCounts = routes.map((route) => route.recordCount);
  console.log("《山河无名》阶段 A 路线审计通过");
  console.log(`- 节点：${bundle.scene.nodes.length}`);
  console.log(`- 完整路线：${routes.length}`);
  console.log(`- 结局节点：${endings.size}`);
  console.log(`- 单路线事件：${Math.min(...eventCounts)}—${Math.max(...eventCounts)}`);
  console.log(`- 单路线记录：${Math.min(...recordCounts)}—${Math.max(...recordCounts)}`);
  console.log(`- 存档回放：${routes.length}/${routes.length}`);
  if (issues.length) console.log(`- 非阻断提示：${issues.length}`);
}

void main();
