from __future__ import annotations

import html
import re
from pathlib import Path

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS
OUT.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#13263A")
BLUE = colors.HexColor("#22577A")
GREEN = colors.HexColor("#2A9D6F")
AMBER = colors.HexColor("#E6A23C")
IVORY = colors.HexColor("#F7F4ED")
INK = colors.HexColor("#1A252F")
MUTED = colors.HexColor("#596773")
LINE = colors.HexColor("#D8E0E6")


def register_fonts() -> None:
    base = Path("/usr/share/fonts/truetype/dejavu")
    pdfmetrics.registerFont(TTFont("DejaVu", str(base / "DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(base / "DejaVuSans-Bold.ttf")))
    pdfmetrics.registerFont(TTFont("DejaVu-Mono", str(base / "DejaVuSansMono.ttf")))


def inline(text: str) -> str:
    text = text.replace("(TM)", "™")
    code_spans = []
    def save_code(match):
        code_spans.append(match.group(1))
        return f"@@CODE{len(code_spans) - 1}@@"
    text = re.sub(r"`([^`]+)`", save_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    for index, code in enumerate(code_spans):
        text = text.replace(f"@@CODE{index}@@", f'<font name="DejaVu-Mono">{html.escape(code)}</font>')
    return text


def styles():
    s = getSampleStyleSheet()
    return {
        "h1": ParagraphStyle("h1", parent=s["Title"], fontName="DejaVu-Bold", fontSize=27, leading=31, textColor=NAVY, spaceAfter=12),
        "h2": ParagraphStyle("h2", parent=s["Heading2"], fontName="DejaVu-Bold", fontSize=16, leading=20, textColor=BLUE, spaceBefore=12, spaceAfter=7, keepWithNext=True),
        "h3": ParagraphStyle("h3", parent=s["Heading3"], fontName="DejaVu-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("body", parent=s["BodyText"], fontName="DejaVu", fontSize=8.6, leading=12.2, textColor=INK, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", parent=s["BodyText"], fontName="DejaVu", fontSize=8.4, leading=11.5, leftIndent=14, firstLineIndent=-7, bulletIndent=5, textColor=INK, spaceAfter=3),
        "quote": ParagraphStyle("quote", parent=s["BodyText"], fontName="DejaVu-Bold", fontSize=12, leading=17, leftIndent=18, rightIndent=18, textColor=NAVY, borderColor=GREEN, borderWidth=0, borderPadding=8, backColor=IVORY, spaceBefore=8, spaceAfter=10),
        "small": ParagraphStyle("small", parent=s["BodyText"], fontName="DejaVu", fontSize=7.2, leading=9.5, textColor=MUTED, spaceAfter=3),
        "code": ParagraphStyle("code", parent=s["Code"], fontName="DejaVu-Mono", fontSize=7.6, leading=10, textColor=NAVY, backColor=colors.HexColor("#EEF3F7"), borderPadding=5, spaceAfter=6),
        "cover_title": ParagraphStyle("cover_title", fontName="DejaVu-Bold", fontSize=31, leading=36, textColor=colors.white, alignment=TA_LEFT, spaceAfter=12),
        "cover_sub": ParagraphStyle("cover_sub", fontName="DejaVu", fontSize=15, leading=21, textColor=colors.HexColor("#DDEAF2"), spaceAfter=18),
        "cover_meta": ParagraphStyle("cover_meta", fontName="DejaVu", fontSize=9.5, leading=14, textColor=colors.HexColor("#DDEAF2")),
        "table": ParagraphStyle("table", fontName="DejaVu", fontSize=6.8, leading=8.8, textColor=INK),
        "table_head": ParagraphStyle("table_head", fontName="DejaVu-Bold", fontSize=6.8, leading=8.8, textColor=colors.white),
    }


def cover(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(GREEN)
    canvas.rect(0, h - 18, w, 18, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#203D55"))
    canvas.circle(w - 45, 55, 130, fill=1, stroke=0)
    canvas.restoreState()


def later(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(LINE)
    canvas.line(0.65 * inch, h - 0.55 * inch, w - 0.65 * inch, h - 0.55 * inch)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, h - 0.42 * inch, "ARTIFICIAL STUPIDITY | A MONAHINGA™ EVIDENCE PROJECT")
    canvas.drawRightString(w - 0.65 * inch, 0.38 * inch, f"{doc.page - 1}")
    canvas.drawString(0.65 * inch, 0.38 * inch, "Working research prototype | September 2026")
    canvas.restoreState()


def make_chart() -> Path:
    path = OUT / "protected_holdout_result.png"
    labels = ["Validation", "Protected holdout"]
    baseline = [1.000213, 0.999357]
    candidate = [0.990934, 0.990126]
    x = range(len(labels))
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    fig.patch.set_facecolor("#F7F4ED")
    ax.set_facecolor("#F7F4ED")
    ax.bar([i - 0.18 for i in x], baseline, 0.36, color="#8FA6B8", label="Baseline median")
    ax.bar([i + 0.18 for i in x], candidate, 0.36, color="#2A9D6F", label="Candidate median")
    ax.set_ylim(0.985, 1.004)
    ax.set_ylabel("Bits per byte (lower is better)")
    ax.set_xticks(list(x), labels)
    ax.grid(axis="y", alpha=0.2)
    ax.legend(frameon=False, ncol=2, loc="upper right")
    for spine in ax.spines.values():
        spine.set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def parse_markdown(path: Path, st, chart_path: Path, compact: bool = False):
    lines = path.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    on_cover = True
    inserted_chart = False
    while i < len(lines):
        raw = lines[i].rstrip()
        if raw.startswith("# "):
            title = raw[2:]
            subtitle = lines[i + 2][3:] if i + 2 < len(lines) and lines[i + 2].startswith("## ") else ""
            meta_index = i + 4 if i + 4 < len(lines) else i
            meta = lines[meta_index] if "Raymond" in lines[meta_index] or "Executive" in lines[meta_index] else "Raymond Anthony Gomez | September 2026"
            story.extend([
                Spacer(1, 1.15 * inch),
                Paragraph(inline(title), st["cover_title"]),
                HRFlowable(width="35%", thickness=4, color=GREEN, spaceBefore=4, spaceAfter=18, hAlign="LEFT"),
                Paragraph(inline(subtitle), st["cover_sub"]),
                Spacer(1, 0.25 * inch),
                Paragraph("A MONAHINGA™ Evidence Project", st["cover_meta"]),
                Spacer(1, 0.08 * inch),
                Paragraph(inline(meta), st["cover_meta"]),
                Spacer(1, 1.45 * inch if not compact else 1.7 * inch),
                Paragraph("Intelligence proposes.<br/>Artificial Stupidity challenges.<br/>Evidence adjudicates.<br/>A human authorizes.", ParagraphStyle("cover_doctrine", parent=st["cover_sub"], fontName="DejaVu-Bold", fontSize=14, leading=22, textColor=colors.white)),
                NextPageTemplate("later"),
                PageBreak(),
            ])
            i = meta_index + 1
            continue
        if not raw:
            i += 1
            continue
        if raw.startswith("## "):
            heading = raw[3:]
            story.append(Paragraph(inline(heading), st["h2"]))
            if heading in {"Preregistered protected-holdout experiment", "The result in numbers"} and not inserted_chart:
                story.append(Spacer(1, 2))
            i += 1
            continue
        if raw.startswith("### "):
            story.append(Paragraph(inline(raw[4:]), st["h3"]))
            i += 1
            continue
        if raw.startswith("> "):
            story.append(Paragraph(inline(raw[2:]), st["quote"]))
            i += 1
            continue
        if raw.startswith("|") and i + 1 < len(lines) and lines[i + 1].startswith("|---"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                parts = [p.strip() for p in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", p) for p in parts):
                    rows.append(parts)
                i += 1
            cells = []
            for ridx, row in enumerate(rows):
                style = st["table_head"] if ridx == 0 else st["table"]
                cells.append([Paragraph(inline(c), style) for c in row])
            widths = [(7.0 * inch) / len(cells[0])] * len(cells[0])
            if len(cells[0]) == 6:
                widths = [0.9*inch, 1.8*inch, 1.8*inch, 0.85*inch, 0.85*inch, 0.8*inch]
            elif len(cells[0]) == 4:
                widths = [1.75*inch, 1.75*inch, 1.75*inch, 1.25*inch]
            t = Table(cells, colWidths=widths, repeatRows=1, hAlign="LEFT")
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, IVORY]),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([t, Spacer(1, 8)])
            if not inserted_chart and any("Protected-holdout" in c or "Holdout BPB" in c for row in rows for c in row):
                story.extend([Image(str(chart_path), width=6.8*inch, height=2.35*inch), Paragraph("Median results from the preregistered H100 SXM experiment. Lower BPB is better.", st["small"]), Spacer(1, 6)])
                inserted_chart = True
            continue
        if raw.startswith("- "):
            story.append(Paragraph("• " + inline(raw[2:]), st["bullet"]))
            i += 1
            continue
        if re.match(r"\d+\. ", raw):
            story.append(Paragraph(inline(raw), st["bullet"]))
            i += 1
            continue
        if raw.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            story.append(Paragraph("<br/>".join(html.escape(x) for x in code), st["code"]))
            i += 1
            continue
        paragraph = [raw]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|-|\d+\.|\||```)", lines[i]):
            paragraph.append(lines[i].strip())
            i += 1
        style = st["small"] if raw.startswith("Working dossier") or raw.startswith("Full citations") else st["body"]
        story.append(Paragraph(inline(" ".join(paragraph)), style))
    return story


def build(source: str, output: str, compact: bool = False) -> None:
    st = styles()
    doc = BaseDocTemplate(
        str(OUT / output),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.62 * inch,
        title="Artificial Stupidity: An Independent Evidence Gate for Autonomous AI Research",
        author="Raymond Anthony Gomez",
    )
    w, h = letter
    cover_frame = Frame(0.75*inch, 0.7*inch, w-1.5*inch, h-1.4*inch, id="cover", showBoundary=0)
    later_frame = Frame(0.65*inch, 0.6*inch, w-1.3*inch, h-1.25*inch, id="later", showBoundary=0)
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover),
        PageTemplate(id="later", frames=[later_frame], onPage=later),
    ])
    chart = make_chart()
    doc.build(parse_markdown(DOCS / source, st, chart, compact=compact))


if __name__ == "__main__":
    register_fonts()
    build("DOSSIER_SOURCE.md", "Artificial_Stupidity_Dossier_Ray_Gomez_2026.pdf")
    build("EXECUTIVE_SUMMARY_SOURCE.md", "Artificial_Stupidity_Executive_Summary_Ray_Gomez_2026.pdf", compact=True)
