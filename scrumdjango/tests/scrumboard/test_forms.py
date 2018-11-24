import pytest
from scrumboard.models import Sprint, Task
from scrumboard.forms import SprintForm, TaskForm


def test_create_sprint(db):
    new_data = {'number': 1, 'date_from': '2018-10-10', 'date_to': '2018-10-24'}
    form = SprintForm(data=new_data)
    assert form.is_valid()


def test_update_sprint(dummy_sprint):
    updated_data = {'number': 2, 'date_from': '2018-10-17', 'date_to': '2018-10-31'}
    form = SprintForm(data=updated_data, instance=dummy_sprint)
    assert form.is_valid()


def test_sprint_date_overlap(dummy_sprint):
    overlapping_data = {'number': 2, 'date_from': '2018-10-17', 'date_to': '2018-10-31'}
    form = SprintForm(data=overlapping_data)
    assert not form.is_valid()


def test_create_task(user, dummy_sprint):
    new_data = {
        'user': user.id,
        'text': 'Write more tests',
        'color': 'yellow',
        'points': 3,
        'progress': 0,
    }
    form = TaskForm(data=new_data)
    assert form.is_valid()


def test_edit_task(user, dummy_task):
    new_data = {
        'user': user.id,
        'text': 'Write even more tests',
        'color': 'orange',
        'points': 8,
        'progress': 1,
    }
    form = TaskForm(data=new_data, instance=dummy_task)
    assert form.is_valid()
