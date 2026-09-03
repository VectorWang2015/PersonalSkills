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

包含财报获取/解析工具，以及从金融书籍独立重蒸馏并经匿名留出评测的分析方法，主要面向 A 股财报、基本面与估值任务。

### 标准财报分析工作流

```text
财报获取 → PDF结构化解析 → 行业/方法论分析 → 按需保存结果
```

1. **cninfo-report-downloader** — 从巨潮资讯下载 A 股年报、季报、半年报 PDF
2. **financial-pdf-parser** — 将 PDF 解析为结构化文本、表格、校验报告和分析上下文
3. 按行业选择分析入口（见下表）
4. 用户需要时再保存 Markdown 报告，不强制产生文件副作用

> 所有分析 skill 优先接受 `financial-pdf-parser` 的输出目录，而非直接读取 PDF 长文本。
> 如 validation 存在失败项，相关数字必须标为"待核实"，不能静默引用。

### 工具与专项计算 skill

| Skill | 适用场景 |
|---|---|
| **cninfo-report-downloader** | 从巨潮资讯分页查询并下载指定类型的 A 股定期报告；校验 PDF、原子写入，并支持 TXT 转换回退 |
| **financial-pdf-parser** | 把财报 PDF 解析为结构化文本、表格、校验报告和分析上下文；单位与同表勾稽失败会显式告警 |
| **installment-cost-analysis** | 按借款人实际日期现金流计算 IRR/XIRR 和全部分期成本；原书简化式只作窄条件近似 |

### 行业与公司研究 skill

| Skill | 来源 | 内部能力数 | 适用场景 |
|---|---|---|---|
| **bank-comprehensive-analysis** | 《看透银行》价投谷子地 2021 | 8 | 银行商业模式、息差、信用、资本、流动性与条件化估值 |
| **insurance-comprehensive-analysis** | 《读懂保险股》东先生 2021 + 现行官方规则 | 7 | 保险服务/利润/CSM、投资、偿付能力、EV/VNB 与分红约束 |
| **consumer-analysis** | 《吴劲草讲消费行业》吴劲草 2022 | 6 | 消费企业模式、增长、品牌、渠道、供应链、财务与估值资格 |
| **healthcare-valuation** | 《医疗行业估值》郑华 & 涂宏钢 2020 + 现行制度 | 8 | 医疗机构经营预测、资本成本、DCF 与方法交叉验证 |
| **financial-statement-analysis** | 《七步读懂财务报表》 | 7 | 非金融企业三表联动、现金质量、周转、杠杆与异常分诊 |
| **peter-lynch-investment** | 《彼得·林奇的成功投资》 | 5 | 用增长/盈利机制分类、构造可证伪公司主线并复核退出理由 |

### 估值框架 skill

| Skill | 适用场景 |
|---|---|
| **investment-valuation-comprehensive-framework** | 资产、业务、项目、私人/控制权交易与并购的估值方法选择、价值和模型审计 |
| **equity-valuation-comprehensive-analysis** | 具名上市证券的稀释后每股价值、相对定价、反向 DCF 与市场隐含预期 |

---

## 元技能 (`meta/`)

### book2skill

本仓库唯一启用的图书蒸馏与重蒸馏入口。它从原始书稿建立来源清单、证据账本、公式契约和能力图；刷新旧 skill 时，先在不读取旧实现的条件下独立蒸馏并冻结，再做能力级对照、证据核验和 old/new/no-skill 匿名评测。候选只有在无阻断项且相对旧版不退化时才发布；失败结果会进入下一版回归，而不会被隐藏。

`meta/cangjie-skill` 固定为上游参考实现，目前版本为 v2.5.0。仓库吸收其 Capability Bundle、晋级门、single/compact-pack 和可回滚发布设计，但不同时安装两个同义入口，避免触发竞争与双线漂移。

---

## 安装

克隆本仓库后，在项目的 `.opencode/skills/`（或 `.agents/skills/`、`.dsh/skills/`）目录为需要启用的 skill 建立相对 symlink：

如需审查图书蒸馏上游实现，先初始化参考子模块：

```bash
git submodule update --init --recursive
```

```bash
ln -s /path/to/PersonalSkills/<category>/<skill-name> .opencode/skills/<skill-name>
```

重启 agent 框架即可发现。

`academic-defensive-writing-auditor` 也可直接通过 npx 安装：

```bash
npx academic-defensive-writing-auditor --dir ./.agents/skills
```

下载器的 TXT 转换可使用 `pdfplumber`，未安装时会尝试系统 `pdftotext`。使用完整 `financial-pdf-parser` 前需安装 Python 依赖：

```bash
python -m pip install pymupdf pymupdf4llm pdfplumber camelot-py opencv-python
```
