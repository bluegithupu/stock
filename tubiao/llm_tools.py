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
    text = "\n".join([f"- {d['text']}" for d in discussions])
    
    prompt = f"""请分析以下雪球股票讨论内容，并给出简要总结：

{text}

请从以下几个方面总结：
1. 投资者主要关注点
2. 市场情绪倾向（看多/看空）
3. 重要信息要点
"""
    
    return get_llm_response(prompt)
