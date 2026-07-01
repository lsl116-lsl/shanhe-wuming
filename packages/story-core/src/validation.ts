import type { ContentBundle, StoryEffect, ValidationIssue } from "./types";

const effectRequirements: Partial<Record<StoryEffect["type"], (keyof StoryEffect)[]>> = {
  "fact.set": ["key"],
  "flag.set": ["key"],
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
  const nodeIds = new Set(bundle.scene.nodes.map((node) => node.id));
  const characterIds = new Set(bundle.characters.map((character) => character.id));
  const causeIds = new Set(bundle.causes.map((cause) => cause.id));

  if (!nodeIds.has(bundle.scene.startNode)) {
    issues.push({
      level: "error",
      code: "MISSING_START",
      message: `起点 ${bundle.scene.startNode} 不存在`
    });
  }

  if (nodeIds.size !== bundle.scene.nodes.length) {
    issues.push({ level: "error", code: "DUPLICATE_NODE", message: "存在重复节点 ID" });
  }

  for (const node of bundle.scene.nodes) {
    if (!node.ending && node.choices.length === 0) {
      issues.push({
        level: "error",
        code: "DEAD_END",
        message: "非结局节点没有选择",
        location: node.id
      });
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
      }
    }
  }

  const reachable = new Set<string>();
  const queue = [bundle.scene.startNode];
  while (queue.length) {
    const id = queue.shift();
    if (!id || reachable.has(id)) continue;
    reachable.add(id);
    const node = bundle.scene.nodes.find((candidate) => candidate.id === id);
    node?.choices.forEach((choice) => queue.push(choice.next));
  }
  for (const node of bundle.scene.nodes) {
    if (!reachable.has(node.id)) {
      issues.push({
        level: "warning",
        code: "UNREACHABLE_NODE",
        message: "节点无法从起点到达",
        location: node.id
      });
    }
  }

  return issues;
}
