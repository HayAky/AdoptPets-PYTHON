import pytest
from django.test import Client
from usuarios.models import Usuario

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def admin_client(db, client):
    admin_user = Usuario.objects.create_user(
        email='admin_global@test.com',
        password='123',
        nombre='Admin',
        apellido='Global',
        is_staff=True,
        is_superuser=True
    )
    client.force_login(admin_user)
    return client, admin_user