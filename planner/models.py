from django.db import models


# Create your models here.
class Task(models.Model):
    description = models.CharField(max_length=200, null=False)
    minutes_to_complete = models.IntegerField(null=False)
    is_completed = models.BooleanField(default=False)
