# test_config.py
from helios.services import model_client  # 从services导入model_client服务实例
from helios.config import settings  # 从config导入配置数据

def test_model_client():
    """测试模型客户端"""
    print("\n=== 测试模型客户端 ===")
    
    if model_client is None:
        print("❌ 错误：模型客户端初始化失败")
        return False
    
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say this is a test"}
        ]
        
        # 注意：这里可能需要根据model_client的实际实现调整API调用方式
        config_list = model_client.get_config_list()
        print(f"✅ 模型客户端配置列表获取成功! 包含 {len(config_list)} 个模型配置")
        for i, config in enumerate(config_list):
            print(f"模型 {i+1}: {config.get('model', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ 错误: 模型客户端API调用失败: {e}")
        return False

def test_settings():
    """测试配置设置"""
    print("\n=== 测试配置设置 ===")
    
    try:
        print("✅ 配置加载成功!")
        print(f"日志级别: {settings.LOG_LEVEL}")
        print(f"日志文件: {settings.LOG_FILE}")
        return True
    except Exception as e:
        print(f"❌ 错误: 配置加载失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试配置...")
    
    client_success = test_model_client()
    settings_success = test_settings()
    
    print("\n=== 测试结果摘要 ===")
    print(f"模型客户端: {'成功' if client_success else '失败'}")
    print(f"配置设置: {'成功' if settings_success else '失败'}")
    print("\n测试完成!") 
 