# 阶段 1 — 自适应提取与候选归并

## 目标

从来源中建立高召回、可追溯的候选池，同时避免角色重叠制造出虚假的“多重证据”。并行是可选的执行优化，不是质量要求；同一套角色契约也应能由单个执行者顺序完成。

## 先选角色，再决定并发

只启用与书中内容和用户目标相关的 extractor：

| extractor | 主要负责 | 典型启用条件 |
|---|---|---|
| `../extractors/framework-extractor.md` | 多步思考结构、决策框架、推理路径 | 书中存在可迁移的分析过程 |
| `../extractors/principle-extractor.md` | 有条件的规则、清单、约束、默认原则 | 书中明确规定应该或不应该做什么 |
| `../extractors/case-extractor.md` | 事件事实、作者解释、结果与方法绑定 | 案例承担证据或示范作用 |
| `../extractors/counter-example-extractor.md` | 失败机制、反例、预警和边界 | 作者讨论何时失效或为何失败 |
| `../extractors/glossary-extractor.md` | 作者特定术语、定义、别名和概念差异 | 术语误解会改变后续执行 |
| `../extractors/quantitative-procedure-extractor.md` | 公式、测量、评分、数值算法与单位契约 | 来源包含可复算的量化步骤 |

不要求每本书都启用全部角色。内容稀疏时可由一个工作单元承担多个角色，但输出仍按角色标记；内容密集时可把同一角色按章节或主题拆成多个工作单元。

## 自适应并发

并发度取决于以下约束中最紧的一个：

- 实际可独立的工作单元数量；
- 当前可用的执行槽和上下文容量；
- 来源切块后保持语义完整所需的粒度；
- 成本、时限和用户要求；
- 后续归并者能够审查的候选量；
- 多人同时写同一文件带来的冲突风险。

优先并行互不覆盖的来源分块或角色。共享输出文件时，让工作单元返回结构化结果，由一个归并者统一写入；不要让多个执行者并发追加同一文件。资源有限时顺序处理，不降低证据和覆盖要求。

## 每个工作单元的最小输入

- 来源清单、内容指纹和 locator 规则；
- 被分配的原文范围，或只读原文路径；
- 当前 extractor 的角色契约；
- 用户目标中与提取范围有关的部分；
- 阶段 0 的结构地图（重蒸馏盲态时只能使用本轮独立生成的版本）。

Extractor 不应看到其他角色的结论后再“找证据配合”。独立提取完成后才做归并。

## 通用候选记录

每个 extractor 使用相同的证据外壳，并增加本角色特有字段：

```yaml
id: pca-en-2005.fw.talk05.p231.inversion
kind: framework
title: Inversion
claim:
  text: "先识别必须避免的失败路径，再反推行动。"
  status: explicit          # explicit | synthesized | inferred
evidence:
  - evidence_id: ev.pca-en-2005.talk05.p231.para2
    source_id: pca-en-2005
    anchor: "Talk 5 > §3 > printed p.231 > para.2"
    quote: "最短但足以核对的原文摘录"
    relation: supports      # supports | qualifies | contradicts | example
    evidence_role: framework-statement
    capture: exact          # exact | ocr-uncertain | translated
interpretation:
  text: "这是蒸馏者对执行含义的说明。"
  status: inferred
  evidence_refs: [ev.pca-en-2005.talk05.p231.para2]
role_conflicts:
  - with: principle
    issue: "同一段也含有‘不要做 X’的规则表述"
    proposed_resolution: "framework 保留推理顺序；原则角色只保留独立约束"
handoffs:
  - to: counter-example
    source_id: pca-en-2005
    anchor: "Talk 5 > §3 > printed p.232 > para.1"
    reason: "包含一个独立失败机制"
confidence: medium
open_questions: []
tags: [decision, inversion]
```

### 稳定 ID

- ID 由 `source_id + 类型码 + 精确锚点 + 简短语义键` 组成，不使用候选列表顺序作为身份。
- 同一来源和同一方法单元重跑后应尽量得到同一 ID；排序变化不得让所有 ID 漂移。
- ID 首次登记后即视为不可变；标题或解释修订时保留原 ID，真正换来源或拆成不同单元时用 lineage 表达。
- 合并候选时选择一个 canonical ID，并在 `aliases` 或 lineage 中保留其他 ID；不要静默删除。
- 同一段包含两个真正独立的单元时可用稳定子锚点或语义键区分，而不是用随机序号。

### 证据与推断

- `explicit` 只用于作者直接表达的主张；转述时仍保留原文锚点。
- `synthesized` 必须列出支撑综合结论的全部关键锚点。
- `inferred` 必须说明推断者、依据和不确定性，不能放进 `source_quote` 或作者定义。
- Evidence 的 `relation` 统一描述它对 claim 的认识论关系：`supports | qualifies | contradicts | example`。角色专属用途另写 `evidence_role`，例如 `definition`、`event-fact`、`worked-example`，不要扩张 relation 枚举。
- 每条 evidence 都有稳定 `evidence_id`、`source_id` 和精确 anchor；派生字段用 `evidence_refs` 引用它们。
- 发现反证或限定条件时写入 `qualifies` / `contradicts`，不要只收集支持材料。
- 引用只截取核对所需的最短片段，并遵守来源许可和合理引用限制。

## 角色冲突处理

1. **先判断记录的主功能**：多步推理归 framework；单条约束归 principle；事件事实归 case；失败机制归 counter-example；词义归 glossary；可复算数值过程归 quantitative procedure。
2. **同一事实只保留一个权威记录**：其他角色用 `handoffs` 或 `bound_to` 引用，不复制并改名。
3. **允许一段原文支持多个不同对象**：例如同一案例既展示框架又暴露失败机制，但每个对象必须有不同的 claim 和角色责任。
4. **无法当场决定时显式留冲突**：归并者依据完整上下文裁决，不让 extractor 为保持“纯净”而丢失材料。

## 归并与覆盖检查

所有工作单元完成后，由归并者：

1. 验证 ID、锚点、quote 与状态标签是否完整；
2. 根据语义和证据锚点合并重复候选，保留 aliases 与来源并集；
3. 区分“多个 extractor 重复了同一段”与“书中多个独立证据”；前者不能增加证据权重；
4. 处理 handoff 和角色冲突，建立 case/counter-example/glossary 到方法候选的引用；
5. 对照覆盖地图检查未处理或低置信度区域；
6. 将候选提交阶段 1.5，不在本阶段决定独立 skill 数量。

## 完成条件

- 启用角色与来源特征相匹配，没有为满足固定角色数制造任务；
- 并发策略有理由且不超过实际资源，顺序回退路径明确；
- 每个关键 claim 都有稳定 ID、精确锚点和证据状态；
- 角色冲突、反证、OCR 问题和未决问题没有被隐藏；
- 重复记录已归并，但所有 lineage 可追溯。
