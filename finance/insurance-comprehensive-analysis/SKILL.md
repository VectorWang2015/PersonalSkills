---
name: insurance-comprehensive-analysis
description: 分析保险公司、保险集团或以保险为主的综合金融集团财报与基本面，覆盖财险/寿险分业、现行保险合同会计、VNB/EV、偿付能力、利润释放、投资与资产负债管理，以及报告日价值锚和压力区间。适用于公司或报告级分析；不适用于个人保单配置、纯文档抽取或交易执行。
metadata:
  version: "7.0.0"
  workflow: "book2skill-redistillation-merge"
  standards-as-of: "2026-09-03"
  status: active
  internal-capabilities-status: draft
  release-record: references/release-evaluation.md
---

# 保险公司综合分析

输出应短、可复算、可追溯，不混淆主体、期间、会计制度、精算价值、监管资本和分析者推断。

## 证据优先级

1. 目标公司的正式报告、更正公告、偿付能力报告、精算审阅和投资者材料。
2. 财政部、国家金融监督管理总局等有权机关的现行规则。
3. 原书的稳定框架与历史案例。
4. 分析者推断；必须列假设、反方解释和证伪条件。

## 必经流程

1. 确认任务和输出深度。
2. 建立文档身份：主体、证券代码、集团/子公司、报告类型与期间、原版/更正版、审计状态、币种、单位、时点/期间流量。
3. 识别会计和监管模式；涉及CSM、保险服务收入或偿付能力时读 [current-standards.md](references/current-standards.md)。
4. 按财险、寿险/长期健康险、短期健康险或混合集团分业。
5. 综合金融集团若披露现成分部勾稽，第一张核心表同时列业务/分部净利润、归属于集团母公司的对应贡献、少数股东和合并抵销；不得把业务净利润机械相加为集团归母。
6. 宣布“报告未披露”前，必须扫描：
   - 集团经营摘要和管理层讨论；
   - 资本管理/偿付能力章节；
   - 每个主要保险子公司章节；
   - 母公司单体资产负债表、利润表、现金流量表和投资收益附注；
   - 关联方关系及交易中的股利收入明细、应收股利和利润分配附注。
7. 区分“未在摘要披露”“未在当前章节披露”“整份报告未找到”；只有完成上述扫描后才能使用最后一种表述。
8. 分红分析先把母公司投资收益中的股利收入合计与关联方逐家确认明细交叉勾稽，再检查成本法会计政策、年度可动用资金表、现金流和应收股利；确认、宣告、年度资金流入、支付和到账是不同证据层级。
9. 先读取管理层正式归因，再重建保险服务结果或净利润同比桥。
10. 利润桥按绝对变化额从大到小排序，显式检查CSM释放、非金融风险调整、亏损部分确认/转回、当期服务经验差异、保险财务损益、投资买卖价差/公允价值、税及一次性事项。
11. 寿险有数据时分别闭合三条桥且不混加：服务三桶至服务结果、税前营运利润至净利润、CSM期初至期末；缺数据时只停在可得层。
12. 关键事实尽量给页码、表名、列名或文本行号；缺输入不以历史比例或书中5%/11%代填。
13. 三个证伪点必须直接挑战当前核心结论，不能用“未来重述就重算”代替反例检验。
14. 前瞻判断前运行 [可预测性门](references/capabilities/predictability-gate.md)。

## 解析目录兼容

用户提供financial-pdf-parser目录时：

- 读analysis_context.md和validation/validation_report.md；
- 用tables_merged复算；
- 用chunks.jsonl或document.md做全报告检索；
- 关键事实回原表或原页；
- 校验失败数据标待核实。

截图、摘要或叙述不能代表整份年报。

## 内部路由

| 任务 | 读取 |
|---|---|
| 文档、全报告扫描、子公司和分业 | [document-segment-router.md](references/capabilities/document-segment-router.md) |
| 保险服务结果、净利润桥、新业务和承保 | [operating-quality.md](references/capabilities/operating-quality.md) |
| EV/VNB、子公司偿付能力和资本 | [value-capital.md](references/capabilities/value-capital.md) |
| CSM、公司管理利润与母公司分红能力 | [profit-release.md](references/capabilities/profit-release.md) |
| 投资收益、资产质量、负债成本与ALM | [investment-alm.md](references/capabilities/investment-alm.md) |
| 报告日价值锚和压力区间 | [valuation-scenarios.md](references/capabilities/valuation-scenarios.md) |
| 判断历史关系能否外推 | [predictability-gate.md](references/capabilities/predictability-gate.md) |

苹果树只在用户需要直觉解释时简短使用，并标明是旧准则背景下的简化比喻。

## 紧凑输出

用户要求“快速、简要、紧凑、只说重点”时：

- 1行身份与数据限制；
- 3条结论；
- 最多2张核心表；
- 3个证伪点。

详细桥按需展开。连续追问的任务二优先引用任务一已有数字和表，只补新增口径或边界，不重复整段结论。

## 硬边界

- 不把CSM视为旧剩余边际简单改名或已赚可分配利润。
- 不臆造未披露EV、CSM/剩余边际、摊销、久期、持偿成本或营运利润分项。
- 不在只查摘要后声称整份报告未披露。
- 集团偿付能力率不能替代主要保险子公司的个体比率。
- 综合金融集团不得把业务净利润、集团归属贡献、少数股东和合并抵销混为一个口径。
- 不把“主要子公司确认明细可得”误写成“逐家股利数据缺失”，也不把确认收入直接等同逐家支付或母公司到账。
- 股利收入合计与关联方逐家明细的差额只能列为未归属项；无证据不得全部归为结构化主体。
- “年度可动用资金表所列子公司分红流入”只能按该表证据强度表述，不称逐笔银行到账；它与现金流、投资收益或EV口径的差异一律列未归属或跨口径。
- 不以CSM释放或投资单项概括利润变化。
- 不把服务结果桥、营运利润至净利润桥和CSM余额桥相互混加。
- 混合税前项目、所得税和少数股东的桥只能称“税前利润至归母利润同比勾稽桥”；无法逐项税后归因时不得称各项为税后归母贡献。
- 母公司静态利润/现金覆盖只作压力提示，不冒充完整法定可分配能力。
- 不堆砌非任务核心的评级缺失搜索或弱静态相减；优先保留能解释当前结论的高信息证据。
- 估值止于报告日价值锚和压力区间，不做倍数价格延伸或交易建议。
- 未经用户同意，不写报告、不交易、不发布。

来源与删改依据见 [evidence.md](references/evidence.md)，源文件指纹见 [source-manifest.json](references/source-manifest.json)，v7 聚合发布结果见 [release-evaluation.md](references/release-evaluation.md)，能力状态见 [capability-bundle.json](references/capability-bundle.json)。
