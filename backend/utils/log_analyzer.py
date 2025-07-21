"""
结构化日志分析工具

该模块提供用于分析系统JSON格式日志的工具函数，
帮助开发者和运维人员快速识别系统中的问题模式。
"""

import json
import re
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
from datetime import datetime, timedelta
import os


class LogAnalyzer:
    """
    结构化日志分析器
    
    用于分析JSON格式的系统日志，提取有用的信息和模式。
    """
    
    def __init__(self, log_file_path: Optional[str] = None, log_data: Optional[List[Dict]] = None):
        """
        初始化日志分析器
        
        Args:
            log_file_path: JSON日志文件的路径
            log_data: 已经解析的日志数据列表，如果提供则不读取文件
        """
        self.log_entries = []
        
        if log_data:
            self.log_entries = log_data
        elif log_file_path and os.path.exists(log_file_path):
            self._load_logs_from_file(log_file_path)
            
    def _load_logs_from_file(self, file_path: str) -> None:
        """从文件加载日志"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            log_entry = json.loads(line)
                            self.log_entries.append(log_entry)
                        except json.JSONDecodeError:
                            # 如果不是JSON格式，尝试使用正则表达式提取关键信息
                            self._parse_non_json_log(line)
        except Exception as e:
            print(f"读取日志文件时出错: {str(e)}")
            
    def _parse_non_json_log(self, line: str) -> None:
        """解析非JSON格式的日志行"""
        # 尝试从普通日志中提取时间戳、日志级别和消息
        timestamp_pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\]'
        level_pattern = r'\[(DEBUG|INFO|WARNING|ERROR|CRITICAL)\]'
        
        timestamp_match = re.search(timestamp_pattern, line)
        level_match = re.search(level_pattern, line)
        
        if timestamp_match and level_match:
            timestamp = timestamp_match.group(1)
            level = level_match.group(1)
            
            # 提取消息部分（可能是粗略的）
            message = line.split(level + ']')[-1].strip()
            
            # 创建一个简化的日志条目
            log_entry = {
                "timestamp": timestamp,
                "level": level,
                "message": message
            }
            
            self.log_entries.append(log_entry)
            
    def filter_by_level(self, level: str) -> List[Dict]:
        """
        按日志级别筛选日志
        
        Args:
            level: 日志级别 (例如 "ERROR", "WARNING")
            
        Returns:
            符合条件的日志条目列表
        """
        return [entry for entry in self.log_entries 
                if entry.get('level', '').upper() == level.upper()]
                
    def filter_by_time_range(self, start_time: datetime, end_time: datetime) -> List[Dict]:
        """
        按时间范围筛选日志
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            符合条件的日志条目列表
        """
        filtered_entries = []
        
        for entry in self.log_entries:
            timestamp = entry.get('timestamp')
            if not timestamp:
                continue
                
            try:
                # 尝试解析多种可能的时间格式
                for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", 
                           "%Y-%m-%d %H:%M:%S,%f", "%Y-%m-%d %H:%M:%S"]:
                    try:
                        log_time = datetime.strptime(timestamp, fmt)
                        break
                    except ValueError:
                        continue
                
                if start_time <= log_time <= end_time:
                    filtered_entries.append(entry)
            except Exception:
                # 如果无法解析时间，则跳过
                continue
                
        return filtered_entries
        
    def filter_by_agent(self, agent_name: str) -> List[Dict]:
        """
        按智能体名称筛选日志
        
        Args:
            agent_name: 智能体名称
            
        Returns:
            符合条件的日志条目列表
        """
        return [entry for entry in self.log_entries 
                if entry.get('agent_name') == agent_name]
                
    def filter_by_trace_id(self, trace_id: str) -> List[Dict]:
        """
        按跟踪ID筛选日志
        
        Args:
            trace_id: 跟踪ID
            
        Returns:
            符合条件的日志条目列表
        """
        return [entry for entry in self.log_entries 
                if entry.get('trace_id') == trace_id]
    
    def get_error_summary(self) -> Dict:
        """
        获取错误日志摘要
        
        Returns:
            包含错误统计和分类的字典
        """
        error_logs = self.filter_by_level("ERROR")
        
        # 按事件类型分组
        event_types = Counter([log.get('event_type', 'unknown') for log in error_logs])
        
        # 按智能体名称分组
        agents = Counter([log.get('agent_name', 'unknown') for log in error_logs])
        
        # 提取前10个常见错误消息
        error_messages = [log.get('message', '') for log in error_logs]
        common_errors = Counter(error_messages).most_common(10)
        
        return {
            "total_errors": len(error_logs),
            "event_types": dict(event_types),
            "agents": dict(agents),
            "common_errors": common_errors
        }
        
    def find_tool_call_failures(self) -> List[Dict]:
        """
        查找工具调用失败的实例
        
        Returns:
            工具调用失败的日志条目列表
        """
        # 筛选工具调用失败事件
        return [entry for entry in self.log_entries 
                if entry.get('event_type') == 'tool_call_failed']
                
    def analyze_conversation_flow(self, trace_id: str) -> Dict:
        """
        分析特定跟踪ID的对话流
        
        Args:
            trace_id: 跟踪ID
            
        Returns:
            对话流分析结果
        """
        conversation_logs = self.filter_by_trace_id(trace_id)
        
        if not conversation_logs:
            return {"error": f"没有找到跟踪ID为 {trace_id} 的对话"}
        
        # 按时间排序
        conversation_logs.sort(key=lambda x: x.get('timestamp', ''))
        
        # 提取交互序列
        interactions = []
        for log in conversation_logs:
            if log.get('event_type') in ['message_sent', 'message_received', 'tool_call']:
                interactions.append({
                    'timestamp': log.get('timestamp'),
                    'agent_name': log.get('agent_name', 'unknown'),
                    'event_type': log.get('event_type'),
                    'message': log.get('message', '')[:100]  # 限制消息长度
                })
                
        # 计算各智能体参与度
        agent_participation = Counter([i.get('agent_name') for i in interactions])
        
        return {
            "trace_id": trace_id,
            "total_interactions": len(interactions),
            "interaction_sequence": interactions,
            "agent_participation": dict(agent_participation),
            "duration": self._calculate_conversation_duration(conversation_logs)
        }
        
    def _calculate_conversation_duration(self, logs: List[Dict]) -> str:
        """计算对话持续时间"""
        if not logs or len(logs) < 2:
            return "未知"
            
        try:
            # 尝试解析第一条和最后一条日志的时间戳
            first_log = logs[0]
            last_log = logs[-1]
            
            first_time = datetime.fromisoformat(first_log.get('timestamp').replace('Z', '+00:00'))
            last_time = datetime.fromisoformat(last_log.get('timestamp').replace('Z', '+00:00'))
            
            duration = last_time - first_time
            return str(duration)
        except Exception:
            return "无法计算"
            
    def generate_report(self) -> Dict:
        """
        生成完整的日志分析报告
        
        Returns:
            包含多个分析结果的综合报告
        """
        error_summary = self.get_error_summary()
        
        # 获取日志的时间范围
        time_range = self._get_log_time_range()
        
        # 按级别统计日志数量
        level_counts = Counter([entry.get('level', 'unknown') for entry in self.log_entries])
        
        # 识别重要的跟踪ID（有错误的对话）
        important_traces = set()
        for log in self.filter_by_level("ERROR"):
            trace_id = log.get('trace_id')
            if trace_id:
                important_traces.add(trace_id)
                
        trace_summaries = []
        for trace_id in list(important_traces)[:5]:  # 限制为前5个
            trace_summary = self.analyze_conversation_flow(trace_id)
            trace_summaries.append(trace_summary)
            
        return {
            "log_count": len(self.log_entries),
            "time_range": time_range,
            "level_distribution": dict(level_counts),
            "error_summary": error_summary,
            "important_conversation_flows": trace_summaries,
            "generated_at": datetime.now().isoformat()
        }
        
    def _get_log_time_range(self) -> Dict:
        """获取日志的时间范围"""
        timestamps = []
        
        for entry in self.log_entries:
            timestamp = entry.get('timestamp')
            if timestamp:
                try:
                    # 尝试解析时间戳
                    for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", 
                               "%Y-%m-%d %H:%M:%S,%f", "%Y-%m-%d %H:%M:%S"]:
                        try:
                            log_time = datetime.strptime(timestamp, fmt)
                            timestamps.append(log_time)
                            break
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        if not timestamps:
            return {"start": "未知", "end": "未知", "duration": "未知"}
            
        start_time = min(timestamps)
        end_time = max(timestamps)
        
        return {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration": str(end_time - start_time)
        }


# 命令行使用示例
if __name__ == "__main__":
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='分析结构化日志文件')
    parser.add_argument('log_file', type=str, help='日志文件路径')
    parser.add_argument('--level', type=str, help='按日志级别筛选 (例如 ERROR, WARNING)')
    parser.add_argument('--agent', type=str, help='按智能体名称筛选')
    parser.add_argument('--trace', type=str, help='按跟踪ID筛选')
    parser.add_argument('--report', action='store_true', help='生成综合报告')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.log_file)
    
    if not analyzer.log_entries:
        print("没有找到日志条目或无法读取日志文件")
        sys.exit(1)
        
    if args.level:
        filtered = analyzer.filter_by_level(args.level)
        print(f"找到 {len(filtered)} 条 {args.level} 级别的日志条目:")
        for entry in filtered[:10]:  # 只显示前10条
            print(json.dumps(entry, ensure_ascii=False, indent=2))
        if len(filtered) > 10:
            print(f"... 还有 {len(filtered) - 10} 条日志未显示")
            
    elif args.agent:
        filtered = analyzer.filter_by_agent(args.agent)
        print(f"找到 {len(filtered)} 条与智能体 '{args.agent}' 相关的日志条目:")
        for entry in filtered[:10]:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
        if len(filtered) > 10:
            print(f"... 还有 {len(filtered) - 10} 条日志未显示")
            
    elif args.trace:
        filtered = analyzer.filter_by_trace_id(args.trace)
        print(f"找到 {len(filtered)} 条与跟踪ID '{args.trace}' 相关的日志条目:")
        for entry in filtered:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
            
    elif args.report:
        report = analyzer.generate_report()
        print("日志分析报告:")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        
    else:
        # 默认显示日志摘要
        print(f"共有 {len(analyzer.log_entries)} 条日志条目")
        print("错误日志摘要:")
        print(json.dumps(analyzer.get_error_summary(), ensure_ascii=False, indent=2)) 