import { createInitialState, reduceEvent, StoryEngine } from "./engine";
import type { ContentBundle, SaveFile, StoryEvent, StoryState } from "./types";

export const SAVE_VERSION = "1.0.0";

function stableState(state: StoryState): string {
  return JSON.stringify(state);
}

export function createSave(
  engine: StoryEngine,
  playtimeSeconds: number,
  existingCreatedAt?: string
): SaveFile {
  const now = new Date().toISOString();
  const bundle = engine.getBundle();
  const state = engine.getState();
  return {
    saveVersion: SAVE_VERSION,
    contentVersion: bundle.manifest.contentVersion,
    runtimeVersion: bundle.manifest.runtimeVersion,
    chapterId: bundle.manifest.id,
    currentNode: state.currentNode,
    stateSnapshot: state,
    eventLog: engine.getEvents(),
    chapterHandoffs: [],
    playtimeSeconds,
    createdAt: existingCreatedAt ?? now,
    updatedAt: now
  };
}

export function replayEvents(bundle: ContentBundle, events: StoryEvent[]): StoryState {
  return events.reduce((state, event) => reduceEvent(state, event), createInitialState(bundle));
}

export function validateSave(bundle: ContentBundle, save: SaveFile): string[] {
  const errors: string[] = [];
  if (save.saveVersion !== SAVE_VERSION) errors.push(`不支持的存档版本 ${save.saveVersion}`);
  if (save.chapterId !== bundle.manifest.id) errors.push("存档章节与当前内容不一致");
  if (save.contentVersion !== bundle.manifest.contentVersion) {
    errors.push(`内容版本不一致：存档 ${save.contentVersion} / 当前 ${bundle.manifest.contentVersion}`);
  }
  const replayed = replayEvents(bundle, save.eventLog);
  if (stableState(replayed) !== stableState(save.stateSnapshot)) {
    errors.push("事件回放结果与存档快照不一致");
  }
  if (replayed.currentNode !== save.currentNode) errors.push("存档当前节点不一致");
  return errors;
}

export function restoreSave(engine: StoryEngine, save: SaveFile): void {
  const errors = validateSave(engine.getBundle(), save);
  if (errors.length) throw new Error(errors.join("；"));
  engine.replaceFromEvents(save.eventLog);
}
