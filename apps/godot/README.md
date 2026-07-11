# 《山河无名》Godot 原生序章

> P5 当前可玩样片：标题 → 序章完整流程 → 章节结束回顾 → 第一章标题 → 自动存档 → 继续游戏。剧情、对白、交互、路线回顾和资源引用继续保持 JSON 与运行时代码分离。

## P5 快速验收

```powershell
python tools/generate_art_assets.py --seed 286 --force
python tools/generate_audio_assets.py --seed 286 --force
python tools/build_asset_manifest.py --seed 286
python tools/validate_generated_assets.py
python tools/validate_audio_assets.py
& $env:GODOT_BIN --headless --path . --script res://tests/smoke_load_all_scenes.gd
& $env:GODOT_BIN --headless --path . -- --p5-e2e
```

Windows 导出：

```powershell
& $env:GODOT_BIN --headless --path . --export-release "Windows Desktop" "build/windows/ShanheWuming_P5.exe"
```

或执行：

```bat
export_windows.bat
```

P5 产物：

```text
build/windows/ShanheWuming_P5.exe
build/windows/ShanheWuming_P5.pck
art/reference/generated_p5_character_lineup.svg
art/reference/generated_p5_animation_action_sheet.svg
art/reference/generated_p5_scene_color_script.svg
art/reference/generated_p5_ui_board.svg
review/audio_loudness_report.md
review/audio_cue_list.md
```

## P6-A 视觉样片

P6-A 只重制序章开场的“旧渡清晨 + 主角 / 母亲 / 辛衡”视觉首屏，不新增 ACT，不改项目方向。

```powershell
python tools/generate_p6a_visual_assets.py --seed 286 --force
python tools/build_asset_manifest.py --seed 286
python tools/validate_generated_assets.py
& $env:GODOT_BIN --headless --editor --path . --quit
& $env:GODOT_BIN --path . --scene res://tests/scenes/P6AVisualCapture.tscn
```

截图命令需要正常渲染模式；headless 使用 dummy renderer，无法导出真实 viewport PNG。

P6-A 运行时资源：

```text
assets/environments/old_ferry/p6a/morning_far.svg
assets/environments/old_ferry/p6a/morning_mid.svg
assets/environments/old_ferry/p6a/morning_near.svg
assets/characters/player/p6a/*
assets/characters/mother/p6a/*
assets/characters/xinheng/p6a/*
assets/props/p6a/*
```

P6-A 审查参考：

```text
art/reference/generated_p6a_old_ferry_visual_sheet.svg
art/reference/generated_p6a_character_sheet.svg
review/p6a_sc01_home_morning.png
review/p6a_sc02_xinheng_desk.png
```

当前目录是序章《雨来之前》的 Godot 4.x Windows 原生工程。

当前里程碑：P4“雨夜翻车现场”。P0—P3 已通过内容全部保留；裂钟记忆结束后会黑场半秒，断轮、马嘶和车体砸泥声先到，硬切回旧渡雨夜。玩家先看见左侧车辕下孩子、中间泥水湿简、右侧失散人群，再通过移动靠近获取信息；只有按住 E 才锁定“先救孩子 / 先抢湿简 / 先让活人互认”。

## 技术基线

```text
Godot：4.7 stable（兼容 Godot 4.x 稳定分支）
语言：GDScript
渲染：2D Compatibility
设计分辨率：1280 × 720
目标平台：Windows PC
```

## 运行

安装 Godot 4.x 稳定版后，设置环境变量：

```bat
set GODOT_BIN=C:\Tools\Godot\Godot_v4.7-stable_win64.exe
```

然后双击或运行：

```bat
run_game.bat
```

也可直接执行：

```powershell
& $env:GODOT_BIN --path .
```

控制：

```text
A / D 或方向键：左右移动
W / S 或方向键：有限纵深移动
E：调查 / 对话
按住 E：在辛衡书案写名
按住 E：触碰旧礼器库中的裂钟
按住 E：在翻车现场锁定空间行动方向
Space / Enter：推进需要确认的字幕
```

## 生成 P0/P2/P3/P4/P6-A 资产

所有最低资产可离线生成，不依赖联网服务或外部媒体：

