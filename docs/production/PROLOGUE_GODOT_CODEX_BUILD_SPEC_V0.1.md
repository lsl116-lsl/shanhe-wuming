# 《山河无名》序章 Godot 垂直切片 Codex 制作规格 V0.1

> 用途：交给 Codex 直接执行。  
> 目标平台：Windows PC 原生游戏。  
> 禁止方向：网页、Vite、React、HTML、Electron 套壳。  
> 引擎：Godot 4.x 稳定分支。  
> 语言：GDScript。  
> 渲染：2D，Compatibility 路径优先。  
> 目标内容：序章《雨来之前》完整可玩原型。  
> 目标时长：首次游玩约 15—22 分钟。  
> 核心体验：动画化叙事 + 轻探索 + 一次真正不可逆的关键选择。

---

## 0. Codex 必须先执行的阅读顺序

开始写代码前，完整阅读：

```text
README.md
AGENTS.md
docs/00_项目总框架_V0.5.md
docs/08_项目落地方案_V0.1.md
docs/13_人物塑造规则_V0.1.md
docs/14_可移动探索与眼前代价系统_V0.1.md
docs/chapters/PROLOGUE_雨来之前/README.md
docs/chapters/PROLOGUE_雨来之前/00_序章定位与边界_V0.1.md
docs/chapters/PROLOGUE_雨来之前/01_主线大纲_V0.1.md
docs/chapters/PROLOGUE_雨来之前/02_人物关系表_V0.1.md
docs/chapters/PROLOGUE_雨来之前/03_因果与伏笔表_V0.1.md
docs/chapters/PROLOGUE_雨来之前/04_记忆碎片表_V0.1.md
docs/chapters/PROLOGUE_雨来之前/05_故事剧本_V0.1.md
docs/chapters/PROLOGUE_雨来之前/06_至ACT01_雨后流民_过渡文_V0.1.md
docs/chapters/PROLOGUE_雨来之前/07_动画化叙事与轻交互规格_V0.1.md
docs/chapters/PROLOGUE_雨来之前/08_人物星座原型与视觉参考_V0.1.md
assets/reference/characters/prologue_character_sheet_v0_1.svg
```

不得只读本文件后凭想象改写剧情。

---

## 1. 最终交付物

Codex 完成后，仓库内必须出现一个能独立运行的 Godot 工程：

```text
apps/godot/
```

最终必须交付：

```text
1. 可在 Godot 编辑器中直接打开的 project.godot。
2. 可从头到尾游玩的序章《雨来之前》。
3. Windows 原生导出配置 export_presets.cfg。
4. 一键运行脚本 run_game.bat。
5. 一键导出脚本 export_windows.bat。
6. 至少一个 Windows 可执行构建输出目录约定：build/windows/。
7. 中文界面、中文字幕、音量和文本速度设置。
8. 自动存档、继续游戏、重新开始序章。
9. 所有核心场景、人物、音频均有可运行占位资源。
10. README，写清安装 Godot、运行、导出、替换资源的方法。
```

禁止只提交设计文档、伪代码、静态图片或网页演示。

---

## 2. 原型边界

### 2.1 本次必须做

```text
标题界面。
序章完整剧情流程。
可控制移动的 2D 主角。
场景镜头和转场。
主要人物出场与专属动作。
环境动画。
环境音、动作音、裂钟音、简约配乐。
对话字幕。
调查与互动。
玩家姓名输入。
裂钟记忆动画。
翻车现场三方向空间选择。
选择结果记录与自动存档。
结尾衔接第一章标题。
```

### 2.2 本次不要做

```text
战斗系统。
装备系统。
技能树。
开放世界地图。
复杂背包。
完整第一章。
联网功能。
账号系统。
成就系统。
多人模式。
全角色真人配音。
3D 建模与 3D 场景。
```

本次“人物模型、场景模型”指：

