# 《山河无名》序章自生成美术与音频规格 V0.1

> 用途：约束 Codex 自行完成序章首版美术与音频，而不是等待外部素材。  
> 适用工程：`apps/godot/`  
> 上位规格：`docs/production/PROLOGUE_GODOT_CODEX_BUILD_SPEC_V0.1.md`  
> 目标：生成一套风格统一、可完整游玩、可继续迭代的首版正式资产。  
> 原则：不是灰块占位，不是联网搜图，不是拼贴来源不明素材。

---

## 0. 执行结论

Codex 必须自行完成：

```text
人物视觉设计。
人物分层模型。
人物基础动画。
场景背景。
场景物件。
天气与环境特效。
标题和 UI 美术。
环境音。
动作音效。
裂钟音效。
原创程序配乐。
资源导入、压缩、清单和校验。
```

资产来源只允许：

```text
1. Codex 在仓库内通过代码生成。
2. 当前执行环境中明确可用且授权清楚的生成工具。
3. 仓库已经存在并明确可使用的自有参考素材。
```

禁止：

```text
从网络搜索、抓取或下载不明版权图片、字体、音乐、音效。
照搬具体游戏、电影、动画或在世艺术家的风格。
把矩形、圆形、灰色剪影和蜂鸣声当成最终交付。
以“缺美术人员”为由只完成程序。
把生成脚本做成一次性代码后删除。
```

---

## 1. 资产质量等级

本次资产定位为：

```text
首版正式生成资产。
```

它不是最终商业发行美术，但必须达到：

```text
玩家能辨认每个主要人物。
玩家能感到清晨、午前、傍晚、夜雨的明显变化。
人物动作与性格一致。
场景不是纯色背景。
声音不是单一噪声循环。
音乐、环境和音效有层次。
整个序章不存在明显“开发占位块”。
```

允许后续人工重绘和重新录音，但当前版本必须从头到尾完整可用。

---

## 2. 总体美术方向

### 2.1 风格定义

采用：

```text
战国旧渡生活题材。
国风手绘剪影。
纸张和旧木纹理。
低饱和灰青环境。
暗黄灶火和火把作为暖色焦点。
人物采用有限色块、粗细适中的墨线和少量纹理。
动画采用切片骨骼、关键姿势和低帧循环结合。
```

不要做成：

```text
高饱和二次元。
现代国潮海报。
Q 版萌系。
写实 3D。
像素游戏。
纯黑剪影皮影戏。
水墨泼洒到看不清人物和互动点。
```

### 2.2 色彩规则

建议基础调色板：

```text
雾灰         #A8B0AA
洛水青灰     #60777A
深水蓝灰     #30484E
湿泥褐       #54483E
旧木棕       #6B513D
麻布灰       #8A8174
粟米黄       #C2A45A
灶火橙       #C96B32
火把亮黄     #E1A84A
铜锈青       #4F7770
裂钟暗铜     #6D5A42
旧血褐红     #713F36
夜色墨蓝     #202B33
文字米白     #E8E1D2
```

要求：

```text
不得所有角色同色同轮廓。
主角、禾安、辛衡、韩宁、柳娘、母亲要有不同主色和识别物。
雨夜仍应看清角色和互动目标。
暖色只集中在灶火、火把、粥和人的脸侧，不铺满全画面。
```

### 2.3 线条和纹理

```text
人物外轮廓：2.0—3.5 px 等效线宽。
内部衣褶：1.0—2.0 px。
场景远景线条更轻。
纹理使用低透明度纸纹、木纹、泥点和布纹。
避免高频噪点导致画面发脏。
```

---

## 3. 自生成美术管线

Codex 必须创建并保留：

```text
apps/godot/tools/generate_art_assets.py
apps/godot/tools/generate_character_assets.py
apps/godot/tools/generate_environment_assets.py
apps/godot/tools/generate_ui_assets.py
apps/godot/tools/generate_fx_assets.py
apps/godot/tools/build_asset_manifest.py
apps/godot/tools/validate_generated_assets.py
```

