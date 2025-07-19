from duckduckgo_search import DDGS
import json
from helios_backend.config import logger

def web_search(query: str) -> str:
    """
    根据给定的查询字符串执行DuckDuckGo网页搜索。

    Args:
        query (str): 要搜索的关键词或问题。

    Returns:
        str: 一个格式化的字符串，包含前5个搜索结果的标题、摘要和链接。
             如果搜索失败或没有结果，则返回一条说明信息。
    """
    logger.info(f"执行网络搜索工具，查询: '{query}'")
    try:
        # 使用DDGS上下文管理器来执行搜索
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return "未找到搜索结果。"

        # 将结果格式化为对LLM更易读的格式
        formatted_results = []
        for i, result in enumerate(results):
            formatted_results.append(
                f"结果 {i+1}:\n"
                f"标题: {result.get('title')}\n"
                f"摘要: {result.get('body')}\n"
                f"URL: {result.get('href')}\n"
            )
        
        logger.info("网络搜索工具执行成功")
        return "\n---\n".join(formatted_results)

    except Exception as e:
        logger.error(f"网络搜索工具执行失败: {e}", exc_info=True)
        return f"搜索过程中发生错误: {e}" 