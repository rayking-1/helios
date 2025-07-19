# validate_qwen_api.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥
# 确保.env文件中有 QWEN_API_KEY=sk-xxxxxxxxxxxx
qwen_api_key = os.getenv("QWEN_API_KEY")

if not qwen_api_key:
    print("❌ 错误：未找到 'QWEN_API_KEY' 环境变量。请检查您的 .env 文件。")
else:
    try:
        print("正在初始化OpenAI客户端，目标为Qwen...")
        client = OpenAI(
            api_key=qwen_api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # Qwen的兼容模式端点
        )

        print("客户端初始化成功。正在发送测试请求到 'qwen-plus' 模型...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="qwen-plus",
        )
        print("✅ 成功！API密钥和端点有效。")
        print("模型响应:", chat_completion.choices[0].message.content)

    except Exception as e:
        print(f"❌ 失败！API调用时发生错误。")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {e}")
        print("\n请检查：")
        print("1. 您的API Key是否正确且具有访问'qwen-plus'的权限。")
        print("2. 您的网络连接是否正常，能否访问Qwen API服务器。") 
 