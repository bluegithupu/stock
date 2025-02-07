import akshare as ak

# 替换为你要查询的股票代码，例如 "000063" 代表中兴通讯
stock_code = "000063"

# 获取按报告期的利润表数据
profit_data = ak.stock_financial_benefit_ths(symbol=stock_code, indicator="按报告期")

# 查看所有列名
print("所有列名：", profit_data.columns)

# 选择指定列，例如选择 "报告期"、"营业总收入" 和 "净利润"
selected_columns = ["报告期","*净利润"]
filtered_data = profit_data[selected_columns]

# 打印指定列的数据
print(filtered_data)