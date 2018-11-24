import pytest
from scrumboard.models import Sprint, Task
from backlog.models import Item


@pytest.fixture
def dummy_items(db):
    Item.objects.create(text='Write more tests', points=8)
    Item.objects.create(text='Minify CSS', points=2)
    Item.objects.create(text='Add error monitoring', points=3)
