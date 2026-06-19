import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_descargar_reporte_pdf_mascotas_integration(admin_client):
    client, _ = admin_client
    url = reverse('pdf_mascotas')

    response = client.get(url)

    assert response.status_code == 200
    assert response['Content-Type'] == 'application/pdf'