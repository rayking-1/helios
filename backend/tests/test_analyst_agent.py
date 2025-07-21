import pytest
import json
import sys
import os
from unittest.mock import patch

# 添加项目根目录到Python路径，以便正确导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.analyst_agent import AnalystAgent

# 测试数据
CLEAR_GOAL = "我的目标是在12月前跑完10公里"
AMBIGUOUS_GOAL = "我想变得健康"

def test_process_clear_goal():
    """测试处理明确目标的情况"""
    # 创建代理，不需要实际的LLM配置
    agent = AnalystAgent(name="TestAnalyst", llm_config={})
    
    # 处理清晰的目标
    result = agent.process_message(CLEAR_GOAL)
    
    # 验证结果是有效的JSON
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, dict)
    assert "goal" in parsed_result
    assert parsed_result["goal"] == CLEAR_GOAL
    assert parsed_result["status"] == "clarified"

def test_process_ambiguous_goal():
    """测试处理模糊目标的情况"""
    # 创建代理，不需要实际的LLM配置
    agent = AnalystAgent(name="TestAnalyst", llm_config={})
    
    # 处理模糊的目标
    result = agent.process_message(AMBIGUOUS_GOAL)
    
    # 验证结果包含调用ask_user_clarification工具的指令
    assert "ACTION" in result
    assert "ask_user_clarification" in result
    assert "question" in result 