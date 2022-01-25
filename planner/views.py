import json

from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from planner.models import Task


def index(request):
    return HttpResponse('Hello, world!')


class IndexPage(generic.TemplateView):
    template_name = 'planner/index.html'

    def get_context_data(self, **kwargs):
        tasks = Task.objects.order_by('-pk')
        return {'tasks': tasks}


def create_task(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        min_to_complete = request.POST.get('minutes_to_complete')
        response_data = {}

        task = Task(description=description, minutes_to_complete=min_to_complete)
        task.save()

        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = task.pk
        response_data['description'] = task.description
        response_data['min_to_complete'] = task.minutes_to_complete

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
