import pytest
from django.urls import reverse
from tests.factories import RefugioFactory


@pytest.mark.django_db
def test_admin_lista_refugios_integration(admin_client):
    client, _ = admin_client
    RefugioFactory.create_batch(3)

    url = reverse('admin_lista_refugios')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['refugios']) == 3


@pytest.mark.django_db
def test_crear_refugio_integration(admin_client):
    client, admin_user = admin_client
    url = reverse('crear_refugio')

    data = {
        'nombreRefugio': 'Nuevo Refugio',
        'responsable': 'Juan Pérez',
        'localidad': 'Chapinero',
        'direccion': 'Calle 123 #45-67',
        'usuarioEncargado': '',
    }

    response = client.post(url, data)
    assert response.status_code == 302