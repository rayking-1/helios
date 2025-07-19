"""
Tests for the config.py module.
"""

import os
from unittest.mock import patch
from config import get_config_list

def test_get_config_list_loads_keys():
    """
    测试 get_config_list 函数是否能正确从环境变量加载API密钥
    """
    # 使用patch模拟环境变量
    mock_env = {
        "DASHSCOPE_API_KEY": "test_dashscope_key",
        "DEEPSEEK_API_KEY": "test_deepseek_key"
    }
    with patch.dict(os.environ, mock_env):
        config_list = get_config_list()
        # 断言配置列表包含两个模型
        assert len(config_list) == 2
        # 断言API Key被正确加载
        assert config_list[0]['api_key'] == "test_dashscope_key"
        assert config_list[1]['api_key'] == "test_deepseek_key" 