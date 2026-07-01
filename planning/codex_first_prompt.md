# 给 Codex 的下一条任务

```text
你现在继续《山河无名》项目。

请先阅读：
1. AGENTS.md
2. README.md
3. docs/00_项目总框架_V0.4.md
4. docs/08_项目落地方案_V0.1.md
5. docs/01_跨朝代因果总表_V0.1.md
6. docs/09_章节包制作规范_V0.1.md
7. docs/chapters/CH01_礼崩之世/01_主线大纲_V0.1.md
8. docs/chapters/CH01_礼崩之世/02_人物关系表_V0.1.md
9. docs/chapters/CH01_礼崩之世/03_职业线嵌入表_V0.1.md
10. docs/chapters/CH01_礼崩之世/04_因果节点表_V0.1.md
11. docs/chapters/CH01_礼崩之世/05_记忆碎片表_V0.1.md
12. docs/chapters/CH01_礼崩之世/06_故事剧本_V0.1.md
13. docs/chapters/CH01_礼崩之世/07_至CH02衔接过渡文_V0.1.md

下一任务是建立 ACT01 技术样片和最小故事运行器。

要求：
1. 保留 prototype/chapter1_v4_experiment.html 作为历史实验，不直接继续修改。
2. 先定义 scene、character、cause、record 和 save 的数据契约。
3. 从 ACT01 选择一个 10—15 分钟场景实现最小故事运行器。
4. 所有状态变化通过可回放事件发生，界面不得直接修改状态。
5. 不移植旧随机事件池，不自动按数值判定职业。
6. 玩家选择必须记录受益者、代价承担者、官档与私录差异，不能退回善恶值。
7. 记忆只改变观察和选择表述，不提供技能、预知或正确答案。
8. 建立存读档、事件日志与基础节点校验。
9. 为 ACT01—ACT02 网页核心原型、后续 Godot 适配、ACT07 《无名录》聚合和第二章因果回收预留稳定接口。
10. 完成后用本地静态服务器运行并验证关键流程。
```
