import pytest
from unittest.mock import patch
from django.urls import reverse

@pytest.mark.django_db
@patch("usuarios.views.Usuario.objects.filter")
def test_admin_crear_usuario_email_existente_unit(mock_filter, admin_client):
    """
    Valida que si el administrador intenta crear un usuario con un correo
    que ya existe, la función se detenga y redirija con error.
    """
    # 1. Extraemos el cliente ya autenticado desde el fixture
    client, admin_user = admin_client

    # 2. Simulamos que el filtro devuelve True (el usuario ya existe en BD)
    mock_filter.return_value.exists.return_value = True

    # 3. Ejecutamos la petición con el cliente autenticado
    url = reverse('crear_usuario')
    response = client.post(url, data={
        'email': 'yaexiste@email.com',
        'password': '123',
        'nombre': 'Andres',
        'apellido': 'Prueba'
    })

    # 4. Verificamos que no continuó procesando, sino que redirigió a la misma página
    assert response.status_code == 302
    assert response.url == reverse('crear_usuario')