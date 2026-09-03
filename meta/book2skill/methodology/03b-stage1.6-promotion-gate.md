# 阶段 1.6 — Promotion Gate

## 目标

把“候选内容是真的”与“应发布为独立 skill”分开判断。Promotion gate 在组合层面选择最小但完整的能力边界，避免把每个术语、原则和案例都包装成一个 skill，也避免把整本书塞进一个大而全入口。默认交付可以是一个可发现的书级 router 加内部 capability cards；只有存在独立用户意图、输入输出契约、独立运行能力和评测证据时，才增加独立可发现入口。

## 输入

- 阶段 1.5 的四维验证记录；
- 候选、aliases、handoffs、案例和反例绑定关系；
- 用户目标、目标运行环境和授权边界；
- 当前 portfolio 中已有 skills 及其 trigger；
- 可用的最小 dev probes。重蒸馏时还须遵守阶段 8 的盲态时序。

## 先判断产物类型

每个候选或候选组合只能选择一个当前 disposition：

| disposition | 何时选择 |
|---|---|
| `standalone-skill` | 有独立且可识别的 trigger、完整执行契约和可信增益假设 |
| `merge-into-skill` | 单独过薄，但与另一候选共享 trigger、输入、过程或输出，合并后更完整 |
| `supporting-resource` | 主要提供术语、证据、案例、边界、公式说明或条件性细节 |
| `shared-component` | 多个 skills 确实共同依赖，且集中维护能减少不一致 |
| `defer` | 证据、运行环境或测试资源暂时不足 |
| `reject` | 来源不实、无法操作化、无合理增益或风险不可接受 |

Promotion 后分配稳定的 capability ID，例如 `cap.<book-slug>.<capability-slug>`。它代表用户能力，不随标题、措辞或来源锚点修订而改变；来源身份继续由 candidate IDs 表达。真正拆分、合并或替代能力时，通过 lineage 建立新旧 ID 关系，不复用旧 ID 表示不同契约。

## 独立 skill 的晋升条件

### 1. 来源底线

- 关键 claim 通过来源忠实度检查；
- 推断和现代适配被显式标记；
- 未解决的反证不会使执行核心失真。

这是底线，不用其他优点抵消。

### 2. 能力边界

- 能用一句具体的话说明它帮助完成什么任务；
- trigger 与至少一个相邻能力可区分；
- 输入、产出和停止条件能够形成完整闭环；
- 拆开后不会迫使调用者同时手动加载另一半才能完成基本任务。

### 3. 增益假设

- 至少有一个现实 dev probe，能观察加载该方法相对 no-skill 的预期改善；
- 改善来自决策或执行变化，而不是更多术语、更多篇幅或模仿作者语气；
- 已写出会推翻增益假设的结果。

### 4. 可证伪边界

- 至少有真实的不适用场景、失败信号或转交条件；
- 边界能够转成阶段 4 的负例、边界例或兄弟路由诱饵；
- 高风险任务中的权限、当前数据或专业判断要求明确。

### 5. Portfolio 适配

- 不与已有 skill 形成几乎相同的 trigger 和输出；
- 若能力已存在，能够证明应替换、合并或作为条件性模式，而不是重复发布；
- 新增入口带来的路由成本小于它提供的行为增益。

## 合并与拆分规则

优先按用户任务和执行契约分界，不按书的章节标题分界。

适合合并的信号：

- 候选总是被同一 trigger 同时调用；
- 一个候选只提供另一个候选完成任务所需的一个步骤；
- 分开后输出互相依赖，用户无法独立使用；
- 多个原则本质上是一个检查或决策程序的约束。

适合拆分的信号：

- trigger、所需输入、风险或交付物明显不同；
- 只有某些任务需要大量条件性细节，适合通过支持文件渐进加载；
- 一个部分可安全自动执行，另一部分需要额外授权或专业判断；
- 兄弟能力必须在同一诱饵上做不同路由。

不要用“一个 skill 只能有一个思想”作为机械原子性规则。真正的最小单元是：能够独立完成一个可识别用户任务的最小完整契约。

## Promotion 记录

```yaml
promotion_id: promo-inversion-2026-09
capability_id: cap.poor-charlies-almanack.inversion-review
candidate_ids:
  - pca-en-2005.fw.talk05.p231.inversion
  - pca-en-2005.ce.talk05.p232.failure-paths
decision: standalone-skill
proposed_slug: inversion-review
capability: "为重大方案补做反向失败路径审查"
trigger_boundary:
  positive: "已有正向方案，需要系统找出致命失败路径"
  negative: "纯事实查询或低影响日常选择"
contract_summary:
  inputs: ["目标", "方案", "不可接受结果", "约束"]
  output: "失败路径、预防动作与残余风险"
gain_hypothesis: "相较 no-skill，识别更多会改变决策的失败路径"
falsifier: "在预埋风险任务上未增加有效发现，或误路由率明显上升"
portfolio_conflicts: []
lineage:
  aliases: []
  supporting_records:
    - pca-en-2005.case.talk02.p088.example-a
open_risks: []
```

## Gate 评审方法

- 对明显不确定或高影响的晋升，使用一个未参与提取的评审者复核来源和能力边界；
- 可先做薄原型和小型 dev probe，再决定是否投入完整 skill 包；
- 评审者可以提出合并、拆分或降级，但不得修改原始候选来掩盖分歧；
- 保存被拒绝或延后的原因，以便新证据出现时重新评审。

## 进入阶段 2 的条件

- 每个拟建 skill 都有 promotion 记录和 candidate lineage；
- 每项保留能力都有稳定 capability ID，并区分于来源锚定的 candidate ID；
- slug 只是暂定名称，能力与 trigger 已先定义；
- 支持材料有明确消费者，不创建无人读取的参考文件；
- 已识别最相近的兄弟 skill 或确认当前没有相邻路由；
- 没有把“重复出现”或“作者独特”当作独立的晋升理由。
