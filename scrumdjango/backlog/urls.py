from django.urls import path
from backlog.views import (
    BacklogListView,
    CreateItemView,
    AssignItemView,
    UpdateItemView,
    DeleteItemView,
)


app_name = 'backlog'

urlpatterns = [
    path('', BacklogListView.as_view(), name='items'),
    path('create/', CreateItemView.as_view(), name='create_item'),
    path('<int:pk>/assign/', AssignItemView.as_view(), name='assign_item'),
    path('<int:pk>/update/', UpdateItemView.as_view(), name='update_item'),
    path('<int:pk>/delete/', DeleteItemView.as_view(), name='delete_item'),
]
