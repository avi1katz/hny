from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from planner.models import Task


def index(request):
    return HttpResponse('Hello, world!')


class IndexPage(generic.TemplateView):
    template_name = 'planner/index.html'
    tasks = Task.objects.order_by('-pk')
    context = {'tasks': tasks}
