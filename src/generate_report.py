
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from svglib.svglib import svg2rlg

def generate_report(df):
    """Generate an A4 PDF report from processed training data."""

    output_dir = Path("reports")

    output_dir = (Path(__file__).parent.parent / "reports")
    pdf_path = output_dir / "health_report.pdf"
    svg_path = output_dir / "svg" / "steps_chart.svg"

    registered_days = (
        df["date"].nunique()
        if "date" in df.columns
        else 0
    )

    average_steps = (
        df["steps"].mean()
        if "steps" in df.columns
        else None
    )

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=24,
        leading=30,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#243447"),
        spaceAfter=5 * mm,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#667085"),
        spaceAfter=8 * mm,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#243447"),
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
    )

    story = []

    story.append(Paragraph("Träningsrapport", title_style))
    story.append(
        Paragraph(
            f"Skapad {pd.Timestamp.today():%Y-%m-%d}",
            subtitle_style,
        )
    )

    story.append(Paragraph("Månadsöversikt", section_style))

    steps_text = (
        f"{average_steps:,.0f}".replace(",", " ")
        if pd.notna(average_steps)
        else "Ingen data"
    )

    summary_data = [
        ["Registrerade dagar", "Genomsnittliga steg"],
        [str(registered_days), steps_text],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[82 * mm, 82 * mm],
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#243447")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, 1), 18),
            ("BACKGROUND", (0, 1), (-1, 1),
             colors.HexColor("#F0F4F8")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    story.append(summary_table)
    story.append(Spacer(1, 8 * mm))

    # Add the SVG chart if it exists
    if svg_path.exists():
        story.append(Paragraph("Steg per dag", section_style))

        drawing = svg2rlg(str(svg_path))

        if drawing:
            max_width = 170 * mm
            max_height = 100 * mm

            scale = min(
                max_width / drawing.width,
                max_height / drawing.height,
                1,
            )

            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)

            story.append(drawing)


    doc.build(story)