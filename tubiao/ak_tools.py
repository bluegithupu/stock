import akshare as ak
import pandas as pd


def convert_profit(profit_str):
    """
    转换利润字符串为统一的亿元浮点数
    :param profit_str: 包含单位的利润字符串，如 "630.31亿"、"4124.14万"
    :return: 转换后的浮点数（单位：亿元）
    """
    # 移除逗号
    profit_str = str(profit_str).replace(",", "")
    # 处理单位
    if profit_str.endswith('亿'):
        return float(profit_str.replace('亿', ''))
    elif profit_str.endswith('万'):
        return float(profit_str.replace('万', '')) / 10000
    else:
        return float(profit_str)


def get_stock_profit_data(code, limit=10):
    """
    获取股票的利润数据
    :param code: 股票代码
    :param limit: 获取的数据条数，默认10条
    :return: tuple (years, profits) 或在出错时返回 ([], [])
    """
    try:
        # 获取原始数据
        profit_data = ak.stock_financial_benefit_ths(
            symbol=code, indicator="按报告期")

        # 选择指定数量的数据
        selected_data = profit_data[["报告期", "*净利润"]].head(limit)

        # 处理日期格式，只保留年月
        years = [year.split(" ")[0] for year in selected_data["报告期"].tolist()]

        # 转换利润数据
        profits = [convert_profit(profit)
                   for profit in selected_data["*净利润"].tolist()]

        # 反转数据顺序，使其按时间正序显示
        years.reverse()
        profits.reverse()

        return years, profits

    except Exception as e:
        print(f"获取股票{code}数据失败: {str(e)}")
        return [], []


def get_stock_news(code, limit=10):
    """
    获取股票的新闻数据
    :param code: 股票代码
    :param limit: 获取的新闻条数，默认10条
    :return: list of dict，包含新闻标题、内容、发布时间、来源和链接
    """
    try:
        # 获取原始数据
        news_data = ak.stock_news_em(symbol=code)

        # 按发布时间排序
        news_data = news_data.sort_values(by='发布时间', ascending=False)

        # 选择指定数量的数据
        selected_data = news_data.head(limit)

        # 转换为字典列表格式
        news_list = []
        for _, row in selected_data.iterrows():
            news_list.append({
                'title': row['新闻标题'],
                'content': row['新闻内容'],
                'time': row['发布时间'],
                'source': row['文章来源'],
                'url': row['新闻链接']
            })

        return news_list

    except Exception as e:
        print(f"获取股票{code}新闻数据失败: {str(e)}")
        return []


def get_market_sentiment():
    """
    获取市场情绪指数数据
    Returns:
        tuple: (dates, sentiment_values, index_values)
        - dates: 日期列表
        - sentiment_values: 市场情绪指数列表
        - index_values: 沪深300指数列表
    """
    try:
        df = ak.index_news_sentiment_scope()

        # 确保日期列为datetime格式
        df['日期'] = pd.to_datetime(df['日期'])

        # 转换数据格式
        dates = df['日期'].dt.strftime('%Y-%m-%d').tolist()
        sentiment_values = df['市场情绪指数'].tolist()
        index_values = df['沪深300指数'].tolist()

        return dates, sentiment_values, index_values
    except Exception as e:
        raise Exception(f"获取市场情绪数据失败: {str(e)}")
