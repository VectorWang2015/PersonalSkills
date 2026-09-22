"""Render edited Chinese research offline and check text, figures and typography."""

import argparse
import base64
import html
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

import fitz
from markdown_it import MarkdownIt
from markdown_it.rules_inline import image as parse_image
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    """Normalize PDF spacing without deleting visible punctuation.

    :param text: Input text.
    :return: Comparable text.
    """
    return re.sub(r"[\s\u200b\u00ad]", "", unicodedata.normalize("NFKC", text))


def inline_text(token):
    """Extract rendered inline text from a Markdown token.

    :param token: Inline token.
    :return: Visible text.
    """
    return "".join(inline_text(c) if c.type == "image" else c.content if c.type in ("text", "code_inline") else " "
                   if c.type in ("softbreak", "hardbreak") else ""
                   for c in token.children or [])


def png_data_uri(src, asset_root):
    """Read a source-root-relative PNG without following escaping symlinks.

    :param src: Markdown image destination.
    :param asset_root: Allowed local source directory.
    :return: Self-contained PNG data URI.
    """
    url = urlsplit(src)
    name = unquote(url.path)
    if (asset_root is None or url.scheme or url.netloc or url.query or url.fragment
            or not name or "\\" in name or Path(name).is_absolute()):
        raise ValueError("Figures must be source-root-relative local PNG files")
    root = Path(asset_root).resolve()
    path = (root / name).resolve()
    if not path.is_relative_to(root) or path.suffix.lower() != ".png":
        raise ValueError("PNG figure path escapes asset root or is not a PNG")
    try:
        data = path.read_bytes()
        with Image.open(io.BytesIO(data)) as image:
            if image.format != "PNG":
                raise ValueError("Not a PNG")
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as error:
        raise ValueError(f"Invalid PNG figure: {src}") from error
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def build_html(markdown, title, label, css, asset_root=None):
    """Build semantic HTML and report source text units and editorial warnings.

    :param markdown: Edited Markdown source.
    :param title: Document title.
    :param label: Dated running label.
    :param css: Local stylesheet contents.
    :param asset_root: Optional directory containing relative PNG figures.
    :return: HTML, expected text units, and readability warnings.
    """
    return _build_report(markdown, title, label, css, asset_root)[:3]


def _build_report(markdown, title, label, css, asset_root, embedded=None):
    """Build HTML and portable Markdown with explicitly trusted embedded figures.

    :param markdown: Source Markdown.
    :param title: Document title.
    :param label: Running label.
    :param css: Stylesheet text.
    :param asset_root: Local figure root.
    :param embedded: Internal allowlist of previously validated PNG data URIs.
    :return: HTML, text units, warnings, portable Markdown and validated URI set.
    """
    parser = MarkdownIt("commonmark", {"html": False}).enable("table")
    standard_link_validator = parser.validateLink
    parser.validateLink = lambda url: url.startswith("file://") or standard_link_validator(url)
    replacements, validated = {}, set()

    def local_image(state, silent):
        start = state.pos
        if not parse_image(state, silent):
            return False
        if not silent:
            token = state.tokens[-1]
            src = token.attrGet("src") or ""
            uri = src if embedded is not None and src in embedded else png_data_uri(src, asset_root)
            token.attrSet("src", uri)
            validated.add(uri)
            title_text = token.attrGet("title")
            suffix = (' "' + re.sub(r'([\\"])', r'\\\1', html.escape(title_text, quote=False))
                      + '"') if title_text else ""
            replacements[state.src[start:state.pos]] = f"![{token.content}](<{uri}>{suffix})"
        return True

    def render_image(tokens, index, options, env):
        token = tokens[index]
        caption = inline_text(token)
        token.attrSet("alt", caption)
        token.attrSet("style", "max-width:100%;max-height:85mm;object-fit:contain")
        image = parser.renderer.renderToken(tokens, index, options, env)
        return ('<span class="figure" style="display:inline-block;max-width:100%;break-inside:avoid">'
                + image + '<span class="figure-caption" style="display:block">'
                + html.escape(caption) + '</span></span>')

    parser.inline.ruler.at("image", local_image)
    parser.renderer.rules["image"] = render_image
    sections, units, warnings = [], [], []
    for section in re.split(r"(?m)^<!-- pagebreak -->\s*$", markdown):
        if not section.strip():
            continue
        tokens = parser.parse(section)
        for i, token in enumerate(tokens):
            if token.type in ("html_block", "html_inline", "fence", "code_block"):
                raise ValueError("Reader reports do not accept raw HTML or code blocks")
            if token.type != "inline":
                continue
            visible = inline_text(token)
            for child in token.children or []:
                if child.type == "text" and ("**" in child.content or "__" in child.content
                                               or re.search(r"</?[A-Za-z][^>]*>", child.content)):
                    raise ValueError("Unrendered emphasis/HTML; use **总结**：正文 and real paragraphs")
                if child.type == "link_open":
                    href = child.attrGet("href") or ""
                    if not href.startswith(("https://", "http://", "#", "file://")):
                        raise ValueError("Use absolute source links or document anchors")
            if visible:
                units.append(visible)
            if i and tokens[i-1].type == "paragraph_open":
                if len(normalize(visible)) > 220:
                    warnings.append("Long paragraph: " + visible[:65])
                if visible.startswith(("来源：", "说明：", "编辑日期：")):
                    tokens[i-1].attrSet("class", "note")
        sections.append('<section class="report-section">' + parser.renderer.render(tokens, parser.options, {}) + '</section>')
    if not units:
        raise ValueError("Empty report")
    document = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
                '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src data:; style-src \'unsafe-inline\'; font-src \'self\'">'
                f'<title>{html.escape(title)}</title><style>{css}</style></head><body>'
                f'<header>{html.escape(label)}</header>' + "\n".join(sections) + '</body></html>')
    portable = markdown
    if replacements:
        pattern = "|".join(re.escape(key) for key in sorted(replacements, key=len, reverse=True))
        portable = re.sub(pattern, lambda match: replacements[match.group()], markdown)
    return document, units, warnings, portable, validated


