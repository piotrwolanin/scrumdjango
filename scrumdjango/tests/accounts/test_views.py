import pytest
from django.urls import reverse


URLS = [reverse('accounts:login'), reverse('accounts:logout')]


@pytest.mark.parametrize('url', URLS)
def test_access_login_page(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_pwd_change_not_logged_in(client):
    response = client.get(reverse('accounts:password_change'))
    assert response.status_code == 301 or 302


def test_pwd_change_logged_in(client, user):
    login = client.login(username=user.username, password='H44dp4$$v)4d')
    response = client.get(reverse('accounts:password_change'))
    assert login
    assert response.status_code == 200
