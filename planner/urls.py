from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('create_task/', views.create_task, name='create_task')
]
