# helios_backend/core/logging_config.py

import logging
import sys

# 创建一个全局唯一的logger实例
logger = logging.getLogger("HeliosApp")
logger.setLevel(logging.INFO)

# 防止重复添加处理器
if not logger.handlers:
    # 创建一个handler，用于写入日志文件
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setLevel(logging.INFO)

    # 创建一个handler，用于输出到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 给logger添加handler
    # logger.addHandler(file_handler)
    logger.addHandler(console_handler) 