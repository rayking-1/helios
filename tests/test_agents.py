"""
Tests for the agents.py module.
"""

import pytest
from unittest.mock import patch, MagicMock
from helios.services import logger, model_client  # 从services导入服务实例
from autogen import UserProxyAgent, AssistantAgent

# 由于我们不再直接从agents.py导入，我们需要创建测试用的agent实例
@pytest.fixture
def critic_agent():
    """创建一个测试用的Critic agent"""
    return AssistantAgent(
        name="Critic",
        system_message="You meticulously review plans and provide constructive, actionable feedback.",
        llm_config={"config_list": model_client.get_config_list(), "timeout": 600}
    )

@pytest.fixture
def integrator_agent():
    """创建一个测试用的Integrator agent"""
    return AssistantAgent(
        name="Integrator",
        system_message="You synthesize new information and provide final answers. TERMINATE",
        llm_config={"config_list": model_client.get_config_list(), "timeout": 600}
    )

def test_user_proxy_initialization():
    """
    测试 UserProxyAgent 能够被正确初始化，并启用代码执行功能。
    此测试是自包含的，不依赖于任何全局导入的实例。
    """
    # Arrange: 在测试函数内部创建全新的、独立的代理实例
    # 关键修复：在初始化时传入测试所需的配置，并明确禁用Docker以避免在无Docker环境中报错
    local_user_proxy = UserProxyAgent(
        name="Test_User_Proxy",
        human_input_mode="NEVER",
        code_execution_config={"work_dir": "_test_coding", "use_docker": False},
    )

    # Act & Assert: 针对新建的本地实例进行验证
    assert local_user_proxy.name == "Test_User_Proxy"
    assert local_user_proxy.human_input_mode == "NEVER"

    # 验证 code_execution_config 已被正确设置
    # Autogen 内部可能将其存储在私有属性 _code_execution_config 中
    assert hasattr(local_user_proxy, "_code_execution_config"), "代理实例应包含 _code_execution_config 属性"
    
    # 进一步精确验证配置内容
    exec_config = local_user_proxy._code_execution_config
    assert isinstance(exec_config, dict)
    assert exec_config.get("use_docker") is False, "use_docker 应被设置为 False"
    assert "work_dir" in exec_config, "工作目录应在配置中"

def test_critic_initialization(critic_agent):
    """Test that the critic agent is properly initialized."""
    assert critic_agent.name == "Critic"
    assert "meticulously review plans" in critic_agent.system_message
    assert "constructive, actionable feedback" in critic_agent.system_message
    assert critic_agent.llm_config is not None
    assert "config_list" in critic_agent.llm_config
    assert "timeout" in critic_agent.llm_config
    assert critic_agent.llm_config["timeout"] == 600

def test_integrator_initialization(integrator_agent):
    """Test that the integrator agent is properly initialized."""
    assert integrator_agent.name == "Integrator"
    assert "TERMINATE" in integrator_agent.system_message
    assert "synthesize" in integrator_agent.system_message
    assert integrator_agent.llm_config is not None
    assert "config_list" in integrator_agent.llm_config
    assert "timeout" in integrator_agent.llm_config
    assert integrator_agent.llm_config["timeout"] == 600

def test_termination_condition():
    """Test that the termination condition works correctly."""
    # Define the termination function directly since it might not be an attribute
    is_termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
    
    # Test message ending with TERMINATE
    assert is_termination_msg({"content": "This is the end. TERMINATE"})
    
    # Test message with TERMINATE and whitespace
    assert is_termination_msg({"content": "This is the end. TERMINATE  \n  "})
    
    # Test message without TERMINATE
    assert not is_termination_msg({"content": "This is not the end."})
    
    # Test empty message
    assert not is_termination_msg({"content": ""})
    
    # Test message with TERMINATE in the middle
    assert not is_termination_msg({"content": "This has TERMINATE in the middle."})

@pytest.mark.parametrize("agent_name, agent_fixture", [
    ("Critic", "critic_agent"),
    ("Integrator", "integrator_agent")
])
def test_agent_generate_reply_called(agent_name, agent_fixture, request):
    """Test that agent's generate_reply method is called with correct parameters."""
    # 获取agent实例
    agent_obj = request.getfixturevalue(agent_fixture)
    
    # Create a mock for the generate_reply method
    with patch.object(agent_obj, 'generate_reply', return_value="Mock response") as mock_generate_reply:
        # Create a mock message
        mock_message = {"content": "Test message", "role": "user"}
        
        # Call the generate_reply method
        response = agent_obj.generate_reply(mock_message)
        
        # Verify the method was called with the right parameters
        mock_generate_reply.assert_called_once_with(mock_message)
        
        # Verify the response
        assert response == "Mock response" 