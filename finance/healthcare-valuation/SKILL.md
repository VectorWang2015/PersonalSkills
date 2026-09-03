---
name: healthcare-valuation
description: >-
  为医院、门诊/诊所、日间手术中心、护理院、医疗集团或初创医疗服务机构定义估值任务，建立正常化经营预测，选择并执行合适的估值方法。只查现行法规、实时市场数据、单项资产法定评估或个性化投资建议时不直接使用本流程。
metadata:
  status: active
  release-record: references/release-evaluation.md
  book2skill_capability_id: "bundle.medical-institution-valuation"
  book2skill_revision: "2"
  book2skill_source_manifest: "references/source-manifest.json"
---

# 医疗机构估值

把医疗机构的业务、权利和当前制度条件转成可复算的价值区间。先定义任务，再选择方法；不要先套倍数或折现公式。

## 何时使用

使用于医疗服务提供机构或其业务、集团、部分权益的估值、并购分析、融资定价或基本面价值审查。

不要直接使用于：

- 只查询医保、税务、牌照、人员标准或实时市场数据；先查当前官方来源。
- 单台设备、土地或建筑的法定资产评估；转资产评估或专业评估。
- 制药、器械、保险公司等非医疗服务提供方的独立估值。
- 个性化证券买卖建议、法律/税务意见、签字、申报或交易执行。

## 最小工作流

1. **定义任务**：确认目的、使用者、对象、权益层级、价值标准、价值前提、基准日、法域、币种/单位、纳入范围，以及独立价值还是特定买方协同价值。缺失会改变结论时先问。详见 [任务定义](references/capabilities/engagement-definition.md)。
2. **选择路径**：
   - 只问方法、持续经营或结果协调：读 [方法选择与协调](references/capabilities/method-selection-and-reconciliation.md)。
   - 成熟经营机构：先加载对应的[机构类型](references/capabilities/institution-types/INDEX.md)，再做[财务正常化](references/capabilities/financial-normalization.md)和[经营驱动预测](references/capabilities/operating-driver-forecast.md)。
   - 已有可靠预测并需计算价值：读 [DCF](references/capabilities/discounted-cash-flow.md)；折现率未确定时再读[资本成本](references/capabilities/capital-cost.md)。
   - 种子轮至成长期、无稳定现金流，重点是融资、期权池或稀释：读 [初创融资轮估值](references/capabilities/startup-round-valuation.md)。
   - 只做医院历史财务诊断：读 [医院财务诊断](references/capabilities/financial-diagnostics.md)和[医院类型说明](references/capabilities/institution-types/hospital.md)，不要强制做 DCF。
3. **执行并复核**：输出估值口径、采用和拒绝的方法、关键假设、计算桥、情景与敏感性；冲突结果追溯到数据或假设，不机械平均。

## 当前事实门

医保、税务、监管、人员配置、补贴、费率、利率、Beta、风险溢价、倍数、股价和可比交易都必须带来源、法域、`as_of`、期间和版本。优先使用国家或地方主管部门、交易所、发行人等一手来源。没有当前资料时列为缺口或情景，不沿用书中历史数字。

当前官方来源及来源层级见 [证据与来源](references/evidence.md)。

## 共同计算规则

- 先核对主体、报告期、币种、金额缩放、流量/存量和期末/期间平均。
- FCFF 只配 WACC；FCFE 只配股权成本。
- 永续增长终值要求 `WACC > g`；不满足时停止该公式。
- 企业价值中的终值现值只加一次。
- 税盾只在预计能够利用时进入债务成本；不能把“非营利”机械等同于所有税率为零。
- 初创复杂证券必须使用 fully diluted cap table；简单持股公式不能覆盖期权池、可转债或清算优先权。

公式、符号、单位和原书冲突见 [公式审计](references/formula-audit.md)。

## 停止或升级

出现以下情况，不要输出精确单点价值：

- 被估对象、权利、价值标准/前提或基准日不清；
- 报表主体、期间、币种或单位无法确认；
- 持续经营、关键现金流或可比数据无法支持；
- 重大监管、支付、税务或市场事实未核验；
- 公式口径不匹配、`WACC <= g`，或终值支配结果但无可靠依据；
- 复杂股权条款或完全稀释股数缺失；
- 需要法律、税务、临床或持牌估值专业判断。

## 输出契约

返回：

- 估值任务契约和资料缺口；
- 机构类型与采用/拒绝的方法；
- 经营驱动、正常化及当前事实假设；
- 可复算的企业价值、股权价值或融资轮价值桥；
- 基准、上行、下行情景及关键敏感性；
- 残余风险、时效限制和专业复核点。

除非用户明确要求，否则不要自行写入报告文件或扩大为交易、申报、发布操作。`test-prompts.json` 仅用于开发回归，不在普通执行中加载。根入口发布状态与证据边界见 [release-evaluation.md](references/release-evaluation.md)。
