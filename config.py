# config.py
import os
from dotenv import load_dotenv

# ========================[ 关键指令 ]========================
# 在导入任何其他自定义模块（尤其是配置模块）之前，
# 必须立即调用 load_dotenv()。
# 这将确保 .env 文件中的所有变量都已加载到系统环境中，
# 供后续所有模块安全使用。
load_dotenv()
# ==========================================================

def get_config_list():
    """
    从环境变量动态构建模型配置列表
    """
    config_list = [
        # Qwen-Max (通义千问)
        {
            "model": "qwen-max",
            "api_key": os.environ.get("DASHSCOPE_API_KEY"),
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_type": "openai",
        },
        # DeepSeek V2
        {
            "model": "deepseek-chat",
            "api_key": os.environ.get("DEEPSEEK_API_KEY"),
            "base_url": "https://api.deepseek.com",
            "api_type": "openai", 
        },
    ]
    # 过滤掉那些没有提供API Key的配置
    return [config for config in config_list if config.get("api_key")]

# 可直接导入的配置列表
config_list_instance = get_config_list()

llm_config = {
    "config_list": config_list_instance,
    "cache_seed": 42,
} 