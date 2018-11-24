import pytest
from django.urls import reverse


URLS = [
    reverse('backlog:items'),
    reverse('backlog:create_item'),
    reverse('backlog:assign_item', kwargs={'pk': 1}),
    reverse('backlog:update_item', kwargs={'pk': 1}),
    reverse('backlog:delete_item', kwargs={'pk': 1}),
]


@pytest.mark.parametrize('url', URLS)
def test_access_not_logged_in(client, url, dummy_items):
    response = client.get(url)
    assert response.status_code == 301 or 302


@pytest.mark.parametrize('url', URLS)
def test_access_logged_in(client, user, url, dummy_items):
    login = client.login(username=user.username, password='H44dp4$$v)4d')
    response = client.get(url)
    assert login
    assert response.status_code == 200
