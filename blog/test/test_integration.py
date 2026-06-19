import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_crear_blog_integration(admin_client):
    client, _ = admin_client
    url = reverse('crear_blog')

    data = {
        'titulo': 'Nuevo artículo',
        'contenido': 'Contenido de prueba',
        'publicado': True
    }

    response = client.post(url, data)
    assert response.status_code == 302