from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import Stock

from django.http import JsonResponse

from . import ak_tools, llm_tools
import json


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


def news_summary(request, code):
    """
    生成股票新闻总结
    """
    news_list = ak_tools.get_stock_news(code)
    summary = generate_news_summary(news_list)
    return JsonResponse({'summary': summary})





# help function
def generate_news_summary(news_list):
    """
    使用LLM生成新闻总结
    """
    if not news_list:
        return "暂无新闻可供总结"

    # 构建提示词
    prompt = "请对以下股票相关新闻进行总结：\n\n"

    # 添加新闻内容
    for news in news_list:
        prompt += f"标题：{news['title']}\n"
        prompt += f"时间：{news['time']}\n"
        prompt += f"内容：{news['content']}\n\n"

    prompt += "\n明确列出新闻中的关键信息，包括事件、影响、可能的后果等。"

    # 调用LLM生成总结
    try:
        summary = llm_tools.get_llm_response(prompt)
        return summary
    except Exception as e:
        return f"生成总结时发生错误：{str(e)}"
