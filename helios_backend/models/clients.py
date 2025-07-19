# helios_backend/models/clients.py

from typing import List, Dict
from helios_backend import logger # 从新的中央位置导入
# 注意：这里不再从config导入任何东西

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
            "qwen-max": {"api_key": self.settings.DASHSCOPE_API_KEY, "model": "qwen-max"},
            "glm-4": {"api_key": self.settings.ZHIPUAI_API_KEY, "model": "glm-4"},
            "deepseek-chat": {"api_key": self.settings.DEEPSEEK_API_KEY, "model": "deepseek-chat"},
            "moonshot-v1-8k": {"api_key": self.settings.MOONSHOT_API_KEY, "model": "moonshot-v1-8k"},
        }
        # 实际的客户端初始化逻辑...
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