```powershell
python tools/generate_character_assets.py --seed 286 --force
python tools/generate_p3_character_assets.py --seed 286 --force
python tools/generate_environment_assets.py --seed 286 --force
python tools/generate_p3_art_assets.py --seed 286 --force
python tools/generate_p4_art_assets.py --seed 286 --force
python tools/generate_p6a_visual_assets.py --seed 286 --force
python tools/generate_ui_assets.py --seed 286 --force
python tools/generate_fx_assets.py --seed 286 --force
python tools/generate_ambience.py --seed 286 --force
python tools/generate_sfx.py --seed 286 --force
python tools/generate_music_stems.py --seed 286 --force
python tools/generate_p3_audio_assets.py --seed 286 --force
python tools/generate_p4_audio_assets.py --seed 286 --force
python tools/build_asset_manifest.py
python tools/validate_generated_assets.py
python tools/validate_audio_assets.py
```

汇总入口：

```powershell
python tools/generate_art_assets.py --seed 286 --force
python tools/generate_audio_assets.py --seed 286 --force
```

生成资产均登记在：

```text
assets/generated_asset_manifest.json
assets/ASSET_PROVENANCE.md
content/prologue/asset_manifest.json
```

## 测试

先让 Godot 导入 SVG 和 WAV：

```powershell
& $env:GODOT_BIN --headless --editor --path . --quit
```

再运行场景烟雾测试：

```powershell
& $env:GODOT_BIN --headless --path . --script tests/smoke_load_all_scenes.gd
& $env:GODOT_BIN --headless --path . --script tests/test_player_movement.gd
```

P1 存档与完整叙事流程：

```powershell
& $env:GODOT_BIN --headless --path . res://tests/scenes/SaveManagerTest.tscn -- --p1-save-test
& $env:GODOT_BIN --headless --path . res://tests/scenes/P1NarrativeInfrastructureTest.tscn -- --p1-test
```

P1 自动化流程由以下 JSON 驱动：

```text
tests/fixtures/p1_timeline.json
tests/fixtures/p1_dialogue.zh-CN.json
tests/fixtures/p1_asset_manifest.json
```

验证顺序：

```text
镜头移动
→ 人物入场
→ 动画播放
→ 对话
→ 玩家获得控制
→ 互动
→ 状态写入
→ 存档
→ 转场
→ 场景切换
```

P2 从标题界面到“宋地乱了”的端到端测试：

```powershell
& $env:GODOT_BIN --headless --path . -- --p2-e2e
```

该测试实际验证：

```text
标题新游戏
→ 清晨镜头与母亲动作
→ 半袋粟米 / 父亲旧笔盒 / 河道 / 母亲调查
→ 场景切换
→ 按住 E 1.2 秒
→ 中文姓名输入与存档
→ 写名异常
→ 禾安抱柴、放粥
→ 东来商船靠岸
→ “宋地乱了”
→ 船主 / 禾安 / 辛衡 / 旧渡人四组空间碎片
```

P3 从第一批流民入场到裂钟记忆结束的端到端测试：

```powershell
& $env:GODOT_BIN --headless --path . -- --p3-e2e
```

该测试实际验证：

```text
第一批宋地流民入场
→ 韩宁按袖 / 母亲挡问 / 辛衡停笔 / 柳娘停曲 / 临时名册
→ 禾安倒最后碎米
→ 傍晚转夜与雨意增强
→ 空间钟声引导玩家进入旧礼器库
→ 断足鼎 / 裂边簋 / 残磬 / 裂钟
→ 按住 E 1.5 秒
→ 27 秒裂钟记忆与多层声音
→ “这不是你第一次看见山河改色”
→ 存档检查点 `cracked_bell_memory`
```

P4 从裂钟记忆硬切到翻车现场，并分别验证三条路线：

```powershell
& $env:GODOT_BIN --headless --path . -- --p4-e2e
```

该测试实际验证：

```text
裂钟记忆结束
→ 黑场半秒
→ 断轮 / 马嘶 / 车体砸泥声音先到
→ 硬切雨夜翻车现场
→ 左侧孩子 / 中间湿简 / 右侧失散人群现场扫描
→ 靠近方向只显示信息，不写入 first_priority
→ 按住 E 锁定行动
→ rescue_child / save_records / mutual_recognition 三路线即时反馈
→ prologue.first_priority、choice_elapsed_seconds、saw_*_cost 写入自动存档
```

