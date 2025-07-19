#!/usr/bin/env python
"""
Helios自适应规划系统启动脚本
此脚本作为Helios系统的入口点，负责启动后端服务。
"""

import os
from dotenv import load_dotenv

# ========================[ 关键指令 ]========================
# 在导入任何其他自定义模块（尤其是配置模块）之前，
# 必须立即调用 load_dotenv()。
# 这将确保 .env 文件中的所有变量都已加载到系统环境中，
# 供后续所有模块安全使用。
load_dotenv()
# ==========================================================

from helios_backend.main import main

if __name__ == "__main__":
    print("启动Helios自适应规划系统...")
    main()
    print("Helios系统已关闭。") 