允许合并脚本，但必须保持职责清楚。

脚本要求：

```text
使用固定随机种子，保证可重复生成。
支持 --seed。
支持 --force。
支持只生成单类资源。
生成失败必须非零退出。
输出文件名稳定。
记录生成时间、脚本版本和 seed。
不得依赖联网服务才能完成最低交付。
```

推荐本地技术：

```text
Python 标准库。
Pillow（若已安装）。
SVG XML 生成。
CairoSVG（若已安装，用于光栅化）。
Godot Gradient、Polygon2D、Line2D、ParticleProcessMaterial、ShaderMaterial。
```

依赖缺失时：

```text
优先回退到纯 SVG 和 Godot 原生节点。
不得因此中止整个工程。
README 中记录可选依赖的增强效果。
```

---

## 4. 人物生成规格

### 4.1 统一比例

场景小人采用约 4.5—5.2 头身，符合十岁主角和生活化叙事。

基础导出：

```text
单角色设计画布：1024 × 1024 SVG。
游戏基础高度：主角约 190—230 px。
成年人约 230—280 px。
老人可略矮或弯背。
```

每名主要人物必须有独立分层：

```text
body_back
back_arm
back_leg
front_leg
front_arm
torso
head
hair_back
hair_front
clothing_accessory
held_prop
shadow
```

至少让 Godot 可以通过骨骼、节点旋转或关键帧完成：

```text
呼吸。
走路。
转头。
抬手。
弯腰。
拿取物件。
专属动作。
```

### 4.2 主角

年龄：十岁。

视觉：

```text
瘦，安静。
旧衣干净，主色为灰蓝和麻布色。
头发简单束起或散短发，不现代。
腰间或手里有木牍。
手指可出现墨痕。
裂钟后掌心增加铜锈贴图。
```

识别物：

```text
木牍。
旧笔。
青铜锈手掌。
```

动画必须可读：

```text
idle：目光缓慢在两侧移动。
walk：步子不急。
write：笔尖先停，再落下。
look_up：听钟时身体先停，头后转。
choice_scan：依次看孩子、湿简、人群。
```

### 4.3 禾安

年龄：与主角相近。

视觉：

```text
身形结实一点。
袖口卷起。
头发用布条束住。
主色为土红、旧麻和灶灰。
手上有灶灰或米粉。
站姿重心向前。
```

识别物：

```text
柴捆。
粥碗。
米袋。
热水桶。
```

动画：

```text
walk_fast：步幅更大。
carry_firewood：身体前倾。
place_porridge：手先伸到案边，嘴后说话。
count_jars：手指快速点数。
pour_rice：米袋抖两下，最后只落碎米。
drag_bucket：脚底打滑一下再稳住。
brace_cart：肩顶车辕。
```

### 4.4 辛衡

视觉：

```text
年长，清瘦。
衣服洗得发白。
指尖有墨。
肩背略弯。
主色为旧灰、深褐和暗青。
```

识别物：

```text
书案。
笔。
木牍。
```

动画：

```text
write：节奏稳定。
pause_pen：笔尖悬停至少 0.5 秒。
look_over_tablet：先看字，再看人。
hand_tablet：动作轻而慢。
```

### 4.5 韩宁

视觉：

```text
少年，瘦，湿衣。
衣服颜色比旧渡孩子更暗。
袖口明显可藏木片。
眼神警惕。
```

识别物：

```text
袖中残片。
护住袖口的手。
```

动画：

```text
press_sleeve：手迅速按住袖口。
step_back：身体退，眼神不退。
rush_records：看见湿简时直接前冲。
struggle：被拉住后仍伸手。
kneel_records：跪在泥里捞木简。
```

### 4.6 韩宁母亲

视觉：

```text
疲惫、湿衣、头发略乱。
身体始终靠近韩宁。
主色偏暗褐和灰紫。
```

动画：

