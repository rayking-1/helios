# helios_adaptive_planner/test_imports.py
"""
测试文件：验证所有必要的导入是否正确
"""

print("开始导入测试...")

try:
    from pyautogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
    print("✓ 成功导入 pyautogen 核心组件")
except ImportError as e:
    print(f"✗ 导入 pyautogen 核心组件失败: {e}")

try:
    from pyautogen.oai.client import OpenAIChatCompletionClient
    print("✓ 成功导入 OpenAIChatCompletionClient")
except ImportError as e:
    print(f"✗ 导入 OpenAIChatCompletionClient 失败: {e}")

try:
    from config import model_client
    print("✓ 成功导入 config 模块")
except ImportError as e:
    print(f"✗ 导入 config 模块失败: {e}")

try:
    from agents import Planner, Researcher, Critic, Integrator
    print("✓ 成功导入 agents 模块")
except ImportError as e:
    print(f"✗ 导入 agents 模块失败: {e}")

print("\n导入测试完成!") 