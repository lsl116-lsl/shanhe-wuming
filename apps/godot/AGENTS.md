# apps/godot/AGENTS.md

你正在实现《山河无名》序章《雨来之前》的 Godot 原生游戏版本。

## 1. 当前唯一目标

```text
完成一个 Windows PC 原生可玩的序章垂直切片。
```

它必须包含：

```text
动画化叙事。
2D 可移动轻探索。
人物和场景模型。
声音与配乐。
镜头与转场。
姓名输入。
裂钟记忆演出。
雨夜翻车现场三方向空间选择。
自动存档与继续游戏。
Windows 运行和导出脚本。
```

禁止改做网页、Electron、Vite、React 或 HTML 版本。

## 2. 最高执行规格

完整实现要求见：

```text
docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md
```

开始编码前必须按该文件列出的顺序阅读全部剧情、人物和玩法文档。

若本文件与普通代码习惯冲突，以以下优先级为准：

```text
根目录 AGENTS.md
→ docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md
→ 序章章节包文档
→ 本文件
→ 一般代码习惯
```

## 3. 技术约束

```text
引擎：Godot 4.x 稳定分支。
语言：GDScript。
渲染：2D Compatibility。
设计分辨率：1280×720。
目标平台：Windows PC。
内容与运行时分离。
剧情不得全部硬编码进单个脚本。
```

必须保留：

```text
content/prologue/timeline.json
content/prologue/dialogue.zh-CN.json
content/prologue/asset_manifest.json
```

## 4. 开发行为

```text
先做可运行工程，再逐步替换占位资源。
没有最终美术时，使用自制 SVG、Polygon2D、Sprite2D 或切片骨骼占位。
没有音频时，使用本地 Python 工具生成合法占位 WAV。
不得联网下载来源不明资源。
不得因素材不足停止开发。
```

每完成一个里程碑：

```text
运行项目。
运行 headless 测试。
修复解析错误、缺失资源和场景加载错误。
更新 apps/godot/README.md。
```

## 5. 叙事红线

```text
序章前 70% 以镜头、走位、环境、人物动作和轻探索为主。
不要频繁弹出选择框。
翻车现场才是第一次不可逆重大选择。
重大选择必须通过玩家在场景中走向目标并按住 E 确认。
禾安不是恋爱女主或圣母。
辛衡不是设定讲解机器。
韩宁不是单纯可怜人。
柳娘不是装饰 NPC。
裂钟不是技能。
宋亡不是地图变色。
```

核心玩法原则：

```text
移动负责让玩家看见。
互动负责让玩家承担。
```

## 6. 完成前不得省略

```text
run_game.bat
export_windows.bat
export_presets.cfg
README.md
暂停和设置
自动存档
继续游戏
三种序章选择
音频总线
中文字体回退
场景加载烟雾测试
```

完成定义以 `docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md` 的 Definition of Done 为准。