def check_pdf(path, units, label):
    """Verify visible text, embedded glyphs, real bold type and page bounds.

    :param path: Rendered PDF path.
    :param units: Expected visible text units.
    :param label: Repeated print label to omit from comparisons.
    :return: Focused automated verification record.
    """
    with fitz.open(path) as pdf:
        texts = [normalize(p.get_text()).replace(normalize(label), "") for p in pdf]
        joined = "".join(texts)
        body = "".join(normalize(p.get_textbox(fitz.Rect(35, 30, p.rect.width-35, p.rect.height-40)))
                       .replace(normalize(label), "") for p in pdf)
        missing = [u for u in units if normalize(u) not in joined and normalize(u) not in body]
        if missing:
            raise ValueError("Missing rendered text: " + repr(missing[:3]))
        fonts = set()
        for page in pdf:
            for font in page.get_fonts():
                if font[2] == "Type3":
                    # Chrome embeds CJK CFF outlines as named Type3 glyph programs.
                    descriptor = pdf.xref_get_key(font[0], "FontDescriptor")
                    if descriptor[0] != "xref":
                        raise ValueError("Type3 font lacks a named descriptor")
                    descriptor_id = int(descriptor[1].split()[0])
                    fonts.add(pdf.xref_get_key(descriptor_id, "FontName")[1])
                    kind, programs = pdf.xref_get_key(font[0], "CharProcs")
                    if kind == "xref":
                        programs = pdf.xref_object(int(programs.split()[0]))
                    refs = re.findall(r"(\d+) 0 R", programs)
                    if not refs or not all(pdf.xref_stream(int(ref)) for ref in refs):
                        raise ValueError("Missing embedded Type3 glyph programs")
                else:
                    fonts.add(font[3])
                    if not pdf.extract_font(font[0])[3]:
                        raise ValueError("Unembedded font")
        if not any("Bold" in name or "Black" in name for name in fonts):
            raise ValueError("No real bold font embedded")
        for number, page in enumerate(pdf, 1):
            if "**" in page.get_text():
                raise ValueError("Visible Markdown emphasis markers")
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        box = fitz.Rect(span["bbox"])
                        if box.x0 < 20 or box.x1 > page.rect.width-20 or box.y0 < 15 or box.y1 > page.rect.height-15:
                            raise ValueError(f"Out-of-page text on page {number}: {span['text']}")
        return dict(pages=len(pdf), text_units_checked=len(units), missing_text_units=0,
                    embedded_fonts=sorted(fonts), bold_font_verified=True, page_bounds="passed",
                    visual_review="pending_actual_size_reading")


