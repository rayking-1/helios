import pytest
from fastapi.testclient import TestClient
import json
import sys
import os
from unittest.mock import patch

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 导入FastAPI应用
from main import app

# 创建测试客户端
client = TestClient(app)

class TestGraphQLAPI:
    """测试GraphQL API的端到端功能"""
    
    @patch('routes.graphql_routes.AdaptivePlanTeam')
    def test_generate_plan_mutation(self, mock_team):
        """测试生成计划的GraphQL mutation"""
        # 配置mock
        mock_team_instance = mock_team.return_value
        mock_team_instance.run.return_value = {
            "structured_goal": {"goal": "test goal"},
            "research_report": "test research",
            "plan": '{"tasks": [{"id": "1", "title": "Test Task"}]}'
        }
        
        # 准备GraphQL查询
        query = """
        mutation {
            startNewGoal(prompt: "我想学习编程") {
                planId
                initialPlan {
                    planId
                    version
                }
            }
        }
        """
        
        # 发送请求
        response = client.post("/graphql", json={"query": query})
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "startNewGoal" in data["data"]
        assert "planId" in data["data"]["startNewGoal"]
        assert "initialPlan" in data["data"]["startNewGoal"]
    
    @patch('routes.graphql_routes.AdaptivePlanTeam')
    def test_submit_feedback_mutation(self, mock_team):
        """测试提交反馈的GraphQL mutation"""
        # 配置mock
        mock_team_instance = mock_team.return_value
        mock_team_instance.process_feedback.return_value = {
            "plan": '{"tasks": [{"id": "1", "title": "Adjusted Task"}]}'
        }
        
        # 准备GraphQL查询
        query = """
        mutation {
            submitFeedback(
                planId: "test-plan-id",
                taskId: "test-task-id",
                feedbackType: "TOO_HARD",
                feedbackText: "这个任务太难了"
            ) {
                success
                updatedPlan {
                    planId
                    version
                }
            }
        }
        """
        
        # 发送请求
        response = client.post("/graphql", json={"query": query})
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "submitFeedback" in data["data"]
        assert data["data"]["submitFeedback"]["success"] is True
    
    def test_get_current_plan_query(self):
        """测试获取当前计划的GraphQL query"""
        # 准备GraphQL查询
        query = """
        query {
            currentPlan(planId: "test-plan-id") {
                planId
                version
                weeks {
                    weekNumber
                    theme
                }
            }
        }
        """
        
        # 发送请求
        response = client.post("/graphql", json={"query": query})
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "currentPlan" in data["data"] 