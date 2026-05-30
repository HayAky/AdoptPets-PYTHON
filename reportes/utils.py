from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generar_pdf(template_src, context_dict, filename):
    """Genera un PDF con los datos del contexto."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Título
    titulo = context_dict.get('titulo', 'Reporte')
    elements.append(Paragraph(titulo, styles['Title']))
    elements.append(Spacer(1, 20))

    # Datos en tabla
    datos = context_dict.get('datos', [])
    if datos:
        # Encabezados desde las claves del primer elemento
        headers = list(datos[0].keys())
        table_data = [headers]
        for item in datos:
            table_data.append([str(item.get(h, '')) for h in headers])

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response