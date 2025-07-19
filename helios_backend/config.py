# helios_backend/config.py

import os
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

# 解决Pydantic V2的弃用警告，并从.env文件加载配置
# model_config现在是类变量，而不是内部Config类的属性
class Settings(BaseSettings):
    """
    一个纯净的配置类，只负责加载和提供配置值。
    """
    model_config = ConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'  # 忽略.env文件中多余的变量
    )

    # --- LLM API Keys and Base URLs ---
    DASHSCOPE_API_KEY: str = Field(default="", validation_alias='DASHSCOPE_API_KEY')
    ZHIPUAI_API_KEY: str = Field(default="", validation_alias='ZHIPUAI_API_KEY')
    DEEPSEEK_API_KEY: str = Field(default="", validation_alias='DEEPSEEK_API_KEY')
    MOONSHOT_API_KEY: str = Field(default="", validation_alias='MOONSHOT_API_KEY')

    # 你可以在这里继续添加其他配置，如数据库URL、其他API密钥等

# 创建一个全局可用的配置实例
# 这个实例将在应用的入口点（如main.py）被导入
settings = Settings() 