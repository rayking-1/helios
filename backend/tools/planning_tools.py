def create_task_graph(tasks: list) -> dict:
    """
    创建任务依赖图并验证其逻辑性。
    
    Args:
        tasks: 任务字典列表，每个任务包含'id'和'depends_on'字段
        
    Returns:
        dict: 表示任务图的邻接表
        
    Raises:
        ValueError: 如果检测到循环依赖
    """
    # 创建邻接表
    graph = {}
    for task in tasks:
        task_id = task["id"]
        graph[task_id] = task.get("depends_on", [])
    
    # 检查循环依赖
    def has_cycle(node, visited, stack):
        visited.add(node)
        stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True
                
        stack.remove(node)
        return False
    
    # 对每个节点检查循环
    visited = set()
    stack = set()
    for node in graph:
        if node not in visited:
            if has_cycle(node, visited, stack):
                raise ValueError(f"检测到循环依赖，任务图无效: {graph}")
    
    # 计算拓扑排序
    def topological_sort():
        result = []
        temp_visited = set()
        perm_visited = set()
        
        def visit(node):
            if node in perm_visited:
                return
            if node in temp_visited:
                raise ValueError(f"检测到循环依赖于节点 {node}")
                
            temp_visited.add(node)
            
            for neighbor in graph.get(node, []):
                visit(neighbor)
                
            temp_visited.remove(node)
            perm_visited.add(node)
            result.append(node)
            
        for node in graph:
            if node not in perm_visited:
                visit(node)
                
        return result[::-1]  # 反转以获得正确的拓扑排序
    
    ordered_tasks = topological_sort()
    
    return {
        "adjacency_list": graph,
        "topological_order": ordered_tasks,
        "is_valid": True
    } 