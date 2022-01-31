from django.db import models


class Task(models.Model):
    description = models.CharField(max_length=200, null=False)
    minutes_to_complete = models.IntegerField(null=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'[{ "X" if self.is_completed else " "}] {self.description} ({self.minutes_to_complete})'


# Agenda - date, agenda_items, default_begin_time, default_end_time, parent (template)
class Agenda(models.Model):
    date = models.DateField()
    default_begin_time = models.TimeField(default="06:00")
    default_end_time = models.TimeField(default="22:00")
    parent = models.ForeignKey('self',
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True, )

    def __str__(self):
        return self.date.strftime("%d-%b-%y")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.parent is None and not self.agenda_items.exists():
            self.agenda_items.create(start_time=self.default_begin_time,
                                     task=Task.objects.create(description="Plan day", minutes_to_complete=15))
            self.agenda_items.create(start_time=self.default_end_time,
                                     task=Task.objects.create(description="Head to Bed", minutes_to_complete=15))


# Agenda_Item - agenda_id, start_time, task_id
class AgendaItem(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name='agenda_items')
    start_time = models.TimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='agenda_items')

    class Meta:
        ordering = ['start_time', ]

    def __str__(self):
        return f'Agenda: {self.agenda}, start_time: {self.start_time}, task: {self.task}'
