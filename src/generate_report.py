
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
from calculate_scores import steps


class ChartCard(Flowable):
    def __init__(self, svg_path, width, height, points, goal_percentage, activity_name):
        super().__init__()

        self.svg_path = svg_path
        self.width = width
        self.height = height
        self.points = points
        self.goal_percentage = goal_percentage
        self.activity_name = activity_name

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
            self.activity_name
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

        # Informationsvärden längst ner
        info_y = 18

        left_x = 12
        right_x = self.width - 12

        canvas.setFillAlpha(1)
        canvas.setFillColor(colors.HexColor("#24415C"))

        # Värden
        canvas.setFont("Helvetica-Bold", 16)

        canvas.drawString(
            left_x,
            info_y + 15,
            f"{self.goal_percentage}%"
        )

        canvas.drawRightString(
            right_x,
            info_y + 15,
            f"{self.points} poäng"
        )

        # Beskrivningar
        canvas.setFillColor(colors.HexColor("#71869A"))
        canvas.setFont("Helvetica", 8)

        canvas.drawString(
            left_x,
            info_y,
            "Måluppfyllelse"
        )

        canvas.drawRightString(
            right_x,
            info_y,
            "Intjänade poäng"
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

def draw_header(canvas, doc):
    canvas.saveState()

    # Halvtransparent vit yta
    canvas.setFillColor(colors.white)
    canvas.setFillAlpha(0.55)

    canvas.roundRect(
        15,
        doc.height + doc.topMargin - 770, # 80
        doc.width + doc.leftMargin + doc.rightMargin-30,
        800,
        fill=1,
        radius=20,
        stroke=0
    )
    """
    canvas.roundRect(
        30,
        doc.height + doc.topMargin - 95,
        doc.width + doc.leftMargin + doc.rightMargin-60,
        110,
        fill=1,
        radius=20,
        stroke=0
    )
    """
    canvas.setFillAlpha(1)

    # Rubrik
    canvas.setFillColor(colors.HexColor("#24415C"))
    canvas.setFont("Helvetica-Bold", 24)

    canvas.drawString(
        45,
        doc.height + doc.topMargin - 10,
        "Hälsorapport | November"
    )

    # Underrubrik
    canvas.setFont("Helvetica-Bold", 12)

    canvas.drawString(
        45,
        doc.height + doc.topMargin - 30,
        "Din hälsa · Din utveckling · Din statistik"
    )

    # Datum
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.HexColor("#71869A"))

    canvas.drawString(
        45,
        doc.height + doc.topMargin - 50,
        f"Skapad {pd.Timestamp.today():%Y-%m-%d}"
    )

    # heart icon
    heart_path = (Path(__file__).parent.parent / "src" / "icons" / "heart_icon.svg")
    icon = svg2rlg(heart_path)
    icon_size = 50
    scale = icon_size / icon.width
    icon.scale(scale, scale)
    icon.drawOn(canvas, 500, 750)


    canvas.setFillColor(colors.white)
    canvas.setFillAlpha(0.55)



    canvas.restoreState()

def draw_first_page(canvas, doc):
    draw_background(canvas, doc)
    draw_header(canvas, doc)

def generate_report(df, points_data):
    """Generate an A4 PDF report from processed training data."""

    output_dir = (Path(__file__).parent.parent / "reports")
    pdf_path = output_dir / "health_report.pdf"
    svg_path = output_dir / "svg" / "steps_chart.svg"



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

    """    story.append(Paragraph("Hälsorapport", title_style))
    story.append(
        Paragraph(
            "Din hälsa · Din utveckling · Din statistik",
            section_style,
        )
    )
    story.append(
        Paragraph(
            f"Skapad {pd.Timestamp.today():%Y-%m-%d}",
            subtitle_style,
        )
    )"""

    #story.append(Paragraph("Månadsöversikt", section_style))



    story.append(Spacer(1, 200))

    step_total_points, step_procent, missing_dates = steps(df, points_data, period_start="2026-11-01", period_end="2026-11-30")


    # Add the SVG chart
    charts = Table(
        [[
            ChartCard(svg_path, 250, 210, points=step_total_points, goal_percentage=step_procent, activity_name="Antal steg"),
            ChartCard(svg_path, 250, 210, points=step_total_points, goal_percentage=step_procent, activity_name="Antal steg"),
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


    doc.build(story, onFirstPage=draw_first_page, onLaterPages=draw_background)