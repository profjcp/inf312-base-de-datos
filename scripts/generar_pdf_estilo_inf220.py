from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "guia_inf312_estilo_inf220.md"
OUTPUT_PDF = ROOT / "guia_inf312_estilo_inf220.pdf"


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CoverSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverCode",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=28,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=36,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSub",
            parent=styles["BodyText"],
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#374151"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=7,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontSize=10.4,
            leading=14.4,
            textColor=colors.HexColor("#111827"),
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletINF",
            parent=styles["BodyText"],
            fontSize=10.4,
            leading=14,
            leftIndent=10,
            bulletIndent=0,
            spaceAfter=2,
        )
    )

    return styles


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawRightString(doc.pagesize[0] - 2 * cm, 1.2 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def parse_md(md_text: str, styles):
    story = []
    lines = md_text.splitlines()

    for idx, raw in enumerate(lines):
        line = raw.strip()

        if not line:
            story.append(Spacer(1, 0.16 * cm))
            continue

        if line == "---":
            story.append(Spacer(1, 0.28 * cm))
            continue

        if idx == 0 and line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), styles["CoverSmall"]))
            story.append(Spacer(1, 0.15 * cm))
            continue

        if line.startswith("# INF-"):
            story.append(Paragraph(line[2:].strip(), styles["CoverCode"]))
            continue

        if line.startswith("# BASES"):
            story.append(Paragraph(line[2:].strip(), styles["CoverTitle"]))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:].strip(), styles["H1"]))
            continue

        if line.startswith("## "):
            title = line[3:].strip()
            if title == "UNIDADES DEL CURSO":
                story.append(Spacer(1, 0.2 * cm))
                story.append(Paragraph(title, styles["H2"]))
            else:
                story.append(Spacer(1, 0.08 * cm))
                story.append(Paragraph(title, styles["H1"]))
            continue

        if line.startswith("### "):
            story.append(Paragraph(line[4:].strip(), styles["H2"]))
            continue

        if line.startswith("- "):
            story.append(Paragraph(f"• {line[2:].strip()}", styles["BulletINF"]))
            continue

        story.append(Paragraph(line, styles["Body"]))

    return story


def main():
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"No existe: {SOURCE_MD}")

    styles = build_styles()
    content = SOURCE_MD.read_text(encoding="utf-8")
    story = parse_md(content, styles)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=LETTER,
        leftMargin=2.1 * cm,
        rightMargin=2.1 * cm,
        topMargin=2 * cm,
        bottomMargin=1.8 * cm,
        title="Guia INF-312 estilo INF220",
        author="INF-312",
    )

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"PDF generado: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