```text
2D 人物切片模型 / 骨骼模型 / 精灵模型。
2D 分层场景模型 / 可碰撞场景资产 / 前中后景层。
```

不改成 3D 游戏。

---

## 3. 视觉实现方案

### 3.1 总体风格

采用：

```text
国风手绘剪影 + 低帧角色动画 + 分层横向场景 + 水墨雾雨特效。
```

画面不是写实 3D，也不是纯像素风。

参考方向：

```text
旧木、湿泥、灰青河雾、暗黄火光、褪色布衣。
冷色环境与暖色灶火形成对比。
人物轮廓清楚，面部细节适度简化。
镜头有电影感，但不频繁晃动。
```

### 3.2 视角与移动

使用：

```text
2D 侧视横向场景。
局部允许轻微纵深移动，角色在一条有限 Y 轴活动带内移动。
场景像舞台，但玩家可以实际走动、靠近人物和物件。
```

玩家控制：

```text
A / D 或左右方向键：左右移动。
W / S 或上下方向键：局部纵深移动。
E：互动 / 按住写字 / 确认行动。
Space / Enter：推进对话。
Esc：暂停。
鼠标：可用于菜单、设置和名字输入，不作为主要移动方式。
```

### 3.3 基础分辨率

```text
设计分辨率：1280 × 720。
窗口比例：16:9。
默认窗口模式运行。
支持无边框全屏。
采用 viewport 拉伸，保持宽高比。
```

---

## 4. 场景清单

本次序章至少需要以下场景：

```text
SC00_Title                 标题界面
SC01_Home_Morning          旧渡清晨、主角家与河岸
SC02_Xinheng_Desk          辛衡书案、写下姓名
SC03_Ferry_Day             午前渡口、宋亡消息
SC04_Refugee_Shelter       傍晚流民抵达、韩宁与柳娘、灶火
SC05_Ritual_Storehouse     夜间旧礼器库、裂钟
SC06_Cart_Crash_Rain       雨夜翻车现场、三方向选择
SC07_Prologue_End          结果短演出、第一章标题
```

允许 SC01—SC04 共用一个旧渡大场景，通过时间、天气、人物布置和镜头区域切换实现；但代码和剧情节点必须清楚分段。

---

## 5. 序章完整演出时间线

### 5.1 SC00 标题界面

画面：

```text
黑场。
先听见河水和木缆轻响。
雾中慢慢显出旧渡轮廓。
标题《山河无名》淡入。
副标题：序章《雨来之前》。
```

菜单：

```text
新游戏
继续游戏
设置
退出
```

新游戏后先短黑场，再进入河雾镜头。

### 5.2 SC01 洛水旧渡的早晨

目标：让玩家先相信这里是家。

自动镜头：

```text
河雾 → 木船 → 木缆 → 主角家门口 → 母亲洗木盆。
```

母亲专属动作：

```text
数米。
数柴。
数布。
听到船声后抬头看河道尽头。
继续低头做事，不说“等”。
```

玩家获得控制权后可调查：

```text
半袋粟米。
父亲旧笔盒。
门外河道尽头。
母亲。
```

调查不是选项框，使用场景内移动和 E 互动。

父亲不出现，只通过：

```text
旧笔盒。
未兑现的新笔承诺。
母亲望河。
```

建立存在感。

### 5.3 SC02 写下本世姓名

辛衡把湿木牍推给主角。

先播放一句：

```text
“写你的名字。”
```

交互分两步：

```text
1. 玩家靠近书案，按住 E，触发笔尖落下动画。
2. 弹出简洁中文姓名输入框，允许 1—8 个 Unicode 字符。
```

规则：

```text
不得强制使用固定姓名。
开发模式可预填“无名”，正式输入为空时不能继续。
姓名写入 SaveState.player_name。
后续字幕可用 {player_name} 替换。
```

写名时的短暂异常：

```text
笔尖停顿。
画面暗半秒。
更长的案。
更暗的灯。
更冷的水声。
一只陌生手按住名册。
立即回到现实。
```

