---
name: bank-comprehensive-analysis
description: |
  用户提供银行财报（年报/季报数据）要求全面分析银行基本面时使用。触发器：用户说"分析这家银行""帮我看看招商银行Q1""XX银行的财报怎么样"。不适用于：单一指标询问（如只问"招行不良率多少"）、非银行金融机构分析、纯宏观讨论。
source_book: 《看透银行：投资银行股从入门到精通》 价投谷子地
tags: [bank, comprehensive-analysis, investment, financial-report]
---

# 银行全面分析

## 定位

聚合 skill，作为银行财报分析的唯一外部入口。按分析依赖关系自动编排 12 个原子 skill 的执行顺序，输出结构化综合报告。

## 输入要求

分析前必须确认：
1. **银行名称 + 报告期**（如"招商银行 2026Q1"）
2. **财报数据来源**（PDF/TXT 文件路径，或用户直接粘贴的关键数据）
3. 如果仅提供报表截图/摘要，提醒用户补充关键指标（净息差、不良率、RORWA 等）

## 执行流水线

按以下顺序逐层递进，每层完成后再进入下一层。每个子 skill 的详细方法论见 `atomic/<skill-slug>/SKILL.md`。

```
第一层：盈利地基
├─ 1. 负债成本评估 (atomic/liability-cost-evaluation/SKILL.md)
│      → 存款总额/活期占比/存款成本/AUM体系
└─ 2. 净息差拆解 (atomic/nim-decomposition/SKILL.md)
       → 净息差数值/资产端收益率/负债端成本率/含金量判断
       （依赖：第1步的负债成本数据）

第二层：质量检验
├─ 3. 不良贷款生命周期 (atomic/npl-lifecycle-analysis/SKILL.md)
│      → 不良率/关注率/逾期率/新生成不良/迁徙率/广义不良率
├─ 4. 信用减值识别 (atomic/provision-profit-identification/SKILL.md)
│      → 拨备前利润vs净利润/减值计提方向/三种牌桌判断
│      （依赖：第3步的不良数据）
├─ 5. 风险加权减值准备率 (atomic/rwa-provision-ratio/SKILL.md)
│      → 风险加权资产减值准备率/拨备覆盖率交叉验证
└─ 6. 手续费粉饰识别 (atomic/fee-income-authenticity/SKILL.md)
       → 非息收入占比→手续费占比→真手续费占比三级提纯

第三层：效率与估值
├─ 7. RORWA+内生性增长 (atomic/rorwa-endogenous-growth/SKILL.md)
│      → RORWA计算/底线公式/内生性增长判定
│      （依赖：第1-5步的全部数据）
└─ 8. 估值决策树 (atomic/bank-valuation-decision-tree/SKILL.md)
       → 银行类型判定/PE还是PB/合理估值区间
       （依赖：第7步的RORWA和内生性结论）

第四层：场景与护城河（视情况选做）
├─ 9. 加息降息影响 (atomic/rate-cycle-impact/SKILL.md)
│      → 仅当有利率政策变化背景时执行
├─ 10. 护城河分析 (atomic/cmb-moat-analysis/SKILL.md)
│      → 四层穿透分析，综合判断竞争优势
└─ 11. 名义GDP利率锚 (atomic/nominal-gdp-rate-anchor/SKILL.md)
       → 仅在讨论低利率/宏观环境时执行
```

## 输出格式

分析完成后，按以下结构输出综合报告：

```markdown
# <银行名称> <报告期> 全面分析

## 一、盈利地基
### 负债成本 (表)
### 净息差拆解 (表)
→ **净息差含金量判断**

## 二、质量检验
### 不良贷款生命周期 (四池三过程)
→ **资产质量判断**
### 信用减值识别
→ **拨备前利润vs净利润判断**: 主动增提/在释放利润?
### 手续费粉饰
→ **真手续费占比**

## 三、效率与估值
### RORWA+内生性增长 (表)
→ **内生性增长判定**: 达标/临界/不达标
### 估值判断
→ **估值方法**: PE / PB, 合理区间

## 四、护城河分析 (可选)

## 五、综合结论
### 亮点 / 隐忧 / 一句话总结
```

## 保存分析结果

分析完成后，**必须**主动询问用户：

> "是否需要将以上分析保存为本地 Markdown 文件？"

- 若用户确认，保存到 `reports/<报告期>/` 目录
- 文件名格式：`<银行名称>-<报告期>-全面分析.md`
- 若用户拒绝，跳过

## 与原子 skill 的关系

本聚合 skill 编排所有原子 skill，原子 skill 不面向用户直接调用，不提供保存功能。所有入口和保存通过本 skill 统一管理。原子 skill 方法论文件位于 `atomic/` 子目录下，随本 skill 一起部署。
