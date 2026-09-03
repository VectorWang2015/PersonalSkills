# 来源证据与执行推断

来源：《七步读懂财务报表：股票投资的简要财务分析法》，林昌华，2022年8月第1版。定位使用文本抽取件的 `PAGE` 标记；完整来源指纹见 `source-manifest.json`。

| Evidence ID | 类型 | 定位 | 支持内容 |
|---|---|---|---|
| `ev-sevensteps-p025-accrual-cash` | explicit | PAGE 25—27，印刷7—9页 | 权责确认与现金收付会使利润和现金不同 |
| `ev-sevensteps-p032-accounting-identity` | explicit | PAGE 32，印刷14—15页 | 资产=负债+所有者权益 |
| `ev-sevensteps-p033-stock-flow` | explicit | PAGE 33，印刷15—16页 | 资产负债表是报告日静态快照 |
| `ev-sevensteps-p047-depreciation-cash` | explicit | PAGE 47—48，印刷30—31页 | 资本支出与后续折旧造成利润现金时间差 |
| `ev-sevensteps-p058-stock-loan-warning` | explicit/qualifies | PAGE 58，印刷40—41页 | 存贷双高只是可疑迹象，不是证据 |
| `ev-sevensteps-p089-parent-profit` | explicit | PAGE 88—89，印刷70—72页 | 母公司股东关注归母净利润；并表利润含少数股东份额 |
| `ev-sevensteps-p100-cash-equivalents` | explicit | PAGE 100—101，印刷82—84页 | 现金及现金等价物不等于货币资金 |
| `ev-sevensteps-p105-dupont` | explicit | PAGE 105—106，印刷87—89页 | ROE=净利率×总资产周转率×权益乘数 |
| `ev-sevensteps-p106-average-denominator` | explicit | PAGE 105—108，印刷88—90页 | ROE和周转的存量分母使用期初期末平均 |
| `ev-sevensteps-p112-comparison` | explicit | PAGE 112—113，印刷95—96页 | 同行横比和自身历史纵比 |
| `ev-sevensteps-p118-roe-band-typo` | explicit/contradicts | PDF物理118页，印刷101页 | 原书第二档印为不可成立的20%＜ROE≤15% |
| `ev-sevensteps-p120-cash-collection` | explicit | PAGE 120—122，印刷102—105页 | 收现比正确分子及含税影响 |
| `ev-sevensteps-p127-profit-cash` | explicit | PAGE 127—128，印刷109—111页 | 经营现金/净利润公式及极端值异常提示 |
| `ev-sevensteps-p128-recurring-profit` | explicit | PAGE 128—131，印刷111—114页 | 扣非净利润/净利润及非经常项目明细 |
| `ev-sevensteps-p132-turnover` | explicit | PAGE 132—136，印刷115—119页 | 总资产、存货和应收周转；按资产占比选重点 |
| `ev-sevensteps-p135-receivables-scope` | explicit/qualifies | PAGE 135—136，印刷118—119页 | 应收周转需考虑应收票据与应收款项融资 |
| `ev-sevensteps-p138-debt-types` | explicit | PAGE 138—140，印刷121—123页 | 带息与无息负债、有息负债率 |
| `ev-sevensteps-p140-cash-debt-cover` | explicit | PAGE 140—141，印刷123—124页 | 现金及等价物/带息债务压力测试 |
| `ev-sevensteps-p142-not-buy-rule` | explicit/qualifies | PAGE 142—146，印刷125—129页 | 财务筛选只决定是否继续研究，不等于买入 |
| `ev-sevensteps-p146-related-party-leverage` | explicit/qualifies | PAGE 145—146，印刷128—129页 | 关联方预收不能自动解释为议价权 |
| `ev-sevensteps-p204-financial-boundary` | explicit/qualifies | PAGE 204，印刷187页 | 银行报表特殊，原流程不适合初学者直接套用 |
| `ev-sevensteps-p237-standard-differences` | explicit/qualifies | PAGE 237—245，印刷220—228页 | 跨市场同名科目含义可能不同 |
| `ev-sevensteps-p264-anomaly-triage` | explicit/qualifies | PAGE 264—266，印刷247—249页 | 异常不一定意味着造假 |
| `ev-sevensteps-p267-big-numbers` | explicit | PAGE 267—269，印刷249—252页 | 大数字是相对整张报表的重大科目 |
| `ev-sevensteps-p324-method-limit` | explicit/qualifies | PAGE 324—327，印刷307—310页 | ROE主导方法不适合部分未盈利成长企业；财务不是投资全部 |

## 合并版执行推断

下列规则是为可靠执行加入的操作化推断，不冒充作者原话：

- 将主体、版本、合并范围、币种、单位和准则做成计算前硬门。
- 母公司股东视角保持归母利润与归母权益一致。
- 零、负、近零分母标记NM并改看绝对额。
- 现金覆盖扣除受限资金，并增加期限、利息与再融资情景。
- 异常登记区分观察、替代解释、证据状态和处置建议。
- parser目录以结构化表格为计算源，文本只做解释和追溯。

这些推断来自来源的限定、book2skill金融质量门和旧版可归因的运行经验；正式行为增益仍待独立评测。
