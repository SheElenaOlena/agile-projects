from django.db import models


@property
def count_of_files(self):
    return self.files.count()


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField('ProjectFile', related_name='projects')

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']