from django.shortcuts import render

from django.http import HttpResponse

from .models import Stock

from django.http import JsonResponse


def list(request):
    stocks = Stock.objects.all()
    stock_data = [{"code": stock.code, "name": stock.name} for stock in stocks]
    return JsonResponse(stock_data, safe=False)


def listPage(request):
    stocks = Stock.objects.all()
    return render(request, "tubiao/list.html", {'stocks': stocks})


# Create your views here.
