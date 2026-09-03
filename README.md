# PersonalSkills

个人 AI agent skill 集合，按领域分类整理，供 opencode / DSH / Claude Code 等 agent 框架调用。

---

## 目录结构

```
PersonalSkills/
├── academic/          学术写作与论文分析
├── finance/           金融分析与投资方法论
└── meta/              元技能：用于生产或管理其他 skill
```

---

## 学术类 (`academic/`)

### academic-defensive-writing-auditor

检测并改写学术论文中防御性、过度免责、面向审稿人的措辞，同时保留必要的科学审慎表达。

- 覆盖 14 种防御性写作模式（D1–D14）
- 区分 NECESSARY_CAVEAT / DEFENSIVE / MIXED / CLEAN
- 输出带严重程度的审计表 + 论文级评分（0–10）+ 优先修改列表
- 支持 audit-only 和 full-paper-cleanup 两种模式

**安装（推荐）：**

```bash
npx academic-defensive-writing-auditor
# 指定目标目录
npx academic-defensive-writing-auditor --dir ./.agents/skills
```

**快速调用：**

```text
Audit this manuscript for defensive writing only.
Preserve necessary scientific caveats.
Rank issues by likely reviewer-perception impact.
```

**14 种模式速览：**
D1 面向审稿人的预先辩驳 · D2 重复否定性免责 · D3 堆砌保留意见 · D4 为不理想结果辩解 ·
D5 为未做的实验辩护 · D6 "公平性"自我辩护 · D7 重复"初步/有限范围"标签 ·
D8 法律式免责措辞 · D9 无关防御性披露 · D10 宣传性补偿形容词 ·
D11 AI 式自动总结句 · D12 证据边界过度标注 · D13 绝对防御性断言 · D14 重新贴标签式贡献声明

---

### drl-marine-writing-skill

DRL（深度强化学习）船舶控制类论文写作指南，面向 *Ocean Engineering* 及相关海洋控制类期刊。
覆盖动态定位（DP）、船舶保位、轨迹跟踪等学习型控制方向。

基于 6 篇精读论文整理（Øvereng 2021 OE、Gao 2022 OE、Yuan & Rui 2023 CEE、
Lee 2020 OE、Sarda 2016 OE、Sui 2024 Remote Sens），覆盖 15 节：

abstract · introduction · notation · materials & methods · results ·
discussion · conclusion · ML/RL 术语替换表 · 方程 · 表格 · 图形 ·
引用规范 · 单位 · 可重复性报告规范 · 常见审稿意见

每条规则标注置信度：`[Sample]` 样本观察 · `[Practice]` 通用惯例 · `[Recommend]` 建议

> **注意**：样本中无 JMSE 论文，投稿 JMSE 前请另行核查该期刊指南和近期代表性文章。

---

## 金融类 (`finance/`)

来源于高影响力金融书籍的方法论蒸馏，面向 A 股二级市场投资分析场景。

### 标准财报分析工作流

```text
财报获取 → PDF结构化解析 → 行业/方法论分析 → 报告导出
```

1. **cninfo-report-downloader** — 从巨潮资讯下载 A 股年报、季报、半年报 PDF
2. **financial-pdf-parser** — 将 PDF 解析为结构化文本、表格、校验报告和分析上下文
3. 按行业选择分析入口（见下表）
4. 聚合完成后导出 Markdown 报告

> 所有分析 skill 优先接受 `financial-pdf-parser` 的输出目录，而非直接读取 PDF 长文本。
> 如 validation 存在失败项，相关数字必须标为"待核实"，不能静默引用。

### 行业分析 skill

| Skill | 来源 | 原子方法论数 | 适用场景 |
|---|---|---|---|
| **bank-comprehensive-analysis** | 《看透银行》价投谷子地 2021 | 12 | 银行财报全面分析 |
| **insurance-comprehensive-analysis** | 《读懂保险股》东先生 2021 | 9 | 保险股年报分析 |
| **consumer-analysis** | 《吴劲草讲消费行业》吴劲草 2022 | 9 | 消费行业基本面 |
| **healthcare-valuation** | 《医疗行业估值》郑华 & 涂宏钢 2020 | 9 | 医疗机构 DCF 估值 |
| **financial-statement-analysis** | 《七步读懂财务报表》 | 7 | 上市公司通用财报 |
| **peter-lynch-investment** | 《彼得·林奇的成功投资》1989/2000 | 8 | 选股估值卖出时机 |

### 估值框架 skill

| Skill | 适用场景 |
|---|---|
| **investment-valuation-comprehensive-framework** | Damodaran 整书级估值方法分流（DCF / 相对估值 / 期权 / 金融服务 / 概率估值） |
| **equity-valuation-comprehensive-analysis** | 二级市场按股票类型分发估值方法，输出三情景区间和关键假设边界 |

---

## 元技能 (`meta/`)

### book2skill

使用 RIA-TV++ 流水线将一本书蒸馏为一组可独立调用的 AI skill。适用于将方法论类书籍系统性提炼为结构化 skill 集合。

---

## 安装

克隆本仓库后，在项目的 `.opencode/skills/`（或 `.agents/skills/`、`.dsh/skills/`）目录为需要启用的 skill 建立相对 symlink：

```bash
ln -s /path/to/PersonalSkills/<category>/<skill-name> .opencode/skills/<skill-name>
```

重启 agent 框架即可发现。

`academic-defensive-writing-auditor` 也可直接通过 npx 安装：

```bash
npx academic-defensive-writing-auditor --dir ./.agents/skills
```

使用 `financial-pdf-parser` 前需安装 Python 依赖：

```bash
python -m pip install pymupdf pymupdf4llm pdfplumber camelot-py opencv-python
```
