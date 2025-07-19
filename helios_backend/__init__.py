# helios_backend/__init__.py

"""
Helios Backend Package.

This file makes core components like settings and logger
available for easy import across the application.
"""

from .config import settings
from .core.logging_config import logger

# 导出，以便其他模块可以通过 from helios_backend import ... 来使用
__all__ = ["settings", "logger"] 