不要解释苏醒机制，也不要把残梦做成寻找真名或前世身份的线索。

禾安进入：

```text
抱柴快步进来。
说早饭要冷了。
把粥放到案边。
嘴上说是主角母亲让端的。
```

不得出现恋爱选项。

### 5.4 SC03 宋亡消息到来

东来商船靠岸。

声音先到：

```text
船主远处喊：“宋地乱了！”
```

人物动作：

```text
旧渡人停下手里的活。
辛衡推开木牍。
禾安立即跑去数水瓮和米袋。
母亲下意识看向船。
```

玩家获得控制权，可走向不同人，听见碎片：

```text
船主：宋地乱了，关验换了。
旧渡人：宋也亡了。
禾安：二十三户？水要烧到后半夜。
辛衡：他们不肯说旧里？
```

不得弹出“你想先问谁”的菜单。

### 5.5 SC04 流民、韩宁、柳娘与碎米

第一批宋地流民进入场景。

必须有：

```text
老人被扶着。
妇人抱发热孩子。
男人背湿粟。
韩宁按住袖口。
韩宁母亲挡在他身前。
柳娘带戏箱，发簪仍端正。
```

轻探索点：

```text
靠近韩宁：看见他按袖口。
靠近韩宁母亲：她阻止追问旧里。
靠近辛衡：看见笔尖停下。
靠近柳娘：旧曲唱到地名处停住。
查看临时名册：旧邑、旧里、父名等被留空。
```

这一段不得让玩家决定是否逼问韩宁。

随后进入碎米演出：

```text
禾安倒空米袋。
袋底只落一点碎米。
她停一下，看主角。
说：“别看我。就这么多。”
她仍把碎米倒进锅里。
```

这是禾安自己的选择，玩家不能替她决定。

时间从傍晚渐入夜，雨声逐渐增强。

### 5.6 SC05 裂钟

先用空间声音吸引玩家：

```text
一道很远又很近的钟声。
声源方向来自旧礼器库。
```

禾安在身后喊：

```text
“你去哪？”
```

玩家控制主角走向旧礼器库。

进入后：

```text
光线明显变暗。
灰尘粒子。
断足鼎、裂边簋、残磬。
角落有裂钟。
```

靠近裂钟显示：

```text
【按住 E】触碰
```

触碰后锁定控制，进入 20—35 秒记忆演出：

```text
水纹遮罩铺满画面。
旧渡环境音抽离。
低频钟声进入。
城门火光。
烟黑旗帜。
断裂礼器。
竹简上的名字被刮去。
湿手按住名册。
裂钟沉入无尽水面。
字幕：“这不是你第一次看见山河改色。”
```

视觉要求：

```text
不要做成炫技超能力动画。
不要用现代科幻 HUD。
不要大面积霓虹色。
使用黑、水、火、铜锈和褪色红。
```

### 5.7 SC06 最后一辆车

记忆结束后，先黑场 0.5 秒。

突然播放：

```text
木轮断裂。
马嘶。
人群惊喊：“车翻了！”
```

硬切回旧渡，轻微镜头震动。

玩家冲出旧礼器库，雨已落下。

先播放不可操作的 5—8 秒现场扫描：

```text
左侧：车辕下的孩子。
中间：泥水中的湿简。
右侧：棚下互相寻找亲人的人群。
禾安拖热水桶跑向孩子。
韩宁扑向湿简又被拉住。
柳娘抱着孩子喊人互认。
辛衡把空木牍塞给主角。
```

辛衡台词：

```text
“先看眼前的人。”
```

随后玩家获得控制权。

### 5.8 三方向空间选择

这不是 A/B/C 菜单。

场景空间布局：

```text
左：车下孩子。
中：湿简。
右：失散人群。
```

玩家走近后才显示具体互动。

#### 左侧：救孩子

视觉：

```text
车辕压住孩子。
孩子哭声越来越轻。
禾安用肩顶住木梁。
```

