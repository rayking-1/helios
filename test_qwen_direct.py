import os
from dashscope import Generation

# 创建客户端
client = Generation(
    api_key=os.getenv("QWEN_API_KEY", ""),  # Replace hardcoded key with environment variable
    model="qwen-turbo"
)

# 发送请求
response = client.call(
    messages=[
        {"role": "system", "content": "你是由大搜车开发的通义千问大模型。"},
        {"role": "user", "content": "你好，请进行自我介绍。"}
    ]
)

# 打印完整响应
print(f"Status code: {response['status_code']}")
print(f"Request ID: {response['request_id']}")
print(f"Output:\n{response['output']['choices'][0]['message']['content']}") 
 