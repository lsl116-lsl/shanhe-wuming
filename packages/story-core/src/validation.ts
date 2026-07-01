import type { ContentBundle, StoryEffect, ValidationIssue } from "./types";

const effectRequirements: Partial<Record<StoryEffect["type"], (keyof StoryEffect)[]>> = {
  "fact.set": ["key"],
  "flag.set": ["key"],
  "profile.set": ["key", "value"],
  "resource.set": ["key", "value"],
  "resource.change": ["key", "amount"],
  "relationship.change": ["character", "field", "amount"],
  "record.write": ["channel", "record"],
  "record.redact": ["channel", "recordId"],
  "testimony.learn": ["key"],
  "cause.activate": ["causeId"],
  "cause.resolve": ["causeId"],
  "memory.trigger": ["memoryId"]
};

export function validateBundle(bundle: ContentBundle): ValidationIssue[] {
  const issues: ValidationIssue[] = [];
  const allNodes = bundle.scenes.flatMap((scene) => scene.nodes);
  const nodeIds = new Set(allNodes.map((node) => node.id));
  const sceneIds = new Set(bundle.scenes.map((scene) => scene.id));
  const characterIds = new Set(bundle.characters.map((character) => character.id));
  const causeIds = new Set(bundle.causes.map((cause) => cause.id));
  const memoryIds = new Set(bundle.memories.map((memory) => memory.id));
  const choiceIds = allNodes.flatMap((node) => node.choices.map((choice) => choice.id));
  const textEntryIds = allNodes.flatMap((node) => (node.textEntry ? [node.textEntry.id] : []));

  if (bundle.scenes.length === 0) {
    issues.push({ level: "error", code: "NO_SCENES", message: "内容包没有场景文件" });
    return issues;
  }

  if (sceneIds.size !== bundle.scenes.length) {
    issues.push({ level: "error", code: "DUPLICATE_SCENE", message: "存在重复场景 ID" });
  }
  if (characterIds.size !== bundle.characters.length) {
    issues.push({ level: "error", code: "DUPLICATE_CHARACTER", message: "存在重复人物 ID" });
  }
  if (causeIds.size !== bundle.causes.length) {
    issues.push({ level: "error", code: "DUPLICATE_CAUSE", message: "存在重复因果 ID" });
  }
  if (memoryIds.size !== bundle.memories.length) {
    issues.push({ level: "error", code: "DUPLICATE_MEMORY", message: "存在重复记忆 ID" });
  }
  for (const memory of bundle.memories) {
    for (const causeId of memory.linkedCauses) {
      if (!causeIds.has(causeId)) {
        issues.push({
          level: "error",
          code: "MISSING_MEMORY_CAUSE",
          message: `记忆 ${memory.id} 关联未知因果 ${causeId}`
        });
      }
    }
  }
  for (const requiredChannel of ["official", "private", "oral"] as const) {
    if (!bundle.recordChannels.some((channel) => channel.id === requiredChannel)) {
      issues.push({
        level: "error",
        code: "MISSING_RECORD_CHANNEL",
        message: `缺少记录层 ${requiredChannel}`
      });
    }
  }

  for (const scene of bundle.scenes) {
    if (!nodeIds.has(scene.startNode)) {
      issues.push({
        level: "error",
        code: "MISSING_START",
        message: `场景 ${scene.id} 的起点 ${scene.startNode} 不存在`
      });
    }
    const start = allNodes.find((node) => node.id === scene.startNode);
    if (start && start.sceneId !== scene.id) {
      issues.push({
        level: "error",
        code: "INVALID_SCENE_START",
        message: `场景 ${scene.id} 的起点属于 ${start.sceneId}`
      });
    }
  }

  const chapterStart = bundle.scenes[0]?.startNode ?? "";
  if (!nodeIds.has(chapterStart)) {
    issues.push({
      level: "error",
      code: "MISSING_START",
      message: `章节起点 ${chapterStart} 不存在`
    });
  }

  if (nodeIds.size !== allNodes.length) {
    issues.push({ level: "error", code: "DUPLICATE_NODE", message: "存在重复节点 ID" });
  }
  if (new Set(choiceIds).size !== choiceIds.length) {
    issues.push({ level: "error", code: "DUPLICATE_CHOICE", message: "存在重复选择 ID" });
  }
  if (new Set(textEntryIds).size !== textEntryIds.length) {
    issues.push({ level: "error", code: "DUPLICATE_TEXT_ENTRY", message: "存在重复文字输入 ID" });
  }

  for (const scene of bundle.scenes) {
    for (const node of scene.nodes) {
      if (!sceneIds.has(node.sceneId) || node.sceneId !== scene.id) {
        issues.push({
          level: "error",
          code: "INVALID_SCENE_REFERENCE",
          message: `节点声明属于 ${node.sceneId}，实际位于 ${scene.id}`,
          location: node.id
        });
      }
    if (!node.ending && node.choices.length === 0 && !node.textEntry) {
      issues.push({
        level: "error",
        code: "DEAD_END",
        message: "非结局节点没有选择",
        location: node.id
      });
    }
    if (node.textEntry && node.choices.length > 0) {
      issues.push({
        level: "error",
        code: "AMBIGUOUS_INTERACTION",
        message: "节点不能同时提供选择和文字输入",
        location: node.id
      });
    }
    if (node.textEntry) {
      if (!nodeIds.has(node.textEntry.next)) {
        issues.push({
          level: "error",
          code: "MISSING_TEXT_NEXT",
          message: `文字输入 ${node.textEntry.id} 指向不存在的节点 ${node.textEntry.next}`,
          location: node.id
        });
      }
      if (
        node.textEntry.minLength < 1 ||
        node.textEntry.maxLength < node.textEntry.minLength
      ) {
        issues.push({
          level: "error",
          code: "INVALID_TEXT_LENGTH",
          message: `文字输入 ${node.textEntry.id} 的长度约束无效`,
          location: node.id
        });
      }
    }
    for (const choice of node.choices) {
      if (!nodeIds.has(choice.next)) {
        issues.push({
          level: "error",
          code: "MISSING_NEXT",
          message: `选择 ${choice.id} 指向不存在的节点 ${choice.next}`,
          location: node.id
        });
      }
      for (const effect of choice.effects) {
        for (const required of effectRequirements[effect.type] ?? []) {
          if (effect[required] === undefined) {
            issues.push({
              level: "error",
              code: "INVALID_EFFECT",
              message: `${effect.type} 缺少字段 ${String(required)}`,
              location: `${node.id}/${choice.id}`
            });
          }
        }
        if (
          effect.type === "relationship.change" &&
          effect.character &&
          !characterIds.has(effect.character)
        ) {
          issues.push({
            level: "error",
            code: "MISSING_CHARACTER",
            message: `关系效果引用未知人物 ${effect.character}`,
            location: `${node.id}/${choice.id}`
          });
        }
        if (
          (effect.type === "cause.activate" || effect.type === "cause.resolve") &&
          effect.causeId &&
          !causeIds.has(effect.causeId)
        ) {
          issues.push({
            level: "error",
            code: "MISSING_CAUSE",
            message: `因果效果引用未知节点 ${effect.causeId}`,
            location: `${node.id}/${choice.id}`
          });
        }
        if (
          effect.type === "memory.trigger" &&
          effect.memoryId &&
          !memoryIds.has(effect.memoryId)
        ) {
          issues.push({
            level: "error",
            code: "MISSING_MEMORY",
            message: `记忆效果引用未知碎片 ${effect.memoryId}`,
            location: `${node.id}/${choice.id}`
          });
        }
      }
    }
  }
  }

  const reachable = new Set<string>();
  const queue = [chapterStart];
  while (queue.length) {
    const id = queue.shift();
    if (!id || reachable.has(id)) continue;
    reachable.add(id);
    const node = allNodes.find((candidate) => candidate.id === id);
    node?.choices.forEach((choice) => queue.push(choice.next));
    if (node?.textEntry) queue.push(node.textEntry.next);
  }
  for (const node of allNodes) {
    if (!reachable.has(node.id)) {
      issues.push({
        level: "warning",
        code: "UNREACHABLE_NODE",
        message: "节点无法从起点到达",
        location: node.id
      });
    }
  }

  if (!allNodes.some((node) => node.ending && reachable.has(node.id))) {
    issues.push({
      level: "error",
      code: "NO_REACHABLE_ENDING",
      message: "从章节起点无法抵达任何结局节点"
    });
  }

  return issues;
}
