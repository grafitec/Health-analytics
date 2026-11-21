from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.lib.pagesizes import A4

pdf = canvas.Canvas("C:/Users/admin/PycharmProjects/Health-analytics/reports/test_svg.pdf", pagesize=A4)

# Rita en blå bakgrund
pdf.setFillColorRGB(0.65, 0.85, 0.95)
pdf.rect(0, 0, 595, 842, fill=1, stroke=0)

# Läs in SVG
drawing = svg2rlg("C:/Users/admin/PycharmProjects/Health-analytics/reports/svg/steps_chart.svg")

# Placera diagrammet
drawing.drawOn(pdf, 100, 300)

pdf.save()