```text
hold_child_hand。
block_question。
shield_hanning。
```

### 4.7 柳娘

视觉：

```text
衣服旧，但收拾得比流民整齐。
发簪端正。
戏箱是明确轮廓。
主色为褪色青绿、旧红和木色。
```

动画：

```text
carry_trunk。
sing：身体很稳，手势少。
song_pause：唱到地名处眼神下落，嘴停止。
hold_child。
call_names：雨夜抬头喊名。
```

### 4.8 主角母亲

视觉：

```text
朴素，克制。
围裙或旧布腰带。
主色为麻布灰、褐和淡蓝。
```

动画：

```text
wash_basin。
count_grain。
count_wood。
look_river：手停，眼睛抬起。
resume_work：很快低头继续。
```

### 4.9 群众

程序生成至少：

```text
成年男性 4 种体型或衣着组合。
成年女性 4 种组合。
老人 3 种组合。
儿童 3 种组合。
```

通过以下参数形成差异：

```text
身高。
肩宽。
衣摆长度。
头发形状。
背包、湿粟袋、孩子、拐杖等附件。
布料颜色。
```

禁止只换颜色而轮廓完全一致。

---

## 5. 人物设计图输出

生成游戏资源之外，必须输出：

```text
apps/godot/art/reference/generated_character_lineup.png
apps/godot/art/reference/generated_character_lineup.svg
apps/godot/art/reference/generated_character_palette.png
apps/godot/art/reference/generated_animation_contact_sheet.png
```

用途：

```text
让用户快速审查人物是否像同一个世界。
后续人工重绘时作为基准。
防止角色在不同场景中变脸。
```

---

## 6. 场景美术生成规格

### 6.1 旧渡清晨

必须包含：

```text
洛水河面。
木船和木桩。
缆绳。
低矮屋舍。
主角家门口。
木盆。
半袋粟米。
柴堆。
远处河道。
```

层级：

```text
sky_fog
far_bank
water
far_boats
buildings_back
walkable_ground
props_mid
foreground_reeds
fog_front
```

### 6.2 午前渡口

新增：

```text
东来商船。
卸货木板。
停下手中活计的人群。
水瓮与米袋区域。
```

场景不能只是清晨场景换亮度，必须有商船、人群和物件变化。

### 6.3 傍晚流民棚

必须包含：

```text
临时草棚。
灶火。
铺开的草席。
湿衣和行囊。
柳娘戏箱。
辛衡临时书案。
名册木牍。
```

色彩：

```text
环境转冷。
灶火成为主暖光。
远景雾更厚。
```

### 6.4 旧礼器库

必须包含：

```text
歪门。
漏瓦光束。
灰尘粒子。
断足鼎。
裂边簋。
残磬。
裂钟。
```

裂钟设计：

```text
中小型青铜钟。
肩部到下腹有明显斜裂纹。
纹饰克制，不做华丽神器。
铜锈集中在裂缝和下缘。
```

### 6.5 雨夜翻车现场

必须包含：

```text
翻倒木车。
陷入泥里的车轮。
车辕下的孩子。
泥水中的湿简。
右侧避雨棚和失散人群。
火把。
热水桶。
受惊马匹或清楚的马影。
```

空间引导：

```text
孩子区域用暖火把和哭声引导。
湿简区域用水面反光和韩宁动作引导。
人群区域用密集轮廓和喊名声引导。
```

不能靠三支巨大箭头引导。

---

## 7. 场景输出与审查图

必须输出：

```text
apps/godot/art/reference/generated_scene_morning.png
apps/godot/art/reference/generated_scene_day.png
apps/godot/art/reference/generated_scene_evening.png
apps/godot/art/reference/generated_scene_storehouse.png
apps/godot/art/reference/generated_scene_crash.png
apps/godot/art/reference/generated_scene_color_script.png
```

`generated_scene_color_script.png` 横向排出全部时间段的小缩略图，检查色彩和时间过渡。

---

## 8. 动画生成规格

