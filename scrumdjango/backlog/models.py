from django.db import models
from django.urls import reverse


class Item(models.Model):
    text = models.CharField(max_length=255, verbose_name='Text')
    points = models.PositiveSmallIntegerField(verbose_name='Points')

    class Meta:
        db_table = 'item'
        verbose_name = 'Backlog item'
        verbose_name_plural = 'Backlog items'

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('backlog:items')