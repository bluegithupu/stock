from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import Stock

from django.http import JsonResponse

from . import ak_tools
import json


def list(request):
    stocks = Stock.objects.all()
    stock_data = [{"code": stock.code, "name": stock.name} for stock in stocks]
    return JsonResponse(stock_data, safe=False)


def list_stock(request):
    stocks = Stock.objects.all()
    return render(request, "tubiao/list.html", {'stocks': stocks})


def view_stock(request, code):
    stock = get_object_or_404(Stock, code=code)

    # 获取利润数据
    years, profits = ak_tools.get_stock_profit_data(code)

    # 转换为JSON格式传递给模板
    chart_data = {
        'years': years,
        'profits': profits
    }

    return render(request, "tubiao/view.html", {
        'stock': stock,
        'chart_data': json.dumps(chart_data)
    })


def news_stock(request, code):
    """
    显示股票新闻页面
    """
    news_list = ak_tools.get_stock_news(code)
    context = {
        'code': code,
        'news_list': news_list,
    }
    return render(request, 'tubiao/news.html', context)


# Create your views here.
