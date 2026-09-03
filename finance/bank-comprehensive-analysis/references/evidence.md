# 来源与合并证据

## 版本与身份

- 来源：价投谷子地《看透银行：投资银行股从入门到精通》，2021年4月第1版、2021年5月第2次印刷。
- 可核验来源指纹和解析限制见 [source-manifest.json](source-manifest.json)。
- 当前已发布能力包为 revision 3；严格盲态 revision 1 先冻结，revision 2 才读取旧实现并做能力级合并。本轮仅调整入口语言、默认深度、不良余额桥边界和评测状态。
- 旧12个 atomic 仍由 revision 2/3 的 aliases/supersedes 关系承接，不复制其全文。

## 保留的旧实现增益

| 旧能力 | 保留内容 | 新去向 |
|---|---|---|
| liability-cost-evaluation | 存款数量/质量表、AUM与客户服务问题 | funding-liquidity |
| nim-decomposition | 资产/负债拆解表、信用成本交叉 | net-interest-margin |
| npl-lifecycle-analysis | 四池三流程可视化 | credit-risk-lifecycle |
| provision-profit-identification | 拨备前利润桥 | earnings-quality |
| fee-income-authenticity | 会计分类、分期和信贷相关收费核查 | earnings-quality |
| rorwa-endogenous-growth | RORWA、净派现、作者简化公式 | capital-growth |
| bank-valuation-decision-tree | 方法适配和周期高点低PE警告 | bank-valuation |
| rate-cycle-impact | 短期/中期重定价教学矩阵 | funding + NIM |
| cmb-moat-analysis | 利润→风险→客群→战略四层展示 | competitive-advantage |
| installment-apr-calculation | 固定手续费单利近似 | 独立installment-cost skill |

`nominal-gdp-rate-anchor`不保留为入口；只允许把名义增长、通胀和信贷需求作为当前宏观情景输入。

## 明确删除的旧规则

- 活期占比相差10个百分点即判定负债弱。
- 默认把营运费用50%分摊为负债间接成本。
- 信用成本低于0.3%即可简化风险分析。
- 不良偏离度超过100%即证明故意藏不良。
- 拨备覆盖率120%、150%或200%作为统一安全线。
- 资产减值准备/RWA的2.5%、4%、6%红黄绿阈值。
- 以单季数据乘4作为默认RORWA、信用成本或手续费年化。
- 缺核销、回收、转让等流量时反推精确新生成不良。
- 在范围、分类或其他流量未知时，把“期末不良-期初不良+核销”称为毛新生成不良或其无条件下限；此时它仅是不良净新增与未披露变动的平衡项。
- 缺银行卡交易额仍估算“真手续费占比”。
- 招行2.4%或其他历史RORWA作为当前达标线。
- 15倍PE、1倍PB、0.5—0.8倍PB及PEG阈值作为合理价值常量。
- “买入、回避、做空、排序靠后”等交易建议。

## 原书证据索引

完整逐条证据在 [capabilities/](capabilities/) 的 `ria.reading` 中。高频锚点：

- 负债成本、存款质量、同业与期限错配：第1章，TXT lines 101-204。
- 资产收益/风险/流动性权衡：第2章，TXT lines 229-276。
- 中间业务和客户黏性：第3章，TXT lines 315-355。
- NIM定义、增长桥、重定价与非息口径：第4章，TXT lines 363-539。
- 利润前置、减值和费用质量：第5章，TXT lines 543-579。
- 资本、信用风险四池三流程、流动性：第6章，TXT lines 587-900。
- 估值、RORWA与内生增长：第8章，TXT lines 1032-1218。
- 三张报表的银行式读法：第9章，TXT lines 1222-1324。
- 招商银行案例的方法论与数据过时提示：第10章，TXT lines 1441-1535，尤其line 1445。

## 声明状态

- `explicit`：作者在锚点直接给出的定义、公式或命题。
- `synthesized`：由多个锚点形成的经营链或执行框架。
- `inferred`：revision 2加入的文档身份、当前规则、缺失值、情景和安全边界。

当前官方标准不归属于原书证据，单独维护在 [current-standards.md](current-standards.md)，并带核验日期。

匿名银行 holdout 的发布结论及不可逐卡归因的边界见 [evaluation-summary.md](evaluation-summary.md)。

## 已有样例的用途

旧目录中的七份2026Q1分析仅作为dev回归：它们证明旧输出结构可读，也暴露缺数据造值、季度年化、固定阈值、无来源估值和建议越界。不得把这些样例当作old优于new的holdout证据。
