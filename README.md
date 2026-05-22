# PersonalSkills

高影响力金融书籍蒸馏出的 opencode AI 技能集。供 AI agent 在投资决策场景中调用。

## 技能

### bank-comprehensive-analysis

银行财报全面分析。输入季报/年报数据，按 12 个原子方法论自动编排分析流水线，输出结构化综合报告。

**流水线**: 负债成本 → 净息差拆解 → 不良生命周期 → 信用减值识别 → 风险抵补 → 手续费粉饰 → RORWA内生性增长 → 估值决策树 → 护城河分析

**原子方法论（12 个）**:

| # | 技能 | 功能 |
|---|------|------|
| 1 | nim-decomposition | 净息差拆解：区分"高质量息差"与"高风险息差" |
| 2 | liability-cost-evaluation | 负债成本双维评估 + AUM导向反直觉逻辑 |
| 3 | npl-lifecycle-analysis | 不良贷款四池三过程动态模型 |
| 4 | provision-profit-identification | 穿透拨备滤镜识别银行真实利润 |
| 5 | rwa-provision-ratio | 风险加权资产减值准备率（作者自创指标） |
| 6 | fee-income-authenticity | 手续费三级提纯 + 交易佣金率锚定法 |
| 7 | rorwa-endogenous-growth | RORWA + 内生性增长量化黄金法则 |
| 8 | bank-valuation-decision-tree | PE还是PB的估值决策框架 |
| 9 | rate-cycle-impact | 加息降息对存贷型/同业型银行的差异化影响 |
| 10 | cmb-moat-analysis | 护城河四层穿透（净息差→风控→客群→战略） |
| 11 | nominal-gdp-rate-anchor | 名义GDP锚定法破解低利率恐慌 |
| 12 | installment-apr-calculation | 信用卡分期真实年化利率通用公式 |

来源：《看透银行：投资银行股从入门到精通》（价投谷子地, 2021）蒸馏产出。

### book2skill

元技能。使用 RIA-TV++ 流水线将一本书蒸馏为一组可独立调用的 AI skill：

```
阶段 0: Adler 整书理解 → 阶段 1: 5维并行提取 → 阶段 1.5: 三重验证
→ 阶段 2: RIA++ 构造 → 阶段 3: Zettelkasten 链接 → 阶段 4: 压力测试
```

## 目录结构

```
├── bank-comprehensive-analysis/
│   ├── SKILL.md              # 聚合入口（面向用户）
│   └── atomic/               # 12 个原子方法论（仅由聚合器调用）
│       ├── nim-decomposition/SKILL.md
│       ├── liability-cost-evaluation/SKILL.md
│       └── ... (共12个)
├── book2skill/
│   ├── SKILL.md              # 拆书元技能
│   ├── methodology/          # RIA-TV++ 各阶段执行规范
│   ├── extractors/           # 5个并行提取器 prompt
│   └── templates/            # SKILL / BOOK_OVERVIEW / INDEX 模板
├── .gitignore
└── README.md
```

## 安装

克隆到 opencode 技能的发现路径（如 `<project>/.opencode/skills/`），重启 opencode 即可使用。
