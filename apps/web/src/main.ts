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
  RecordChannel,
  RecordFile,
  SaveFile,
  SceneFile,
  StoryState
} from "../../../packages/story-core/src/types";

const MANUAL_SAVE_KEY = "shanhe-wuming:stage-a:manual-save";
const AUTO_SAVE_KEY = "shanhe-wuming:stage-a:auto-save";
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
  const [scene, characterFile, causeFile, recordFile] = await Promise.all([
    loadJson<SceneFile>(manifest.sceneFiles[0] ?? ""),
    loadJson<CharacterFile>(manifest.characterFile),
    loadJson<CauseFile>(manifest.causeFile),
    loadJson<RecordFile>(manifest.recordFile)
  ]);
  return {
    manifest,
    scene,
    characters: characterFile.characters,
    causes: causeFile.causes,
    recordChannels: recordFile.channels
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
    registerKeeper: "临时名册去向"
  };
  return labels[key] ?? key;
}

function renderResources(state: StoryState): void {
  const names: Record<string, string> = { daylight: "暮色", grain: "粮", strength: "体力" };
  const maximums: Record<string, number> = { daylight: 5, grain: 3, strength: 4 };
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
  $("#character-list").innerHTML = bundle.characters
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
          <span class="relation-delta">关系<strong>${scoreLabel}</strong></span>
        </article>`;
    })
    .join("");
}

function renderRecords(state: StoryState): void {
  const facts = Object.entries(state.facts);
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
              <small>${escapeHtml(entry.source)} · ${escapeHtml(entry.confidence)}</small>
            </article>`
        )
        .join("");
      return `
        <section class="record-group">
          <div class="record-group-header">
            <strong>${escapeHtml(definition.name)}</strong>
            <span class="meter-pair">
              <i>完整 ${channel.integrity}/5</i>
              <i class="${channel.exposure > 2 ? "risk" : ""}">风险 ${channel.exposure}/5</i>
            </span>
          </div>
          <p class="panel-intro">${escapeHtml(definition.description)}</p>
          ${entries || '<div class="empty-state">这一层还没有留下记录</div>'}
        </section>`;
    })
    .join("");

  $("#records-panel").innerHTML = `
    <p class="panel-intro">同一件事会留下互不相同的版本。完整不等于安全，公开也不自动等于正义。</p>
    ${factsHtml}${recordGroups}`;
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
              <span>${escapeHtml(event.nodeId.replace("CH01-ACT01-", ""))}</span>
            </div>
            <p>${escapeHtml(event.label)}</p>
          </article>`
      )
      .join("")}`;
}

function renderStory(): void {
  const state = engine.getState();
  const node = engine.getCurrentNode();
  const choices = engine.getAvailableChoices();

  $("#game").setAttribute("aria-busy", "false");
  $("#act-label").textContent = `${bundle.manifest.subtitle} · ${bundle.manifest.sampleTitle}`;
  $("#scene-progress").textContent = `${state.selectedChoices.length} / 7 次选择`;
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
  renderResources(state);
  renderCharacters(state);
  renderRecords(state);
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
  const save = JSON.parse(raw) as SaveFile;
  restoreSave(engine, save);
  savedCreatedAt = save.createdAt;
  showToast(`已读取${manual ? "手动存档" : "自动存档"} · ${save.eventLog.length} 条事件。`);
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
  showToast("已回到雨后的洛水渡口。");
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
      issues.length === 0 ? "内容校验通过 · 0 个断点" : `校验通过 · ${issues.length} 个提示`;
  } catch (error) {
    $("#fatal-error").toggleAttribute("hidden", false);
    $("#fatal-message").textContent = error instanceof Error ? error.message : String(error);
    $("#game").setAttribute("aria-busy", "false");
    throw error;
  }
}

void bootstrap();
