import "./styles.css";
import { StoryEngine } from "../../../packages/story-core/src/engine";
import {
  createSave,
  restoreSave,
  validateSave
} from "../../../packages/story-core/src/save";
import { validateBundle } from "../../../packages/story-core/src/validation";
import type {
  CauseFile,
  ChapterManifest,
  CharacterFile,
  ContentBundle,
  MemoryFile,
  RecordChannel,
  RecordFile,
  SaveFile,
  SceneFile,
  StoryState
} from "../../../packages/story-core/src/types";

const MANUAL_SAVE_KEY = "shanhe-wuming:ch01-act01-act02:manual-save";
const AUTO_SAVE_KEY = "shanhe-wuming:ch01-act01-act02:auto-save";
const sessionStartedAt = Date.now();
let savedCreatedAt: string | undefined;
let engine: StoryEngine;
let bundle: ContentBundle;
let toastTimer = 0;

const $ = <T extends HTMLElement>(selector: string): T => {
  const element = document.querySelector<T>(selector);
  if (!element) throw new Error(`界面缺少元素：${selector}`);
  return element;
};

async function loadJson<T>(path: string): Promise<T> {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`无法读取 ${path}（${response.status}）`);
  return (await response.json()) as T;
}

async function loadBundle(): Promise<ContentBundle> {
  const manifest = await loadJson<ChapterManifest>("/chapters/ch01/chapter.json");
  const [scenes, characterFile, causeFile, recordFile, memoryFile] = await Promise.all([
    Promise.all(manifest.sceneFiles.map((path) => loadJson<SceneFile>(path))),
    loadJson<CharacterFile>(manifest.characterFile),
    loadJson<CauseFile>(manifest.causeFile),
    loadJson<RecordFile>(manifest.recordFile),
    loadJson<MemoryFile>(manifest.memoryFile)
  ]);
  return {
    manifest,
    scenes,
    characters: characterFile.characters,
    causes: causeFile.causes,
    recordChannels: recordFile.channels,
    memories: memoryFile.memories
  };
}

function playtimeSeconds(): number {
  return Math.floor((Date.now() - sessionStartedAt) / 1000);
}

