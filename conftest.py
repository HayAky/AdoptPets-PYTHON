import pytest
from tests.factories import UsuarioFactory

@pytest.fixture
def admin_client(db, client):
    admin_user = UsuarioFactory(
        email='admin_test@admin.com',
        is_staff=True,
        is_superuser=True
    )
    client.force_login(admin_user)
    return client, admin_user