### 8.1 首选方案

```text
分层 SVG / PNG + Godot Skeleton2D 或分层 Node2D 关键帧。
```

每个动作不追求高帧率，但必须有起势、主体动作和回稳。

推荐帧感：

```text
走路：8—12 fps 观感。
呼吸：2—4 秒循环。
专属动作：0.8—2.5 秒。
唱曲停顿：停顿至少 0.7 秒。
写字停笔：停顿 0.4—0.8 秒。
```

### 8.2 禁止动画偷懒

```text
所有人物上下漂浮代替呼吸。
所有动作只做整体位移。
所有 NPC 使用同一个 walk。
用镜头抖动代替角色反应。
角色说话时完全静止。
```

允许低帧，但姿势必须读得懂。

### 8.3 动画状态机

主要角色至少有：

```text
idle
walk
interact
story_action
react
```

专属动作作为 `story_action` 子状态，剧情导演通过动画名调用。

---

## 9. UI 美术生成

Codex 必须自行生成：

```text
游戏标题字标。
主菜单背景。
按钮九宫格纹理。
对话框底板。
人物名牌。
互动提示框。
按住 E 进度环或进度条。
暂停菜单底板。
设置滑块和开关。
章节标题卡。
选择回顾卡。
```

风格：

```text
旧木、薄纸、墨线、铜钉。
不做现代玻璃拟态。
不做手机 App 风格。
不堆砌龙纹、祥云和金边。
```

文字必须高对比，不能为了“古风”牺牲可读性。

---

## 10. 特效生成

Codex 必须使用 Godot 原生粒子、Shader 或程序纹理完成：

```text
河雾。
水面缓动。
屋檐滴水。
细雨。
地面积水涟漪。
泥点飞溅。
火焰和烟。
湿墨扩散。
灰尘光柱。
水纹记忆遮罩。
铜锈掌心叠加。
```

所有特效需提供质量档位：

```text
low
medium
high
```

设置菜单至少允许关闭：

```text
镜头震动。
高密度雨粒。
前景雾层。
```

---

## 11. 自生成音频管线

Codex 必须创建并保留：

```text
apps/godot/tools/generate_audio_assets.py
apps/godot/tools/generate_music_stems.py
apps/godot/tools/generate_ambience.py
apps/godot/tools/generate_sfx.py
apps/godot/tools/validate_audio_assets.py
```

推荐使用：

```text
Python wave。
array / math / random。
NumPy 和 SciPy 若环境已有则使用。
```

最低输出格式：

```text
WAV PCM 16-bit。
采样率 44.1 kHz。
单声道用于多数近距离音效。
立体声用于环境和音乐。
峰值不超过 -1 dBFS。
循环音频首尾无明显爆音。
```

必须记录固定 seed，确保可重复生成。

---

## 12. 环境音生成

### 12.1 河岸清晨

组合：

```text
低频缓慢水流噪声。
随机木船轻响。
远处稀疏鸟声，可用短正弦滑音合成，不要像电子提示音。
木缆偶尔绷紧。
极轻风声。
```

时长：至少 90 秒无明显重复感。

### 12.2 午前渡口

组合：

```text
水声更亮。
木板脚步。
远处人群低语。
船体摩擦。
绳结和货物落地声。
```

### 12.3 傍晚流民棚

组合：

```text
灶火。
锅中水声。
布料摩擦。
疲惫人群低语。
远处旧曲哼唱的无词音色，可用柔和气声合成。
```

### 12.4 旧礼器库

组合：

```text
低空气噪声。
屋顶滴水。
细微金属共振。
偶尔木梁响。
```

### 12.5 雨夜

组合：

```text
宽频雨声。
近处泥水。
屋檐与木车不同材质的雨滴。
远处雷声可极少，不做暴雨灾难片。
```

时长：至少 120 秒可循环。

---

## 13. 动作音效生成

必须生成并接入：