声音 / 台词：

```text
禾安：“搭把手！车辕还压着他！”
```

交互：

```text
【按住 E】抬车救孩子
```

眼前代价提示：

```text
雨水仍在冲刷湿简。
棚下仍有人喊错名字。
```

#### 中间：抢救湿简

视觉：

```text
墨迹在水中散开。
韩宁挣扎着要扑过去。
```

声音 / 台词：

```text
韩宁：“别踩！那不是废木头！”
```

交互：

```text
【按住 E】抢救湿简
```

眼前代价提示：

```text
车下孩子的哭声断了一下。
人群仍未完成互认。
```

#### 右侧：让活人互认

视觉：

```text
抱错孩子的人。
互相喊名字的人。
惊慌的老人。
```

声音 / 台词：

```text
柳娘：“谁家少了人？先喊名字！”
```

交互：

```text
【按住 E】组织互认
```

眼前代价提示：

```text
雨水还在泡湿简。
车下孩子仍被压着。
```

### 5.9 时间压力

规则：

```text
前 3 秒：只展示，不计后果。
第 4—10 秒：环境变化，但不给隐藏惩罚。
第 10 秒后：孩子哭声减弱、墨迹扩散、人群错认增加。
玩家靠近任一方向只显示信息，不锁定选择。
只有按住 E 完成互动才锁定。
```

不得因为玩家不熟悉按键，在几秒内直接判失败。

### 5.10 选择后的即时反馈

不在序章中宣布“好结局 / 坏结局”。

三个行动最终都会由其他 NPC 继续处理，但先后不同，现场代价不同。

#### 选择救孩子

```text
孩子的呼吸稳定下来。
禾安继续照看伤者。
部分湿简墨迹已经散开。
棚下仍有人一时没有找到亲属。
```

#### 选择抢救湿简

```text
主角和韩宁捞起更多木简。
部分名字得以辨认。
禾安和其他人稍后抬起车辕，孩子伤得更重但仍活着。
棚下仍有短暂错认。
```

#### 选择组织互认

```text
失散者先按家庭和同行关系站到一起。
柳娘开始逐个喊名。
孩子稍后被救出，伤势更重。
更多湿简字迹无法辨认。
```

这些是原型即时反馈，不得在这里提前写死第一章全部长期后果。

写入状态：

```text
prologue.first_priority = rescue_child | save_records | mutual_recognition
prologue.choice_elapsed_seconds
prologue.saw_child_cost
prologue.saw_record_cost
prologue.saw_recognition_cost
```

### 5.11 SC07 序章结束

短演出：

```text
雨落在空木牍上。
主角掌心有青铜锈。
镜头扫过孩子、湿简和互认的人群。
裂钟声极远地回响一次。
```

字幕：

```text
这一世，真正开始了。
```

淡出后显示：

```text
第一章
钟裂于洛水
```

本原型到此结束，提供：

```text
返回标题
重新体验序章
查看本次选择
```

---

## 6. 人物模型与动画最低要求

### 6.1 主角

至少需要：

```text
idle
walk
look_up
write
hold_tablet
reach_bell
shock
push_lift
kneel_pickup
organize_crowd
```

动作气质：

```text
慢半拍。
先看两边。
决定后动作明确。
```

### 6.2 禾安

至少需要：

```text
idle_busy
walk_fast
carry_firewood
place_porridge
count_jars
pour_rice
stoke_fire
drag_bucket
brace_cart
call_player
```

动作气质：

```text
重心向前。
先动起来。
嘴上快，手更快。
```

### 6.3 辛衡

至少需要：

```text
idle_seated
write
pause_pen
look_over_tablet
hand_tablet
```

动作气质：

```text
动作少。
停笔比挥手更重要。
```

### 6.4 韩宁

至少需要：

```text
idle_guarded
press_sleeve
step_back
stare
rush_records
struggle
kneel_records
```

### 6.5 韩宁母亲

