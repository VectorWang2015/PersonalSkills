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

DRL（深度强化学习）船舶控制类论文写作指南，覆盖动态定位（DP）、船舶保位、
轨迹跟踪，以及 *Ocean Engineering* / JMSE 相关论文的工程叙事与证据边界。

保留原有 6 篇 OE 及相关期刊的精读基础，并补充 **4 篇 JMSE 论文的定向章节核查**
（Shi & Liu 2020、Wang 2021、Zhu 2021、Gao 2024），不将定向检查等同于全文技术审计。
详见 [JMSE 范文结构、结尾篇幅与写作经验](academic/drl-marine-writing-skill/references/jmse-writing-evidence.md)。

覆盖摘要、引言、符号、方法、结果、讨论、结论与未来工作、术语、方程、表格、图形、
引用、单位、统计复现、常见审稿关注及章节组织/修改流程。新增重点包括：

- 核心学习方程与实际实现一致，不以算法名称替代机制解释；
- 从数字比较提炼工程发现，区分指令活动与能耗、观察与因果归因；
- 结论按“具体动机—方法贡献—定性结果—工程价值”收束；
- 未来方向由发现与未解决问题引出，可合并为 Conclusions and Future Work；
- 分章依据内容功能而非凑章节数，范文观察不等于期刊要求；
- 精确强调表格数值、保留统计口径，并编译检查实际页面。

证据分为 `[Sample]` 样本观察、`[Practice]` 通用惯例、`[Recommend]` 编辑建议。
JMSE 官方章节/篇幅要求尚未在此次核查中确认，投稿前仍需核对当前作者指南。
安装时请复制或链接**整个 skill 目录（含 references/）**；入口包含 name/description
frontmatter，可直接用于项目级 `.dsh/skills/` 安装。

---

## 金融类 (`finance/`)

包含财报获取/解析工具，以及从金融书籍独立重蒸馏并经匿名留出评测的分析方法，主要面向 A 股财报、基本面与估值任务。

### 标准财报分析工作流

```text
财报获取 → PDF结构化解析 → 行业/方法论分析 → 读者版编辑 → 按需交付
```

1. **cninfo-report-downloader** — 从巨潮资讯下载 A 股年报、季报、半年报 PDF
2. **financial-pdf-parser** — 将 PDF 解析为结构化文本、表格、校验报告和分析上下文
3. 按行业选择分析入口（见下表）
4. 用户需要报告时，用 **human-readable-equity-report** 按理解顺序编辑正文，并按需输出 Markdown / HTML / PDF；普通问答不强制产生文件

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

### 研究写作与交付 skill

| Skill | 适用场景 |
|---|---|
| **[human-readable-equity-report](finance/human-readable-equity-report/SKILL.md)** | 将已有研究编辑为正式、易理解的中文公司或Top10研报；解释具体因果、统一利润口径，提供模板及离线HTML/PDF导出 |

该入口经过三类公司试读反馈迭代，采用“业务—本期变化—原因—风险”的开篇顺序，将估值集中到专章。包内自带脚本、样式、依赖及小型测试，可整体复制安装。详见[安装与使用](finance/human-readable-equity-report/README.md)。

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
