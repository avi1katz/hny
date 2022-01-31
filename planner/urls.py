from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('toggle_complete_task/<int:task_id>', views.toggle_complete_task, name='toggle_complete_task'),
    path('create_task/', views.create_task, name='create_task'),
]
