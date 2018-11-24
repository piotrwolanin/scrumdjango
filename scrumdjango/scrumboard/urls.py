from django.urls import path, include
from scrumboard.views import (
    SprintListView,
    SprintDetailView,
    sprint_detail_redirect_view,
    CreateSprintView,
    CreateMultipleTasksView,
    UpdateSprintView,
    DeleteSprintView,
    CreateTaskView,
    progress_task,
    unprogress_task,
    UpdateTaskView,
    CopySprintView,
    DeleteTaskView,
)


app_name = 'scrumboard'

urlpatterns = [
    path('', sprint_detail_redirect_view, name='current_sprint'),
    path('sprints/', SprintListView.as_view(), name='all_sprints'),
    path('sprints/<int:pk>/', SprintDetailView.as_view(), name='sprint_details'),
    path('sprints/create-sprint/', CreateSprintView.as_view(), name='create_sprint'),
    path('sprints/<int:pk>/update-sprint/', UpdateSprintView.as_view(), name='update_sprint'),
    path('sprints/<int:pk>/copy-sprint/', CopySprintView.as_view(), name='copy_sprint'),
    path('sprints/<int:pk>/delete-sprint/', DeleteSprintView.as_view(), name='delete_sprint'),
    path(
        'sprints/<int:sprint>/create-task/',
        CreateTaskView.as_view(),
        name='create_task',
    ),
    path(
        'sprints/<int:sprint>/create-multiple-tasks/',
        CreateMultipleTasksView.as_view(),
        name='create_multiple_tasks',
    ),
    path(
        'sprints/<int:sprint>/progress-task/<int:pk>/',
        progress_task,
        name='progress_task',
    ),
    path(
        'sprints/<int:sprint>/unprogress-task/<int:pk>/',
        unprogress_task,
        name='unprogress_task',
    ),
    path(
        'sprints/<int:sprint>/update-task/<int:pk>/',
        UpdateTaskView.as_view(),
        name='update_task',
    ),
    path(
        'sprints/<int:sprint>/delete-task/<int:pk>/',
        DeleteTaskView.as_view(),
        name='delete_task',
    ),
]
