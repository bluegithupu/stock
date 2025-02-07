from django.urls import path

from . import views

urlpatterns = [
    path('', views.listPage, name='list_page'),
    path('view/<str:code>/', views.view_stock, name='view_stock'),
]