至少需要：

```text
idle_tired
hold_child_hand
block_question
shield_hanning
```

### 6.6 柳娘

至少需要：

```text
idle_composed
carry_trunk
sing
song_pause
hold_child
call_names
```

### 6.7 主角母亲

至少需要：

```text
wash_basin
count_grain
count_wood
look_river
resume_work
```

### 6.8 群众与流民

可复用基础模型，但至少提供：

```text
3 种成年轮廓。
2 种老人轮廓。
2 种儿童轮廓。
湿衣、背袋、扶人、抱孩子等差异附件。
```

不得所有 NPC 使用完全相同的站立动画。

---

## 7. 场景模型与特效最低要求

### 7.1 旧渡

分层：

```text
远景：河、对岸、雾。
中景：船、木桩、屋舍、祠堂、灶棚。
近景：泥地、芦苇、木盆、柴堆、粮袋。
前景：偶尔掠过的芦苇、屋檐滴水、雾层。
```

动画：

```text
水面缓动。
木船轻晃。
木缆偶尔拉紧。
雾层缓慢横移。
灶火跳动。
烟向上飘。
```

### 7.2 旧礼器库

需要：

```text
歪门。
破瓦漏光。
灰尘粒子。
断足鼎。
裂边簋。
残磬。
裂钟。
```

### 7.3 雨夜翻车现场

需要：

```text
翻倒车体。
陷泥车轮。
受惊马匹或可替代的马影动画。
积水反光。
湿简漂动。
火把在雨中抖动。
雨粒与地面溅水。
```

### 7.4 特效

必须有：

```text
雾。
细雨 → 稳定雨势。
灶火和火把。
水面涟漪。
湿墨扩散。
低强度镜头震动。
裂钟记忆水纹遮罩。
淡入、淡出、交叉溶解、硬切。
```

---

## 8. 音频设计

本次原型必须有声音，不允许全程静音配字幕。

### 8.1 环境音层

```text
audio/ambience/river_morning.wav
audio/ambience/ferry_day.wav
audio/ambience/shelter_evening.wav
audio/ambience/rain_night.wav
audio/ambience/storehouse_roomtone.wav
```

### 8.2 动作音

```text
木缆绷响。
船身木响。
木盆和水。
笔在木牍上的摩擦。
柴枝落地。
米粒落锅。
灶火噼啪。
脚踩湿泥。
雨打屋檐。
车轮断裂。
车体砸泥。
马嘶。
湿简落水。
人群喊名。
```

### 8.3 裂钟声音

至少三层：

```text
真实青铜钟低频主体。
水下闷响层。
极轻的反向尾音或空气抽离层。
```

裂钟音不得像技能释放音效。

### 8.4 配乐

至少三段可循环音乐：

```text
旧渡主题：安静、五声音阶、少量拨弦和木质敲击。
宋亡与流民：低音持续音、极少旋律、不煽情。
裂钟记忆：低频、稀疏、带水下空间感。
```

翻车现场以环境和节奏性低鼓为主，避免热血战斗音乐。

### 8.5 音频资源策略

Codex 不得联网抓取不明版权素材。

优先顺序：

```text
1. 仓库已有合法资源。
2. 本地程序合成的占位 WAV。
3. 自制简单采样 / CC0 资源由用户后续替换。
```

若仓库没有音频，Codex 必须创建：

```text
tools/generate_placeholder_audio.py
```

用 Python 生成可运行的占位 WAV，包括：

```text
河水噪声。
雨声。
火焰噪声。
木响。
低频钟声。
简单五声音阶拨弦循环。
```

占位资源必须可被统一替换，不得把音频生成逻辑散落在剧情代码中。

不要求首版真人配音。必须保留角色语音资源槽位和音量总线。

---

## 9. 技术架构

### 9.1 推荐目录

