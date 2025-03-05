from django.urls import path

from . import views

# app_name = 'tubiao'

urlpatterns = [
    path('', views.list_stock, name='list_stock'),
    path('view/<str:code>/', views.view_stock, name='view_stock'),
    path('news/<str:code>/summary/', views.news_summary, name='news_summary'),
    path('news/<str:code>/', views.news_stock, name='news_stock'),
    path('sentiment/', views.sentiment, name='sentiment'),
    path('xueqiu/<str:code>/', views.xueqiu_summary, name='xueqiu_summary'),
]
