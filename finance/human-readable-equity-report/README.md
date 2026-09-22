# human-readable-equity-report

将证据完整的研究稿编辑为正式、清楚的中文读者版。支持单公司和Top10报告；随包包含编辑规范、模板、离线PDF导出器及小型测试。

## 包结构

```text
human-readable-equity-report/
├── SKILL.md
├── references/         编辑规范、调研和发布说明
├── templates/          公司/Top10写作模板、PDF样式
├── scripts/            离线导出器
├── tests/              语义、图片、字体、分页及文件保护测试
├── examples/           虚构数据的排版示例
└── requirements*.txt
```

技能目录可以整体复制或按宿主约定建立链接，不依赖原研究项目。相关金融分析skill位于同仓库的`finance/`下；本入口负责编辑与交付，新增分析按任务加载相应能力。

## 环境

- Python 3.10+；运行环境服从宿主项目约定。
- Python依赖：PyMuPDF、markdown-it-py、Pillow。
- 本地Chrome/Chromium；可使用`--chrome`明确指定可执行文件，或设置`CHROME_BIN`。
- 中文字体：推荐安装Noto CJK常规与粗体。默认正文使用Noto Serif CJK SC，标题使用Noto Sans CJK SC；样式可通过`--style`替换。

```bash
python -m pip install -r "$SKILL_DIR/requirements.txt"
```

工具本身不安装浏览器或字体、不调用LLM、不获取行情。Chrome使用独立临时用户目录，临时目录遵循系统及`TMPDIR`等标准设置，结束后自动清理。

## 使用

先将`SKILL_DIR`设置为本目录的实际路径，再准备已完成编辑的Markdown。示例命令可从任何工作目录执行：

```bash
SKILL_DIR="/path/to/PersonalSkills/finance/human-readable-equity-report"
mkdir -p ./reader_exports
python "$SKILL_DIR/scripts/export_reader_report.py" \
  --source "$SKILL_DIR/examples/reader-example.md" \
  --output-dir ./reader_exports \
  --title "示例企业｜排版示例" \
  --label "虚构数据 · 仅用于格式演示"
```

输出同名HTML、PDF、逐页PNG与`*.validation.json`。默认深度样式为连续段落及三线表；`<!-- pagebreak -->`可显式分页。

`--chrome "/path/to/browser"`指定浏览器；`--style /path/to/style.css`指定本地样式。

### 图表及链接

图片仅接受源稿目录内的相对PNG路径，跨目录或符号链接越界会报错。远程图片应先在原研究任务中获取并核对，导出器不下载。图题取自图片alt文字，并进入文本完整性检查。

引用链接使用绝对HTTP(S)地址、本地`file://`地址或文内锚点。公开分享时选择接收方可访问的来源；本地路径仅适用于对应机器。原始HTML和代码块不属于读者正文输入。

### 草稿和交付

- 默认拒绝覆盖已有输出。
- `--replace-draft`仅用于明确属于当前任务的未发布草稿；仍拒绝覆盖交付目录中的同名文件。
- `--documents-dir /path/to/delivery`可将PDF和Markdown复制到指定的现存目录。有PNG时，Markdown会内嵌图片，并核对渲染语义与原稿一致；阅读器需支持data URI图片。
- 完整尺寸阅读检查安排在用户交付前。首次可先省略`--documents-dir`，检查输出，再将所选版本保存到新的交付位置。

## 检查范围

自动检查可发现残留强调标记、缺失文本、未嵌入字形、缺少真实粗体、越界文本、无效图片和交付内容变化。220字段落提示仅作编辑参考。检查不证明财务结论正确，也不代替人工可读性验收。

## 测试

```bash
python -m pip install -r "$SKILL_DIR/requirements-dev.txt"
python -m pytest -q "$SKILL_DIR/tests"
```

测试只使用小型合成文本和本地图片。可用Chrome时运行真实PDF集成测试；未安装时明确跳过相关用例，不发起模型或网络调用。
