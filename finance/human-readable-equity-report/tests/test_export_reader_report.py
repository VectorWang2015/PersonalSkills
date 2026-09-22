"""Behavioral checks for portable reader-report semantics and PDF typography."""

import base64
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import fitz
import pytest
from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts/export_reader_report.py"
SPEC = importlib.util.spec_from_file_location("reader_export", SCRIPT)
reader = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reader)


def test_bold_paragraphs_and_table_are_semantic():
    rendered, units, warnings = reader.build_html(
        "# 标题\n\n**结论**：增长降速。\n\n第二段。\n\n|指标|同比|\n|---|---:|\n|收入|14.51%|", "标题", "2026H1", "")
    assert "<strong>结论</strong>" in rendered
    assert "<p>第二段。</p>" in rendered
    assert "<table>" in rendered and "<thead>" in rendered
    assert "14.51%" in units and not warnings


def test_broken_chinese_emphasis_is_rejected_not_stripped():
    with pytest.raises(ValueError, match="Unrendered emphasis"):
        reader.build_html("**判断：**增长。", "标题", "日期", "")


def test_pagebreak_is_structural_and_raw_html_rejected():
    rendered, _, _ = reader.build_html("第一页\n\n<!-- pagebreak -->\n\n第二页", "标题", "日期", "")
    assert rendered.count('class="report-section"') == 2
    assert "<!-- pagebreak -->" not in rendered
    with pytest.raises(ValueError):
        reader.build_html("<script>alert(1)</script>", "标题", "日期", "")


def test_dense_paragraph_warns_without_changing_facts():
    paragraph = "这是一段需要编辑的长文字。" * 25
    _, units, warnings = reader.build_html(paragraph, "标题", "日期", "")
    assert units == [paragraph] and warnings


def test_local_source_link_keeps_label_not_raw_markdown():
    rendered, units, _ = reader.build_html("[完整底稿](file:///tmp/研究.md)", "标题", "日期", "")
    assert units == ["完整底稿"]
    assert 'href="file:///tmp/' in rendered
    assert '[完整底稿]' not in rendered


def test_missing_pdf_text_is_not_a_pass(tmp_path):
    path = tmp_path / "missing.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((60, 60), "Only one fact")
    doc.save(path)
    doc.close()
    with pytest.raises(ValueError, match="Missing rendered text"):
        reader.check_pdf(path, ["A missing claim"], "")


def test_existing_export_is_preserved(tmp_path):
    source = tmp_path / "report.md"
    source.write_text("# 报告\n\n**结论**：原文。", encoding="utf-8")
    previous = tmp_path / "report.pdf"
    previous.write_bytes(b"previous report")
    with pytest.raises(FileExistsError):
        reader.export(source, tmp_path, "标题", "日期")
    assert previous.read_bytes() == b"previous report"


@pytest.mark.skipif(not reader.find_chrome(), reason="Local Chrome unavailable")
def test_chinese_pdf_preserves_bold_table_and_pagebreak(tmp_path):
    source = tmp_path / "sample.md"
    source.write_text("# 中文阅读样例\n\n> **增长仍在，但速度下降。**\n\n第一段解释变化。\n\n第二段说明盈利影响。\n\n|指标|同比|\n|---|---:|\n|收入|14.51%|\n\n<!-- pagebreak -->\n\n## 风险与观察\n\n**观察重点**：净新增患者与经营现金。", encoding="utf-8")
    result = reader.export(source, tmp_path, "阅读样例", "财务2026H1")
    assert result["pages"] == 2
    assert result["bold_font_verified"] and not result["readability_warnings"]
    assert result["missing_text_units"] == 0


@pytest.fixture
def figure(tmp_path):
    path = tmp_path / "图 1.png"
    Image.new("RGB", (160, 80), (30, 90, 140)).save(path)
    return path


def test_local_png_caption_and_source_are_visible(figure):
    rendered, units, _ = reader.build_html(
        '![图1：收入 **14.51%**](<图 1.png>)\n\n来源：公司中报。',
        "标题", "日期", "", asset_root=figure.parent)
    assert 'img-src data:' in rendered
    assert '<span class="figure-caption" style="display:block">图1：收入 14.51%</span>' in rendered
    assert units == ["图1：收入 14.51%", "来源：公司中报。"]
    assert '<p class="note">来源：公司中报。</p>' in rendered
    encoded = re.search(r'src="data:image/png;base64,([^"]+)"', rendered).group(1)
    assert base64.b64decode(encoded) == figure.read_bytes()


@pytest.mark.parametrize("destination", [
    "https://example.com/a.png", "//example.com/a.png", "file:///tmp/a.png",
    "/tmp/a.png", "../outside.png", "%2e%2e/outside.png",
    "data:image/png;base64,AAAA", "图%201.png?download=1", "图%201.png#fragment", "missing.png",
])
def test_unsafe_image_destinations_are_rejected(figure, destination):
    with pytest.raises(ValueError):
        reader.build_html(f"![图]({destination})", "标题", "日期", "", figure.parent)


def test_symlink_escape_and_missing_asset_root_are_rejected(figure, tmp_path):
    root = tmp_path / "assets"
    root.mkdir()
    (root / "escape.png").symlink_to(figure)
    with pytest.raises(ValueError, match="escapes"):
        reader.build_html("![图](escape.png)", "标题", "日期", "", root)
    with pytest.raises(ValueError, match="source-root-relative"):
        reader.build_html("![图](figure.png)", "标题", "日期", "")


