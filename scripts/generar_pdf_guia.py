from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "guia_clases_inf312.md"
OUTPUT_PDF = ROOT / "guia_clases_inf312.pdf"


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="TitleCenter",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitleCenter",
            parent=styles["Heading2"],
            alignment=TA_CENTER,
            fontSize=13,
            leading=18,
            textColor=colors.HexColor("#334155"),
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#0b3d5c"),
            backColor=colors.HexColor("#e8f1f7"),
            borderPadding=(4, 6, 4, 6),
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1e3a5f"),
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontSize=10.4,
            leading=14.2,
            textColor=colors.HexColor("#111827"),
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontSize=10.3,
            leading=13.8,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=2,
        )
    )

    styles.add(
        ParagraphStyle(
            name="MetaCenter",
            parent=styles["BodyText"],
            alignment=TA_CENTER,
            fontSize=10.5,
            leading=14,
            textColor=colors.HexColor("#334155"),
            spaceAfter=2,
        )
    )

    return styles


def draw_header_footer(canvas, doc):
    canvas.saveState()
    width, height = LETTER

    # Top accent line.
    canvas.setFillColor(colors.HexColor("#0b3d5c"))
    canvas.rect(0, height - 0.55 * cm, width, 0.18 * cm, stroke=0, fill=1)

    # Running header text.
    canvas.setFont("Helvetica", 8.8)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.drawString(2 * cm, height - 0.95 * cm, "INF-312 · Base de Datos I · Guia de clases")

    # Footer with page number.
    canvas.setFont("Helvetica", 8.8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawRightString(width - 2 * cm, 1 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def parse_markdown_to_story(text, styles):
    story = []
    lines = text.splitlines()

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 0.18 * cm))
            continue

        if line == "---":
            story.append(
                HRFlowable(
                    width="100%",
                    color=colors.HexColor("#b6c8d6"),
                    thickness=0.7,
                    lineCap="round",
                    spaceBefore=5,
                    spaceAfter=8,
                )
            )
            story.append(Spacer(1, 0.35 * cm))
            continue

        if line.startswith("# "):
            # First title is rendered prominently centered.
            if i <= 2:
                story.append(Paragraph(line[2:].strip(), styles["TitleCenter"]))
            else:
                story.append(Paragraph(line[2:].strip(), styles["H1"]))
            continue

        if line.startswith("## "):
            subtitle = line[3:].strip()
            if "INF-312" in subtitle:
                story.append(Paragraph(subtitle, styles["SubTitleCenter"]))
            else:
                story.append(Paragraph(subtitle, styles["H2"]))
            continue

        if line.startswith("### "):
            story.append(Paragraph(line[4:].strip(), styles["H2"]))
            continue

        if line.startswith("- "):
            bullet_text = line[2:].strip().replace("&", "&amp;")
            story.append(Paragraph(f"• {bullet_text}", styles["BulletCustom"]))
            continue

        numbered_prefix = ""
        if len(line) > 2 and line[0].isdigit() and line[1:3] == ". ":
            numbered_prefix = line[:2]

        safe_line = line.replace("&", "&amp;")

        if i <= 8 and not line.startswith(("1.", "2.", "3.", "4.", "5.")):
            story.append(Paragraph(safe_line, styles["MetaCenter"]))
            continue

        if numbered_prefix:
            story.append(Paragraph(safe_line, styles["BodyCustom"]))
        else:
            story.append(Paragraph(safe_line, styles["BodyCustom"]))

    return story


def main():
    if not SOURCE_MD.exists():
        raise FileNotFoundError(f"No se encontro el archivo fuente: {SOURCE_MD}")

    styles = build_styles()
    text = SOURCE_MD.read_text(encoding="utf-8")
    story = parse_markdown_to_story(text, styles)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=LETTER,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.1 * cm,
        bottomMargin=1.6 * cm,
        title="Guia de clases INF-312",
        author="INF-312",
    )

    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)
    print(f"PDF generado en: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
