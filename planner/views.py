import json
from datetime import datetime, timedelta, date

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from planner.forms import TaskForm
from planner.models import Task, Agenda, AgendaItem


def index(request):
    return HttpResponse('Hello, world!')


# class IndexPage(generic.TemplateView):
#     template_name = 'planner/index.html'
#
#     def get_context_data(self, **kwargs):
#         tasks = Task.objects.order_by('-pk')
#         return {'tasks': tasks}


class IndexPage(generic.edit.FormView):
    template_name = 'planner/index.html'
    form_class = TaskForm
    success_url = '/planner/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(Q(agenda_items__isnull=True)
                                               | Q(agenda_items__agenda__date=datetime.now()))

        # get todays agenda
        today_agenda, _ = Agenda.objects.get_or_create(date=datetime.now().date())
        context['agenda'] = today_agenda

        return context

    def form_valid(self, form):
        description = form.cleaned_data['description']
        min_to_complete = form.cleaned_data['minutes_to_complete']
        task = Task(description=description, minutes_to_complete=min_to_complete)
        task.save()
        return super().form_valid(form)


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return HttpResponseRedirect('/planner')


def toggle_complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.is_completed = not task.is_completed
    task.save()
    return HttpResponseRedirect('/planner')


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


def add_task_at_index(request, task_id, item_index):
    task = get_object_or_404(Task, pk=task_id)
    today_agenda = Agenda.objects.get(date=datetime.now().date())
    agenda_items_list = today_agenda.agenda_items.all()
    if item_index == 0:
        new_item_start_time = '06:00'
    else:
        prev_item_start_time = agenda_items_list[item_index-1].start_time
        new_item_start_time = (datetime.combine(date(1, 1, 1), prev_item_start_time) + timedelta(minutes=30)).time()
    # today_agenda.agenda_items.create(start_time=new_item_start_time,
    #                                  task=task)
    AgendaItem.objects.update_or_create(
        task=task, agenda=today_agenda,
        defaults={'start_time': new_item_start_time})
    return HttpResponseRedirect('/planner')


def update_agenda_item_time(request, item_id, new_time):
    AgendaItem.objects.filter(id=item_id).update(start_time=new_time)
    return HttpResponseRedirect('/planner')


def delete_agenda_item(request, item_id):
    AgendaItem.objects.filter(id=item_id).delete()
    return HttpResponseRedirect('/planner')