验证主场景实际启动：

```powershell
& $env:GODOT_BIN --headless --path . --quit-after 5
```

## Windows 导出

先在 Godot 中安装与引擎版本匹配的 Export Templates，然后执行：

```bat
export_windows.bat
```

输出约定：

```text
build/windows/ShanheWuming_P3.exe
build/windows/ShanheWuming_P3.pck
```

P3 使用 Godot 标准的 EXE + 外置 PCK 分发，两者必须放在同一目录；制作参考图、验收截图和生成工具不进入运行包。

如果缺少导出模板，脚本会保留错误信息并说明原因。

## 中文字体

工程使用 `SystemFont` 依次尝试：

```text
Microsoft YaHei
Noto Sans CJK SC
Source Han Sans SC
SimSun
sans-serif
```

系统缺少某一种字体不会导致游戏启动失败。仓库不提交来源不明或受限的商业字体文件。

## P4 新增生成资产

```text
场景：雨夜翻车现场远中近景、重雨层、积水反光与三方向暖火引导。
物件：翻倒木车、车辕下孩子、泥水湿简、失散人群、马影、热水桶、湿墨扩散。
动作：主角抬车、跪捞湿简、组织互认；禾安拖桶并顶车；韩宁扑简挣扎并跪捞；柳娘抱孩子并喊名。
声音：120 秒雨夜环境，翻车压力配乐，断轮、砸泥、马嘶、拖桶、湿简入水、湿墨扩散、孩子哭声、人群喊名。
交互：ChoicePressureController 只负责空间预览、耗时和锁定；剧情、提示与反馈仍由 JSON 驱动。
```

## P3 保留生成资产

```text
人物：韩宁、韩宁母亲、柳娘、流民老者、抱病儿妇人、背湿粮汉子均为分层 SVG，并拥有区别动作。
场景：流民棚傍晚与夜景各含远中近景；旧礼器库含暗木空间、断足鼎、裂边簋、残磬与裂钟。
特效：双层雨幕与六段克制的裂钟记忆画面，配色限定为黑、水灰、火色、铜绿和褪红。
环境音：90 秒流民棚雨声与 90 秒礼器库漏雨室内声。
动作音：旧曲哼唱、碎米、灶火和裂钟本体/裂口/水下/倒尾四层声音。
音乐：流民棚傍晚与裂钟记忆两段原创程序配乐；裂钟最终混音长度为 27 秒。
```

## P2 保留生成资产

```text
人物：主角、母亲、辛衡、禾安、船主和两种旧渡群众均使用分层 SVG；人物拥有不同持有物、轮廓和专属动作。
场景：清晨与午前分别拥有远景、中景、近景、水面、雾层；包含木船、木缆、商船、书案、粟米袋和旧笔盒。
UI：标题、字幕、互动进度、姓名输入与当前目标使用统一纸木视觉。
特效：河雾、水面缓动与写名水冷记忆遮罩。
环境音：90 秒河岸清晨与 90 秒午前渡口立体声环境。
动作音：木缆、船体、写字、提笔、木盆水声、柴落地、粥碗、商船靠岸等多组变体。
音乐：旧渡清晨、名与籍、宋亡消息三段原创程序配乐。
```

以上均是首版生成资产，不使用默认 Godot 图标、灰色方块、纯色火柴人或网络下载素材。

运行时审查图：

```text
review/p2_sc_01_home_morning.png
review/p2_sc_02_xinheng_desk.png
review/p2_sc_03_ferry_day.png
review/p3_sc04_refugees_arrived.png
review/p3_sc04_night_bell_lure.png
review/p3_sc05_ritual_storehouse.png
review/p3_sc05_cracked_bell_memory.png
review/p3_sc05_memory_line.png
art/reference/generated_p4_crash_scene.svg
```

`art/reference/*_ai_reference.png` 是使用内置图像生成工具制作的风格参考；游戏运行时不依赖这些参考图。实际运行资产由仓库内固定 seed 的 SVG / WAV 生成器重建。
