import pytest


def test_not_superuser(user):
    assert not user.is_superuser
