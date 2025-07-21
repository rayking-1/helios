import pytest
import sys
import os
from unittest.mock import patch

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.researcher_agent import ResearcherAgent

# 测试数据
TEST_GOAL = {"goal": "学习Python数据科学", "timeframe": "3个月"}

def test_generate_research_plan():
    """测试生成研究计划的方法"""
    # 创建代理
    agent = ResearcherAgent(name="TestResearcher", llm_config={})
    
    # 获取研究计划
    result = agent.generate_research_plan(TEST_GOAL)
    
    # 验证结果包含web_search调用
    assert "ACTION" in result
    assert "web_search" in result
    assert "实现 学习Python数据科学 的最佳方法" in result

@patch('tools.research_tools.web_search')
def test_web_search_tool_call(mock_web_search):
    """测试代理调用web_search工具的逻辑"""
    # 配置mock
    mock_web_search.return_value = [
        {"title": "测试标题", "url": "https://example.com/test", "snippet": "测试摘要"}
    ]
    
    # 创建代理
    agent = ResearcherAgent(name="TestResearcher", llm_config={})
    
    # 获取研究计划 (这是模拟调用，不会真正调用到工具函数)
    result = agent.generate_research_plan(TEST_GOAL)
    
    # 验证调用指令格式正确
    assert result.startswith("ACTION: web_search")
    assert TEST_GOAL["goal"] in result 