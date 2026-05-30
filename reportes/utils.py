from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from weasyprint import HTML


def generar_pdf(template_src, context_dict, filename):
    """Toma una plantilla HTML y datos, y devuelve un archivo PDF descargable."""
    template = get_template(template_src)
    html = template.render(context_dict)

    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response