from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tubiao.xueqiu_crawler import get_xueqiu_discussions
from .models import Stock
from . import ak_tools, llm_tools
import json
import os
import tempfile
import pickle
from datetime import datetime, timedelta


def get_cached_discussions(code):
    """从缓存获取讨论内容，如果缓存不存在或已过期则重新爬取"""
    # 项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 创建 tmp 文件夹（如果不存在）
    temp_dir = os.path.join(base_dir, 'tmp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    cache_file = os.path.join(temp_dir, f'xueqiu_discussions_{code}.pkl')
    
    # 检查缓存文件是否存在且未过期（24小时内）
    if os.path.exists(cache_file):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - file_mod_time < timedelta(hours=24):
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"读取缓存文件出错: {e}")
    
    # 缓存不存在或已过期，重新爬取
    discussions = get_xueqiu_discussions(code)
    
    # 保存到缓存
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(discussions, f)
    except Exception as e:
        print(f"保存缓存文件出错: {e}")
    
    return discussions

def xueqiu_summary(request, code):
    # 获取雪球讨论数据（使用缓存）
    discussions = get_cached_discussions(code)
    
    # 首次加载时不生成总结
    return render(request, 'tubiao/xueqiu_summary.html', 
                 {'stock_code': code,
                  'discussions': discussions,
                  'summary': ''})


@csrf_exempt
def generate_xueqiu_summary(request, code):
    """生成雪球讨论的AI总结并返回JSON响应"""
    if request.method == 'POST':
        # 使用缓存的讨论数据，避免重复爬取
        discussions = get_cached_discussions(code)
        summary = llm_tools.summarize_xueqiu_discussions(discussions)
        return JsonResponse({'summary': summary})
    return JsonResponse({'error': '方法不允许'}, status=405)


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


def sentiment(request):
    """市场情绪页面"""
    try:
        # 获取市场情绪数据
        dates, sentiment_values, index_values = ak_tools.get_market_sentiment()

        context = {
            'dates': json.dumps(dates),
            'sentiment_values': json.dumps(sentiment_values),
            'index_values': json.dumps(index_values),
        }
        return render(request, 'tubiao/sentiment.html', context)
    except Exception as e:
        return render(request, 'tubiao/sentiment.html', {'error': str(e)})


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
