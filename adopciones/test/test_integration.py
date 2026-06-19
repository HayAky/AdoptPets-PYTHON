import pytest
from django.urls import reverse
from tests.factories import SeguimientoFactory, MascotaFactory, AdopcionFactory


@pytest.mark.django_db
def test_admin_lista_adopciones_integration(admin_client):
    client, _ = admin_client
    SeguimientoFactory.create_batch(2)

    url = reverse('admin_lista_adopciones')
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['adopciones']) == 2


@pytest.mark.django_db
def test_crear_adopcion_integration(admin_client):
    client, _ = admin_client
    adopcion = AdopcionFactory()

    url = reverse('crear_seguimiento', args=[adopcion.pk])

    data = {
        'tipo_contacto': 'llamada',
        'estado_bienestar': 'bueno',
        'observaciones': 'Prueba de integración'
    }

    response = client.post(url, data)
    assert response.status_code == 302