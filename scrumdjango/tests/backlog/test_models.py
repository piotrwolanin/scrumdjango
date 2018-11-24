import pytest
from backlog.models import Item


def test_populate_backlog(dummy_items):
    assert Item.objects.count() == 3
