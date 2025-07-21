# examples/plan_example.py
"""
示例脚本: 演示如何使用智能体团队进行自适应规划
"""

import os
import sys
import logging
import json
from pathlib import Path
from dotenv import load_dotenv

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_root))

# 加载环境变量
load_dotenv()

# 设置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("adaptive_planning.log")
    ]
)

logger = logging.getLogger("example")

def main():
    """主函数：演示智能体团队的使用"""
    try:
        from helios_backend.agent_team import AdaptivePlanTeam
        
        # 检查API密钥
        api_keys_available = check_api_keys()
        if not api_keys_available:
            logger.error("未找到必要的API密钥，请检查.env文件")
            return
        
        logger.info("创建适应性规划团队...")
        team = AdaptivePlanTeam()
        
        # 示例目标
        goal = """
        我想在3个月内学习人工智能并完成一个实际项目。
        我的背景是计算机科学本科学历，有良好的编程基础。
        我每周可以投入约20小时学习，希望最终能够开发一个智能推荐系统。
        请帮我制定一个详细的学习和项目计划。
        """
        
        logger.info("启动规划会话...")
        result = team.start_planning_session(goal)
        
        if result["success"]:
            logger.info("规划成功完成!")
            
            # 保存计划和会话历史
            save_results("initial_plan.md", result["plan"])
            save_results("initial_conversation.json", result["history"])
            
            # 提供反馈示例
            logger.info("提供反馈...")
            feedback = {
                "text": "我觉得计划中的机器学习部分太浅，我需要更深入地学习推荐系统算法。另外，我发现我每周能投入的时间可能只有15小时，而不是20小时。",
                "ratings": {
                    "practicality": 4,
                    "depth": 2,
                    "timeframe": 3
                }
            }
            
            updated_result = team.provide_feedback(feedback)
            
            if updated_result["success"]:
                logger.info("反馈处理成功，计划已更新!")
                
                # 保存更新后的计划和会话历史
                save_results("updated_plan.md", updated_result["updated_plan"])
                save_results("updated_conversation.json", updated_result["history"])
            else:
                logger.error(f"反馈处理失败: {updated_result.get('error', '未知错误')}")
        else:
            logger.error(f"规划失败: {result.get('error', '未知错误')}")
    
    except ImportError as e:
        logger.error(f"导入错误: {str(e)}，请确保已安装所有依赖")
    except Exception as e:
        logger.error(f"发生错误: {str(e)}", exc_info=True)

def check_api_keys():
    """检查必要的API密钥是否存在"""
    # 检查必要的API密钥
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
    
    if not dashscope_key and not deepseek_key:
        logger.warning("DASHSCOPE_API_KEY和DEEPSEEK_API_KEY均未设置")
        return False
    
    if not dashscope_key:
        logger.warning("DASHSCOPE_API_KEY未设置，将使用DEEPSEEK_API_KEY")
    
    if not deepseek_key:
        logger.warning("DEEPSEEK_API_KEY未设置，将使用DASHSCOPE_API_KEY")
    
    return True

def save_results(filename, content):
    """保存结果到文件"""
    try:
        # 创建results目录（如果不存在）
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        file_path = results_dir / filename
        
        # 根据文件扩展名处理内容
        if filename.endswith(".json"):
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        
        logger.info(f"结果已保存到: {file_path}")
    
    except Exception as e:
        logger.error(f"保存结果到 {filename} 失败: {str(e)}")

if __name__ == "__main__":
    main() 