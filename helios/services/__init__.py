# helios/services/__init__.py
"""
服务实例化层

这个模块负责创建和提供服务实例，如logger和model_client。
它只依赖config层，不依赖应用层。
"""

import logging
import sys
from typing import Dict, List

# 从config层导入配置
from helios.config import settings

# 创建日志服务
logger = logging.getLogger("HeliosApp")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# 防止重复添加处理器
if not logger.handlers:
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 创建文件处理器
    file_handler = logging.FileHandler(settings.LOG_FILE)
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # 定义格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

logger.info("Logger initialized")

# 创建模型客户端服务
class MultiModelClient:
    """
    管理多个LLM客户端的类。
    配置通过依赖注入在初始化时传入，而不是从全局模块导入。
    """
    def __init__(self, settings):
        """
        使用传入的settings对象初始化客户端。
        """
        self.settings = settings
        self.clients = self._initialize_clients()
        logger.info("MultiModelClient initialized with available models.")

    def _initialize_clients(self) -> Dict:
        """
        根据传入的配置初始化所有模型客户端。
        """
        # 这是一个示例，请根据你的实际逻辑调整
        clients = {
            "qwen-max": {
                "model": "qwen-max",
                "api_key": self.settings.DASHSCOPE_API_KEY,
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            },
            "glm-4": {
                "model": "glm-4",
                "api_key": self.settings.ZHIPUAI_API_KEY,
                "base_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            },
            "deepseek-chat": {
                "model": "deepseek-chat",
                "api_key": self.settings.DEEPSEEK_API_KEY,
                "base_url": "https://api.deepseek.com/v1",
            },
            "moonshot-v1-8k": {
                "model": "moonshot-v1-8k",
                "api_key": self.settings.MOONSHOT_API_KEY,
                "base_url": "https://api.moonshot.cn/v1",
            },
        }
        logger.info(f"Initialized {len(clients)} clients.")
        return clients

    def get_client(self, model_name: str):
        """
        根据模型名称获取对应的客户端配置。
        """
        return self.clients.get(model_name)

    def get_config_list(self) -> List[Dict]:
        """
        生成autogen兼容的config_list。
        """
        config_list = []
        for model_name, config in self.clients.items():
            config_list.append(config)
        return config_list

# 创建LLM配置
def create_llm_config(model_client):
    """创建LLM配置"""
    return {
        "config_list": model_client.get_config_list(),
        "temperature": 0.2,
        "request_timeout": 120,
        "retry_wait_time": 5,
        "max_retries": 3,
        "seed": 42,
    }

# 实例化服务
model_client = MultiModelClient(settings)
llm_config = create_llm_config(model_client)

logger.info("All services initialized")

# 导出服务实例，使其可以通过 from helios.services import ... 访问
__all__ = ["logger", "model_client", "llm_config"] 