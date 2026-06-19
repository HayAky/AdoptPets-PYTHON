import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
@patch("mascotas.views.Mascota.objects.filter")
def test_busqueda_mascotas_unit(mock_filter, client):
    mock_filter.return_value.order_by.return_value = []

    url = reverse('lista_mascotas')
    response = client.get(url, {'q': 'inexistente'})

    mock_filter.assert_called_once()
    assert response.status_code == 200