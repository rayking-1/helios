import pytest
import json
import sys
import os
from unittest.mock import patch

# 添加项目根目录到Python路径，以便正确导入模块
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.strategist import StrategistAgent

# 测试数据
TEST_GOAL = {"domain": "编程", "topic": "学习Python", "timeframe": "3个月", "difficulty": "初级到中级"}
TEST_RESEARCH = "Python最佳学习方法包括项目式学习和交互式教程。推荐资源：Python官方文档、Real Python网站和Codecademy课程。"

def test_generate_plan():
    """测试计划生成功能"""
    # 创建代理，不需要实际的LLM配置
    agent = StrategistAgent(name="TestStrategist", llm_config={})
    
    # 生成计划
    plan_json = agent.generate_plan(TEST_GOAL, TEST_RESEARCH)
    
    # 验证结果是有效的JSON字符串
    plan = json.loads(plan_json)
    assert isinstance(plan, list)
    assert len(plan) > 0
    
    # 验证计划项的格式
    for task in plan:
        assert "id" in task
        assert "description" in task
        assert "due_date" in task
        assert "depends_on" in task

def test_plan_is_sequential():
    """测试生成的计划是否有合理的依赖关系"""
    # 创建代理，不需要实际的LLM配置
    agent = StrategistAgent(name="TestStrategist", llm_config={})
    
    # 生成计划
    plan_json = agent.generate_plan(TEST_GOAL, TEST_RESEARCH)
    plan = json.loads(plan_json)
    
    # 构建任务ID集合
    task_ids = {task["id"] for task in plan}
    
    # 验证依赖关系
    for task in plan:
        # 每个依赖的任务ID都应该存在于计划中
        for dep_id in task["depends_on"]:
            assert dep_id in task_ids 