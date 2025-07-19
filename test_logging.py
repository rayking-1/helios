# test_logging.py
"""
测试新的日志记录系统是否正常工作。
这个简单的脚本导入logger并记录一些消息，以确保日志正确写入到控制台和文件。
"""

import os
from helios.services import logger  # 从services导入logger服务实例

def test_logging():
    """测试日志系统的各个级别"""
    logger.debug("这是一条DEBUG级别的日志消息")
    logger.info("这是一条INFO级别的日志消息")
    logger.warning("这是一条WARNING级别的日志消息")
    logger.error("这是一条ERROR级别的日志消息")
    
    try:
        # 故意引发一个异常
        1 / 0
    except Exception as e:
        logger.error("发生了一个除零错误", exc_info=True)
    
    logger.info(f"当前工作目录: {os.getcwd()}")
    logger.info("日志测试完成")

if __name__ == "__main__":
    logger.info("开始日志测试")
    test_logging()
    logger.info("测试结束") 