def find_chrome(explicit=None):
    """Resolve a configured browser or a common executable on PATH.

    :param explicit: Optional executable name or path supplied by the caller.
    :return: Browser path, or None when unavailable.
    """
    configured = explicit or os.environ.get("CHROME_BIN")
    if configured:
        return str(Path(configured).expanduser())
    return next((found for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")
                 if (found := shutil.which(name))), None)


def export(source, output_dir, title, label, documents_dir=None, chrome=None, replace_draft=False, style=None):
    """Export an edited report using an isolated local Chrome profile.

    :param source: Existing edited Markdown path.
    :param output_dir: Existing output directory.
    :param title: Report title.
    :param label: Financial and market date label.
    :param documents_dir: Optional existing delivery directory.
    :param chrome: Optional Chrome executable; CHROME_BIN and PATH are fallbacks.
    :param replace_draft: Explicitly replace known unpublished output artifacts.
    :param style: Optional CSS path; defaults to the bundled depth stylesheet.
    :return: Verification record with output paths.
    """
    source, output_dir = Path(source).expanduser().resolve(), Path(output_dir).expanduser().resolve()
    if not output_dir.is_dir():
        raise ValueError("Output parent must already exist")
    paths = {ext: output_dir / (source.stem + "." + ext) for ext in ("html", "pdf", "validation.json")}
    if any(p.exists() for p in paths.values()) and not replace_draft:
        raise FileExistsError("Use a new output name/directory; existing reports are preserved")
    delivery = Path(documents_dir).expanduser().resolve() if documents_dir else None
    if delivery and (not delivery.is_dir() or any((delivery/(source.stem+ext)).exists() for ext in (".md", ".pdf"))):
        raise FileExistsError("Delivery directory missing or destination exists")
    css = Path(style or ROOT / "templates/research_depth.css").expanduser().read_text(encoding="utf-8")
    document, units, warnings, portable, validated = _build_report(
        source.read_text(encoding="utf-8"), title, label, css, source.parent)
    if delivery and validated:
        delivered = _build_report(portable, title, label, css, None, embedded=validated)
        if delivered[:3] != (document, units, warnings) or delivered[4] != validated:
            raise ValueError("Portable Markdown differs from original semantic content")
    binary = find_chrome(chrome)
    if not binary:
        raise RuntimeError("Local Chrome/Chromium is required; set --chrome or CHROME_BIN")
    paths["html"].write_text(document, encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="reader-chrome-") as profile:
        command = [binary, "--headless", "--disable-gpu", "--disable-background-networking", "--disable-extensions",
                   "--no-first-run", "--no-default-browser-check", "--no-pdf-header-footer",
                   "--virtual-time-budget=1500", f"--user-data-dir={profile}",
                   f"--print-to-pdf={paths['pdf']}", paths["html"].as_uri()]
        subprocess.run(command, check=True, capture_output=True, timeout=90)
    result = check_pdf(paths["pdf"], units, label)
    result.update(source=str(source), html=str(paths["html"]), pdf=str(paths["pdf"]), readability_warnings=warnings,
                  title=title, label=label, network_acquisition=False)
    with fitz.open(paths["pdf"]) as pdf:
        for i, page in enumerate(pdf, 1):
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(output_dir / f"{source.stem}_page{i}.png")
    if delivery:
        for original in (source, paths["pdf"]):
            destination = delivery / original.name
            content = portable.encode("utf-8") if original == source and validated else original.read_bytes()
            with destination.open("xb") as target:
                target.write(content)
            if destination.read_bytes() != content:
                raise ValueError("Delivery copy differs")
        result["documents_pdf"] = str(delivery / paths["pdf"].name)
        result["documents_markdown"] = str(delivery / source.name)
    paths["validation.json"].write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return result


def main():
    """Parse CLI options and print the automated verification record."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--documents-dir", type=Path)
    parser.add_argument("--style", type=Path, help="Optional local CSS stylesheet")
    parser.add_argument("--chrome", help="Chrome/Chromium executable path or name")
    parser.add_argument("--replace-draft", action="store_true", help="Replace known task-local drafts; never overwrite delivered files")
    args = parser.parse_args()
    print(json.dumps(export(**vars(args)), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
