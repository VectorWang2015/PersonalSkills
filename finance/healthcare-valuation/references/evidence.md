# 证据、lineage 与当前官方来源

> Revision 2 编译说明。普通执行只在需要来源核对、当前事实或边界解释时读取本文件。

## Canonical lineage

| Capability ID | 运行 reference | 主要原书锚点 | 声明类型 |
|---|---|---|---|
| `cap.medical-institution-valuation.engagement-definition` | `engagement-definition.md` | 第5章，`text/part0027.html#filepos174808` 至 `text/part0038.html#filepos191528` | 原文规则 + 执行综合 |
| `cap.medical-institution-valuation.method-selection-and-reconciliation` | `method-selection-and-reconciliation.md` | 第5-6章，`text/part0039.html#filepos192875` 至 `text/part0047.html#filepos242544` | 原文规则 + 执行综合 |
| `cap.medical-institution-valuation.operating-driver-forecast` | `operating-driver-forecast.md` | 第8/10/11章，`text/part0054.html#filepos330777`、`text/part0060.html#filepos497985`、`text/part0067.html#filepos596628` | 多章综合 |
| `cap.medical-institution-valuation.financial-normalization` | `financial-normalization.md` | 第6/8/10章，`text/part0045.html#filepos204996`、`text/part0054.html#filepos330777`、`text/part0059.html#filepos469442` | 原文规则 + 执行综合 |
| `cap.medical-institution-valuation.discounted-cash-flow` | `discounted-cash-flow.md` | 第6/13章，`text/part0045.html#filepos204996`、`text/part0094.html#filepos1052841` | 原文公式 + 明示纠偏 |
| `cap.medical-institution-valuation.capital-cost` | `capital-cost.md` | 第7/8/13章，`text/part0050.html#filepos281660`、`text/part0054.html#filepos330777`、`text/part0094.html#filepos1052841` | 原文公式 + 当前数据门 |
| `cap.medical-institution-valuation.institution-specific-adjustments` | `institution-types/` | 第8-11章，`text/part0054.html#filepos330777` 至 `text/part0069.html#filepos645582` | 原文类型规则 + 综合路由 |
| `cap.medical-institution-valuation.startup-round-valuation` | `startup-round-valuation.md` | 第12章，`text/part0071.html#filepos650860` 至 `text/part0077.html#filepos756038` | 原文方法 + cap-table 推断 |
| `support.medical-institution-valuation.financial-diagnostics` | `financial-diagnostics.md` | 第13章，`text/part0080.html#filepos763702` 至 `text/part0087.html#filepos839880` | 旧版保留 supporting resource |

## 声明标签

- **原文**：作者在所列锚点直接陈述。
- **综合**：由多个锚点整理出的执行结构，措辞不是原句。
- **推断**：为了安全执行增加的单位、缺失值、停止、当前事实或权限规则。

现代化工作流、官方来源优先、`WACC>g`、fully diluted cap table 和禁止未授权写入属于推断或实现约束，不冒充作者原话。

## 从旧版保留的内容

旧版仅在以下方面提供增量，现已重新放入条件性 reference：

| 旧能力 | 保留 | 删除 |
|---|---|---|
| 医院四层财务分析 | 功能重构、经营/业绩/管理/财务、杜邦与预测桥 | 固定 25%/90%/0.5 阈值、负营运资本必然利好 |
| 门诊/日间手术 | 医生报酬、医生—患者—收入、可转移性、专科和应急支持 | 固定 DLOC/DLOM、营收倍数、三年门槛 |
| 长期照护 | 床日收入、支付/补贴、合规双情景、医院转诊 | 历史费率、审批周期、入住率和风险溢价默认值 |
| 医疗集团 | 独立/集团价值、母体支持、担保和内部抵销 | 通用 PS 方法、未经证明的集团折价 |
| 供需竞争 | 五力、市场界定、桃林供给反例 | 固定半径、供需倍数和评分加点 |
| 初创 | 预警清单、预测偏差、多方法并排 | 固定权重/回报、冲突留存率公式 |

## 当前官方来源登记

登记 `as_of: 2026-09-03`。这里记录的是核验入口，不把网页上的动态数字固化到估值模型。

### 医保支付

- 来源：国家医疗保障局《医保支付方式改革有关情况介绍（第2期）》，发布于 2026-06-03。
- URL：https://www.nhsa.gov.cn/art/2026/6/3/art_14_20842.html
- 已核事实：官方说明 DRG/DIP 2.0 的全国落地状态及 3.0 调整安排。
- 使用限制：具体分组、点值、费率、特例单议和结算政策必须再查目标统筹地区、病种和年度的医保官方文件。

### 护理院人员标准

- 来源：国家卫生健康委员会《护理院基本标准（2011版）》官方文本。
- URL：https://www.nhc.gov.cn/wjw/gfxwj/201103/b4f382489a064ff1ba39dc364e4fb306.shtml
- 已核事实：原始国家标准文本包含每床至少 0.8 名护理人员等要求。
- 使用限制：估值时仍须确认目标机构确属护理院、文件当前有效状态、地方实施与许可校验要求。

### 医疗机构税务

- 来源一：国家税务总局法规库《中华人民共和国增值税法实施条例》，自 2026-01-01 施行。
- URL：https://fgk.chinatax.gov.cn/zcfgk/c100010/c5246349/content.html
- 来源二：财政部、国家税务总局财税〔2000〕42号原文。
- URL：https://www.mof.gov.cn/gkml/caizhengwengao/caizhengbuwengao2000/caizhengbuwengao20004/200805/t20080519_21526.htm
- 已核事实：税收处理取决于机构资格、收入性质、税种与现行政策；医疗与非医疗收入不能用一个 `t=0` 概括。
- 使用限制：WACC 税盾需要预测期所得税的边际影响和可利用性，必须由当前税务事实支持；必要时升级税务专业复核。

### 无风险利率

- 来源：中央国债登记结算有限责任公司“财政部—中国国债收益率曲线”。
- URL：https://yield.chinabond.com.cn/cbweb-mn/pgxh/pgxhIndex
- 已核事实：提供人民币国债标准期限的动态官方曲线。
- 使用限制：记录查询日期、具体期限和名义/实际口径；不复制本文件编译日的数值。

### 其他市场事实

股价、股本、公告、财务报表和重大交易优先使用交易所、监管披露或发行人正式文件。ERP、Beta、行业/规模溢价和交易数据库通常不是官方常量；如采用第三方估计，必须标明其性质、方法和版本。

## 已知原书冲突

- 第5章价值层级中有金额减百分比的量纲错误，不编译为公式。
- 第7章 WACC 例子的税后债务成本正文写 4.88%，按公式为 4.7625%；最终 WACC 9.1% 可复算。
- 第10章少数权益例子的最后一步写成 `30×90%`，上下文应为 `25×90%`。
- 第12章股权留存率的文字定义与公式图片不一致，不编译该公式。
- 第13章企业价值公式图片的括号可能导致重复终值，运行式明确只加一次。
- 第13章历史股价文字与乘法算式使用 30.23/30.50 两个数，不把该市值当公式校验样本。

详细处理见 [公式审计](formula-audit.md)。
