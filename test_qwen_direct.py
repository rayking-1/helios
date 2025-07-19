import os
from openai import OpenAI

# 直接使用API密钥，而不是通过环境变量
client = OpenAI(
    api_key="sk-101435ec51774961a9a835efbe7c6f4b",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

try:
    print("正在调用Qwen API...")
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你是谁？"},
        ],
    )
    print("✅ API调用成功!")
    print(completion.model_dump_json())
except Exception as e:
    print(f"❌ API调用失败: {e}")
    print(f"错误类型: {type(e).__name__}") 
 