```text
footstep_dry_01—06.wav
footstep_mud_01—08.wav
wood_cable_creak_01—04.wav
boat_hull_creak_01—04.wav
wood_tablet_write_01—05.wav
brush_lift.wav
firewood_drop_01—03.wav
grain_pour_small.wav
grain_last_scatter.wav
bowl_place_01—03.wav
fire_crackle_loop.wav
water_bucket_drag.wav
cart_wheel_break.wav
cart_impact_mud.wav
horse_panic.wav
wood_tablet_splash_01—04.wav
wet_ink_spread.wav
crowd_call_names_loop.wav
child_cry_pressure_loop.wav
cloth_rustle_01—05.wav
```

同类音效必须有随机变体，避免每一步完全一样。

---

## 14. 裂钟音效设计

裂钟是全序章最重要的声音资产。

必须程序生成多层：

```text
bell_body.wav          青铜主体，低频基音和非整数泛音。
bell_crack.wav         裂纹造成的短促沙哑高频。
bell_underwater.wav    低通、慢起音、水下闷响。
bell_reverse_tail.wav  极轻反向尾音。
bell_memory_mix.wav    最终记忆混音。
```

技术建议：

```text
多个指数衰减正弦叠加。
泛音频率略微失谐。
加入短噪声冲击模拟槌击。
水下版本使用低通、延迟和更慢包络。
```

听感要求：

```text
古旧。
沉重。
有裂痕。
不像寺庙钟声。
不像技能音效。
不像现代电影预告片低音炮。
```

---

## 15. 原创程序配乐

Codex 必须自行生成至少四段音乐：

```text
music_old_ferry_morning.wav
music_name_and_registry.wav
music_refugees_evening.wav
music_cracked_bell_memory.wav
```

可选第五段：

```text
music_cart_crash_pressure.wav
```

### 15.1 音乐语言

```text
五声音阶为基础。
旋律稀疏。
避免明显现代和弦进行。
避免热血、史诗、英雄化。
避免直接模拟具体古乐曲。
```

可合成音色：

```text
短促拨弦：衰减正弦 + 轻噪声。
低木音：低频正弦与三角波。
木质敲击：短噪声 + 共振滤波。
气息层：滤波噪声。
远钟层：低频衰减泛音。
```

### 15.2 各曲功能

清晨：

```text
安静，留白多。
不要一开始就煽情。
```

名与籍：

```text
轻微不安。
写名字时有单音停顿。
```

流民傍晚：

```text
低音持续，旋律非常少。
让灶火和人声留出空间。
```

裂钟：

```text
非稳定拍感。
低频与水声融合。
不形成英雄主题。
```

翻车：

```text
优先环境、呼喊和低鼓。
配乐只是压力，不盖住方向性声音。
```

---

## 16. 人声与对白

首版不强制完整角色配音。

必须完成：

```text
全部中文字幕。
角色说话时的轻微呼吸、衣物或姿态声音。
雨夜人群喊名、惊呼、喘息等非语言或短语音氛围。
```

若当前环境存在合法可调用的本地中文 TTS：

```text
可以生成临时对白试听轨。
必须单独放在 assets/audio/voice_generated/。
默认设置中可关闭。
不得让低质量 TTS 覆盖字幕节奏或成为强制体验。
```

没有 TTS 时，不得用含混电子音代替中文对白。

---

## 17. 混音和音频总线

Godot 总线至少：

```text
Master
Music
Ambience
SFX
Voice
UI
```

要求：

```text
对白出现时音乐自动降低 3—6 dB。
裂钟进入时环境音逐渐抽离。
翻车硬切先让断轮和马嘶突出，再恢复雨声。
方向性目标声音使用 AudioStreamPlayer2D。
孩子、湿简、人群三方向必须能靠声音辨别。
```

不得所有音频直接挂 Master。

---

## 18. 资源清单与来源记录

必须生成：

```text
apps/godot/assets/generated_asset_manifest.json
apps/godot/assets/ASSET_PROVENANCE.md
```

每个资源记录：

