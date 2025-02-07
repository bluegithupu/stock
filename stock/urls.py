"""
URL configuration for stock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render
from django.urls.resolvers import URLResolver, URLPattern


def list_routes(request):
    """展示主要应用路由"""
    routes = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            path = str(pattern.pattern)
            view_name = path.rstrip('/').capitalize()
            routes.append((path, view_name))
    return render(request, 'home.html', {'routes': routes})


urlpatterns = [
    path("", list_routes, name="home"),  # 添加首页路由
    path("tubiao/", include("tubiao.urls")),
    path("admin/", admin.site.urls),
]