```text
apps/godot/
├── project.godot
├── export_presets.cfg
├── AGENTS.md
├── README.md
├── run_game.bat
├── export_windows.bat
├── assets/
│   ├── characters/
│   ├── environments/
│   ├── props/
│   ├── fx/
│   ├── ui/
│   ├── audio/
│   └── manifests/
├── content/
│   └── prologue/
│       ├── timeline.json
│       ├── dialogue.zh-CN.json
│       ├── interactables.json
│       └── asset_manifest.json
├── scenes/
│   ├── core/
│   ├── ui/
│   ├── characters/
│   └── prologue/
├── scripts/
│   ├── autoload/
│   ├── core/
│   ├── player/
│   ├── narrative/
│   ├── interaction/
│   ├── audio/
│   └── prologue/
├── tests/
└── tools/
```

### 9.2 Autoload

至少：

```text
GameState.gd
SaveManager.gd
SceneRouter.gd
AudioDirector.gd
SettingsManager.gd
```

### 9.3 核心节点

```text
PrologueDirector
PlayerController2D
CameraDirector
DialogueLayer
InteractionPrompt
InteractableArea2D
TimelineRunner
TransitionLayer
ChoicePressureController
CharacterActor2D
AmbientZone2D
```

### 9.4 内容与运行时分离

剧情对白、事件顺序、角色资源、互动提示不得全部写死在单个 `.gd` 文件中。

至少使用：

```text
content/prologue/timeline.json
content/prologue/dialogue.zh-CN.json
content/prologue/asset_manifest.json
```

`TimelineRunner` 需要支持：

```text
camera_move
camera_focus
character_enter
character_exit
character_move
animation_play
dialogue
wait
player_control
interaction_enable
interaction_disable
audio_play
audio_stop
music_crossfade
weather_set
transition
state_set
state_check
scene_change
choice_pressure_start
choice_pressure_end
save_checkpoint
```

不要求开发通用商业叙事引擎，但必须避免把全部流程塞进一个超长脚本。

### 9.5 存档

存档路径：

```text
user://save_0.json
```

至少保存：

```text
save_version
current_scene
current_timeline_event
player_name
prologue_flags
first_priority
settings
playtime
```

检查点：

```text
写完姓名后。
宋亡消息后。
进入旧礼器库前。
翻车选择后。
序章结束。
```

继续游戏应从最近检查点恢复，而不是永远从头开始。

---

## 10. UI 与字幕

### 10.1 对话

```text
底部半透明字幕框。
人物名在左上。
正文支持中文自动换行。
重要旁白可使用无人物名样式。
支持快进单句，但不能默认跳过镜头。
```

### 10.2 互动提示

```text
靠近后出现。
离开后消失。
不要常驻大图标。
按住 E 的交互要有环形或横向进度反馈。
```

### 10.3 设置

至少包含：

```text
主音量。
音乐音量。
环境 / 音效音量。
字幕速度。
窗口 / 全屏。
镜头震动开关。
```

### 10.4 字体

必须保证中文显示正常。

不得把字体文件提交为来源不明的商业字体。

若仓库无可用中文字体：

```text
README 中要求用户放入合法中文字体，或使用系统字体回退。
开发环境必须有清晰的字体缺失提示。
```

不得因字体缺失导致游戏启动崩溃。

---

## 11. 资源占位策略

Codex 不应因为缺最终美术而停止。

必须做到：

```text
没有成品角色时，用分层 SVG / Polygon2D / Sprite2D 占位模型。
没有成品背景时，用分层 SVG 场景和简单纹理占位。
没有逐帧动画时，用骨骼 / 节点补间 + 少量关键姿势实现。
没有音乐时，生成合法的程序占位音频。
```

占位资源也要遵守人物区别：

```text
主角轮廓安静、偏瘦。
禾安重心向前、袖口卷起。
辛衡坐姿和停笔明显。
韩宁始终护袖口。
柳娘发簪和戏箱明确。
母亲有望河动作。
```

所有资源通过 `asset_manifest.json` 引用，后续替换文件不应改剧情代码。

