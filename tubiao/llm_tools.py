import json
from openai import OpenAI
import sys
import os

# 初始化 OpenAI 客户端
client = OpenAI(api_key="sk-cdjsim5KBne5thQJ2bF279E94fEa487aA347A7D85747Af10",
                base_url="https://api.rcouyi.com/v1")


def get_llm_response(prompt, model="gpt-3.5-turbo"):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content


def summarize_xueqiu_discussions(discussions):
    """使用 LLM 总结雪球讨论内容"""
    if not discussions:
        return "暂无相关讨论"
        
    # 将讨论内容整理成文本
    text = "\n".join([f"- {d['content']}" for d in discussions])
    
    prompt = f"""请分析以下雪球股票讨论内容，并给出结构化的总结：

{text}

请使用以下结构化格式进行总结，每个部分都必须包含标题和内容：

## 投资者关注点
在这里列出3-5个投资者最关注的话题或问题，每个用要点形式列出。

## 市场情绪
分析讨论中的市场情绪倾向（看多/看空/中性），并给出具体原因。

## 重要信息
列出讨论中提到的重要信息，如公司公告、行业动向、政策变化等。

## 投资建议
根据讨论内容，总结出投资者普遍提到的投资建议或策略。

请确保总结简洁明了，每个部分不超过100字。使用Markdown格式进行排版。
"""
    
    return get_llm_response(prompt)
