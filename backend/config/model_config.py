# helios_backend/model_config.py
"""
提供LLM配置和模型配置列表
"""

from .config import settings
import logging

logger = logging.getLogger(__name__)

# 配置列表，包含多个模型配置
config_list_instance = [
    {
        "model": "qwen-max",
        "api_key": settings.DASHSCOPE_API_KEY,
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    },
    {
        "model": "glm-4",
        "api_key": settings.ZHIPUAI_API_KEY,
        "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
    },
    {
        "model": "deepseek-chat",
        "api_key": settings.DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com/v1",
    },
    {
        "model": "moonshot-v1-8k",
        "api_key": settings.MOONSHOT_API_KEY,
        "base_url": "https://api.moonshot.cn/v1",
    }
]

# LLM配置
llm_config = {
    "config_list": config_list_instance,
    "temperature": 0.2,
    "request_timeout": 120,
    "retry_wait_time": 5,
    "max_retries": 3,
    "seed": 42,
}

logger.info("Model configuration loaded successfully") 