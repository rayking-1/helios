import pytest
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.strategist_agent import StrategistAgent

# 测试数据
TEST_GOAL = {"goal": "学习Python数据科学", "timeframe": "3个月"}
TEST_RESEARCH = """根据研究，最有效的学习方法包括：
1. 费曼技巧：通过教授概念来加深理解
2. 间隔重复：利用记忆曲线优化复习时间
3. 基于项目学习：通过实践项目应用所学知识"""

def test_generate_plan_returns_valid_json():
    """测试生成计划方法返回的是有效JSON"""
    # 创建代理
    agent = StrategistAgent(name="TestStrategist", llm_config={})
    
    # 生成计划
    result = agent.generate_plan(TEST_GOAL, TEST_RESEARCH)
    
    # 验证结果是有效的JSON
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, list)

def test_plan_has_required_fields():
    """测试计划中的任务包含所有必需字段"""
    agent = StrategistAgent(name="TestStrategist", llm_config={})
    result = agent.generate_plan(TEST_GOAL, TEST_RESEARCH)
    parsed_result = json.loads(result)
    
    # 验证列表中第一项是具有必需键的字典
    assert len(parsed_result) > 0
    first_task = parsed_result[0]
    
    assert "id" in first_task
    assert "description" in first_task
    assert "due_date" in first_task
    assert "depends_on" in first_task
    assert isinstance(first_task["depends_on"], list) 