function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const rest = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${rest}`;
}

function showToast(message: string): void {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("show"), 2200);
}

function escapeHtml(value: unknown): string {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function labelForFact(key: string): string {
  const labels: Record<string, string> = {
    childLiftedFromCart: "车辕下的孩子获救",
    sickSheltered: "病者被安置进旧库",
    unconfirmedDead: "未确认死者",
    slipsRecovered: "抢救湿简",
    careDelayed: "救治曾被延迟",
    collectiveRollCall: "流民共同点名",
    fugitiveExposed: "假名者身份暴露",
    refusalPreserved: "拒绝说明得到保留",
    slipKeeper: "半名残简保管",
    songForm: "旧曲形态",
    registerKeeper: "临时名册去向",
    yearsSinceRain: "渡口雨夜之后",
    grainSolution: "旧仓赈粮办法",
    grainReleased: "本季放粮",
    grainDebt: "聚落粮债",
    provisionalHouseholds: "暂编户数",
    deletedNameHandling: "被划姓名处理",
    overlookedHousehold: "仓后漏记一户",
    overlookedHouseholdPlan: "漏记户安置",
    seasonOutcome: "本季结果"
  };
  return labels[key] ?? key;
}

function renderResources(state: StoryState): void {
  const act = engine.getCurrentNode().act;
  const names: Record<string, string> = {
    daylight: act === "ACT01" ? "暮色" : "农时",
    grain: "粮",
    strength: "体力"
  };
  const maximums: Record<string, number> = {
    daylight: 5,
    grain: act === "ACT01" ? 3 : 5,
    strength: act === "ACT01" ? 4 : 5
  };
  $("#resource-list").innerHTML = Object.entries(state.player.resources)
    .map(([key, value]) => {
      const max = maximums[key] ?? 5;
      const percent = Math.max(0, Math.min(100, (value / max) * 100));
      return `
        <div class="resource">
          <span>${escapeHtml(names[key] ?? key)}</span>
          <div class="resource-track"><div class="resource-fill" style="width:${percent}%"></div></div>
          <strong>${value}</strong>
        </div>`;
    })
    .join("");
}

function renderCharacters(state: StoryState): void {
  const act = engine.getCurrentNode().act;
  const visibleCharacters =
    act === "ACT01"
      ? bundle.characters.filter((character) =>
          ["JIBO", "HEAN", "HANNING", "LIUNIANG"].includes(character.id)
        )
      : bundle.characters;
  $("#character-list").innerHTML = visibleCharacters
    .map((character) => {
      const relation = state.relations[character.id];
      const score = (relation?.trust ?? 0) + (relation?.sharedDebt ?? 0) - (relation?.rift ?? 0);
      const scoreLabel = score > 0 ? `+${score}` : String(score);
      return `
        <article class="character-card" title="${escapeHtml(character.desire)}">
          <span class="character-avatar" style="--character-color:${character.color}">${escapeHtml(character.name[0])}</span>
          <span>
            <strong class="character-name">${escapeHtml(character.name)}</strong>
            <small class="character-role">${escapeHtml(character.role)}</small>
          </span>
          <span class="relation-delta" aria-label="信任 ${relation?.trust ?? 0}，共同债 ${relation?.sharedDebt ?? 0}，裂痕 ${relation?.rift ?? 0}">
            关系<strong>${scoreLabel}</strong>
            <small>信 ${relation?.trust ?? 0} · 债 ${relation?.sharedDebt ?? 0} · 裂 ${relation?.rift ?? 0}</small>
          </span>
        </article>`;
    })
    .join("");
}

function renderRecords(state: StoryState): void {
  const facts = Object.entries(state.facts);
  const totalRecords = Object.values(state.records).reduce(
    (total, channel) => total + channel.entries.length,
    0
  );
  const solution = state.facts.grainSolution;
  const comparison =
    solution === "OLD_RITE"
      ? "请恤文书承认流民应被救济，仓册却仍把他们留在名籍之外。"
      : solution === "NEW_REGISTER"
        ? "新籍让一部分人领到粮，也同时把田、役与连带责任写进每一户。"
        : solution === "PRIVATE_GRAIN"
          ? "官档没有发生赈粮，商旅私账却留下了一笔无法只用粮价结清的债。"
          : "故事继续后，这里会并列事实、官档、私录与口述的差异。";
  const factsHtml = `
    <section class="fact-card">
      <div class="record-group-header"><strong>真实发生</strong><span>${facts.length} 项</span></div>
      ${
        facts.length
          ? facts
              .map(
                ([key, value]) =>
                  `<p><b>${escapeHtml(labelForFact(key))}</b> · ${escapeHtml(value)}</p>`
              )
              .join("")
          : '<div class="empty-state">尚未形成可确认事实</div>'
      }
    </section>`;

  const recordGroups = bundle.recordChannels
    .map((definition) => {
      const channel = state.records[definition.id];
      const entries = channel.entries
        .map(
          (entry) => `
            <article class="record-entry ${entry.redacted ? "redacted" : ""}">
              <strong>${escapeHtml(entry.title)}${entry.redacted ? " · 已删隐" : ""}</strong>
              <p>${escapeHtml(entry.text)}</p>
              <small>
                ${escapeHtml(entry.source)}
                · ${escapeHtml(
                  entry.confidence === "confirmed"
                    ? "已确认"
                    : entry.confidence === "partial"
                      ? "部分确认"
                      : "存在争议"
                )}
                ${entry.sensitivity ? ` · ${escapeHtml(entry.sensitivity === "high" ? "高暴露" : entry.sensitivity === "medium" ? "中暴露" : "低暴露")}` : ""}
              </small>
            </article>`
        )
        .join("");
      return `
        <section class="record-group">
          <div class="record-group-header">
            <strong>${escapeHtml(definition.name)}</strong>
            <span class="meter-pair">
              <i>完整 ${channel.integrity}/10</i>
              <i class="${channel.exposure > 5 ? "risk" : ""}">风险 ${channel.exposure}/10</i>
            </span>
          </div>
          <p class="panel-intro">${escapeHtml(definition.description)}</p>
          ${entries || '<div class="empty-state">这一层还没有留下记录</div>'}
        </section>`;
    })
    .join("");

  $("#records-panel").innerHTML = `
    <p class="panel-intro">同一件事会留下互不相同的版本。完整不等于安全，公开也不自动等于正义。</p>
    <section class="archive-summary">
      <span><b>${facts.length}</b> 项事实</span>
      <span><b>${totalRecords}</b> 份记录</span>
      <span><b>${state.visitedNodes.length}</b> 个现场</span>
    </section>
    <section class="record-conflict">
      <small>当前版本差异</small>
      <p>${escapeHtml(comparison)}</p>
    </section>
    ${factsHtml}${recordGroups}`;
}

function renderMemories(state: StoryState): void {
  const triggered = bundle.memories.filter((memory) => state.memories[memory.id] === "triggered");
  $("#memories-panel").innerHTML = `
    <p class="panel-intro">记忆只改变你会注意、追问和告诉谁，不提供预知或正确答案。</p>
    <div class="memory-progress">
      <span>本章已触发 <b>${triggered.length}</b> / ${bundle.memories.length}</span>
      <span>当前上限 ${engine.getCurrentNode().act === "ACT01" ? "M0" : "M1"}</span>
    </div>
    ${bundle.memories
      .map((memory) => {
        const seen = state.memories[memory.id] === "triggered";
        return `
          <article class="memory-card ${seen ? "triggered" : "locked"}">
            <div class="memory-header">
              <strong>${escapeHtml(seen ? memory.title : "尚未触发的回声")}</strong>
              <span>${escapeHtml(memory.act)} · ${escapeHtml(memory.revealLevel)}</span>
            </div>
            <p>${escapeHtml(seen ? memory.perceivedContent : memory.mandatory ? "它会在本幕找到兜底入口。" : "它只回应特定做法，不影响主线通行。")}</p>
            ${seen ? `<small>现实作用：${escapeHtml(memory.realityEffect)}</small>` : ""}
          </article>`;
      })
      .join("")}`;
}

function renderCauses(state: StoryState): void {
  $("#causes-panel").innerHTML = `
    <p class="panel-intro">因果不是善恶分。它记录一件事何时种下、以什么形态进入后世。</p>
    ${bundle.causes
      .map((cause) => {
        const status = state.causes[cause.id] ?? "dormant";
        const statusLabel = status === "active" ? "已种下" : status === "resolved" ? "已回收" : "未触发";
        return `
          <article class="cause-card ${status}">
            <div class="cause-header">
              <strong>${escapeHtml(cause.name)}</strong>
              <span>${escapeHtml(cause.id)} · ${statusLabel}</span>
            </div>
            <p>${escapeHtml(cause.description)}</p>
            <p><b>后世：</b>${escapeHtml(cause.futureReturn)}</p>
          </article>`;
      })
      .join("")}`;
}

function renderEvents(): void {
  const events = engine.getEvents().slice().reverse().slice(0, 30);
  $("#events-panel").innerHTML = `
    <p class="panel-intro">界面不直接改状态。每次变化都形成可回放事件，存档会用它们重建同一结果。</p>
    ${events
      .map(
        (event) => `
          <article class="event-card">
            <span class="event-index">${event.id.toString().padStart(2, "0")}</span>
            <div class="event-header">
              <span class="event-type">${escapeHtml(event.type)}</span>
              <span>${escapeHtml(event.nodeId.replace("CH01-", ""))}</span>
            </div>
            <p>${escapeHtml(event.label)}</p>
          </article>`
      )
      .join("")}`;
}

function renderStory(): void {
  const state = engine.getState();
  const node = engine.getCurrentNode();
  const scene = engine.getCurrentScene();
  const choices = engine.getAvailableChoices();

  $("#game").setAttribute("aria-busy", "false");
  $("#act-label").textContent = `第一章 · ${node.act} · ${scene.title}`;
  $("#scene-progress").textContent = `已作 ${state.selectedChoices.length} 次行动`;
  $("#location-label").textContent = node.location;
  $("#time-label").textContent = node.time;
  $("#node-title").textContent = node.title;
  $("#speaker-label").textContent = node.speaker;
  $("#scene-caption").textContent = node.visual.caption;
  $("#scene-art").dataset.motif = node.visual.motif;
  $("#story-copy").innerHTML = engine
    .getVisibleParagraphs(node)
    .map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`)
    .join("");

  $("#choice-list").innerHTML = choices
    .map(
      (choice) => `
        <button class="choice" type="button" data-choice="${escapeHtml(choice.id)}" data-tone="${escapeHtml(choice.tone ?? "caution")}">
          <strong>${escapeHtml(choice.label)}</strong>
          <small>${escapeHtml(choice.detail)}</small>
        </button>`
    )
    .join("");
  $("#choice-list")
    .querySelectorAll<HTMLButtonElement>("[data-choice]")
    .forEach((button) => {
      button.addEventListener("click", () => {
        engine.choose(button.dataset.choice ?? "");
        autoSave();
        window.scrollTo({ top: 0, behavior: "smooth" });
      });
    });

  $("#ending-card").toggleAttribute("hidden", !node.ending);
  const endingTitle = $("#ending-card strong");
  const endingCopy = $("#ending-card p");
  if (node.ending) {
    endingTitle.textContent =
      node.act === "ACT02" ? "核心原型已抵达 ACT02 结尾" : "本世档案已经生成第一行";
    endingCopy.textContent =
      node.act === "ACT02"
        ? "打开“档案”和“记忆”，比较这次活命如何进入不同版本。"
        : "打开右侧“档案”，比较真实发生、官档、私录与口述。";
  }
  renderResources(state);
  renderCharacters(state);
  renderRecords(state);
  renderMemories(state);
  renderCauses(state);
  renderEvents();
}

