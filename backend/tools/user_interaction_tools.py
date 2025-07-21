def ask_user_clarification(question: str) -> str:
    """
    向人类用户提出澄清问题并返回他们的答案。
    当代理需要从用户那里获得更具体的信息以继续时，应使用此工具。
    
    Args:
        question: 需要问用户的问题
        
    Returns:
        str: 用户的回答
    """
    print(f"\n[系统] 分析代理需要更多信息：\n{question}")
    response = input("你的回应：")
    return response 