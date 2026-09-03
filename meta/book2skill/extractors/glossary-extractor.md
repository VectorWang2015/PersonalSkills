# Glossary Extractor

## 角色

提取会改变理解或执行的作者特定术语、定义、别名、概念边界和用法变化。术语表是共享解释资源，不因词频高或名字新颖就自动生成独立 skill。

## 输入

- 原始书本文本、版本指纹和 locator 规则；
- 被分配的来源范围；
- 用户目标与可选的本轮独立结构地图。

重新蒸馏盲态阶段不得读取旧 glossary、旧 skill 或旧总结。字典定义只能帮助发现差异，不能替代作者用法。

## 收录标准

收录至少符合一项且对下游决策有影响的词：

- 作者显式定义或重新定义；
- 普通词在书中有特殊技术含义；
- 同一词在不同章节有需要说明的用法变化；
- 多个关键主张依赖该词的精确边界；
- 误解该词会导致错误 trigger、步骤、公式或结论。

仅仅频繁出现不是充分理由。人名、地名、一般词汇和没有执行影响的修辞通常不收录。

## 定义状态

- `explicit`：来源有直接定义；
- `synthesized`：从多个使用实例综合出作者用法；
- `inferred`：蒸馏者提出的工作定义或现代映射。

若作者在书中前后用法不一致，不要强行合成单一定义；记录 `usage_variants` 和可能的演变。

## 与其他角色的冲突

- 术语对应的多步方法归 framework，行动约束归 principle；
- 术语的算式、测量定义或阈值归 quantitative procedure；
- 案例与失败机制分别归 case 和 counter-example。

Glossary 只维护“这个词在此来源中是什么意思、与什么不同、谁会使用”。其他候选通过 ID 引用它，不复制整段定义。若一个词本身也是完整操作协议，建议由相应方法角色 canonical ownership，术语记录只做定义入口。

## 稳定 ID 与锚点

ID 使用 `source_id + gl + 精确主锚点 + 术语键`，例如：

`pca-en-2005.gl.talk02.p087.circle-of-competence`

不使用 `g01`。显式定义所在位置作为主锚点；综合定义选择最具定义性的锚点作为身份，并列出其他用例。不同版本的术语不要静默共用同一 ID。

## 输出

```yaml
- id: pca-en-2005.gl.talk02.p087.circle-of-competence
  kind: term
  term: circle of competence
  aliases:
    - "能力圈"
  definition:
    text: "知道自己在哪些问题上具有可验证判断优势，以及边界在哪里。"
    status: synthesized
  evidence:
    - evidence_id: ev.pca-en-2005.talk02.p087.para2
      source_id: pca-en-2005
      anchor: "Talk 2 > §4 > printed p.87 > para.2"
      quote: "最短充分定义摘录"
      relation: supports
      evidence_role: definition
      capture: translated
    - evidence_id: ev.pca-en-2005.talk02.p089.para1
      source_id: pca-en-2005
      anchor: "Talk 2 > §4 > printed p.89 > para.1"
      quote: "用法或限定摘录"
      relation: qualifies
      evidence_role: usage-limitation
      capture: exact
  distinctions:
    - from: "熟悉"
      difference: "熟悉不等于具有经校准的判断能力"
      status: synthesized
      evidence_refs:
        - ev.pca-en-2005.talk02.p087.para2
        - ev.pca-en-2005.talk02.p089.para1
  usage_variants: []
  downstream_effect:
    - text: "若按‘熟悉领域’理解，会错误扩大相关决策 skill 的适用范围"
      status: inferred
      evidence_refs:
        - ev.pca-en-2005.talk02.p087.para2
        - ev.pca-en-2005.talk02.p089.para1
  consumers:
    - "unresolved: competence-boundary"
  role_conflicts: []
  handoffs: []
  confidence: medium
  open_questions: []
  tags: [term, decision-boundary]
```

## 提交前检查

- 词条会实质改变理解或执行，而不是一般词汇收藏；
- 定义来自精确锚点，显式、综合和推断已区分；
- 不同章节或版本的用法冲突没有被抹平；
- 与框架、原则、量化过程、案例和反例没有重复职责；
- downstream effect 和消费者明确，避免创建无人使用的 glossary；
- 引用最短充分，不复制长篇版权文本。
