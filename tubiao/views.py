from django.shortcuts import render, get_object_or_404

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


def view_stock(request, code):
    stock = get_object_or_404(Stock, code=code)
    return render(request, "tubiao/view.html", {'stock': stock})


# Create your views here.
