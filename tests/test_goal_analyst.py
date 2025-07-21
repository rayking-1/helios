# tests/test_goal_analyst.py
import pytest
from unittest.mock import patch, MagicMock
from helios_backend.agents.goal_analyst import GoalAnalysisAgent
from autogen.agentchat.conversable_agent import ConversableAgent

class TestGoalAnalysisAgent:
    """GoalAnalysisAgent的单元测试类"""
    
    def test_init(self):
        """测试智能体是否正确初始化"""
        agent = GoalAnalysisAgent(name="TestAnalyst")
        assert agent.name == "TestAnalyst"
        assert isinstance(agent, ConversableAgent)
        assert "SMART目标" in agent.system_message
    
    def test_tools_registration(self):
        """测试是否正确注册了工具函数"""
        agent = GoalAnalysisAgent()
        llm_config = agent.llm_config
        
        # 验证工具函数是否正确注册
        assert llm_config is not None
        assert "tools" in llm_config
        
        tools = llm_config["tools"]
        tool_names = [t["function"]["name"] for t in tools]
        
        # 验证两个预期的工具函数是否存在
        assert "ask_user_clarification" in tool_names
        assert "extract_entities" in tool_names
    
    @patch("helios_backend.model_config.llm_config")
    def test_model_config_usage(self, mock_llm_config):
        """测试是否正确使用模型配置"""
        # 模拟llm_config
        mock_llm_config.return_value = {
            "config_list": [{"model": "qwen-max"}],
            "temperature": 0.2
        }
        
        agent = GoalAnalysisAgent()
        # 验证是否使用了模型配置
        assert agent.llm_config is not None
    
    @pytest.mark.asyncio
    async def test_message_processing(self):
        """测试消息处理逻辑"""
        agent = GoalAnalysisAgent()
        
        # 模拟发送者
        sender = MagicMock()
        sender.name = "TestUser"
        
        # 测试消息处理
        message = {"content": "我想提高工作效率"}
        with patch.object(ConversableAgent, "_process_received_message") as mock_process:
            mock_process.return_value = message
            result = agent._process_received_message(message, sender, {})
            
            # 验证父类方法被调用
            mock_process.assert_called_once_with(message, sender, {})
            
            # 验证返回值
            assert result == message 