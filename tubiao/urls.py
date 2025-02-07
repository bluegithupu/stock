from django.urls import path

from . import views

urlpatterns = [
    path('', views.listPage, name='list_page'),
]
