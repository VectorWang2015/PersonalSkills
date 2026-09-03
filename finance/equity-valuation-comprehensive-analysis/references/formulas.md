# 公式与机械边界

仅在实际计算或审计公式时读取本文件。所有市场数据必须带来源、观测日期、币种和期间；不得使用书中案例数值或历史参数作为当前默认值。

## 1. 现金流与折现率

\[
FCFF = EBIT(1-t)-Reinvestment
\]

常用展开：

\[
Reinvestment=(CapEx-Depreciation)+\Delta Noncash\ WC
\]

若研发、客户获取、品牌投入或并购实质上为增长投资，应在盈利与再投资两端采用一致的资本化处理。

\[
FCFE = Net\ Income-(CapEx-Depreciation)-\Delta Noncash\ WC+Net\ Debt\ Issued
\]

- FCFF 用 WACC；FCFE 或股利用股权成本 `K_e`。
- FCFF 位于利息和本金之前；FCFE 位于债务现金流之后。
- 优先股、租赁、养老金等债务类要求权必须单独且一致处理。

\[
K_e=R_f+\beta\times ERP
\]

国家风险暴露只有在独立论证且未重复计入 ERP、现金流或 beta 时才另加。

\[
WACC=K_e\frac{E}{D+E}+K_d(1-t)\frac{D}{D+E}
\]

`E`、`D` 使用与估值资本结构一致的市场价值；`K_d` 是当前边际借款成本。币种、名义/实际、税前/税后和期限必须与现金流匹配。

## 2. 增长、再投资与回报

\[
g_{equity}=Equity\ Reinvestment\ Rate\times ROE
\]

\[
g_{firm}=Reinvestment\ Rate\times ROIC
\]

关注未来边际回报，不把历史平均 ROIC/ROE 永久外推。负盈利、负资本或严重会计失真时，这些比率不能直接使用。

Top-down 预测可用：

\[
Reinvestment_t=\frac{\Delta Revenue_t}{Sales\text{-}to\text{-}Capital_t}
\]

若投资到收入有时滞，应显式建模。

## 3. 终值

\[
Stable\ Reinvestment\ Rate=\frac{g}{ROIC_{stable}}
\]

\[
TV_{firm,n}=\frac{EBIT_{n+1}(1-t)(1-g/ROIC_{stable})}{WACC_{stable}-g}
\]

\[
TV_{equity,n}=\frac{FCFE_{n+1}}{K_{e,stable}-g}
\]

硬停止：`WACC <= g`、`K_e <= g`、稳定 ROIC 为零却假设正增长、或稳定期税率/利润率/风险/杠杆/再投资/存续状态尚未定义时，不计算永续终值。

## 4. 企业价值到股权及每股价值

\[
Equity\ Value=Operating\ Asset\ Value+Excess\ Cash+Nonoperating\ Assets+Cross\ Holdings
-Debt-Debtlike\ Claims-Preferred\ Claims-Market\ Value\ of\ NCI
\]

每项只处理一次。合并口径经营价值包含子公司全部经营资产时，必须扣除非控股股东权益的市场价值；不得在重大情况下机械使用账面少数股东权益。

期权价值法：

\[
Value\ per\ Share=\frac{Aggregate\ Common\ Equity-Value\ of\ Employee\ Options}{Primary\ Shares+Expected\ Vested\ Restricted\ Shares}
\]

若采用库存股法，不得再完整扣除同一批期权价值。披露基本股、稀释股、限制性股份、可转债及不同投票权类别。

## 5. 相对估值驱动

\[
Forward\ PE=\frac{Payout\ Ratio}{K_e-g}
\]

\[
PBV=\frac{Payout\ Ratio\times ROE}{K_e-g}
\]

\[
\frac{EV}{Sales}=\frac{Aftertax\ Operating\ Margin\times(1-Reinvestment\ Rate)}{WACC-g}
\]

这些公式解释驱动，不提供当前“合理倍数”。股权价值分子只能配股权口径分母；企业价值分子只能配经营口径分母。同行身份不能替代对增长、风险、利润率、资本回报、会计和币种差异的控制。

## 6. 金融企业与特殊情景

- 银行和保险的存款/保单负债通常是经营原材料，不强套普通工业企业 FCFF/WACC 或 EV/EBITDA。
- 优先使用股利、监管资本约束下的股权现金流或超额收益：增长必须与新增监管资本和可持续 ROE 相容。
- 周期/商品企业先正常化全周期利润、利润率或商品价格；景气峰值低 PE 不能直接视为便宜。
- 年轻/亏损企业从收入规模、目标利润率、再投资效率、融资稀释和存活概率建模；只在损失确属暂时或周期性时正常化。
- 深度困境股权只有在有限责任、资产价值、债务面值/期限和波动率可辨识时才考虑看涨期权框架。

## 7. 并购、期权和概率

\[
Net\ Synergy=V_{combined,with\ synergy}-V_{acquirer,standalone}-V_{target,standalone}-Implementation\ Costs
\]

\[
Maximum\ Target\ Price=V_{target,status\ quo}+V_{control}+Net\ Synergy
\]

这是收购方 NPV 降至零前的经济上限；实际报价应低于上限以保留收购方收益，并考虑融资副作用。交易倍数样本通常有被收购溢价偏差。

只有存在可识别、可执行且具有排他性的延迟、扩张、放弃或其他或有权利时，才在基础价值之外讨论期权增量。

\[
Expected\ Value=\sum_s p_sV_s,\quad \sum_s p_s=1
\]

情景中的收入、利润率、再投资和风险必须共同可行。若各状态已用风险调整折现率估值，不因结果离散度大再次扣减价值；若采用无风险折现并用分布衡量风险，则必须说明投资者分散化假设。

## 8. 反向 DCF

以当前市场企业价值或股权价值为等式左端，只求解一个或少数有界经营变量，例如收入 CAGR、目标利润率、稳定 ROIC 或竞争优势期。结果是“价格隐含条件”，不是预测。

硬停止：缺当前价格/市值、股本或 EV 桥；固定输入不足；未知数过多导致非唯一解；求解结果违反市场规模、利润率、再投资或终值约束。
