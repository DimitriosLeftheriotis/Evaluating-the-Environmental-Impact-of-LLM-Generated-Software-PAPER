from collections import deque

def dinic(graph: dict, source: int, sink: int) -> int:
    # Build residual graph with forward and reverse edges
    # residual[u][v] holds the current residual capacity of edge (u, v)
    nodes = set(graph.keys())
    for u in graph:
        for v, _ in graph[u]:
            nodes.add(v)
            
    residual = {node: {} for node in nodes}
    
    for u in graph:
        for v, cap in graph[u]:
            residual[u][v] = residual[u].get(v, 0) + cap
            if u not in residual[v]:
                residual[v][u] = 0  # Initialize back-edge capacity

    level = {}

    def bfs():
        """Constructs the level graph using BFS."""
        nonlocal level
        level = {node: -1 for node in nodes}
        level[source] = 0
        queue = deque([source])
        
        while queue:
            u = queue.popleft()
            for v, cap in residual[u].items():
                if cap > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
                    
        return level[sink] >= 0

    def dfs(u, flow, ptr):
        """Pushes flow along blocking paths in the level graph using DFS."""
        if u == sink:
            return flow
        
        # Unique list of neighbors to iterate using pointer
        neighbors = list(residual[u].keys())
        
        while ptr[u] < len(neighbors):
            v = neighbors[ptr[u]]
            cap = residual[u][v]
            
            if cap > 0 and level[v] == level[u] + 1:
                pushed = dfs(v, min(flow, cap), ptr)
                if pushed > 0:
                    residual[u][v] -= pushed
                    residual[v][u] += pushed
                    return pushed
            
            ptr[u] += 1
            
        return 0

    max_flow = 0
    
    # Continue while a path exists from source to sink in the residual graph
    while bfs():
        ptr = {node: 0 for node in nodes}  # Track visited edges per phase
        while True:
            pushed = dfs(source, float('inf'), ptr)
            if pushed == 0:
                break
            max_flow += pushed

    return max_flow