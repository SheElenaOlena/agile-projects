from django.contrib.auth.models import User
from django.db import models

from apps.projects.models import Project
from apps.tasks.choices.statuses import Statuses
from apps.tasks.choices.priority import Priority
from apps.tasks.models import Tag
from apps.tasks.utils.set_end_of_month import calculate_end_of_month


class Task(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(null=False, blank=False)
    status = models.CharField(max_length=15, default=Statuses.NEW, choices=Statuses.choices())
    priority = models.SmallIntegerField(default=Priority.MEDIUM[0], choices=Priority.choices())
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField(Tag, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deadline = models.DateTimeField(blank=False, null=False, default=calculate_end_of_month)
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tasks', null=True, blank=True)

    def __str__(self):
        return f" {self.name}, status: {self.status}"
    class Meta:
        ordering = ['-deadline']
        unique_together = ('name', 'project')
