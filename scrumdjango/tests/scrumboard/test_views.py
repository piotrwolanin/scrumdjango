import pytest
from django.urls import reverse
from scrumboard.models import Task


URLS = [
    reverse('scrumboard:all_sprints'),
    reverse('scrumboard:sprint_details', kwargs={'pk': 1}),
    reverse('scrumboard:create_sprint'),
    reverse('scrumboard:update_sprint', kwargs={'pk': 1}),
    reverse('scrumboard:copy_sprint', kwargs={'pk': 1}),
    reverse('scrumboard:delete_sprint', kwargs={'pk': 1}),
    reverse('scrumboard:create_task', kwargs={'sprint': 1}),
    reverse('scrumboard:create_multiple_tasks', kwargs={'sprint': 1}),
    reverse('scrumboard:update_task', kwargs={'sprint': 1, 'pk': 1}),
    reverse('scrumboard:delete_task', kwargs={'sprint': 1, 'pk': 1}),
]


@pytest.mark.parametrize('url', URLS)
def test_access_unauthorized(db, client, url, dummy_tasks):
    response = client.get(url)
    assert response.status_code == 301 or 302


@pytest.mark.parametrize('url', URLS)
def test_access_authorized(client, user, url, dummy_tasks):
    login = client.login(username=user.username, password='H44dp4$$v)4d')
    response = client.get(url)
    assert login
    assert response.status_code == 200


def test_homepage_redirect(client, user):
    login = client.login(username=user.username, password='H44dp4$$v)4d')
    # login = client.force_login(user=user)
    response = client.get(reverse('scrumboard:current_sprint'))
    assert login
    assert response.status_code == 302


def test_progress_task(db, client, dummy_tasks):
    tasks = Task.objects.all()

    for task in tasks:
        response = client.get(
            reverse(
                'scrumboard:progress_task',
                kwargs={'sprint': task.sprint_id, 'pk': task.id},
            )
        )
        assert response.status_code == 302

        if task.progress < 2:
            assert Task.objects.get(pk=task.id).progress == task.progress + 1
        else:
            assert Task.objects.get(pk=task.id).progress == 2


def test_unprogress_task(db, client, dummy_tasks):
    tasks = Task.objects.all()

    for task in tasks:
        response = client.get(
            reverse(
                'scrumboard:unprogress_task',
                kwargs={'sprint': task.sprint_id, 'pk': task.id},
            )
        )
        assert response.status_code == 302

        if task.progress > 0:
            assert Task.objects.get(pk=task.id).progress == task.progress - 1
        else:
            assert Task.objects.get(pk=task.id).progress == 0
