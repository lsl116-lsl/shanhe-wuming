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
完整人物和场景模型。
自行生成的正式首版美术。
自行生成的环境音、音效和原创程序配乐。
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
docs/production/PROLOGUE_GENERATED_ART_AUDIO_SPEC_V0.1.md
```

开始编码前必须按主制作规格列出的顺序阅读全部剧情、人物和玩法文档，并完整执行美术与音频自生成规格。

若本文件与普通代码习惯冲突，以以下优先级为准：

```text
根目录 AGENTS.md
→ docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md
→ docs/production/PROLOGUE_GENERATED_ART_AUDIO_SPEC_V0.1.md
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
美术与音频生成过程必须可重复执行。
```

必须保留：

```text
content/prologue/timeline.json
content/prologue/dialogue.zh-CN.json
content/prologue/asset_manifest.json
assets/generated_asset_manifest.json
assets/ASSET_PROVENANCE.md
```

## 4. 美术与音频责任

美术和音频也是当前任务的一部分，不等待用户补素材。

必须自行生成：

```text
主要人物分层模型。
群众差异化模型。
人物基础动画和专属动作。
清晨、午前、傍晚、旧库、雨夜分层场景。
UI、标题、互动提示和章节卡。
雾、雨、火、水、湿墨、灰尘和裂钟记忆特效。
河岸、渡口、棚下、旧库和雨夜环境音。
脚步、写字、米粒、木响、车翻等动作音效。
多层裂钟声音。
至少四段原创程序配乐。
```

生成规则：

```text
优先通过仓库内 Python、SVG、Godot 原生图形、粒子和 Shader 生成。
当前环境若有明确可用且授权清楚的生成工具，可以使用。
不得联网搜索或下载来源不明的图片、字体、音乐和音效。
不得照搬具体游戏、影视作品或在世艺术家的风格。
不得以素材不足为由停止开发。
```

以下不能作为最终运行资产：

```text
灰色方块。
纯色火柴人。
默认 Godot 图标。
只有名字标签的角色。
单一蜂鸣声。
名为 placeholder、dummy、temp 的资源。
```

首版生成资产可以以后升级，但当前必须达到从头到尾风格统一、人物可辨、场景完整、声音有层次的可玩标准。

## 5. 必须建立的生成工具

至少实现或等效实现：

```text
tools/generate_art_assets.py
tools/generate_character_assets.py
tools/generate_environment_assets.py
tools/generate_ui_assets.py
tools/generate_fx_assets.py
tools/generate_audio_assets.py
tools/generate_music_stems.py
tools/generate_ambience.py
tools/generate_sfx.py
tools/build_asset_manifest.py
tools/validate_generated_assets.py
tools/validate_audio_assets.py
```

工具必须：

```text
使用固定 seed。
可重复执行。
生成失败返回非零状态。
记录资产来源和生成脚本。
不依赖联网才能完成最低交付。
```

## 6. 开发行为

```text
先做可运行工程，再按里程碑完善首版正式生成资产。
不得长期保留灰块占位后宣称完成。
美术生成后要输出人物阵容图、动画接触表和场景色彩脚本。
音频生成后要输出 cue 清单和响度报告。
所有生成资产都必须进入清单并经过校验。
```

每完成一个里程碑：

```text
运行项目。
运行 headless 测试。
运行资产校验。
修复解析错误、缺失资源和场景加载错误。
更新 apps/godot/README.md。
```

## 7. 叙事红线

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

## 8. 完成前不得省略

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
美术生成脚本
音频生成脚本
生成资产清单
资产来源说明
人物阵容图
场景色彩脚本
音频 cue 清单
资产自动校验
```

完成定义以以下两个文件共同为准：

```text
docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md
docs/production/PROLOGUE_GENERATED_ART_AUDIO_SPEC_V0.1.md
```
