import pytest
from django.urls import reverse
from tests.factories import MascotaFactory


@pytest.mark.django_db
def test_admin_lista_mascotas_integration(admin_client):
    client, admin_user = admin_client

    # Genera 3 mascotas, 3 refugios y 3 encargados en 1 línea
    MascotaFactory.create_batch(3)

    url = reverse('admin_lista_mascotas')  # Revisa urls.py para el nombre exacto
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['mascotas']) == 3


@pytest.mark.django_db
def test_admin_crear_mascota_integration(admin_client):
    client, admin_user = admin_client
    url = reverse('crear_mascota')

    # La validación requiere enviar el ID del refugio
    from tests.factories import RefugioFactory
    refugio = RefugioFactory()

    data = {
        'nombre': 'Firulais',
        'especie': 'perro',
        'sexo': 'macho',
        'tamano': 'mediano',
        'color': 'Cafe',
        'refugio': refugio.pk,
        'estadoAdopcion': 'disponible',
        'fechaIngreso': '2026-01-01',
    }

    response = client.post(url, data)
    assert response.status_code == 302