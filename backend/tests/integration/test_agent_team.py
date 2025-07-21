import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agent_team import AdaptivePlanTeam

class TestAdaptivePlanTeam:
    """测试AG2智能体团队集成"""
    
    def setup_method(self):
        """每个测试方法前设置模拟配置"""
        # 创建模拟LLM配置
        self.mock_config = {
            "config_list": [{"model": "test-model", "api_key": "test-key"}]
        }
        
    @patch('agent_team.AnalystAgent')
    @patch('agent_team.ResearcherAgent')
    @patch('agent_team.StrategistAgent')
    @patch('agent_team.AdaptorAgent')
    @patch('agent_team.autogen.UserProxyAgent')
    @patch('agent_team.autogen.GroupChat')
    @patch('agent_team.autogen.GroupChatManager')
    def test_agent_team_initialization(self, mock_manager, mock_groupchat, 
                                      mock_user_proxy, mock_adaptor, 
                                      mock_strategist, mock_researcher, 
                                      mock_analyst):
        """测试AG2团队的初始化过程"""
        # 创建AdaptivePlanTeam实例
        team = AdaptivePlanTeam(config_list=self.mock_config["config_list"])
        
        # 验证是否创建了所有智能体
        mock_analyst.assert_called_once()
        mock_researcher.assert_called_once()
        mock_strategist.assert_called_once()
        mock_adaptor.assert_called_once()
        mock_user_proxy.assert_called_once()
        
        # 验证是否创建了GroupChat和GroupChatManager
        mock_groupchat.assert_called_once()
        mock_manager.assert_called_once()
        
    @patch('agent_team.AnalystAgent')
    @patch('agent_team.ResearcherAgent')
    @patch('agent_team.StrategistAgent')
    @patch('agent_team.AdaptorAgent')
    @patch('agent_team.autogen.UserProxyAgent')
    @patch('agent_team.autogen.GroupChat')
    @patch('agent_team.autogen.GroupChatManager')
    def test_fsm_transitions(self, mock_manager, mock_groupchat, 
                           mock_user_proxy, mock_adaptor, 
                           mock_strategist, mock_researcher, 
                           mock_analyst):
        """测试有限状态机的状态转换逻辑"""
        # 创建模拟对象
        mock_analyst_instance = MagicMock()
        mock_analyst_instance.name = "Analyst"
        mock_analyst.return_value = mock_analyst_instance
        
        mock_researcher_instance = MagicMock()
        mock_researcher_instance.name = "Researcher"
        mock_researcher.return_value = mock_researcher_instance
        
        # 创建团队
        team = AdaptivePlanTeam(config_list=self.mock_config["config_list"])
        
        # 测试状态转换: 初始状态 -> 分析状态
        assert team.state == team.STATES["INIT"]
        next_speaker = team._fsm_transition(mock_user_proxy.return_value, "test message")
        assert next_speaker == "Analyst"
        assert team.state == team.STATES["ANALYZING"]
        
        # 测试状态转换: 分析状态 -> 研究状态
        # 模拟分析师返回带有structured_goal的消息
        structured_goal_message = '{"goal": "test goal", "status": "clarified"}'
        next_speaker = team._fsm_transition(mock_analyst_instance, structured_goal_message)
        assert next_speaker == "Researcher"
        assert team.state == team.STATES["RESEARCHING"]
    
    @patch('agent_team.AdaptivePlanTeam._fsm_transition')
    @patch('agent_team.autogen.GroupChatManager.orchestrate_chat')
    def test_run_method_calls_orchestrate_chat(self, mock_orchestrate, mock_transition):
        """测试run方法调用了orchestrate_chat"""
        # 创建AdaptivePlanTeam实例，跳过实际初始化
        with patch('agent_team.AdaptivePlanTeam._setup_agents'), \
             patch('agent_team.AdaptivePlanTeam._setup_groupchat'):
            team = AdaptivePlanTeam(config_list=self.mock_config["config_list"])
            
            # 调用run方法
            team.run("测试目标")
            
            # 验证orchestrate_chat被调用
            mock_orchestrate.assert_called_once()
            
    @patch('agent_team.AdaptivePlanTeam._fsm_transition')
    @patch('agent_team.autogen.GroupChatManager.orchestrate_chat')
    def test_process_feedback_calls_orchestrate_chat(self, mock_orchestrate, mock_transition):
        """测试process_feedback方法调用了orchestrate_chat"""
        # 创建AdaptivePlanTeam实例，跳过实际初始化
        with patch('agent_team.AdaptivePlanTeam._setup_agents'), \
             patch('agent_team.AdaptivePlanTeam._setup_groupchat'):
            team = AdaptivePlanTeam(config_list=self.mock_config["config_list"])
            
            # 调用process_feedback方法
            team.process_feedback("测试反馈")
            
            # 验证orchestrate_chat被调用，且状态已设置为FEEDBACK
            mock_orchestrate.assert_called_once()
            assert team.state == team.STATES["FEEDBACK"] 