---

## 12. 转场规则

必须实现以下转场：

```text
黑场淡入：游戏开始。
河雾交叉溶解：清晨建立。
笔尖匹配切：写名异常。
时间渐变：午前 → 傍晚 → 夜。
环境音交叉淡化：渡口 → 棚下 → 旧库。
水纹吞没：裂钟记忆。
声音先行硬切：车翻事故。
雨中慢淡出：序章结束。
```

禁止每段剧情都使用同一种黑场淡入淡出。

---

## 13. 镜头规则

```text
玩家自由移动时，镜头平滑跟随，不应过度滞后。
剧情演出时，CameraDirector 暂时接管镜头。
演出结束后平滑归还控制。
镜头不得频繁大幅缩放。
翻车现场允许一次轻微震动。
裂钟记忆使用缓慢推进和漂移，不使用快速炫目剪辑。
```

需要提供镜头震动关闭选项。

---

## 14. 状态字段

最低状态结构：

```json
{
  "player": {
    "name": "",
    "can_move": true
  },
  "prologue": {
    "inspected_grain": false,
    "inspected_pen_box": false,
    "looked_downriver": false,
    "heard_song_pause": false,
    "inspected_hanning_tablet": false,
    "touched_cracked_bell": false,
    "first_priority": "",
    "choice_elapsed_seconds": 0.0,
    "completed": false
  }
}
```

长期后果只记录接口，不在本次擅自扩写第一章。

---

## 15. 实施顺序

Codex 必须按以下里程碑推进，不能一开始就堆全部资源。

### P0 工程可启动

```text
创建 Godot 工程。
标题界面。
中文显示。
主角可移动。
一个占位场景。
基础音频总线。
run_game.bat。
```

验收：点击新游戏后进入场景，角色能移动和互动。

### P1 叙事基础设施

```text
TimelineRunner。
DialogueLayer。
CameraDirector。
TransitionLayer。
GameState / SaveManager。
```

验收：可以通过 JSON 播放一段镜头、走位、对白和场景切换。

### P2 清晨到宋亡

```text
SC01—SC03。
姓名输入。
母亲、辛衡、禾安动作。
东来商船与轻探索。
```

验收：从新游戏玩到“宋地乱了”，无断链。

### P3 流民与裂钟

```text
SC04—SC05。
韩宁、韩宁母亲、柳娘。
旧曲停顿。
碎米演出。
夜雨和裂钟记忆。
```

验收：触碰裂钟后完整播放记忆动画并返回现实。

### P4 翻车现场

```text
SC06。
三方向压力。
按住 E 锁定行动。
即时反馈。
选择存档。
```

验收：三种选择均可完成，状态正确写入存档。

### P5 完整打磨与导出

```text
音量设置。
暂停菜单。
继续游戏。
自动存档。
Windows 导出。
README。
自动烟雾测试。
```

验收：干净环境按 README 操作可启动和导出。

---

## 16. 测试要求

不得只依靠手工试玩。

至少提供：

```text
tests/test_timeline_runner.gd
tests/test_save_manager.gd
tests/test_prologue_choice_state.gd
tests/smoke_load_all_scenes.gd
```

无需引入外部测试插件也可使用 Godot headless 脚本。

最低测试：

```text
所有 .tscn 可加载。
所有 JSON 可解析。
所有对白 ID 可找到。
所有 asset_manifest 路径存在或有 fallback。
三个选择均能写入正确状态。
存档可以保存并恢复玩家姓名和序章进度。
缺失可选音频时不崩溃。
```

README 中给出 headless 测试命令。

---

## 17. Windows 脚本要求

### run_game.bat

功能：

```text
查找 GODOT_BIN 环境变量。
若存在则运行 apps/godot/project.godot。
若不存在，尝试常见 Godot 安装路径。
仍找不到时保留窗口并显示中文错误，不允许一闪而过。
```

### export_windows.bat

