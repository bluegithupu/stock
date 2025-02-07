from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_stock, name='list_stock'),
    path('view/<str:code>/', views.view_stock, name='view_stock'),
    path('news/<str:code>/', views.news_stock, name='news_stock'),
]
