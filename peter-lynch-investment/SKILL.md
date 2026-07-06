---
name: peter-lynch-investment
description: 基于彼得·林奇《彼得·林奇的成功投资》的完整投资方法论体系。当用户需要系统性的股票分析指导时使用，涵盖分类、选股、估值、卖出时机、风险回避、组合管理、情绪判断和认知纠偏八个维度。触发器：用户说"这家公司值得投资吗""怎么系统分析一只股票""彼得林奇会怎么看这只股票""帮我用林奇的方法分析XX"。不适用于：纯粹的技术分析、期货/期权策略、宏观择时、已在进行专业量化分析的场景。
---

# peter-lynch-investment: 彼得·林奇投资方法聚合Skill

基于彼得·林奇《One Up on Wall Street》蒸馏的8个原子技能，覆盖投资全流程。

## 输入兼容

如用户提供 `financial-pdf-parser` 解析目录，先读取 `analysis_context.md` 和 `validation/validation_report.md`，再用 `tables_merged/*.json` 提取营收、利润、现金、资产负债等定量数据；用 `chunks.jsonl` 和 `document.md` 提取产品、渠道、竞争格局、管理层讨论和风险因素。不要只凭 PDF 长文本或 OCR 文本做林奇框架判断。

## 编排逻辑

```
发现标的 → [six-stock-types] 分类
        ↓
      [perfect-stock-traits] 定性筛选 ←→ [dangerous-stocks] 负面排除
        ↓
      [peg-valuation] 定量估值
        ↓
      [portfolio-building] 组合配置
        ↓
      [sell-timing-guide] 持有监测
        ↓
      [cocktail-party-theory] 情绪参考
        ↓
      [twelve-dangerous-myths] 认知纠偏
```

## 原子Skill清单

| Skill | 路径 | 功能 |
|---|---|---|
| six-stock-types | atomic/six-stock-types/SKILL.md | 六类股票分类法 |
| perfect-stock-traits | atomic/perfect-stock-traits/SKILL.md | 13条选股准则 |
| peg-valuation | atomic/peg-valuation/SKILL.md | PEG估值法 |
| sell-timing-guide | atomic/sell-timing-guide/SKILL.md | 各类股票卖出时机 |
| dangerous-stocks | atomic/dangerous-stocks/SKILL.md | 6种应避开的危险股票 |
| portfolio-building | atomic/portfolio-building/SKILL.md | 投资组合构建原则 |
| cocktail-party-theory | atomic/cocktail-party-theory/SKILL.md | 鸡尾酒会理论 |
| twelve-dangerous-myths | atomic/twelve-dangerous-myths/SKILL.md | 12种关于股价的危险说法 |

## 执行流程

当用户请求进行完整分析时，按以下步骤执行：

### 第一步：分类 (six-stock-types)
判定目标公司属于六种类型中的哪一种，确定分析框架。

### 第二步：定性筛选 (perfect-stock-traits + dangerous-stocks)
- 对照13条选股准则逐条评估加分项
- 对照6种危险股票清单检查红灯信号
- 两套清单正反交叉验证

### 第三步：定量估值 (peg-valuation)
- 计算PEG = PE / 收益增长率
- 含股息调整：取(增长率+股息率)/PE
- 检查净现金头寸，调整实际买入成本
- 根据公司类型给出"低估/合理/高估"结论

### 第四步：综合判断
给出最终投资建议：值得深入研究 / 等更好价格 / 建议回避

### 第五步（可选）：组合与情绪
- 如用户已有持仓，调用portfolio-building评估组合结构
- 如用户关心市场时机，调用cocktail-party-theory判断情绪阶段
- 如用户陷入认知误区，调用twelve-dangerous-myths纠偏

## 分析报告保存

分析执行完毕后，**必须**主动询问用户："是否需要将以上分析保存为本地 Markdown 文件？"

用户确认后保存到 `reports/<年份>/` 目录，文件名格式：`<股票名称>-<报告期>-林奇框架分析.md`。

用户拒绝则跳过。

## 重要提醒

- 本方法论基于彼得·林奇1977-1990年美国市场经验，A股应用需适当调整
- 林奇本人不预测市场、不碰期权期货、不做技术分析
- 分类是动态的——同一公司可能在不同阶段属于不同类型
- 定性筛选 + 定量估值必须结合，不可偏废
