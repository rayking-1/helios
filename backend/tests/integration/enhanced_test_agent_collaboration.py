import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.analyst import AnalystAgent
from agents.researcher import ResearcherAgent
from agents.strategist import StrategistAgent
from agents.adaptor import AdaptorAgent
from tools.research_tools import web_search

# 测试夹具 - 模拟llm_config
@pytest.fixture
def llm_config_fixture():
    """提供测试用的LLM配置"""
    return {
        "model": "test-model",
        "config_list": [{"model": "test-model", "api_key": "test-key"}]
    }

# 为每个智能体创建一个夹具
@pytest.fixture
def analyst(llm_config_fixture):
    return AnalystAgent(name="TestAnalyst", llm_config=llm_config_fixture)

@pytest.fixture
def researcher(llm_config_fixture):
    return ResearcherAgent(name="TestResearcher", llm_config=llm_config_fixture)

@pytest.fixture
def strategist(llm_config_fixture):
    return StrategistAgent(name="TestStrategist", llm_config=llm_config_fixture)

@pytest.fixture
def adaptor(llm_config_fixture):
    return AdaptorAgent(name="TestAdaptor", llm_config=llm_config_fixture)


class TestAgentCollaboration:
    """测试智能体之间的协作流程"""
    
    def test_analyst_to_researcher_flow(self, analyst, researcher):
        """测试分析师智能体到研究员智能体的数据流转"""
        # 1. 准备明确目标
        clear_goal = "我想在3个月内学会Python数据分析 by when"
        
        # 2. 分析师处理目标
        analyst_output = analyst.process_message(clear_goal)
        structured_goal = json.loads(analyst_output)
        
        # 3. 验证分析师输出符合预期
        assert isinstance(structured_goal, dict)
        assert structured_goal["status"] == "clarified"
        
        # 4. 模拟研究员调用web_search工具
        with patch('agents.researcher.ResearcherAgent.web_search') as mock_web_search:
            # 设置mock返回值
            mock_web_search.return_value = "Python数据分析最佳学习路径包括：Pandas, NumPy, Matplotlib"
            
            # 研究员生成研究报告
            research_result = researcher.research_methods(structured_goal)
            
            # 验证web_search被调用，且结果包含预期内容
            mock_web_search.assert_called_once()
            assert "Python" in research_result
            assert "数据分析" in research_result
    
    def test_researcher_to_strategist_flow(self, researcher, strategist):
        """测试从研究员到策略师的数据流转"""
        # 1. 准备测试数据
        goal = {"domain": "编程", "topic": "Python数据分析", "timeframe": "3个月", "difficulty": "初级到中级"}
        
        # 2. 模拟研究员生成研究报告
        with patch('agents.researcher.ResearcherAgent.web_search') as mock_web_search:
            mock_web_search.return_value = "Python数据分析推荐资源：Pandas文档，NumPy教程"
            research_report = researcher.research_methods(goal)
        
        # 3. 策略师根据目标和研究报告生成计划
        plan_json = strategist.generate_plan(goal, research_report)
        plan = json.loads(plan_json)
        
        # 4. 验证计划是否包含预期元素
        assert isinstance(plan, list)
        assert len(plan) > 0
        assert all("id" in task for task in plan)
        assert all("description" in task for task in plan)
        assert all("due_date" in task for task in plan)
        assert all("depends_on" in task for task in plan)
    
    def test_full_analysis_to_planning_chain(self, analyst, researcher, strategist):
        """测试完整的从分析到研究再到规划链"""
        # 1. 准备测试数据
        user_goal = "我想在3个月内学会Python数据分析 by when"
        
        # 2. 模拟实际流程：分析 -> 研究 -> 规划
        with patch('agents.researcher.ResearcherAgent.web_search') as mock_web_search:
            # 设置mock
            mock_web_search.return_value = "Python数据分析推荐资源和学习路径"
            
            # 第一步：分析师处理用户目标
            analyst_output = analyst.process_message(user_goal)
            structured_goal = json.loads(analyst_output)
            
            # 第二步：研究员进行研究
            research_report = researcher.research_methods(structured_goal)
            
            # 第三步：策略师生成计划
            plan_json = strategist.generate_plan(structured_goal, research_report)
            final_plan = json.loads(plan_json)
        
        # 3. 验证完整流程的输出
        assert isinstance(final_plan, list)
        assert len(final_plan) > 0
        # 验证计划中的任务是否基于研究和目标
        task_descriptions = ' '.join([task["description"] for task in final_plan])
        assert "Python" in task_descriptions
    
    def test_feedback_and_replanning_chain(self, analyst, researcher, strategist, adaptor):
        """测试用户反馈和重新规划流程"""
        # 1. 准备测试数据
        user_goal = "我想在3个月内学会Python数据分析 by when"
        user_feedback = "这个计划太难了，我跟不上"
        
        # 2. 模拟初始计划流程
        with patch('agents.researcher.ResearcherAgent.web_search') as mock_web_search:
            mock_web_search.return_value = "Python数据分析学习路径"
            
            # 初始计划流程
            analyst_output = analyst.process_message(user_goal)
            structured_goal = json.loads(analyst_output)
            research_report = researcher.research_methods(structured_goal)
            initial_plan_json = strategist.generate_plan(structured_goal, research_report)
            initial_plan = json.loads(initial_plan_json)
        
        # 3. 处理用户反馈
        adaptor_output = adaptor.process_feedback(user_feedback)
        
        # 4. 验证适配器输出包含重规划指令
        assert "策略师" in adaptor_output
        assert "修订计划" in adaptor_output
        
        # 5. 模拟根据反馈进行重规划
        # 在实际场景中，这将重新触发策略师的计划生成
        # 这里我们简单验证流程连续性
        assert "太难" in adaptor_output
        assert "降低" in adaptor_output 