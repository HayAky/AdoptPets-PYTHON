import pytest
from unittest.mock import patch
from django.urls import reverse
from django.http import HttpResponse


@pytest.mark.django_db
@patch("reportes.views.generar_pdf")
def test_generar_reporte_mock(mock_generar_pdf, admin_client):
    client, _ = admin_client
    mock_generar_pdf.return_value = HttpResponse(b'%PDF-1.4 mock content', content_type='application/pdf')

    url = reverse('pdf_mascotas')
    response = client.get(url)

    mock_generar_pdf.assert_called_once()
    assert response.status_code == 200