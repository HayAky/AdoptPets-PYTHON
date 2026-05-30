from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(template_src, context_dict, filename):
    """Genera un PDF con columnas y filas del contexto."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    titulo = context_dict.get('titulo', 'Reporte')
    fecha = context_dict.get('fecha', '')
    elements.append(Paragraph(titulo, styles['Title']))
    elements.append(Paragraph(f"Generado el: {fecha}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Tabla
    columnas = context_dict.get('columnas', [])
    filas = context_dict.get('filas', [])

    if columnas and filas:
        table_data = [columnas] + filas
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2d6a4f')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response