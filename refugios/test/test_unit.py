import pytest
from unittest.mock import patch
from django.urls import reverse


# refugios/test/test_unit.py
@pytest.mark.django_db
def test_lista_publica_refugios_unit(client):
    url = reverse('lista_refugios')
    response = client.get(url)
    assert response.status_code == 200