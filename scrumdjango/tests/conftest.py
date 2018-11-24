import pytest
from scrumboard.models import Sprint, Task
from backlog.models import Item


@pytest.fixture
def user(django_user_model):
    yield django_user_model.objects.create_user(
        username='test_user', password='H44dp4$$v)4d'
    )
