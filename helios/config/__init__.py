# helios/config/__init__.py
"""
配置层 - 纯净的配置数据

这个模块负责加载和提供配置值，不依赖项目的其他部分。
它使用Pydantic-settings从环境变量加载配置。
"""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

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

    # --- 数据库配置 ---
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/helios",
        validation_alias='DATABASE_URL'
    )

    # --- 日志配置 ---
    LOG_LEVEL: str = Field("INFO", validation_alias='LOG_LEVEL')
    LOG_FILE: str = Field("helios.log", validation_alias='LOG_FILE')

    # 你可以在这里继续添加其他配置，如数据库URL、其他API密钥等

# 创建一个全局可用的配置实例
settings = Settings()

# 导出settings，使其可以通过 from helios.config import settings 访问
__all__ = ["settings"] 