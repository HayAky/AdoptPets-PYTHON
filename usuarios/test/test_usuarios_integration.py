import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_create_user_integration(client):
    url = reverse('registro')

    # Se añaden los campos obligatorios para pasar la validación del formulario
    data = {
        'username': 'nuevo_usuario',
        'email': 'nuevo@tests.com',
        'password': 'password123',
        'nombre': 'Andres',
        'apellido': 'Prueba'
    }

    response = client.post(url, data)

    assert response.status_code == 302