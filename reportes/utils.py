from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def generar_pdf(template_src, context_dict, filename):
    """Toma una plantilla HTML y datos, y devuelve un archivo PDF descargable."""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # Renderizamos el HTML a PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        # La propiedad 'attachment' fuerza la descarga del archivo
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return HttpResponse("Error crítico al generar el PDF", status=500)