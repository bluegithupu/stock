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

# print(get_llm_response("hello"))
