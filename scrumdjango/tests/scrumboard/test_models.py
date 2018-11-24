import pytest
from django.db import IntegrityError
from scrumboard.models import Sprint, Task


sprint_fields = 'number, date_from, date_to'

SPRINTS = [
    (1, '2018-10-10', '2018-10-24'),
    (2, '2018-10-09', '2018-10-24'),
    (3, '2018-10-24', '2018-11-07'),
    (4, '2018-10-10', '2018-10-25'),
]

task_fields = 'text, color, points, progress, number, date_from, date_to'

TASKS = [
    ('Write more tests', 'yellow', 3, 0, 1, '2018-10-10', '2018-10-24'),
    ('Minify CSS', 'pink', 1, 2, 2, '2018-10-09', '2018-10-24'),
]


@pytest.mark.parametrize(sprint_fields, SPRINTS)
def test_unique_sprint(sprint):
    assert Sprint.objects.count() == 1
    with pytest.raises(IntegrityError):
        Sprint.objects.create(number=3, date_from='2018-10-10', date_to='2018-10-24')


@pytest.mark.parametrize(task_fields, TASKS)
def test_unique_task(
    task, user, text, color, points, progress, sprint, number, date_from, date_to
):
    assert Task.objects.count() == 1
    with pytest.raises(IntegrityError):
        Task.objects.create(
            user=task.user,
            text=task.text,
            color='orange',
            points=8,
            progress=1,
            sprint=task.sprint,
        )