function makeSave(): SaveFile {
  return createSave(engine, playtimeSeconds(), savedCreatedAt);
}

function autoSave(): void {
  const save = makeSave();
  savedCreatedAt = save.createdAt;
  localStorage.setItem(AUTO_SAVE_KEY, JSON.stringify(save));
}

function manualSave(): void {
  const save = makeSave();
  savedCreatedAt = save.createdAt;
  localStorage.setItem(MANUAL_SAVE_KEY, JSON.stringify(save));
  showToast("进度已保存，事件日志可完整回放。");
}

function loadLocalSave(): void {
  const manual = localStorage.getItem(MANUAL_SAVE_KEY);
  const raw = manual ?? localStorage.getItem(AUTO_SAVE_KEY);
  if (!raw) {
    showToast("还没有可读取的本地存档。");
    return;
  }
  try {
    const save = JSON.parse(raw) as SaveFile;
    restoreSave(engine, save);
    savedCreatedAt = save.createdAt;
    showToast(`已读取${manual ? "手动存档" : "自动存档"} · ${save.eventLog.length} 条事件。`);
  } catch (error) {
    showToast(error instanceof Error ? error.message : "本地存档无法读取");
  }
}

function exportSave(): void {
  const save = makeSave();
  const blob = new Blob([JSON.stringify(save, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `shanhe-wuming-${save.chapterId}-${save.currentNode}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
  showToast("JSON 存档已导出。");
}

async function importSave(file: File): Promise<void> {
  const save = JSON.parse(await file.text()) as SaveFile;
  const errors = validateSave(bundle, save);
  if (errors.length) throw new Error(errors.join("；"));
  restoreSave(engine, save);
  savedCreatedAt = save.createdAt;
  localStorage.setItem(MANUAL_SAVE_KEY, JSON.stringify(save));
  localStorage.setItem(AUTO_SAVE_KEY, JSON.stringify(save));
  showToast("JSON 存档已导入并通过事件回放校验。");
}

function resetStory(): void {
  engine = new StoryEngine(bundle);
  savedCreatedAt = undefined;
  localStorage.removeItem(MANUAL_SAVE_KEY);
  localStorage.removeItem(AUTO_SAVE_KEY);
  wireEngine();
  renderStory();
  showToast("已回到洛水暮雨。");
}

function wireEngine(): void {
  engine.subscribe(renderStory);
}

function wireUi(): void {
  $("#save-button").addEventListener("click", manualSave);
  $("#load-button").addEventListener("click", loadLocalSave);
  $("#export-button").addEventListener("click", exportSave);
  $("#import-button").addEventListener("click", () => $("#import-input").click());
  $("#import-input").addEventListener("change", async (event) => {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (!file) return;
    try {
      await importSave(file);
    } catch (error) {
      showToast(error instanceof Error ? error.message : "存档导入失败");
    }
    (event.target as HTMLInputElement).value = "";
  });
  $("#reset-button").addEventListener("click", resetStory);

  document.querySelectorAll<HTMLButtonElement>(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach((item) => {
        item.classList.toggle("active", item === tab);
        item.setAttribute("aria-selected", String(item === tab));
      });
      document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("active"));
      $(`#${tab.dataset.tab}-panel`).classList.add("active");
    });
  });

  window.setInterval(() => {
    $("#playtime").textContent = formatTime(playtimeSeconds());
  }, 1000);
}

async function bootstrap(): Promise<void> {
  try {
    bundle = await loadBundle();
    const issues = validateBundle(bundle);
    const errors = issues.filter((issue) => issue.level === "error");
    if (errors.length) throw new Error(errors.map((issue) => issue.message).join("；"));

    engine = new StoryEngine(bundle);
    wireEngine();
    wireUi();
    renderStory();
    $("#content-version").textContent =
      `内容 ${bundle.manifest.contentVersion} · 运行时 ${bundle.manifest.runtimeVersion}`;
    $("#validation-status").textContent =
      issues.length === 0
        ? `内容校验通过 · ${bundle.scenes.length} 个场景文件`
        : `校验通过 · ${issues.length} 个提示`;
  } catch (error) {
    $("#fatal-error").toggleAttribute("hidden", false);
    $("#fatal-message").textContent = error instanceof Error ? error.message : String(error);
    $("#game").setAttribute("aria-busy", "false");
    throw error;
  }
}

void bootstrap();
