import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.adaptor_agent import AdaptorAgent

# 测试数据
DIFFICULT_FEEDBACK = "这周太难了，我筋疲力尽。"
SIMPLE_FEEDBACK = "这些任务太简单了，不够挑战。"
TIME_FEEDBACK = "我时间不够，完成不了这些任务。"
POSITIVE_FEEDBACK = "一切都很顺利！"

def test_process_difficult_feedback():
    """测试处理'太难'类型的反馈"""
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    result = agent.process_feedback(DIFFICULT_FEEDBACK)
    
    # 验证输出包含预期的关键词
    assert "策略师" in result
    assert "修订计划" in result
    assert "强度降低" in result

def test_process_simple_feedback():
    """测试处理'太简单'类型的反馈"""
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    result = agent.process_feedback(SIMPLE_FEEDBACK)
    
    # 验证输出包含预期的关键词
    assert "策略师" in result
    assert "更多挑战性" in result

def test_process_time_feedback():
    """测试处理'时间不够'类型的反馈"""
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    result = agent.process_feedback(TIME_FEEDBACK)
    
    # 验证输出包含预期的关键词
    assert "策略师" in result
    assert "时间" in result
    assert "减少" in result or "延长" in result

def test_process_positive_feedback():
    """测试处理积极反馈"""
    agent = AdaptorAgent(name="TestAdaptor", llm_config={})
    result = agent.process_feedback(POSITIVE_FEEDBACK)
    
    # 验证输出包含预期的关键词
    assert "无需采取行动" in result 