from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


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
            fontSize=22,
            leading=26,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SubTitleCenter",
            parent=styles["Heading2"],
            alignment=TA_CENTER,
            fontSize=14,
            leading=18,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            spaceBefore=10,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=15,
            spaceAfter=5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletCustom",
            parent=styles["BodyText"],
            fontSize=10.5,
            leading=14,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=2,
        )
    )

    return styles


def parse_markdown_to_story(text, styles):
    story = []
    lines = text.splitlines()

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 0.18 * cm))
            continue

        if line == "---":
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
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Guia de clases INF-312",
        author="INF-312",
    )

    doc.build(story)
    print(f"PDF generado en: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
