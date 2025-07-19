"""
Pytest配置文件，用于设置测试环境和通用fixture
"""

import pytest
from unittest.mock import MagicMock, patch
import os
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    在所有测试开始前，自动设置测试环境
    1. 加载测试环境变量（如果存在）
    2. 设置必要的环境变量
    """
    # 优先加载测试专用的环境变量文件
    test_env_path = os.path.join(os.path.dirname(__file__), '..', '.env.test')
    if os.path.exists(test_env_path):
        load_dotenv(test_env_path, override=True)
    else:
        # 如果没有测试专用环境变量，加载普通的.env文件
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'), override=True)
    
    # 设置测试环境标志
    os.environ["HELIOS_TEST_ENV"] = "true"
    
    # 设置测试用的API密钥（如果环境中没有）
    if not os.environ.get("DASHSCOPE_API_KEY"):
        os.environ["DASHSCOPE_API_KEY"] = "test-dashscope-key"
    if not os.environ.get("DEEPSEEK_API_KEY"):
        os.environ["DEEPSEEK_API_KEY"] = "test-deepseek-key"
    if not os.environ.get("ZHIPUAI_API_KEY"):
        os.environ["ZHIPUAI_API_KEY"] = "test-zhipuai-key"
    if not os.environ.get("MOONSHOT_API_KEY"):
        os.environ["MOONSHOT_API_KEY"] = "test-moonshot-key"

@pytest.fixture
def mock_llm_response():
    """
    提供一个模拟的LLM API响应，用于测试不依赖真实API调用
    """
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message = MagicMock()
    mock_response.choices[0].message.content = "这是一个来自模拟API的预设回复。TERMINATE"
    return mock_response

@pytest.fixture
def mock_openai_api(mock_llm_response):
    """
    模拟OpenAI API调用，避免在测试中进行真实的API请求
    """
    # 创建一个模拟的create函数
    mock_create = MagicMock(return_value=mock_llm_response)
    
    # 使用patch替换autogen中的API调用函数
    with patch('autogen.oai.client.create', mock_create):
        yield mock_create

@pytest.fixture
def mock_autogen_completion(mock_llm_response):
    """
    模拟autogen中的completion函数，用于集成测试
    """
    # 模拟completion函数
    with patch('autogen.agentchat.conversable_agent.ConversableAgent._generate_oai_reply', 
               return_value=("", mock_llm_response.choices[0].message.content)) as mock_completion:
        yield mock_completion 