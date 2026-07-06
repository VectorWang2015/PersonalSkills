# PersonalSkills

高影响力金融书籍蒸馏出的 opencode AI 技能集。供 AI agent 在投资决策场景中调用。

## 技能

## 标准工作流

面向真实财报分析时，优先使用以下流水线：

```text
财报获取 → PDF结构化解析 → 行业/方法论分析 → 报告导出
```

1. 财报获取：使用 `cninfo-report-downloader` 下载 A 股年报、季报、半年报到 `raw/reports/<报告期>/`。
2. PDF结构化解析：使用 `financial-pdf-parser` 将 PDF 转为 `document.md`、`chunks.jsonl`、`tables_merged/`、`validation/`、`analysis_context.md`。
3. 分析入口选择：按行业进入 `financial-statement-analysis`、`bank-comprehensive-analysis`、`insurance-comprehensive-analysis`、`consumer-analysis`、`healthcare-valuation` 或 `peter-lynch-investment`。
4. 报告导出：聚合分析 skill 完成后询问用户是否保存 Markdown 到 `reports/<报告期>/`。

### 解析目录作为统一输入

所有财报分析入口都应优先接受 `financial-pdf-parser` 的输出目录，而不是直接读取 PDF 长文本。下游分析时按以下顺序取数：

1. `analysis_context.md`：报告来源、校验状态、关键表路径。
2. `validation/validation_report.md`：判断关键数据是否可直接使用。
3. `tables_merged/*.json`：财务数字、表格计算、页码追溯的首选来源。
4. `chunks.jsonl` / `document.md`：业务描述、管理层讨论、风险因素等文本上下文。

如 validation 存在失败项，相关数字必须在分析报告中标为“待核实”，不能静默引用。

### bank-comprehensive-analysis

银行财报全面分析。输入季报/年报数据，按 12 个原子方法论自动编排分析流水线，输出结构化综合报告。来源：《看透银行》（价投谷子地, 2021）。

**原子方法论（12 个）**: 净息差拆解 / 负债成本评估 / 不良贷款生命周期 / 信用减值识别 / RORWA内生性增长 / 银行估值决策树 / 加息降息影响 / 手续费粉饰识别 / 分期利率计算 / 风险加权减值准备率 / 招行护城河分析 / 名义GDP利率锚

### insurance-comprehensive-analysis

保险股全面分析。输入年报数据，按 9 个原子方法论分析保险公司估值。

**原子方法论（9 个）**: 内含价值估值(EV) / 三套准则框架(GAAP/EV/OP) / 苹果树模型 / 剩余边际分析 / 新业务价值(NBV) / 营运利润四因子 / 偿付能力体系 / 保险投资分析 / 保险股估值方法

来源：《读懂保险股》（东先生, 2021）。

### consumer-analysis

消费行业公司基本面分析。按品牌-渠道-供应链三角框架编排 9 个原子方法论。来源：《吴劲草讲消费行业》（吴劲草, 2022）。

### healthcare-valuation

医疗机构估值分析。按机构类型分发 9 个原子方法论，覆盖医院/门诊/长期照护/初创机构的 DCF 估值与财务分析。来源：《医疗行业估值》（郑华 & 涂宏钢, 2020）。

### financial-statement-analysis

上市公司财报全面分析。按七步成诗法编排 7 个原子方法论，自动编排盈利能力→周转效率→杠杆安全→综合判断的分析流水线。来源：《七步读懂财务报表》[^1]。

**原子方法论（7 个）**: 七步成诗法 / 盈利能力分析 / 运营效率分析 / 杠杆评估 / 避雷方法 / 招股书评估 / 综合判断

[^1]: 无公开署名作者信息，系财务分析通识框架。

### peter-lynch-investment

彼得·林奇投资方法论。按 8 个原子方法论覆盖分类、选股、估值、卖出时机、风险回避、组合管理、情绪判断和认知纠偏。来源：《彼得·林奇的成功投资》（Peter Lynch, 1989/2000）。

**原子方法论（8 个）**: 六种股票类型 / 完美股票特质 / PEG估值 / 卖出时机指南 / 避而不买的股票 / 组合构建 / 鸡尾酒会理论 / 十二条危险谬误

### cninfo-report-downloader

工具型 skill。输入 A 股股票代码，从巨潮资讯自动下载最新年度报告完整版和最近一期非年报定期报告，保存为 PDF/TXT 到项目归档目录。

### financial-pdf-parser

工具型 skill。将 A 股年报、季报、半年报 PDF 解析为结构化文本、表格、校验报告和下游分析上下文。推荐作为所有财报分析 skill 的前置步骤。

### book2skill

元技能。使用 RIA-TV++ 流水线将一本书蒸馏为一组可独立调用的 AI skill。

## 安装

克隆到 opencode 技能的发现路径（如 `<project>/.opencode/skills/`），重启 opencode 即可使用。

本仓库的标准安装方式是让 `.opencode/skills/<skill-name>` 指向 `skills/<skill-name>`。例如：

```bash
ln -s ../../skills/financial-pdf-parser .opencode/skills/financial-pdf-parser
```

新主机使用 `financial-pdf-parser` 前需准备 Python 3.11+ 环境并安装核心依赖：

```bash
python -m pip install pymupdf pymupdf4llm pdfplumber camelot-py opencv-python
```
