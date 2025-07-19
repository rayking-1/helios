# helios/__init__.py
"""
Helios Package - Main Entry Point

This file makes the directory a proper Python package and
provides a clean interface for importing core components.
"""

# 从services层导入已实例化的服务
from helios.services import logger, model_client

# 从config层导入配置
from helios.config import settings

# 导出核心组件，使其可以通过 from helios import ... 访问
__all__ = ["logger", "model_client", "settings"] 