功能：

```text
检查 Godot。
检查导出模板。
创建 build/windows。
导出 Windows 可执行文件。
失败时保留窗口并打印原因。
```

脚本必须使用：

```bat
@echo off
setlocal
...
pause
```

不得出现报错后窗口一闪而过。

---

## 18. 质量红线

Codex 不得：

```text
把序章做成连续对话框和选择题。
把人物钉在原地只播放文字。
把禾安做成恋爱女主或圣母。
把辛衡做成不停讲设定的 NPC。
把韩宁做成只负责可怜的工具人。
把柳娘做成背景装饰。
把裂钟做成主角技能。
把宋亡做成一张地图变色图片。
把最终美术缺失当作无法开发的理由。
把剧情全部硬编码进一个脚本。
联网下载来源不明的图片、字体和音乐。
生成网页版、Electron 版或浏览器启动器。
```

---

## 19. 完成定义 Definition of Done

只有同时满足以下条件，任务才算完成：

```text
[ ] Windows 上通过 Godot 原生运行，不依赖浏览器。
[ ] 玩家从标题界面开始，能完整玩到第一章标题。
[ ] 主角能在多个场景实际移动和调查。
[ ] 姓名输入能保存并在字幕中使用。
[ ] 六名主要人物至少各有一个专属动作。
[ ] 清晨、白日、傍晚、夜雨有明显环境变化。
[ ] 裂钟有完整声音和动画转场。
[ ] 翻车现场不是 A/B/C 菜单，而是空间移动选择。
[ ] 三个行动方向均展示眼前代价。
[ ] 三种选择均有即时反馈和状态记录。
[ ] 环境音、动作音、裂钟音和简约音乐均存在。
[ ] 暂停、设置、自动存档、继续游戏可用。
[ ] 所有场景可通过自动烟雾测试加载。
[ ] run_game.bat 不闪退。
[ ] export_windows.bat 能生成或明确说明缺少导出模板。
[ ] README 足以让不了解项目的人运行。
```

---

## 20. Codex 执行方式

Codex 接到本任务后：

```text
1. 先检查仓库现状，不删除网页原型。
2. 新建 apps/godot，保持与 apps/web 并存。
3. 建立 P0 后先运行测试和截图验证场景。
4. 逐里程碑实现，每个里程碑结束都运行工程。
5. 缺资源时立即制作可替换占位资源，不暂停等待。
6. 不擅自改剧情核心，不补写尚未确定的第一章长期后果。
7. 遇到普通技术选择自行做合理决定，并在 README 记录。
8. 只有涉及剧情冲突、授权资源或不可逆架构改变时才向用户提问。
```

Codex 最终回复必须包含：

```text
完成了什么。
如何运行。
如何导出 Windows。
测试结果。
哪些资源是占位资源。
下一步最值得替换的三类资源。
```

---

## 21. 直接给 Codex 的启动指令

将下面这段直接发送给 Codex：

```text
请在当前仓库中制作《山河无名》序章《雨来之前》的 Godot 原生 Windows 可玩垂直切片。

先完整阅读根目录 AGENTS.md，以及 docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md 指定的全部前置文档。严格按该规格执行。

硬性要求：
- 使用 Godot 4.x 稳定分支和 GDScript；
- 新建 apps/godot，与现有网页原型并存；
- 不做网页、React、Vite 或 Electron 版本；
- 必须包含动画、声音、转场、移动探索、人物模型、场景模型、姓名输入、裂钟记忆和翻车现场空间选择；
- 缺少最终资源时自行生成可替换的 2D SVG / 程序音频占位资源，不要停下来等待素材；
- 按 P0—P5 里程碑实施，并在每个里程碑后运行项目和测试；
- 最终提供 run_game.bat、export_windows.bat、README、自动存档和 Windows 导出配置。

不要只写方案。请直接创建工程、代码、内容文件、占位资源、测试和脚本，直到序章可以完整游玩。
```
