---
name: insurance-comprehensive-analysis
description: |
  用户提供保险公司财报（年报/季报数据）要求全面分析保险股基本面时使用。触发器：用户说"分析这家保险公司""帮我看看中国平安""XX保险的财报怎么样"。不适用于：单一指标询问（如只问"平安PEV多少"）、非保险金融机构分析、纯宏观讨论。
source_book: 《读懂保险股》 东先生 (自由派的诗人)
tags: [insurance, comprehensive-analysis, investment, financial-report]
---

# 保险股全面分析

## 定位

聚合 skill，作为保险股财报分析的唯一外部入口。按分析依赖关系自动编排 9 个原子 skill 的执行顺序，输出结构化综合报告。

## 输入要求

分析前必须确认：
1. **保险公司名称 + 报告期**（如"中国平安 2025年报"）
2. **财报数据来源**（PDF/TXT 文件路径，或用户直接粘贴的关键数据）
3. 如果仅提供报表截图/摘要，提醒用户补充关键指标（内含价值、新业务价值、营运利润等）

## 执行流水线

```
第一层：理解地基
├─ 1. 苹果树模型 (atomic/apple-tree-model/SKILL.md)
│      → 商业模式理解: 费用前置→利润后置, GAAP为何低估
└─ 2. 三套准则框架 (atomic/triple-framework/SKILL.md)
       → GAAP/EV/OP三套准则钩稽关系
       （依赖：第1步的商业模式认知）

第二层：核心估值
├─ 3. 内含价值估值 (atomic/ev-valuation/SKILL.md)
│      → EV = ANA + VIF - CoC, PEV锚定
└─ 4. 新业务价值评估 (atomic/nbv-analysis/SKILL.md)
       → NBV驱动: 新单保费×NBV率, 增长发动机分析
       （依赖：第3步的EV框架）

第三层：利润与资本
├─ 5. 剩余边际分析 (atomic/residual-margin-analysis/SKILL.md)
│      → 准备金里的利润蓄水池, 剩余边际摊销
├─ 6. 营运利润拆解 (atomic/op-four-factors/SKILL.md)
│      → 四因子: 摊销+投资收益+息差+偏差
└─ 7. 偿付能力体系 (atomic/solvency-system/SKILL.md)
       → 偿二代, 持偿成本, 资本约束

第四层：投资与估值
├─ 8. 保险投资分析 (atomic/insurance-investment/SKILL.md)
│      → 久期匹配, 利差损安全边际, 战略/战术配置
└─ 9. 估值决策 (atomic/insurance-valuation-method/SKILL.md)
       → PEV+ROEV+股息率+NBY增长综合判断
       （依赖：第3-7步的全部数据）
```

## 保存分析结果

分析完成后，**必须**主动询问用户：

> "是否需要将以上分析保存为本地 Markdown 文件？"

- 若用户确认，保存到 `books/du-dong-bao-xian-gu/analyses/` 目录
- 文件名格式：`<保险公司名称>-<报告期>-全面分析.md`
- 若用户拒绝，跳过
