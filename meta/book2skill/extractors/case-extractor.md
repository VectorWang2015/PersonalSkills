# Case Extractor

## 角色

提取书中用于展示、支持、限定或反驳某种方法的具体事件。Case 负责事件事实、参与者、时间、行动、结果和作者解释；案例通常是支持材料，不因故事完整就独立晋升为 skill。

## 输入

- 原始书本文本、来源版本和 locator 规则；
- 被分配的来源范围；
- 用户目标与可选的本轮独立结构地图。

重新蒸馏盲态阶段不得读取旧 skill、旧案例库或旧评测。

## 收录标准

收录与候选方法有明确关系的：

- 作者亲历或参与的决策；
- 作者引用的他人、组织、历史或实验案例；
- 虚构例、思想实验或算例，但必须标清类型；
- 成功、失败和结果不确定的案例。

不要只收成功故事。纯背景叙事、无法绑定方法的轶事和没有来源定位的传闻不进入主案例池。

## 事实层次

每条案例分开记录：

1. `event_facts`：来源明确给出的时间、参与者、行动和结果；
2. `author_interpretation`：作者如何解释事件及其与方法的关系；
3. `extractor_inference`：蒸馏者额外提出的因果、类比或适用性；
4. `unknowns`：来源未说明、无法核实或存在矛盾的部分。

后发生不等于由前者导致。作者声称因果时标为作者解释；蒸馏者不能把单个成功案例升级为已证明机制。

## 与其他角色的冲突

- 方法的多步结构归 framework，单条规范归 principle；
- 失败机制和停用信号归 counter-example；
- 公式或可复算步骤归 quantitative procedure；
- 术语定义归 glossary。

Case 记录“发生了什么”和“作者说它说明什么”，其他角色记录可迁移对象。用 `bound_to` / `handoffs` 连接，不复制 claim。若一个案例可能支持多个方法，分别说明关系强度。

## 稳定 ID 与锚点

ID 使用 `source_id + case + 精确主锚点 + 事件键`，例如：

`pca-en-2005.case.talk03.p118.sees-candy`

不使用会随排序变化的 `c01`。锚点至少到页/段或可复现位置；跨多页案例记录主锚点与 `source_range`。

## 输出

```yaml
- id: pca-en-2005.case.talk03.p118.sees-candy
  kind: case
  title: See's Candy acquisition
  case_type: reported-history       # firsthand | reported-history | experiment | hypothetical | worked-example
  source_range:
    source_id: pca-en-2005
    start: "Talk 3 > printed p.118 > para.2"
    end: "Talk 3 > printed p.121 > para.1"
  evidence:
    - evidence_id: ev.pca-en-2005.talk03.p118.para2
      source_id: pca-en-2005
      anchor: "Talk 3 > printed p.118 > para.2"
      quote: "最短充分摘录"
      relation: supports
      evidence_role: event-fact
      capture: exact
    - evidence_id: ev.pca-en-2005.talk03.p120.para4
      source_id: pca-en-2005
      anchor: "Talk 3 > printed p.120 > para.4"
      quote: "作者解释该案例的最短摘录"
      relation: supports
      evidence_role: author-interpretation
      capture: exact
  event_facts:
    status: explicit
    evidence_refs: [ev.pca-en-2005.talk03.p118.para2]
    actors: ["..."]
    situation: "..."
    action: "..."
    outcome: "..."
  author_interpretation:
    status: explicit
    evidence_refs: [ev.pca-en-2005.talk03.p120.para4]
    text: "作者认为该案例说明……"
  extractor_inference:
    status: inferred
    evidence_refs:
      - ev.pca-en-2005.talk03.p118.para2
      - ev.pca-en-2005.talk03.p120.para4
    text: "它可能为某类定价权判断提供类比，但不能单独证明因果。"
  bound_to:
    - candidate_ref: "unresolved: pricing-power-framework"
      relation: illustrates
      status: inferred
      evidence_refs:
        - ev.pca-en-2005.talk03.p118.para2
        - ev.pca-en-2005.talk03.p120.para4
      confidence: medium
  role_conflicts: []
  handoffs: []
  unknowns:
    - "来源没有给出同时期失败收购样本"
  tags: [case, acquisition]
```

若目标候选尚未获得稳定 ID，使用 `unresolved:<semantic-key>`，归并阶段再解析，不凭空猜 ID。

## 提交前检查

- 事件事实、作者解释和蒸馏者推断没有混在 summary 中；
- 每个结论都有精确锚点，跨页范围清楚；
- 没有把相关性、后见结果或作者评价冒充因果证据；
- 至少说明案例支持、限定、反驳还是仅说明某方法；
- handoff 不复制框架、原则、公式或失败机制；
- 结果未知、样本偏差和来源矛盾被保留。
