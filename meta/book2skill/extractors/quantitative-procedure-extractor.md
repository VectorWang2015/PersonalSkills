# Quantitative Procedure Extractor

## 角色

提取能够复算的公式、测量方法、评分规则、阈值、数值决策表、估算流程和算法。目标不是把所有出现数字的段落收进来，而是建立带单位、口径、输入、步骤和边界的确定性契约。

当产物影响财务或金融任务时，同时遵守 `../methodology/09-financial-quality-gates.md`。

## 输入

- 原始书本文本、来源版本和 locator 规则；
- 被分配的来源范围及其中的表格、脚注、图注和算例；
- 用户目标与可选的本轮独立结构地图。

OCR 表格、扫描公式和图表轴需要单独核对。重新蒸馏盲态阶段不得读取旧脚本、旧公式实现、旧测试或旧 skill。

## 收录标准

收录至少具备可恢复计算契约的内容：

- 明确公式、比率、恒等式或换算；
- 带输入和输出的估算或测量过程；
- 评分、排序、阈值或数值分支规则；
- 可执行的表格查找、迭代或算法；
- 作者给出算例，且算法能从中复原。

单独出现的统计数字、年份、金额、案例结果或修辞性数量不属于 quantitative procedure。

## 与其他角色的冲突

- 不含数值契约的多步推理归 framework；
- “不得超过 X”若 X 是可计算阈值，本角色负责计算和单位，principle 负责政策约束；
- 算例中的事件事实归 case，本角色只保留输入、运算和结果；
- 数值失败条件可 handoff 给 counter-example；
- 变量术语的作者特定含义可 handoff 给 glossary。

一个 procedure 可以被更大 framework 调用，但不复制整个框架。用 candidate ID 或 unresolved 语义引用连接。

## 证据与实现纪律

- `explicit`：作者直接给出公式或步骤；
- `synthesized`：由文字、表格和算例共同复原，必须列出所有关键锚点；
- `inferred`：蒸馏者选择的默认值、异常处理、插值、舍入或实现细节。

书中未定义的单位、缺失值策略或阈值不能被静默补齐。若存在多种合理实现，列出 `implementation_choices` 并保留不确定性。

## 稳定 ID 与锚点

ID 使用 `source_id + qp + 精确主锚点 + 过程键`，例如：

`valuation-book-2019.qp.ch07.p143.owner-earnings`

不使用 `q01`。公式、表格或算法首次完整定义的位置作为主锚点；算例和限定另列 evidence。锚点应包含公式号、表号、页/段或等价的稳定位置。

## 输出

```yaml
- id: valuation-book-2019.qp.ch07.p143.owner-earnings
  kind: quantitative-procedure
  title: Owner earnings calculation
  claim:
    text: "按来源定义，从报告期数据计算 owner earnings。"
    status: explicit
  evidence:
    - evidence_id: ev.valuation-book-2019.ch07.p143.eq2
      source_id: valuation-book-2019
      anchor: "Chapter 7 > printed p.143 > eq.2"
      quote: "最短充分公式或文字摘录"
      relation: supports
      evidence_role: formula-definition
      capture: exact
    - evidence_id: ev.valuation-book-2019.ch07.p145.table7-2
      source_id: valuation-book-2019
      anchor: "Chapter 7 > printed p.145 > table 7-2"
      quote: "算例关键行"
      relation: example
      evidence_role: worked-example
      capture: exact
  inputs:
    - name: reported_earnings
      type: decimal
      unit: currency
      currency_code: "<same ISO 4217 code, required>"
      scale: "<numeric multiplier to base currency unit, required>"
      period_basis: same-reporting-period
      required: true
      source_meaning_status: explicit
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
    - name: noncash_charges
      type: decimal
      unit: currency
      currency_code: "<same ISO 4217 code, required>"
      scale: "<numeric multiplier to base currency unit, required>"
      period_basis: same-reporting-period
      required: true
      source_meaning_status: explicit
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
    - name: maintenance_capex
      type: decimal
      unit: currency
      currency_code: "<same ISO 4217 code, required>"
      scale: "<numeric multiplier to base currency unit, required>"
      period_basis: same-reporting-period
      required: true
      source_meaning_status: synthesized
      evidence_refs:
        - ev.valuation-book-2019.ch07.p143.eq2
        - ev.valuation-book-2019.ch07.p145.table7-2
    - name: additional_working_capital
      type: decimal
      unit: currency
      currency_code: "<same ISO 4217 code, required>"
      scale: "<numeric multiplier to base currency unit, required>"
      period_basis: same-reporting-period
      required: true
      source_meaning_status: explicit
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
  formula:
    expression: "reported_earnings + noncash_charges - maintenance_capex - additional_working_capital"
    status: explicit
    evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
    sign_convention:
      status: inferred
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
      rules:
        reported_earnings: "signed reported profit or loss"
        noncash_charges: "nonnegative add-back magnitude"
        maintenance_capex: "nonnegative cash-outflow magnitude"
        additional_working_capital: "positive when cash is consumed; negative when working capital is released"
  procedure:
    status: inferred
    evidence_refs:
      - ev.valuation-book-2019.ch07.p143.eq2
      - ev.valuation-book-2019.ch07.p145.table7-2
    steps:
      - "统一币种、单位和报告期"
      - "按来源口径与符号约定映射全部输入"
      - "计算并保留中间值"
  outputs:
    - name: owner_earnings
      type: decimal
      unit: currency
      currency_code: "<same ISO 4217 code as inputs>"
      scale: "<same multiplier as normalized inputs>"
      period_basis: same-reporting-period
      status: explicit
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
  assumptions:
    - text: "maintenance capex 可可靠估计"
      status: inferred
      evidence_refs:
        - ev.valuation-book-2019.ch07.p143.eq2
        - ev.valuation-book-2019.ch07.p145.table7-2
  edge_cases:
    - condition: "maintenance_capex 缺失"
      behavior: "返回输入缺口，不以总资本开支静默替代"
      status: inferred
      evidence_refs: []
  implementation_choices:
    - choice: "舍入只在最终展示时进行"
      status: inferred
      evidence_refs: []
  worked_checks:
    - check_id: synthetic-owner-earnings-01
      check_type: synthetic
      status: inferred
      inputs:
        reported_earnings: {value: 100.00, currency_code: USD, scale: 1}
        noncash_charges: {value: 20.00, currency_code: USD, scale: 1}
        maintenance_capex: {value: 15.00, currency_code: USD, scale: 1}
        additional_working_capital: {value: 5.00, currency_code: USD, scale: 1}
      expected:
        owner_earnings: 100.00
        currency_code: USD
        scale: 1
        tolerance: 0.01
      evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
  mechanical_assertions:
    status: inferred
    evidence_refs: [ev.valuation-book-2019.ch07.p143.eq2]
    checks:
      - "所有货币输入的 currency_code、scale 和 period_basis 已统一"
      - "每个必需输入缺失时不得输出精确结果"
      - "中间值与最终公式关系可复算"
  role_conflicts: []
  handoffs: []
  confidence: medium
  open_questions: []
  tags: [calculation, valuation]
```

## 提交前检查

- ID 稳定，公式、表格、算例和限定都有精确锚点；
- 输入类型、单位、币种、符号、时间基础和必填状态明确；
- 来源定义与蒸馏者实现选择分开；
- 缺失值、除零、负值、异常值、舍入和口径冲突有可观察行为；
- 至少提出一个可复算算例或机械断言；
- 没有把 OCR 错位数字、案例金额或未定义默认值当成可靠算法；
- 与 framework、principle、case、counter-example 和 glossary 的 handoff 清楚。
