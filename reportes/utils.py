from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(template_src, context_dict, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    titulo = context_dict.get('titulo', 'Reporte')
    elements.append(Paragraph(titulo, styles['Title']))
    elements.append(Spacer(1, 20))

    # Fecha
    fecha = context_dict.get('fecha', '')
    if fecha:
        elements.append(Paragraph(f"Generado el: {fecha}", styles['Normal']))
        elements.append(Spacer(1, 12))

    # Tabla con columnas y filas
    columnas = context_dict.get('columnas', [])
    filas = context_dict.get('filas', [])

    if columnas and filas:
        table_data = [columnas] + filas  # encabezado + datos

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#22C55E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0fdf4')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No hay datos para mostrar.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response