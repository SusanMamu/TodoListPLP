from django.db import models
from users.models import CustomUser


class Task(models.Model):
    PRIORITY_CHOICES = (
        (0, 'Low'),
        (1, 'High')
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.SmallIntegerField(choices=PRIORITY_CHOICES, default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'tasks'
