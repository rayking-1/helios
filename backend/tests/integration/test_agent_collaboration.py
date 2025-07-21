import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.analyst_agent import AnalystAgent
from agents.researcher_agent import ResearcherAgent

@pytest.fixture
def llm_config_fixture():
    """测试用的LLM配置"""
    return {
        "model": "test-model",
        "config_list": [{"model": "test-model", "api_key": "test-key"}]
    }

def test_analyst_to_researcher_flow(monkeypatch, llm_config_fixture):
    """
    测试从AnalystAgent到ResearcherAgent的数据流转
    验证分析智能体输出的结构化目标能被研究智能体正确处理
    """
    # 1. 准备测试数据
    test_goal = "我想在3个月内学习数据科学"
    expected_structured_goal = {"goal": test_goal, "status": "clarified"}
    
    # 2. 创建智能体
    analyst = AnalystAgent(name="TestAnalyst", llm_config=llm_config_fixture)
    researcher = ResearcherAgent(name="TestResearcher", llm_config=llm_config_fixture)
    
    # 3. 模拟analyst的process_message方法，使其返回预定义的结构化目标
    def mock_process_message(self, message):
        return json.dumps(expected_structured_goal)
    
    monkeypatch.setattr(AnalystAgent, 'process_message', mock_process_message)
    
    # 4. 模拟researcher的generate_research_plan方法
    mock_research_output = "ACTION: web_search(query='实现 数据科学 的最佳方法')"
    
    def mock_generate_research(self, structured_goal):
        assert structured_goal == expected_structured_goal, "研究智能体应收到正确的结构化目标"
        return mock_research_output
    
    monkeypatch.setattr(ResearcherAgent, 'generate_research_plan', mock_generate_research)
    
    # 5. 执行流程
    analyst_output = analyst.process_message(test_goal)
    parsed_output = json.loads(analyst_output)
    research_result = researcher.generate_research_plan(parsed_output)
    
    # 6. 验证结果
    assert research_result == mock_research_output, "研究智能体应返回预期的研究结果"

@patch('backend.tools.research_tools.web_search')
def test_researcher_web_search_integration(mock_web_search, llm_config_fixture):
    """
    测试ResearcherAgent与web_search工具的集成
    """
    # 1. 设置mock的web_search返回值
    mock_search_results = [
        {
            "title": "数据科学最佳学习路径",
            "url": "https://example.com/datascience",
            "snippet": "从统计学基础开始，然后学习Python和数据分析库..."
        }
    ]
    mock_web_search.return_value = mock_search_results
    
    # 2. 创建研究智能体
    researcher = ResearcherAgent(name="TestResearcher", llm_config=llm_config_fixture)
    
    # 3. 定义测试输入
    structured_goal = {"goal": "学习数据科学", "status": "clarified"}
    
    # 4. 执行研究计划生成（这会触发对mock的web_search的调用）
    result = researcher.generate_research_plan(structured_goal)
    
    # 5. 验证web_search工具被正确调用
    assert "ACTION: web_search" in result
    assert "学习数据科学" in result

def test_full_analysis_research_strategist_flow(monkeypatch, llm_config_fixture):
    """
    测试从目标分析到研究再到规划的完整流程
    """
    from agents.strategist_agent import StrategistAgent
    
    # 1. 准备测试数据和智能体
    test_goal = "学习Python数据科学"
    analyst = AnalystAgent(name="TestAnalyst", llm_config=llm_config_fixture)
    researcher = ResearcherAgent(name="TestResearcher", llm_config=llm_config_fixture)
    strategist = StrategistAgent(name="TestStrategist", llm_config=llm_config_fixture)
    
    # 2. 模拟各个智能体的方法
    structured_goal = {"goal": test_goal, "status": "clarified"}
    research_report = "# 数据科学学习方法\n\n1. 学习Python基础\n2. 学习Pandas和NumPy\n3. 学习可视化库"
    
    def mock_analyst_process(self, message):
        return json.dumps(structured_goal)
    
    def mock_researcher_process(self, structured_goal):
        return research_report
    
    def mock_strategist_process(self, goal, research):
        assert goal == structured_goal, "策略师应接收到正确的目标"
        assert research == research_report, "策略师应接收到正确的研究报告"
        return json.dumps([
            {"id": "task_1", "description": "学习Python基础", "due_date": "2025-08-01", "depends_on": []},
            {"id": "task_2", "description": "学习数据分析库", "due_date": "2025-08-15", "depends_on": ["task_1"]}
        ])
    
    monkeypatch.setattr(AnalystAgent, 'process_message', mock_analyst_process)
    monkeypatch.setattr(ResearcherAgent, 'generate_research_plan', mock_researcher_process)
    monkeypatch.setattr(StrategistAgent, 'generate_plan', mock_strategist_process)
    
    # 3. 执行完整流程
    analyst_output = analyst.process_message(test_goal)
    parsed_goal = json.loads(analyst_output)
    research_output = researcher.generate_research_plan(parsed_goal)
    plan_output = strategist.generate_plan(parsed_goal, research_output)
    
    # 4. 验证最终计划
    plan_data = json.loads(plan_output)
    assert len(plan_data) == 2, "计划应包含两个任务"
    assert plan_data[0]["description"] == "学习Python基础", "第一个任务应为学习Python基础"
    assert plan_data[1]["description"] == "学习数据分析库", "第二个任务应为学习数据分析库"
    assert plan_data[1]["depends_on"] == ["task_1"], "第二个任务应依赖第一个任务" 