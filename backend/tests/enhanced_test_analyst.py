import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.analyst import AnalystAgent
from tools.user_interaction_tools import ask_user_clarification

# 测试数据 - 更加丰富多样的案例
TEST_DATA = {
    "clear_goals": [
        "我的目标是在12月前跑完10公里 by when",
        "我想要在2个月内what学习Python编程基础 by when",
        "我计划在what六个月内减轻5公斤体重 by when",
    ],
    "ambiguous_goals": [
        "我想变得健康",
        "我想提升自己",
        "学习新技能",
        "提高收入"
    ]
}

# 测试夹具 - 模拟llm_config
@pytest.fixture
def llm_config_fixture():
    """提供测试用的LLM配置"""
    return {
        "model": "test-model",
        "config_list": [{"model": "test-model", "api_key": "test-key"}]
    }

# 测试夹具 - 创建Analyst实例
@pytest.fixture
def analyst_agent(llm_config_fixture):
    """创建一个AnalystAgent实例供测试使用"""
    return AnalystAgent(name="TestAnalyst", llm_config=llm_config_fixture)


class TestAnalystAgent:
    """AnalystAgent的结构化测试集"""
    
    @pytest.mark.parametrize("goal", TEST_DATA["clear_goals"])
    def test_process_clear_goals(self, analyst_agent, goal):
        """
        参数化测试: 处理多个明确目标的情况
        
        Args:
            analyst_agent: 测试夹具提供的智能体实例
            goal: 参数化提供的目标文本
        """
        # 处理目标
        result = analyst_agent.process_message(goal)
        
        # 验证结果是有效的JSON
        parsed_result = json.loads(result)
        
        # 通用断言
        assert isinstance(parsed_result, dict)
        assert "goal" in parsed_result
        assert parsed_result["goal"] == goal
        assert parsed_result["status"] == "clarified"
    
    @pytest.mark.parametrize("goal", TEST_DATA["ambiguous_goals"])
    def test_process_ambiguous_goals(self, analyst_agent, goal):
        """
        参数化测试: 处理多个模糊目标的情况
        
        Args:
            analyst_agent: 测试夹具提供的智能体实例
            goal: 参数化提供的模糊目标文本
        """
        # 处理目标
        result = analyst_agent.process_message(goal)
        
        # 验证结果包含指向澄清工具的动作
        assert "ACTION:" in result
        assert "ask_user_clarification" in result
        assert "question" in result
    
    @patch('tools.user_interaction_tools.ask_user_clarification')
    def test_tool_interaction(self, mock_ask_clarification, analyst_agent):
        """
        测试智能体与工具的交互
        模拟工具调用并验证结果处理
        """
        # 设置模拟工具的返回值
        mock_ask_clarification.return_value = "我想在3个月内学会Python编程"
        
        # 处理一个模糊目标，这应该触发工具调用
        ambiguous_goal = "我想学编程"
        result = analyst_agent.process_message(ambiguous_goal)
        
        # 验证结果中包含正确的工具调用格式
        assert "ACTION: ask_user_clarification" in result
        
        # 提取问题参数 (实际环境中，这是由框架完成的)
        import re
        question_match = re.search(r"ask_user_clarification\(question='(.+?)'\)", result)
        assert question_match, "工具调用格式不正确"
        question = question_match.group(1)
        
        # 模拟调用工具并获取响应
        clarification = ask_user_clarification(question)
        
        # 验证工具被调用
        mock_ask_clarification.assert_called_once()
        assert clarification == "我想在3个月内学会Python编程"
        
        # 在实际环境中，这个结果会被传回智能体进行进一步处理
    
    def test_exception_handling(self, analyst_agent):
        """测试异常情况下的行为"""
        # 使用一个极端情况: 空输入
        empty_input = ""
        result = analyst_agent.process_message(empty_input)
        
        # 这应该触发澄清过程而不是抛出异常
        assert "ACTION:" in result
        assert "ask_user_clarification" in result

    def test_long_input_handling(self, analyst_agent):
        """测试处理非常长的输入"""
        # 生成一个长文本输入
        long_input = "我想" + "非常" * 100 + "健康"
        
        # 应该能正常处理而不崩溃
        result = analyst_agent.process_message(long_input)
        assert result is not None
        assert len(result) > 0 