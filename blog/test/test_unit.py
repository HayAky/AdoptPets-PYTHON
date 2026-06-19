import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
@patch("blog.views.Blog.objects.filter")
def test_lista_blog_unit(mock_filter, client):
    mock_filter.return_value.order_by.return_value = []

    url = reverse('lista_blogs')
    response = client.get(url)

    assert response.status_code == 200
    mock_filter.assert_called_once()
