from django.contrib import admin
from scrumboard.models import Sprint, Task


admin.site.register([Sprint, Task])