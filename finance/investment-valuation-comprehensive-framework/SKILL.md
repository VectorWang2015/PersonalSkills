---
name: investment-valuation-comprehensive-framework
description: 为资产、业务、项目、私有或控制权交易选择并执行估值方法，交付资产、企业或交易价值及模型审计。若最终交付是具名上市证券的稀释后每股价值、相对定价或市场隐含预期，使用 equity-valuation-comprehensive-analysis。
metadata:
  status: active
  internal-capabilities-status: draft
  release-record: references/release-evaluation.md
  source: Investment Valuation, Fourth Edition
---

# 综合投资估值框架

按最终交付物路由。本入口负责资产、企业、项目、私人交易、并购、房地产或或有权利的估值方法与价值；不接管具名上市股票的每股估值。

## 硬门

- 先确认对象、要求权、控制/少数股东视角、估值日、币种、单位、报告期和合并范围。
- 市场价格、无风险利率、ERP、beta、违约利差、汇率、税率和可比倍数必须有当前来源与观测日期；不得引用书中案例数值充当当前输入。
- 缺少会改变方法或价值的输入时，输出缺口和可完成范围，不编造参数或伪精确价值。
- 事实、模型假设、情景和判断分开；不提供自动交易或个性化买卖指令。
- 只有用户明确要求写文件时才保存结果。

## 执行

1. 确定交付：内在价值、相对价格、清算/重置价值、交易上限、或有权利或模型审计。
2. 按现金流能力、资产可分离性、可比性、期限、杠杆稳定性和决策灵活性选择主方法。
3. 需要计算时读取 [公式与机械边界](references/formulas.md)，校验现金流/折现率、增长/再投资/回报、终值和价值桥。
4. 遇到金融、周期、年轻、亏损、困境、并购、期权或概率问题时读取 [特殊情景路由](references/special-situations.md)。
5. 用不同假设基础的辅助方法交叉检查，不机械平均内在价值与相对价格。
6. 输出方法、输入及来源、计算、价值桥、敏感性、反方情景、数据缺口和停止条件。

## 方法选择

| 条件 | 主路径 |
|---|---|
| 可构造持续现金流 | FCFF/FCFE/DDM/APV/SOTP |
| 目标是市场相对定价且可控制差异 | 基本面驱动的相对估值 |
| 资产可单独出售或替代 | 清算、资产或重置价值 |
| 有排他且可执行的或有权利 | 真实期权，作为基础价值的增量 |
| 风险为一致状态、顺序事件或连续分布 | 分别用情景、决策树或模拟 |

若用户要求具名上市证券的每股价值、当前价格比较或反向 DCF，转由 `equity-valuation-comprehensive-analysis`；不要同时运行两个入口。

来源审计时读取 [证据](references/evidence.md)；发布结论与内部卡边界见 [发布评测记录](references/release-evaluation.md)。