@pytest.mark.parametrize("kind", ["text", "jpeg", "truncated"])
def test_bad_png_is_rejected(tmp_path, kind):
    path = tmp_path / "bad.png"
    if kind == "jpeg":
        Image.new("RGB", (10, 10)).save(path, format="JPEG")
    elif kind == "truncated":
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"broken")
    else:
        path.write_text("<script>alert(1)</script>", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid PNG"):
        reader.build_html("![图](bad.png)", "标题", "日期", "", tmp_path)


def test_caption_cannot_inject_html(figure):
    rendered, units, _ = reader.build_html(
        '![<script>alert(1)</script>](<图 1.png>)', "标题", "日期", "", figure.parent)
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert units == ["<script>alert(1)</script>"]


@pytest.mark.skipif(not reader.find_chrome(), reason="Local Chrome unavailable")
def test_png_survives_chrome_pdf_and_portable_delivery(figure, tmp_path):
    source = tmp_path / "figure_report.md"
    markdown = '# 中文图表报告\n\n**结论**：收入增长14.51%。\n\n![图1：收入14.51%][chart]\n\n来源：公司中报。\n\n[chart]: <图 1.png> "经营图表"\n'
    source.write_text(markdown, encoding="utf-8")
    delivery = tmp_path / "Documents"
    delivery.mkdir()
    style = reader.ROOT / "templates/research_depth.css"
    result = reader.export(source, tmp_path, "阅读样例", "财务2026H1", documents_dir=delivery, style=style)
    assert result["missing_text_units"] == 0 and result["bold_font_verified"]
    with fitz.open(result["pdf"]) as pdf:
        images = [image for page in pdf for image in page.get_images(full=True)]
        assert any(image[2:4] == (160, 80) for image in images)
        assert any(page.get_image_rects(image[0]) for page in pdf for image in page.get_images())
        assert any("图1：收入14.51%" in page.get_text() for page in pdf)
    delivered = (delivery / source.name).read_text(encoding="utf-8")
    assert "data:image/png;base64," in delivered
    assert "收入增长14.51%" in delivered and "来源：公司中报。" in delivered
    assert source.read_text(encoding="utf-8") == markdown
    assert (delivery / "figure_report.pdf").read_bytes() == Path(result["pdf"]).read_bytes()
    original = reader.build_html(markdown, "阅读样例", "财务2026H1", style.read_text(encoding="utf-8"), tmp_path)
    uris = set(re.findall(r"data:image/png;base64,[A-Za-z0-9+/=]+", delivered))
    portable = reader._build_report(delivered, "阅读样例", "财务2026H1", style.read_text(encoding="utf-8"), None, embedded=uris)
    assert portable[:3] == original
    assert "Noto Serif CJK SC" in Path(result["html"]).read_text(encoding="utf-8")
    with pytest.raises(FileExistsError, match="destination exists"):
        reader.export(source, tmp_path, "标题", "日期", documents_dir=delivery, replace_draft=True)
    assert (delivery / source.name).read_text(encoding="utf-8") == delivered


def test_portable_rewrite_refuses_semantic_changes(figure, tmp_path):
    source = tmp_path / "ambiguous.md"
    source.write_text('# 标题\n\n![图](<图 1.png>)\n\n`![图](<图 1.png>)`', encoding="utf-8")
    delivery = tmp_path / "Documents"
    delivery.mkdir()
    with pytest.raises(ValueError, match="semantic content"):
        reader.export(source, tmp_path, "标题", "日期", documents_dir=delivery)
    assert not list(delivery.iterdir())


def test_portable_images_preserve_title_entities_and_alt_markup(figure):
    markdown = '![图 **14.51%**](<图 1.png> "Literal &amp;amp; and &quot;quote&quot;")'
    original = reader._build_report(markdown, "标题", "日期", "", figure.parent)
    portable = reader._build_report(original[3], "标题", "日期", "", None, embedded=original[4])
    assert original[:3] == portable[:3]


def test_explicit_browser_takes_precedence(monkeypatch):
    monkeypatch.setenv("CHROME_BIN", "/environment/browser")
    assert reader.find_chrome("/explicit/browser") == "/explicit/browser"
    assert reader.find_chrome() == "/environment/browser"


def test_common_browser_names_and_missing_browser(monkeypatch):
    monkeypatch.delenv("CHROME_BIN", raising=False)
    monkeypatch.setattr(reader.shutil, "which", lambda name: "/bin/chromium-browser" if name == "chromium-browser" else None)
    assert reader.find_chrome() == "/bin/chromium-browser"
    monkeypatch.setattr(reader.shutil, "which", lambda name: None)
    assert reader.find_chrome() is None


@pytest.mark.skipif(not reader.find_chrome(), reason="Local Chrome unavailable")
def test_isolated_skill_cli_works_outside_repository(tmp_path):
    isolated = tmp_path / "copied skill"
    (isolated / "scripts").mkdir(parents=True)
    (isolated / "templates").mkdir()
    shutil.copyfile(SCRIPT, isolated / "scripts/export_reader_report.py")
    shutil.copyfile(SKILL / "templates/research_depth.css", isolated / "templates/research_depth.css")
    source = tmp_path / "中文示例.md"
    source.write_text("# 独立目录示例\n\n**关键判断**：文字和金额保持完整。\n\n|指标|值|\n|---|---:|\n|收入|12.34亿元|", encoding="utf-8")
    output = tmp_path / "out"
    output.mkdir()
    result = subprocess.run([sys.executable, "-B", str(isolated / "scripts/export_reader_report.py"),
                             "--source", str(source), "--output-dir", str(output),
                             "--title", "独立运行", "--label", "合成测试", "--chrome", reader.find_chrome()],
                            cwd=tmp_path, capture_output=True, text=True, check=True, timeout=110)
    receipt = json.loads(result.stdout)
    assert receipt["missing_text_units"] == 0 and receipt["bold_font_verified"]
    assert receipt["pages"] == 1
    assert "Noto Serif CJK SC" in (output / "中文示例.html").read_text(encoding="utf-8")
