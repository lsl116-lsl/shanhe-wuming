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

阶段 B 序章—ACT02 网页核心原型已经完成。

下一任务是根据用户首轮试玩反馈修订核心原型，并在评审通过后设计 ACT03 职业入口。

要求：
1. 先阅读 docs/10_阶段A技术样片说明_V0.1.md、docs/11_阶段B网页核心原型说明_V0.1.md、docs/12_序章设计与剧情逻辑说明_V0.1.md 并运行 pnpm test。
2. 保留 prototype/chapter1_v4_experiment.html 作为历史实验，不直接修改。
3. 先处理用户反馈，不在未评审前直接扩大 ACT04—ACT06 内容量。
4. 复用现有 scene、character、cause、record、memory、save 契约。
5. 扩展内容文件，不把故事条件和效果写入 UI。
6. 所有状态变化继续通过可回放事件发生。
7. 新增节点后运行完整路线审计和浏览器验证。
```
