
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.platypus import Flowable
from reportlab.lib import colors
from svglib.svglib import svg2rlg

class ChartCard(Flowable):
    def __init__(self, svg_path, width, height, points, goal_percentage):
        super().__init__()

        self.svg_path = svg_path
        self.width = width
        self.height = height
        self.points = points
        self.goal_percentage = goal_percentage

    def draw(self):
        canvas = self.canv

        canvas.saveState()

        # Rita den nästan vita bakgrundsrutan
        canvas.setFillColor(colors.white)
        canvas.setFillAlpha(0.5)

        canvas.roundRect(
            0, 0,
            self.width, self.height,
            radius=10,
            fill=1,
            stroke=0
        )

        # Rita aktivitetsinformationen
        canvas.setFillAlpha(1)
        canvas.setFillColor(colors.HexColor("#24415C"))

        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(
            12,
            self.height - 22,
            f"Antal steg per dag"
        )

        # Adding icon
        icon = ImageReader((Path(__file__).parent / "icons" / "steps_icon.png"))
        icon_size = 32

        canvas.drawImage(
            icon,
            210,
            self.height - 40,
            width=icon_size,
            height=icon_size,
            mask="auto"
        )

        # Läs in SVG-diagrammet
        drawing = svg2rlg(str(self.svg_path))
        padding = 0
        top_space = 20
        bottom_space = 30

        available_width = self.width - padding * 2
        available_height = self.height - top_space - bottom_space

        scale = min(
            available_width / drawing.width,
            available_height / drawing.height
        )

        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)

        x = (self.width - drawing.width) / 2
        y = self.height - top_space - drawing.height

        drawing.drawOn(canvas, x, y)

        canvas.setFillAlpha(1)
        canvas.setFillColor(colors.HexColor("#24415C"))

        canvas.setFont("Helvetica", 10)
        canvas.drawCentredString(
            self.width / 2,
            12,
            "Du uppnådde 112% av dina mål"
        )

        canvas.restoreState()

def draw_background(canvas, doc):
    canvas.saveState()
    background = (Path(__file__).parent.parent / "src" / "images" / "background.png")
    canvas.drawImage(
        background,
        0,
        0,
        width=A4[0],
        height=A4[1]
    )


def generate_report(df):
    """Generate an A4 PDF report from processed training data."""

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

    # Add the SVG chart
    charts = Table(
        [[
            ChartCard(svg_path, 250, 170, points=12, goal_percentage=130),
            ChartCard(svg_path, 250, 230, points=12, goal_percentage=130),
        ]],
        colWidths=[260, 260],
    )

    charts.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    story.append(charts)


    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)