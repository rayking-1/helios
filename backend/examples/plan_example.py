"""
使用AdaptivePlanTeam的示例脚本

该脚本演示如何初始化和使用自适应规划团队来处理用户目标和反馈。
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_team import AdaptivePlanTeam

def main():
    """主函数，演示AdaptivePlanTeam的使用"""
    print("=" * 50)
    print("自适应规划团队示例")
    print("=" * 50)
    
    # 设置LLM配置 (实际使用时需要替换为你的API密钥)
    config_list = [
        {
            "model": "qwen-max",  # 使用通义千问大模型
            "api_key": os.environ.get("DASHSCOPE_API_KEY", "your_api_key_here")
        },
        {
            "model": "deepseek-chat",  # 使用DeepSeek大模型
            "api_key": os.environ.get("DEEPSEEK_API_KEY", "your_api_key_here")
        }
    ]
    
    # 初始化自适应规划团队
    team = AdaptivePlanTeam(config_list=config_list)
    
    # 用户目标示例
    user_objective = "我想在3个月内学习Python数据科学，每周可以投入15小时学习时间。"
    
    print(f"\n用户目标: {user_objective}\n")
    print("开始处理...\n")
    
    try:
        # 运行规划过程
        result = team.run(user_objective)
        
        # 打印结构化结果
        print("\n" + "=" * 50)
        print("结构化目标:")
        print("-" * 50)
        print(json.dumps(result["structured_goal"], ensure_ascii=False, indent=2))
        
        print("\n" + "=" * 50)
        print("研究报告摘要:")
        print("-" * 50)
        if result["research_report"]:
            print(result["research_report"][:500] + "..." if len(result["research_report"]) > 500 else result["research_report"])
        else:
            print("未生成研究报告")
        
        print("\n" + "=" * 50)
        print("最终计划:")
        print("-" * 50)
        if result["plan"]:
            try:
                plan_data = json.loads(result["plan"])
                print(json.dumps(plan_data, ensure_ascii=False, indent=2))
            except:
                print(result["plan"])
        else:
            print("未生成计划")
        
        # 处理用户反馈示例
        print("\n" + "=" * 50)
        print("用户反馈示例")
        print("-" * 50)
        
        feedback = "我觉得这个计划有点太难了，我是Python初学者，可能需要更基础一些的内容。"
        print(f"用户反馈: {feedback}\n")
        
        # 处理反馈
        feedback_result = team.process_feedback(feedback)
        
        print("\n调整后的计划:")
        print("-" * 50)
        if feedback_result["updated_plan"]:
            try:
                updated_plan = json.loads(feedback_result["updated_plan"])
                print(json.dumps(updated_plan, ensure_ascii=False, indent=2))
            except:
                print(feedback_result["updated_plan"])
        else:
            print("未生成调整后的计划")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 