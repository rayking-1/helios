import pytest
import sys
import os
from unittest.mock import patch

# 添加项目根目录到Python路径，以便正确导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.adaptor import AdaptorAgent

# 测试数据
FEEDBACK_TOO_DIFFICULT = "这个计划太难了，我跟不上"
FEEDBACK_TOO_EASY = "这个计划太简单了，没有挑战性"
FEEDBACK_TIME_CONFLICT = "我下周有考试，没时间完成这些任务"
FEEDBACK_FALLING_BEHIND = "我已经落后于计划了"

def test_process_difficulty_feedback():
    """测试处理难度反馈的情况"""
    # 创建代理，不需要实际的LLM配置
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    
    # 处理"太难"的反馈
    result = agent.process_feedback(FEEDBACK_TOO_DIFFICULT)
    assert "太难" in result
    assert "策略师" in result
    
    # 处理"太简单"的反馈
    result = agent.process_feedback(FEEDBACK_TOO_EASY)
    assert "简单" in result
    assert "策略师" in result

def test_process_time_feedback():
    """测试处理时间相关反馈的情况"""
    # 创建代理，不需要实际的LLM配置
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    
    # 处理时间冲突反馈
    result = agent.process_feedback(FEEDBACK_TIME_CONFLICT)
    assert "时间" in result
    assert "策略师" in result
    
    # 处理落后反馈
    result = agent.process_feedback(FEEDBACK_FALLING_BEHIND)
    assert "落后" in result
    assert "策略师" in result
    assert "重新安排" in result

def test_process_neutral_feedback():
    """测试处理中性反馈的情况"""
    # 创建代理，不需要实际的LLM配置
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    
    # 处理无需行动的反馈
    result = agent.process_feedback("计划进行得很顺利")
    assert "无需" in result
    assert "当前计划" in result 