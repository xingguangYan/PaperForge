#!/usr/bin/env python3
"""
PaperForge — manuscript writer.

Converts a `results` dict (paper metadata + figures + tables + references)
into three artifacts:

  * manuscript.md   (Markdown source of truth)
  * manuscript.html (styled, self-contained, browser-ready)
  * manuscript.docx (Word document with embedded figures)

The module is deliberately dependency-lenient:

  * `markdown`   → optional (used for HTML conversion when installed)
  * `python-docx` → optional (used for DOCX export when installed)

When a dependency is missing, PaperForge still writes the Markdown file and
prints exactly how to install the missing converter.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any, Dict, List

# --- Word counts ------------------------------------------------------------


def _wc(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text or ""))


def count_words(md: str, asian_multiplier: float = 1.0) -> int:
    """Approximate word count for a Markdown document.

    English words are counted as tokens, CJK characters are counted with
    `asian_multiplier` accounting for the dense nature of Chinese text.
    """
    en = len(re.findall(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", md or ""))
    zh = len(re.findall(r"[\u4e00-\u9fff]", md or ""))
    return int(en + zh * asian_multiplier)


# --- Core rendering ----------------------------------------------------------


def render_manuscript(results: Dict[str, Any]) -> str:
    """Render the full Markdown manuscript from a results dict."""
    title = results.get("title", "Untitled Study")
    abstract = results.get("abstract", "")
    keywords = results.get("keywords", [])
    sections = results.get("sections", [])
    figures = results.get("figures", [])
    tables = results.get("tables", [])
    references = results.get("references", [])

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## Abstract")
    lines.append("")
    lines.append(abstract.strip() or "_Abstract pending._")
    if keywords:
        lines.append("")
        lines.append("**Keywords:** " + "; ".join(keywords))
    lines.append("")

    for section in sections:
        heading = section.get("heading", "Section")
        level = section.get("level", 2)
        lines.append(f"{'#' * level} {heading}")
        lines.append("")
        lines.append(section.get("body", "").strip() or "_Content pending._")
        lines.append("")

    if figures:
        lines.append(f"{'#' * 2} Figures")
        lines.append("")
        for fig in figures:
            path = fig.get("path", "")
            alt = fig.get("alt", fig.get("caption", "figure"))
            lines.append(f"![{alt}]({path})")
            if fig.get("caption"):
                lines.append(f"*{fig['caption']}*")
            lines.append("")

    if tables:
        lines.append(f"{'#' * 2} Tables")
        lines.append("")
        for tb in tables:
            if tb.get("caption"):
                lines.append(f"**{tb['caption']}**")
                lines.append("")
            lines.append(render_md_table(tb.get("headers", []), tb.get("rows", [])))
            lines.append("")

    if references:
        lines.append(f"{'#' * 2} References")
        lines.append("")
        for i, ref in enumerate(references, 1):
            lines.append(f"[{i}] {ref}")
        lines.append("")

    return "\n".join(lines) + "\n"


def render_manifest(results: Dict[str, Any]) -> str:
    """Alias for render_manuscript (used by tests / external callers)."""
    return render_manuscript(results)


def render_md_table(headers: List[str], rows: List[List[Any]]) -> str:
    """Render a Markdown table from headers and rows."""
    if not headers:
        return ""
    hdr = "| " + " | ".join(str(h) for h in headers) + " |"
    sep = "|" + "---|" * len(headers)
    body = "\n".join(
        "| " + " | ".join(str(c) for c in row) + " |" for row in rows
    )
    return f"{hdr}\n{sep}\n{body}"


def render_gb_reference(entry: Dict[str, str]) -> str:
    """Render one reference in GB/T 7714 style (author. title[J]. journal, year)."""
    author = entry.get("author", "")
    title = entry.get("title", "")
    journal = entry.get("journal", "")
    year = entry.get("year", "")
    return f"{author}. {title}[J]. {journal}, {year}."


def render_apa_reference(entry: Dict[str, str]) -> str:
    """Render one reference in APA (7th) style."""
    author = entry.get("author", "")
    year = entry.get("year", "")
    title = entry.get("title", "")
    journal = entry.get("journal", "")
    return f"{author} ({year}). {title}. *{journal}*."


# --- HTML -------------------------------------------------------------------


def _inline_css() -> str:
    return """
    <style>
      :root { color-scheme: light; }
      body { margin: 0 auto; max-width: 820px; padding: 40px 24px 80px;
             font-family: 'Segoe UI', -apple-system, 'Helvetica Neue', Arial,
             'PingFang SC', 'Microsoft YaHei', sans-serif; line-height: 1.7;
             color: #1a1d26; background: #fbfbfc; }
      h1 { font-size: 2em; border-bottom: 2px solid #e8b324; padding-bottom: .4em; }
      h2 { margin-top: 2em; border-bottom: 1px solid #e3e5ea; padding-bottom: .3em; }
      h3 { color: #33415c; }
      img { max-width: 100%; border: 1px solid #e5e7ec; border-radius: 8px; }
      table { border-collapse: collapse; width: 100%; margin: 1em 0; }
      th, td { border: 1px solid #d8dbe2; padding: 8px 10px; text-align: left; }
      th { background: #f0f2f6; }
      em img + * { color: #555; font-size: .9em; }
      figure { margin: 1.5em 0; }
      figcaption { color: #667; font-size: .9em; margin-top: .5em; }
      blockquote { border-left: 3px solid #e8b324; margin: 1em 0; padding: .2em 1em;
                   background: #fff8e6; color: #444; }
      code { background: #eef1f5; padding: 2px 5px; border-radius: 4px; }
      pre { background: #10131c; color: #d7dce6; padding: 14px; border-radius: 8px;
            overflow-x: auto; }
      @media print { body { max-width: none; } }
    </style>
    """


def render_html(manuscript_md: str, title: str = "PaperForge Manuscript") -> str:
    """Convert Markdown → styled standalone HTML, with graceful degradation."""
    body_html = _md_to_html(manuscript_md)
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        f"<meta charset=\"utf-8\"/>\n"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>\n"
        f"<title>{_escape(title)}</title>\n{_inline_css()}\n</head>\n<body>\n"
        f"{body_html}\n</body>\n</html>\n"
    )


def _escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _md_to_html(md: str) -> str:
    """Convert Markdown to HTML using python-markdown when available."""
    try:
        import markdown as md_mod  # type: ignore

        return md_mod.markdown(
            md,
            extensions=["extra", "tables", "sane_lists", "codehilite", "toc"],
        )
    except ImportError:
        # Minimal fallback: paragraphs, headings, images, bold, tables.
        html_lines: List[str] = []
        in_code = False
        for raw in md.splitlines():
            line = raw.rstrip()
            if line.startswith("```"):
                in_code = not in_code
                html_lines.append("</pre>" if not in_code else "<pre><code>")
                continue
            if in_code:
                html_lines.append(_escape(line))
                continue
            if not line.strip():
                continue
            m = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m:
                level = len(m.group(1))
                html_lines.append(f"<h{level}>{_inline_md(m.group(2))}</h{level}>")
            elif line.startswith("|"):
                html_lines.append(_inline_md(line))
            elif line.startswith("!["):
                m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
                if m:
                    html_lines.append(
                        f'<img src="{m.group(2)}" alt="{_escape(m.group(1))}"/>'
                    )
            else:
                html_lines.append(f"<p>{_inline_md(line)}</p>")
        if in_code:
            html_lines.append("</pre>")
        return "\n".join(html_lines)


def _inline_md(text: str) -> str:
    text = _escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# --- DOCX -------------------------------------------------------------------


def render_docx(
    manuscript_md: str,
    out_path: str,
    results: Dict[str, Any],
    title: str = "PaperForge Manuscript",
) -> bool:
    """Write a Word document with figures embedded. Returns success flag."""
    try:
        import docx  # type: ignore
        from docx.shared import Inches, Pt
    except ImportError:
        return False

    document = docx.Document()
    core = document.core_properties
    core.title = title
    core.author = results.get("author", "PaperForge")

    for p_idx, block in enumerate(_iter_md_blocks(manuscript_md)):
        kind, text = block
        text = text.strip()
        if not text:
            continue
        # Skip raw HTML / frontmatter debris
        if text.startswith("---"):
            continue
        if kind == "heading":
            level = len(text.split(" ", 1)[0]) if text.startswith("#") else 1
            level = max(1, min(level, 6))
            document.add_heading(_strip_heading(text), level=level)
        elif kind == "image":
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", text)
            if m:
                img_path = m.group(2)
                if os.path.exists(img_path):
                    try:
                        document.add_picture(img_path, width=Inches(6.0))
                    except Exception:
                        document.add_paragraph(f"[Figure: {m.group(1)}]")
                else:
                    document.add_paragraph(f"[Missing figure: {img_path}]")
        elif kind.startswith("table"):
            rows = _parse_md_table(text.splitlines())
            if rows:
                tbl = document.add_table(rows=0, cols=len(rows[0]))
                tbl.style = "Light Grid Accent 1" if "Light Grid Accent 1" in [s.name for s in document.styles] else None
                for r in rows:
                    cells = tbl.add_row().cells
                    for i, cell in enumerate(r):
                        cells[i].text = str(cell)
        else:
            document.add_paragraph(text)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    document.save(out_path)
    return True


def _strip_heading(text: str) -> str:
    return re.sub(r"^#+\s*", "", text).strip()


def _iter_md_blocks(md: str):
    """Yield (kind, text) blocks: heading, image, table, or text paragraph."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("#"):
            yield ("heading", line)
            i += 1
            continue
        if line.startswith("!["):
            yield ("image", line)
            i += 1
            continue
        if line.startswith("|"):
            table = [line]
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                table.append(lines[j].rstrip())
                j += 1
            yield ("table", "\n".join(table))
            i = j
            continue
        # accumulate consecutive text lines into one paragraph
        para = [line]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].rstrip()
            if (
                not nxt.strip()
                or nxt.startswith("#")
                or nxt.startswith("![")
                or nxt.startswith("|")
                or nxt.startswith("```")
            ):
                break
            para.append(nxt)
            j += 1
        yield ("text", " ".join(para).replace("*", "").replace("`", ""))
        i = j


def _parse_md_table(lines: List[str]):
    rows = []
    for line in lines:
        if re.match(r"^\s*\|?\s*:?-{2,}", line):
            continue  # separator row
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and any(cells):
            rows.append(cells)
    return rows


# --- Convenience -------------------------------------------------------------


def write_outputs(results: Dict[str, Any], out_dir: str) -> Dict[str, str]:
    """Write manuscript.md/.html/.docx into out_dir. Returns a path map."""
    os.makedirs(out_dir, exist_ok=True)
    md = render_manuscript(results)
    title = results.get("title", "PaperForge Manuscript")

    paths: Dict[str, str] = {}
    md_path = os.path.join(out_dir, "manuscript.md")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
    paths["md"] = md_path

    html_path = os.path.join(out_dir, "manuscript.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(render_html(md, title))
    paths["html"] = html_path

    docx_path = os.path.join(out_dir, "manuscript.docx")
    if render_docx(md, docx_path, results, title):
        paths["docx"] = docx_path
    else:
        print(
            "  ⚠️  python-docx is not installed; manuscript.docx was skipped.\n"
            "     Install it with: pip install python-docx"
        )

    stats = {
        "word_count_est": count_words(md),
        "bytes": os.path.getsize(md_path),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    stat_path = os.path.join(out_dir, "manuscript_stats.json")
    import json

    with open(stat_path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    paths["stats"] = stat_path
    return paths