```text
path
category
generator_script
generator_version
seed
source_type
license
created_at
notes
```

对于程序生成资源：

```text
source_type = procedural_generated
license = project_owned
```

仓库已有资源则写明原路径和用途。

---

## 19. 自动审查

`validate_generated_assets.py` 必须检查：

```text
主要人物资源是否齐全。
每名主要人物是否至少有一个专属动画。
全部场景是否存在远、中、近景层。
所有 manifest 路径是否存在。
音频是否能读取。
WAV 采样率和位深是否符合要求。
循环音频时长是否达到最低值。
同类脚步是否有足够变体。
裂钟五层资源是否齐全。
所有序章场景是否引用了有效背景和音频。
是否存在名为 placeholder、temp、dummy 的最终引用资源。
```

允许源码目录中存在草稿，但游戏运行清单不得引用明显占位资源。

---

## 20. 视觉与音频验收截图 / 试听清单

Codex 最终必须输出：

```text
apps/godot/review/art_character_lineup.png
apps/godot/review/art_scene_color_script.png
apps/godot/review/art_ui_sheet.png
apps/godot/review/art_animation_sheet.png
apps/godot/review/audio_cue_list.md
apps/godot/review/audio_loudness_report.md
```

`audio_cue_list.md` 需列明：

```text
每段音乐何时进入和退出。
每个环境音在哪个场景使用。
裂钟各层如何混合。
翻车三方向声音如何区分。
```

---

## 21. 完成定义

美术与音频只有同时满足以下条件才算完成：

```text
[ ] 七名主要人物视觉可清楚区分。
[ ] 六名主要人物至少各有一个专属动作。
[ ] 群众不是同一模型只换颜色。
[ ] 五个核心场景均有完整分层背景。
[ ] 清晨、午前、傍晚、旧库、雨夜有不同光色和声音。
[ ] 标题、对话、互动、暂停和章节卡拥有统一 UI 美术。
[ ] 雾、雨、火、水、墨、灰尘和记忆水纹均能运行。
[ ] 河岸、渡口、棚下、旧库、雨夜均有独立环境音。
[ ] 脚步、木响、写字、米粒、车翻等动作音已接入。
[ ] 裂钟拥有多层独立设计，不是单一正弦蜂鸣。
[ ] 至少四段原创程序配乐已接入。
[ ] 音频总线、淡入淡出和对白压低音乐可用。
[ ] 不引用来源不明的网络资产。
[ ] 生成脚本可重复执行并重建资源。
[ ] 生成资源清单和来源说明完整。
[ ] 游戏从头到尾不存在明显灰块或临时蜂鸣声。
```

---

## 22. 直接给 Codex 的补充指令

```text
美术和音频也由你完成，不要等待用户提供素材。

除主规格外，必须完整阅读并执行：
docs/production/PROLOGUE_GENERATED_ART_AUDIO_SPEC_V0.1.md

要求：
1. 在仓库内建立可重复运行的美术与音频生成管线。
2. 自行生成风格统一的 2D 人物、分层场景、UI、特效、环境音、音效和原创程序配乐。
3. 不联网抓取图片、字体、音乐或音效。
4. 不允许用灰块、纯色人形、默认 Godot 图标、单一蜂鸣或名为 placeholder 的资源作为最终运行资产。
5. 生成所有主要人物的分层模型和专属动作，生成全部核心场景与音频。
6. 输出人物阵容图、场景色彩脚本、UI 图板、动画接触表、音频 cue 清单和资源来源清单。
7. 缺少图像模型时，使用代码生成 SVG / PNG 和 Godot 原生图形；缺少音频模型时，使用 Python 程序合成 WAV。
8. 生成资产必须能被脚本重新构建，且通过 validate_generated_assets.py。
9. 这些资产按首版正式资产处理，不是等待替换的空白占位。
10. 在完成整个序章后再列出未来可提高的美术和音频方向，但不得以此作为未完成当前交付的理由。
```
