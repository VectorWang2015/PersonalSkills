# 公式、单位与机械检查

> 仅在需要实际计算、复核模型或解释来源冲突时读取。

## 通用输入契约

每个数值记录：

- 主体与合并范围；
- 报告期或估值基准日；
- 币种及金额缩放（元、千元、万元、百万元等）；
- 流量/存量、期末/期间平均；
- 税前/税后、名义/实际；
- 来源、版本和 `as_of`；
- 缺失值、异常值和舍入处理。

先统一输入，最后展示时才舍入。缺少必要输入时返回缺口，不使用隐含默认值。

## 现金流与价值

### 单期现值

```text
PV_t = CashFlow_t / (1 + r_t)^t
```

`r_t` 的期间必须与现金流间隔一致。年中现金流、月度模型或不规则期间需要显式调整时点。

来源：第6章 `text/part0045.html#filepos204996` p006-p009，公式图片 `images/00190.jpeg`。

### 无杠杆自由现金流

标准化运行式：

```text
FCFF_t = EBIT_t × (1 - tax_rate_t)
       + depreciation_and_amortization_t
       + other_non_cash_items_t
       - capital_expenditure_t
       - delta_operating_working_capital_t
```

符号约定：正的 `delta_operating_working_capital` 表示经营性营运资本增加、占用现金；释放营运资本时为负。若直接引用现金流量表中带符号的“存货减少/应收减少/应付增加”，必须先转换到同一约定。

税率不是静态常量。亏损、免税或税盾不可利用时按实际预测处理。

来源：第13章 `text/part0094.html#filepos1052841` p047-p076，图片 `images/00028.jpeg`、`00069.jpeg`、`00257.jpeg`。该运行式是多处文字和图片的综合，符号标准化属于实现推断。

### 企业价值

```text
EV = sum(FCFF_t / (1 + WACC_t)^t, t=1..n)
   + TerminalValue_n / (1 + WACC_n)^n
```

终值只加一次。第13章 `images/00073.jpeg` 的括号视觉上可能将终值置于求和号内；本式依据同章文字和第6章 `images/00266.jpeg` 消除歧义。

来源：`text/part0045.html#filepos204996` p033-p039；`text/part0094.html#filepos1052841` p042-p046。

### 永续增长终值

```text
TerminalValue_n = FCFF_n × (1 + g) / (WACC - g)
```

硬门：`WACC > g`。稳定期的利润率、资本支出、营运资本和增长必须互相一致；未达到稳定期时改用更长预测期或其他有证据的情景。

来源：`text/part0094.html#filepos1052841` p169-p175，图片 `images/00168.jpeg`。

### 企业价值到股权价值

```text
EquityValue = EV
            - interest_bearing_debt
            - minority_interest
            + cash_and_cash_equivalents
            +/- other_non_operating_adjustments
```

其他非经营项目只有在任务范围明确且未进入 FCFF/EV 时才桥接，防止重复。

来源：`text/part0094.html#filepos1052841` p033-p038、p159-p187，图片 `images/00313.jpeg`。

## 资本成本

### 债务成本

```text
Kd_after_tax = Kd_pre_tax × (1 - tax_rate_usable_for_shield)
```

只有预计可以利用利息税盾时才使用非零税率。债务成本取估值基准日的未来边际成本，不直接沿用历史借款利率。

来源：第7章 `text/part0050.html#filepos281660` p003-p012，图片 `images/00037.jpeg`。

### CAPM 与 WACC

```text
Ke = Rf + beta × ERP
WACC = Ke × We + Kd_pre_tax × (1 - t) × Wd
We + Wd = 1
```

`Rf`、ERP、Beta 的币种、市场和期限/观测窗口保持一致。非上市机构的行业、规模和特定风险可以进入情景，但不得用固定加点或与 Beta 重复计算。

来源：`text/part0050.html#filepos281660` p013-p032、p074-p088，图片 `images/00340.jpeg`、`00143.jpeg`。

来源算例复核：

```text
Ke=12%, We=60%, Kd=6.35%, t=25%, Wd=40%
Kd_after_tax = 6.35% × 75% = 4.7625%
WACC = 12% × 60% + 6.35% × 75% × 40% = 9.105%
```

书中文字的 4.88% 是算术笔误；不要传播。

## 经营指标

### 床位利用率

```text
available_bed_days = usable_beds × operating_days
occupancy_rate = occupied_bed_days / available_bed_days
```

示例：`65,000 / (200 × 365) = 89.04109589%`。

闰年、开业不足全年、停床、装修和不可用床位必须调整分母。入住率不自动推导利润，仍需费率、支付方、人员和成本。

来源：第11章 `text/part0067.html#filepos596628` p042-p064。

### ROA、ROE 与杜邦

```text
NOPAT = EBIT × (1 - operating_tax_rate)
ROA = NOPAT / average_total_assets
ROE = net_income / average_equity
ROE = net_profit_margin × asset_turnover × equity_multiplier
```

若从净利润桥接，只有在已经剔除非经营/其他融资差异时，才可用“净利润 + 税后净利息”近似 NOPAT。分母为存量时优先使用期间平均。负营运资本、毛利率或利息保障不能脱离行业、历史和现金流自动判好坏。

来源：第8章 `text/part0054.html#filepos330777` p075-p113；第13章 `text/part0086.html#filepos834473`。

## 初创融资轮

简单、同一币种、fully diluted 且无复杂证券条款时：

```text
PostMoney = PreMoney + NewMoney
InvestorOwnership = NewMoney / PostMoney
PostRoundFullyDilutedShares = ExistingFullyDilutedShares / (1 - InvestorOwnership)
```

退出反推：

```text
PostMoneyToday = ExitValue_n / (1 + TargetReturn)^n
PreMoneyToday = PostMoneyToday - NewMoney
```

这些式子不能覆盖投前/投后期权池、可转债折扣与上限、清算优先、参与权、反稀释或未来融资。复杂轮次逐证券、逐轮滚动 cap table，各方完全稀释持股合计 100%。

来源：第12章 `text/part0071.html#filepos650860`、`text/part0075.html#filepos683907`、`text/part0076.html#filepos752329`。

不使用 `text/part0075.html#filepos683907` p269-p276 的股权留存率公式：文字定义为 `1-稀释率`，图片却使用 `1/(1+稀释率)`，内部冲突。

## 不编译为公式的项目

- 第5章“控制权价格减少数股权折价”的金额/百分比量纲错误；DLOC/DLOM 只能由当前交易证据和专业标准校准。
- 第10章部分权益示例最后一步的乘数文字有算术笔误。
- 所有书中风险溢价、医保费率、政府补贴、利用率、增长率和市场倍数均是历史案例或作者判断，不是默认常量。

## 最低机械断言

- 币种、金额缩放和期间统一；百分数转为小数。
- `We + Wd = 1`，允许展示舍入误差。
- FCFF/WACC、FCFE/Ke 配对正确。
- `WACC > g`。
- 终值现值只计一次。
- EV 到 Equity 的每项符号和范围可对账。
- 分母为零、关键输入缺失或单位冲突时不输出精确值。
- 所有中间值可复算，舍入只在展示端完成。
