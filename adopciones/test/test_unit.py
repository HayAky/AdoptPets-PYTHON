import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
@patch("adopciones.views.Adopcion.objects.all")
def test_mis_adopciones_unit(mock_all, admin_client):
    client, _ = admin_client
    mock_all.return_value.order_by.return_value = []

    url = reverse('admin_lista_adopciones')
    response = client.get(url)

    assert response.status_code == 200
    mock_all.assert_called_once()