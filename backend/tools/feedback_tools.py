def interpret_feedback(feedback_text: str) -> dict:
    """
    分析原始用户反馈文本并返回结构化的分析结果。
    
    此函数识别反馈中的情感倾向和用户意图，以便自适应代理可以决定适当的行动。
    
    Args:
        feedback_text: 用户的反馈文本
        
    Returns:
        dict: 包含sentiment和intent等键的结构化反馈分析
    """
    # 在实际实现中，这将使用NLP或LLM来分析文本
    # 现在使用简单的关键词匹配
    
    feedback_text = feedback_text.lower()
    result = {
        "sentiment": "neutral",
        "intent": "none",
        "priority": "low",
        "raw_feedback": feedback_text
    }
    
    # 情感分析
    positive_words = ["好", "喜欢", "感谢", "棒", "excellent", "满意"]
    negative_words = ["不好", "难", "困难", "讨厌", "糟糕", "不满"]
    
    if any(word in feedback_text for word in positive_words):
        result["sentiment"] = "positive"
    elif any(word in feedback_text for word in negative_words):
        result["sentiment"] = "negative"
    
    # 意图分析
    if any(phrase in feedback_text for phrase in ["太难", "难度大", "吃力", "做不到"]):
        result["intent"] = "reduce_difficulty"
        result["priority"] = "high"
    elif any(phrase in feedback_text for phrase in ["太简单", "无聊", "不够挑战"]):
        result["intent"] = "increase_difficulty"
        result["priority"] = "medium"
    elif any(phrase in feedback_text for phrase in ["没时间", "时间不够", "来不及"]):
        result["intent"] = "extend_timeline"
        result["priority"] = "high"
    elif any(phrase in feedback_text for phrase in ["推迟", "改期", "日程冲突"]):
        result["intent"] = "change_schedule"
        result["priority"] = "medium"
    elif any(phrase in feedback_text for phrase in ["不明白", "不理解", "困惑"]):
        result["intent"] = "clarify_tasks"
        result["priority"] = "medium"
    
    return result 