from django import forms


class TaskForm(forms.Form):
    description = forms.CharField(label='Task Description', max_length=15)
    minutes_to_complete = forms.IntegerField(label='Minutes to Complete', max_value=120, min_value=5, initial=30)