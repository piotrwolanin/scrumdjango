from django.db import models
from django.conf import settings
from django.urls import reverse_lazy


class Sprint(models.Model):
    number = models.SmallIntegerField(verbose_name='Sprint number', unique=True)
    date_from = models.DateField(verbose_name='Date from', unique=True)
    date_to = models.DateField(verbose_name='Date to', unique=True)

    class Meta:
        db_table = 'sprint'
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'

    def __str__(self):
        return f'Sprint {self.number}'

    def get_absolute_url(self):
        return reverse_lazy('scrumboard:sprint_details', args=[self.pk])


class Task(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255, verbose_name='Text')

    COLORS = (
        ('yellow', 'yellow'),
        ('orange', 'orange'),
        ('blue', 'blue'),
        ('pink', 'pink'),
    )

    color = models.CharField(
        max_length=10, verbose_name='Color', choices=COLORS, default=COLORS[0]
    )
    points = models.PositiveSmallIntegerField(verbose_name='Points')

    PROGRESS = ((0, 'Not started'), (1, 'In progress'), (2, 'Done'))

    progress = models.PositiveSmallIntegerField(
        verbose_name='Progress', choices=PROGRESS, default=PROGRESS[0]
    )
    sprint = models.ForeignKey(
        to=Sprint, on_delete=models.CASCADE, verbose_name='Sprint'
    )

    class Meta:
        db_table = 'task'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        unique_together = ('user', 'text', 'sprint')

    def __str__(self):
        return self.text

    def move_right(self):
        if self.progress < 2:
            self.progress += 1
            self.save()

    def move_left(self):
        if self.progress > 0:
            self.progress -= 1
            self.save()
