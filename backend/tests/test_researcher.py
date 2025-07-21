import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径，以便正确导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.researcher import ResearcherAgent

# 测试数据
TEST_GOAL = {
    "domain": "编程",
    "topic": "Python学习",
    "timeframe": "3个月",
    "difficulty": "初级到中级"
}

def test_research_methods():
    """测试研究方法的功能"""
    # 创建代理，不需要实际的LLM配置
    agent = ResearcherAgent(name="TestResearcher", llm_config={})
    
    # 模拟web_search工具
    with patch.object(agent, 'web_search', return_value="Python学习方法包括项目驱动学习和交互式教程"):
        # 执行研究
        result = agent.research_methods(TEST_GOAL)
        
        # 验证结果包含研究内容
        assert isinstance(result, str)
        assert len(result) > 0
        assert "Python" in result

def test_generate_report():
    """测试生成报告的功能"""
    # 创建代理，不需要实际的LLM配置
    agent = ResearcherAgent(name="TestResearcher", llm_config={})
    
    # 模拟研究结果
    research_data = "Python学习的最佳方法包括每日练习、构建项目和参与社区"
    
    # 生成报告
    report = agent.generate_report(TEST_GOAL, research_data)
    
    # 验证报告格式和内容
    assert isinstance(report, str)
    assert "报告" in report
    assert "Python" in report 