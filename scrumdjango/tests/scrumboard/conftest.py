import pytest
from scrumboard.models import Sprint, Task


@pytest.fixture
def sprint(db, number, date_from, date_to):
    yield Sprint.objects.create(number=number, date_from=date_from, date_to=date_to)


@pytest.fixture
def dummy_sprint(db):
    yield Sprint.objects.create(number=1, date_from='2018-10-10', date_to='2018-10-24')


@pytest.fixture
def task(db, user, text, color, points, progress, sprint, number, date_from, date_to):

    task = Task.objects.create(
        user=user,
        text=text,
        color=color,
        points=points,
        progress=progress,
        sprint=sprint,
    )

    yield task


@pytest.fixture
def dummy_task(db, user, dummy_sprint):

    task = Task.objects.create(
        user=user,
        text='Write more tests',
        color='yellow',
        points=3,
        progress=0,
        sprint=dummy_sprint,
    )

    yield task


@pytest.fixture
def dummy_tasks(db, user):
    sprint = Sprint.objects.create(
        number=1, date_from='2018-10-10', date_to='2018-10-24'
    )
    Task.objects.create(
        user=user,
        text='Write more tests',
        color='yellow',
        points=8,
        progress=0,
        sprint=sprint,
    )
    Task.objects.create(
        user=user, text='Minify CSS', color='pink', points=2, progress=0, sprint=sprint
    )
    Task.objects.create(
        user=user,
        text='Create a github repository',
        color='yellow',
        points=2,
        progress=1,
        sprint=sprint,
    )
    Task.objects.create(
        user=user,
        text='Build a task backlog',
        color='orange',
        points=3,
        progress=2,
        sprint=sprint,
    )
